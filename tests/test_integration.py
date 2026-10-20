import asyncio
import json
import threading
from pathlib import Path
from http.server import ThreadingHTTPServer
from playwright.async_api import async_playwright
from detector.crawler import Crawler,Config,LocationResolver
from .server import Handler

def test_end_to_end(tmp_path):
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base=f'http://127.0.0.1:{server.server_port}'
    async def run():
        scanner=Crawler(Config(settle_ms=400,max_pages=20))
        result,details=await scanner.scan(base+'/',tmp_path/'result.json')
        truth=json.loads(Path(__file__).with_name('ground_truth.json').read_text(encoding='utf-8'))
        expected={(base+u,s.replace('{base}',base),t) for u,s,t in truth}
        found={(f['url'],f['location'],f['technique']) for f in result['findings']}
        screened=set(scanner.screened)
        tp=len(expected&found);fp=len(found-expected);fn=len(expected-found)
        metrics={'true_positives':tp,'false_positives':fp,'false_negatives':fn,'precision':tp/(tp+fp) if tp+fp else 0,'recall':tp/(tp+fn),'screening_recall':sum((u,s) in screened for u,s,t in expected)/len(expected),'elapsed_sec':result['meta']['elapsed_sec'],'pages':len(details['visited']),'errors':details['errors']}
        evidence_dir=Path(__file__).parents[1]/'test_evidence';evidence_dir.mkdir(exist_ok=True)
        (evidence_dir/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
        (evidence_dir/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        assert not details['errors'],details['errors']
        assert found==expected,{'missing':expected-found,'extra':found-expected}
        async with async_playwright() as pw:
            browser=await pw.chromium.launch(args=['--disable-gpu'])
            page=await browser.new_page()
            for url in sorted({f['url'] for f in result['findings']}):
                await page.goto(url);await page.wait_for_timeout(400)
                for f in [x for x in result['findings'] if x['url']==url]:
                    locator=await LocationResolver.resolve(page,f['location'])
                    assert await locator.count()==1
                    assert (await locator.text_content()).strip()==f['evidence_text']
            await browser.close()
        empty,_=await Crawler(Config(settle_ms=100)).scan(base+'/empty',tmp_path/'empty.json')
        assert empty['findings']==[]
        stopped=Crawler();stopped.stop()
        r,d=await stopped.scan(base+'/',tmp_path/'stopped.json')
        assert d['status']=='stopped' and r['findings']==[]
    try:asyncio.run(run())
    finally:server.shutdown();server.server_close()
