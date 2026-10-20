import json
import os
import tempfile
from pathlib import Path
from jsonschema import validate, FormatChecker

SCHEMA = {'type':'object','required':['meta','findings'],'additionalProperties':False,'properties':{
 'meta':{'type':'object','required':['topic','entry_url','started_at','finished_at','elapsed_sec','tool_version'],'properties':{k:{'type':'number' if k=='elapsed_sec' else 'string'} for k in ('topic','entry_url','started_at','finished_at','elapsed_sec','tool_version')}},
 'findings':{'type':'array','items':{'type':'object','additionalProperties':False,'required':['id','url','is_violation','location','evidence_text','technique'],'properties':{'id':{'type':'string'},'url':{'type':'string'},'is_violation':{'const':True},'location':{'type':'string','minLength':1},'evidence_text':{'type':'string'},'technique':{'enum':['HOMOGLYPH','JAMO','TRANSPARENT','OFFSCREEN']}}}}}}

class ResultManager:
    @staticmethod
    def export(path, meta, findings):
        unique = {(f['url'],f['location'],f['technique']):f for f in findings}
        ordered = sorted(unique.values(), key=lambda f:(f['url'], f['location'], f['technique']))
        rows = [dict(f,id=f'f_{i:03d}') for i,f in enumerate(ordered,1)]
        result = {'meta':meta,'findings':rows}
        SCHEMA['properties']['meta']['additionalProperties']=False
        for key in ('started_at','finished_at'):
            SCHEMA['properties']['meta']['properties'][key]['format']='date-time'
        SCHEMA['properties']['meta']['properties']['elapsed_sec']['minimum']=0
        validate(result,SCHEMA,format_checker=FormatChecker())
        from datetime import datetime
        for key in ('started_at','finished_at'):
            if datetime.fromisoformat(meta[key]).tzinfo is None: raise ValueError('Timezone required')
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
        fd,tmp=tempfile.mkstemp(dir=path.parent,suffix='.tmp')
        try:
            with os.fdopen(fd,'w',encoding='utf-8',newline='\n') as stream: json.dump(result,stream,ensure_ascii=False,indent=2)
            os.replace(tmp,path)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)
        return result
