"""Run explicitly after building: python -m tests.package_smoke"""
import json
import os
import platform
import subprocess
import threading
from pathlib import Path
from http.server import ThreadingHTTPServer
from .server import Handler

def main():
    root=Path(__file__).parents[1]
    exe=root/'release'/'PublicWebAdDetector'/'PublicWebAdDetector.exe'
    evidence=root/'test_evidence';evidence.mkdir(exist_ok=True)
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}'
    env=dict(os.environ)
    for key in ('PLAYWRIGHT_BROWSERS_PATH','PYTHONPATH','PYTHONHOME','VIRTUAL_ENV'):
        env.pop(key,None)
    kwargs={'env':env,'capture_output':True,'encoding':'utf-8','errors':'replace','timeout':90,'creationflags':subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0}
    try:
        # No --output: verifies the required default directory alongside executable.
        cli=subprocess.run([str(exe),'--url',base+'/'],**kwargs)
        result=json.loads(exe.with_name('result.json').read_text(encoding='utf-8'))
        details=json.loads(exe.with_name('scan_details.json').read_text(encoding='utf-8'))
        truth=json.loads((root/'tests'/'ground_truth.json').read_text(encoding='utf-8'))
        expected={(base+u,s.replace('{base}',base),t) for u,s,t in truth}
        found={(f['url'],f['location'],f['technique']) for f in result['findings']}
        gui=subprocess.run([str(exe),'--smoke-gui'],**kwargs)
        report={'platform':platform.platform(),'cli_exit_code':cli.returncode,'gui_exit_code':gui.returncode,'findings':len(result['findings']),'ground_truth_match':found==expected,'status':details['status'],'errors':details['errors'],'elapsed_sec':result['meta']['elapsed_sec'],'bundled_browser_without_environment':True,'gpu_disabled_for_browser':True,'stdout':cli.stdout,'stderr':cli.stderr,'gui_stderr':gui.stderr}
        (evidence/'packaged_smoke.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        (evidence/'packaged_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        assert cli.returncode==0 and gui.returncode==0,report
        assert found==expected and not details['errors'],report
        # Avoid presenting the fixture scan as a user's fresh result.
        exe.with_name('result.json').unlink();exe.with_name('scan_details.json').unlink()
        print(json.dumps(report,ensure_ascii=False,indent=2))
    finally:server.shutdown();server.server_close()

if __name__=='__main__':main()
