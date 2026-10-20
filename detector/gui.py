import asyncio
import json
from pathlib import Path
from PySide6.QtCore import QThread, Signal, QTimer, Qt
from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLineEdit,QPushButton,QLabel,QProgressBar,QTableWidget,QTableWidgetItem,QPlainTextEdit,QComboBox,QSpinBox,QFileDialog,QMessageBox)
from .crawler import Crawler,Config

class ScanThread(QThread):
    progress=Signal(dict)
    complete=Signal(object,object)
    failed=Signal(str)
    def __init__(self,url,output,config):
        super().__init__();self.url=url;self.output=output;self.crawler=Crawler(config,self.progress.emit)
    def run(self):
        try:
            result,details=asyncio.run(self.crawler.scan(self.url,self.output));self.complete.emit(result,details)
        except Exception as exc:self.failed.emit(str(exc))

class DesktopGUI(QMainWindow):
    def __init__(self,base):
        super().__init__();self.base=Path(base);self.job=None;self.result=None;self.details={}
        self.setWindowTitle('Public Web Ad Detector · 공공 웹사이트 광고 탐지');self.resize(1250,800)
        root=QWidget();self.setCentralWidget(root);layout=QVBoxLayout(root)
        title=QLabel('공공 웹사이트 불법광고 탐지');title.setStyleSheet('font-size:24px;font-weight:600;padding:12px');layout.addWidget(title)
        row=QHBoxLayout();self.url=QLineEdit();self.url.setPlaceholderText('https://example.go.kr');row.addWidget(self.url)
        self.start=QPushButton('검사 시작');self.stop=QPushButton('중지');self.stop.setEnabled(False);row.addWidget(self.start);row.addWidget(self.stop);layout.addLayout(row)
        options=QHBoxLayout();self.pages=QSpinBox();self.pages.setRange(1,100000);self.pages.setValue(200);self.workers=QSpinBox();self.workers.setRange(1,16);self.workers.setValue(3);self.topic=QLineEdit('TOPIC')
        for label,widget in [('최대 페이지',self.pages),('동시 작업',self.workers),('공식 topic 값',self.topic)]:options.addWidget(QLabel(label));options.addWidget(widget)
        layout.addLayout(options)
        self.output=QLineEdit(str(self.base/'result.json'));choose=QPushButton('저장 위치');outputrow=QHBoxLayout();outputrow.addWidget(self.output);outputrow.addWidget(choose);layout.addLayout(outputrow)
        self.bar=QProgressBar();self.bar.setRange(0,100);layout.addWidget(self.bar)
        self.status=QLabel('준비 · 출력은 위 경로에 저장됩니다.');layout.addWidget(self.status)
        self.filter=QComboBox();self.filter.addItems(['전체','HOMOGLYPH','JAMO','TRANSPARENT','OFFSCREEN']);layout.addWidget(self.filter)
        self.table=QTableWidget(0,6);self.table.setHorizontalHeaderLabels(['ID','페이지 URL','탐지 기법','원문 증거','CSS 위치','판별 결과']);self.table.setSortingEnabled(True);self.table.setSelectionBehavior(QTableWidget.SelectRows);layout.addWidget(self.table,3)
        self.evidence=QPlainTextEdit();self.evidence.setReadOnly(True);layout.addWidget(self.evidence,1)
        buttons=QHBoxLayout();copyurl=QPushButton('URL 복사');copysel=QPushButton('선택자 복사');export=QPushButton('결과 내보내기')
        for button in (copyurl,copysel,export):buttons.addWidget(button)
        layout.addLayout(buttons)
        self.start.clicked.connect(self.begin);self.stop.clicked.connect(self.cancel);choose.clicked.connect(self.choose)
        self.filter.currentTextChanged.connect(self.populate);self.table.itemSelectionChanged.connect(self.show_evidence)
        copyurl.clicked.connect(lambda:self.copy(1));copysel.clicked.connect(lambda:self.copy(4));export.clicked.connect(self.export)
        self.timer=QTimer(self);self.timer.timeout.connect(self.tick);self.seconds=0
    def choose(self):
        path,_=QFileDialog.getSaveFileName(self,'결과 저장',self.output.text(),'JSON (*.json)')
        if path:self.output.setText(path)
    def begin(self):
        if self.job and self.job.isRunning():return
        self.result=None;self.table.setRowCount(0);self.seconds=0
        self.job=ScanThread(self.url.text().strip(),self.output.text(),Config(max_pages=self.pages.value(),workers=self.workers.value(),topic=self.topic.text()))
        self.job.progress.connect(self.progress);self.job.complete.connect(self.finished);self.job.failed.connect(self.failure)
        self.start.setEnabled(False);self.stop.setEnabled(True);self.bar.setRange(0,0);self.timer.start(1000);self.job.start()
    def tick(self):
        self.seconds+=1;self.status.setText(self.status.text().split(' | ')[0]+f' | 경과 {self.seconds}초')
    def cancel(self):
        if self.job:self.job.crawler.stop();self.stop.setEnabled(False);self.status.setText('중지 요청 · 부분 결과를 저장하고 있습니다.')
    def progress(self,p):self.status.setText(f"방문 {p['visited']} · 후보 {p['candidates']} · 확정 {p['findings']} | 경과 {p['elapsed']:.1f}초")
    def reset(self):self.timer.stop();self.start.setEnabled(True);self.stop.setEnabled(False);self.bar.setRange(0,100);self.bar.setValue(100)
    def finished(self,result,details):
        self.result=result;self.details=details;self.reset();self.populate();self.status.setText(f"상태 {details['status']} · 방문 {len(details['visited'])} · 확정 {len(result['findings'])} · 오류/제외 {len(details['errors'])} · {result['meta']['elapsed_sec']}초")
        self.evidence.setPlainText(json.dumps({'status':details['status'],'errors':details['errors']},ensure_ascii=False,indent=2))
    def failure(self,message):self.reset();QMessageBox.critical(self,'검사 오류',message)
    def populate(self,*args):
        self.table.setSortingEnabled(False);self.table.setRowCount(0)
        if self.result:
            for finding in self.result['findings']:
                if self.filter.currentText() not in ('전체',finding['technique']):continue
                row=self.table.rowCount();self.table.insertRow(row)
                for col,key in enumerate(('id','url','technique','evidence_text','location','is_violation')):
                    item=QTableWidgetItem(str(finding[key]));item.setFlags(item.flags()&~Qt.ItemIsEditable);self.table.setItem(row,col,item)
        self.table.setSortingEnabled(True);self.table.resizeColumnsToContents()
    def copy(self,column):
        item=self.table.item(self.table.currentRow(),column)
        if item:QApplication.clipboard().setText(item.text())
    def show_evidence(self):
        row=self.table.currentRow()
        if row<0:return
        url=self.table.item(row,1).text();location=self.table.item(row,4).text()
        match=next((e for e in self.details.get('evidence',[]) if e['url']==url and e['location']==location),{})
        self.evidence.setPlainText(json.dumps(match,ensure_ascii=False,indent=2))
    def export(self):
        if not self.result:return
        path,_=QFileDialog.getSaveFileName(self,'결과 내보내기',str(self.base/'result.json'),'JSON (*.json)')
        if path:
            from .results import ResultManager
            ResultManager.export(path,self.result['meta'],self.result['findings'])
    def closeEvent(self,event):
        if self.job and self.job.isRunning():
            self.cancel();event.ignore();self.status.setText('중지 및 결과 저장 후 창을 닫아 주세요.')
        else:event.accept()

def launch(base,smoke=False):
    app=QApplication.instance() or QApplication([]);window=DesktopGUI(base);window.show()
    if smoke:QTimer.singleShot(1000,app.quit)
    return app.exec()
