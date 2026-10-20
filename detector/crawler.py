import asyncio
import json
import time
import threading
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser
import httpx
from playwright.async_api import async_playwright
from .engines import ScreeningEngine, VerificationEngine
from .results import ResultManager

@dataclass
class Config:
    max_pages: int = 200
    workers: int = 3
    timeout_seconds: float = 1740
    navigation_timeout_ms: int = 20000
    settle_ms: int = 700
    topic: str = 'TOPIC'
    keywords: list | None = None

def canonical(url):
    p=urlsplit(url)
    if p.scheme not in ('http','https') or not p.hostname or p.username or p.password: return None
    return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path or '/',p.query,''))

class LocationResolver:
    @staticmethod
    async def resolve(page, location):
        import re
        frame = page.main_frame
        parts = location.split(' >>> ')
        for part in parts[:-1]:
            match = re.search(r'\[src=("(?:[^"\\]|\\.)*")\]$', part)
            if not match: raise ValueError('Invalid iframe selector')
            absolute = json.loads(match.group(1))
            structural = part[:match.start()]
            matches = []
            for element in await frame.locator(structural).all():
                if await element.evaluate('(el) => el.src') == absolute:
                    matches.append(element)
            if len(matches) != 1: raise ValueError('Iframe selector is not unique')
            handle = await matches[0].element_handle()
            frame = await handle.content_frame()
            if frame is None: raise ValueError('Iframe detached')
        locator = frame.locator(parts[-1])
        if await locator.count() != 1: raise ValueError('Element selector is not unique')
        return locator

