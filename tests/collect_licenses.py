"""Copy license files from this build environment without embedding its absolute paths."""
import importlib.metadata
import json
import shutil
import sys
from pathlib import Path

def main():
    root=Path(__file__).parents[1]
    target=root/'third_party_licenses';target.mkdir(exist_ok=True)
    inventory=[]
    for dist in importlib.metadata.distributions():
        name=dist.metadata.get('Name','unknown')
        inventory.append({'name':name,'version':dist.version,'license':dist.metadata.get('License-Expression') or dist.metadata.get('License','')})
        for file in dist.files or []:
            if any(x in file.name.upper() for x in ('LICENSE','COPYING','COPYRIGHT')) and '.dist-info' in str(file):
                source=Path(dist.locate_file(file))
                if not source.is_file():continue
                destination=target/name/file.name
                destination.parent.mkdir(exist_ok=True)
                shutil.copy2(source,destination)
    base=Path(sys.base_prefix)
    for source in (base/'LICENSE.txt',base/'LICENSE'):
        if source.is_file():shutil.copy2(source,target/'Python-LICENSE.txt')
    (target/'inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Collected available distribution license files.')

if __name__=='__main__':main()
