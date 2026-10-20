import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from detector.crawler import LocationResolver,frame_path
from detector.engines import ScreeningEngine,VerificationEngine

def test_geometry_and_duplicate_frames():
    async def run():
        async with async_playwright() as pw:
            browser=await pw.chromium.launch(args=['--disable-gpu'])
            page=await browser.new_page()
            await page.set_content('''<body>
                <div style="height:0;overflow:hidden"><p id="clip">카지노 가입 보너스</p></div>
                <p id="far" style="position:absolute;left:99999px">카지노 가입 보너스</p>
                <p id="legit" style="margin-top:3000px">카지노 피해 예방 교육</p>
                <iframe src="about:blank"></iframe><iframe src="about:blank"></iframe>
            </body>''')
            dom=Path(__file__).parents[1]/'detector'/'dom.js'
            data=await page.evaluate(dom.read_text(encoding='utf-8'))
            rows={row['location']:row for row in data['elements']}
            for key in ('p#clip','p#far'):
                assert VerificationEngine().verify(ScreeningEngine().screen(rows[key]))==['OFFSCREEN']
            assert not rows['p#legit']['style']['outside']
            for frame in page.frames[1:]:
                await frame.set_content('<body><p id="ad">카지노 가입 보너스</p></body>')
            paths=[]
            for frame in page.frames[1:]:
                location=' >>> '.join(await frame_path(frame)+['#ad'])
                paths.append(location)
                target=await LocationResolver.resolve(page,location)
                assert await target.count()==1
            assert len(set(paths))==2
            await browser.close()
    asyncio.run(run())
