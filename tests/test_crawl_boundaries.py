import asyncio
import threading
from http.server import ThreadingHTTPServer
from detector.crawler import Crawler,Config
from .server import Handler

def test_error_redirect_robots_auth_timeout(tmp_path):
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}'
    async def run():
        for path,marker in [('/blocked','robots.txt disallowed'),('/login','Authentication/CAPTCHA'),('/missing','HTTP 404'),('/external-redirect','')]:
            result,details=await Crawler(Config(settle_ms=10)).scan(base+path,tmp_path/'result.json')
            assert result['findings']==[]
            if path=='/external-redirect':
                assert not details['visited']
            else:
                assert details['errors']
                assert marker in str(details['errors'])
        r,d=await Crawler(Config(settle_ms=10)).scan(base+'/redirect',tmp_path/'redirect.json')
        assert not d['errors'] and d['visited']==[base+'/empty'] and not r['findings']
        r,d=await Crawler(Config(timeout_seconds=.01)).scan(base+'/',tmp_path/'timeout.json')
        assert d['status']=='timeout'
        assert isinstance(r['findings'],list)
    try:asyncio.run(run())
    finally:server.shutdown();server.server_close()
