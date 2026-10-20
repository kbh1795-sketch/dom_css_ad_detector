import os
import sys
import asyncio
import argparse
from pathlib import Path

if getattr(sys,'frozen',False):
    os.environ['PLAYWRIGHT_BROWSERS_PATH']=str(Path(sys._MEIPASS)/'browsers')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--url');parser.add_argument('--output');parser.add_argument('--config');parser.add_argument('--smoke-gui',action='store_true')
    args=parser.parse_args()
    base=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).parent
    if args.url:
        import json
        from detector.crawler import Crawler,Config
        config=Config(**json.loads(Path(args.config).read_text(encoding='utf-8'))) if args.config else Config()
        result,details=asyncio.run(Crawler(config).scan(args.url,args.output or base/'result.json'))
        print(json.dumps({'status':details['status'],'findings':len(result['findings']),'errors':details['errors']},ensure_ascii=False))
        return 1 if details['status']=='failed' else 0
    from detector.gui import launch
    return launch(base,args.smoke_gui)

if __name__=='__main__':sys.exit(main())
