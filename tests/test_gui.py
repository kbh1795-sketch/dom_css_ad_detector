import threading
import time
from pathlib import Path
from http.server import ThreadingHTTPServer
from PySide6.QtWidgets import QApplication
from detector.gui import DesktopGUI
from .server import Handler

def test_gui_scan_filter_copy_export(tmp_path):
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    app=QApplication.instance() or QApplication([])
    window=DesktopGUI(tmp_path);window.show()
    window.url.setText(f'http://127.0.0.1:{server.server_port}/')
    try:
        window.start.click()
        deadline=time.monotonic()+60
        while window.result is None and time.monotonic()<deadline:
            app.processEvents();time.sleep(.02)
        assert window.result is not None
        assert len(window.result['findings'])==16
        assert window.table.rowCount()==16
        window.filter.setCurrentText('JAMO');app.processEvents()
        assert window.table.rowCount()==3
        window.table.selectRow(0);window.copy(4)
        assert QApplication.clipboard().text()
        assert window.evidence.toPlainText()
        assert (tmp_path/'result.json').exists()
        evidence_dir=Path(__file__).parents[1]/'test_evidence';evidence_dir.mkdir(exist_ok=True)
        assert window.grab().save(str(evidence_dir/'gui.png'))
    finally:
        if window.job and window.job.isRunning():window.job.crawler.stop();window.job.wait(30000)
        window.close();server.shutdown();server.server_close()