class Crawler:
    def __init__(self, config=None, callback=None):
        self.config=config or Config();self.callback=callback or (lambda x:None)
        self.stop_event=threading.Event();self.findings=[];self.evidence=[];self.errors=[]
        self.visited=set();self.candidates=0;self.screened=[]

    def stop(self): self.stop_event.set()

    async def scan(self, entry, output):
        entry=canonical(entry)
        if not entry: raise ValueError('Enter a valid HTTP or HTTPS URL.')
        cfg=self.config
        if not (1<=cfg.workers<=16 and cfg.max_pages>=1 and 0<cfg.timeout_seconds<=1800): raise ValueError('Invalid scan limits')
        start=time.perf_counter();started=datetime.now().astimezone().isoformat()
        origin=urlsplit(entry); origin_key=(origin.scheme,origin.netloc)
        self.findings=[];self.evidence=[];self.errors=[];self.visited=set();self.candidates=0;self.screened=[]
        screening=ScreeningEngine(cfg.keywords) if cfg.keywords else ScreeningEngine();verification=VerificationEngine()
        queue=asyncio.Queue();queue.put_nowait(entry);scheduled={entry}
        robot=RobotFileParser();robot.parse([])
        async with httpx.AsyncClient(timeout=10,follow_redirects=False) as client:
            try:
                r=await client.get(urlunsplit((*origin_key,'/robots.txt','','')))
                if r.status_code==200:robot.parse(r.text.splitlines())
                elif r.status_code in (401,403):robot.disallow_all=True
            except httpx.HTTPError as exc:self.errors.append({'url':entry,'error':'robots.txt unavailable: '+str(exc)})
        dom=Path(__file__).with_name('dom.js').read_text(encoding='utf-8')
        async def route_request(route):
            req=route.request;p=urlsplit(req.url)
            if req.resource_type in ('media','image','font') or (req.is_navigation_request() and req.frame==req.frame.page.main_frame and (p.scheme,p.netloc)!=origin_key):await route.abort()
            elif req.is_navigation_request() and not robot.can_fetch('PublicWebAdDetector', req.url) and (p.scheme,p.netloc)==origin_key:await route.abort()
            else:await route.continue_()
        status='completed'
        try:
            async with async_playwright() as pw:
                browser=await pw.chromium.launch(channel='chromium',headless=True,args=['--disable-gpu'])
                context=await browser.new_context(user_agent='PublicWebAdDetector/1.0',viewport={'width':1366,'height':900})
                await context.route('**/*',route_request)
                async def worker():
                    while True:
                        url=await queue.get()
                        page=None
                        try:
                            if self.stop_event.is_set():continue
                            if not robot.can_fetch('PublicWebAdDetector',url):
                                self.errors.append({'url':url,'error':'robots.txt disallowed'});continue
                            page=await context.new_page()
                            response=await page.goto(url,wait_until='domcontentloaded',timeout=cfg.navigation_timeout_ms)
                            if response and response.status>=400:raise RuntimeError(f'HTTP {response.status}')
                            await page.wait_for_timeout(cfg.settle_ms)
                            if await page.locator('input[type=password],iframe[src*="recaptcha"],iframe[src*="hcaptcha"]').count():
                                raise RuntimeError('Authentication/CAPTCHA encountered; skipped')
                            actual=canonical(page.url)
                            if not actual or (urlsplit(actual).scheme,urlsplit(actual).netloc)!=origin_key:continue
                            self.visited.add(actual)
                            for frame in list(page.frames):
                                try:
                                    # Frame paths resolve without changing the live page.
                                    ancestry=await frame_path(frame)
                                    data=await frame.evaluate(dom)
                                    for element in data['elements']:
                                        candidate=screening.screen(element)
                                        if not candidate:continue
                                        location=' >>> '.join(ancestry+[element['location']])
                                        candidate.update(url=actual,location=location,frame_url=frame.url)
                                        self.candidates+=1;self.screened.append((actual,location))
                                        techniques=verification.verify(candidate)
                                        if techniques:
                                            resolved=await LocationResolver.resolve(page,location)
                                            if (await resolved.text_content()).strip()!=element['text']:
                                                raise ValueError('Element changed during verification')
                                        for technique in techniques:
                                            finding={'url':actual,'is_violation':True,'location':location,'evidence_text':element['text'],'technique':technique}
                                            self.findings.append(finding);self.evidence.append(dict(candidate,technique=technique))
                                    for link in data['links']:
                                        normalized=canonical(link)
                                        if normalized and (urlsplit(normalized).scheme,urlsplit(normalized).netloc)==origin_key and normalized not in scheduled and len(scheduled)<cfg.max_pages:
                                            scheduled.add(normalized);queue.put_nowait(normalized)
                                except Exception as exc:self.errors.append({'url':actual,'frame':frame.url,'error':str(exc)})
                            self.callback({'visited':len(self.visited),'candidates':self.candidates,'findings':len(self.findings),'elapsed':time.perf_counter()-start})
                        except Exception as exc:self.errors.append({'url':url,'error':str(exc)})
                        finally:
                            if page:await page.close()
                            queue.task_done()
                tasks=[asyncio.create_task(worker()) for _ in range(cfg.workers)]
                try:
                    while queue._unfinished_tasks:
                        if self.stop_event.is_set():status='stopped';break
                        if time.perf_counter()-start>=cfg.timeout_seconds:status='timeout';break
                        await asyncio.sleep(.05)
                finally:
                    for task in tasks:task.cancel()
                    await asyncio.gather(*tasks,return_exceptions=True)
                    await browser.close()
        except Exception as exc:
            status='failed';self.errors.append({'url':entry,'error':str(exc)})
        meta={'topic':cfg.topic,'entry_url':entry,'started_at':started,'finished_at':datetime.now().astimezone().isoformat(),'elapsed_sec':round(time.perf_counter()-start,3),'tool_version':'1.0.0'}
        result=ResultManager.export(output,meta,self.findings)
        details={'status':status,'visited':sorted(self.visited),'candidates':self.candidates,'errors':self.errors,'evidence':self.evidence,'config':asdict(cfg)}
        Path(output).with_name('scan_details.json').write_text(json.dumps(details,ensure_ascii=False,indent=2),encoding='utf-8')
        return result,details

async def frame_path(frame):
    parts=[]
    while frame.parent_frame:
        element=await frame.frame_element()
        part=await element.evaluate('''el=>{
            const doc=el.ownerDocument, abs=el.src;
            let s='iframe[src='+JSON.stringify(abs)+']';
            // Resolve absolute iframe URLs by the scanner's documented resolver.
            const same=[...doc.querySelectorAll('iframe')].filter(x=>x.src===abs);
            if(same.length>1){let chain=[];for(let n=el;n;n=n.parentElement){let p=n.localName;if(n.parentElement){let siblings=[...n.parentElement.children].filter(x=>x.localName===n.localName);p+=':nth-of-type('+(siblings.indexOf(n)+1)+')';}chain.unshift(p);}s=chain.join(' > ')+'[src='+JSON.stringify(abs)+']';}
            return s;
        }''')
        parts.insert(0,part);frame=frame.parent_frame
    return parts
