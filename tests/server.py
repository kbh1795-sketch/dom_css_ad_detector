from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit,parse_qs

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        url=urlsplit(self.path)
        if url.path=='/redirect':
            self.send_response(302);self.send_header('Location','/empty');self.end_headers();return
        if url.path=='/external-redirect':
            self.send_response(302);self.send_header('Location','https://example.org/');self.end_headers();return
        if url.path=='/robots.txt':body='User-agent: *\nDisallow: /blocked';kind='text/plain'
        elif url.path=='/login':body='<body><input type="password"></body>';kind='text/html'
        elif url.path=='/board':
            body='<meta charset="utf-8"><body><p id="post" '+('style="display:none">카지노 가입 보너스' if parse_qs(url.query).get('id')==['1'] else '>ㅋㅏㅈㅣㄴㅗ 가입 보너스')+'</p></body>';kind='text/html'
        else:
            filename={'/':'index.html','/frame':'frame.html','/nested':'nested.html','/empty':'empty.html'}.get(url.path)
            if not filename:self.send_error(404);return
            body=(Path(__file__).parent/'site'/filename).read_text(encoding='utf-8');kind='text/html'
        self.send_response(200);self.send_header('Content-Type',kind+'; charset=utf-8');self.end_headers();self.wfile.write(body.encode())

if __name__=='__main__':
    print('Test site: http://127.0.0.1:8765',flush=True);ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
