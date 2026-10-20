import json
import pytest
from detector.text import TextNormalizer
from detector.engines import ScreeningEngine,VerificationEngine
from detector.results import ResultManager
from detector.crawler import canonical

@pytest.mark.parametrize('text,expected', [('ㅋㅏㅈㅣㄴㅗ','카지노'),('ㅋ ㅏ.ㅈ ㅣ.ㄴ ㅗ','카지노'),('카지노','카지노'),('ｃａｓｉｎｏ','casino'),('саsіnо','casino')])
def test_normalization(text,expected):assert TextNormalizer.normalize(text)[0]==expected

def test_public_and_hidden_independent():
    screen=ScreeningEngine();verify=VerificationEngine()
    c=screen.screen({'text':'불법 도박 예방 상담','style':{'displayNone':True}})
    assert c and verify.verify(c)==[]
    c=screen.screen({'text':'메뉴','style':{'opacity':0}})
    assert c and verify.verify(c)==[]

def test_urls():
    assert canonical('https://Example.org/a?id=1#x')=='https://example.org/a?id=1'
    assert canonical('https://example.org/a?id=1')!=canonical('https://example.org/a?id=2')
    assert canonical('javascript:alert(1)') is None

def test_schema(tmp_path):
    meta=dict(topic='TOPIC',entry_url='http://localhost/',started_at='2026-10-20T00:00:00+00:00',finished_at='2026-10-20T00:00:01+00:00',elapsed_sec=1,tool_version='1.0.0')
    f=dict(url=meta['entry_url'],location='#a',evidence_text='ㅋㅏㅈㅣㄴㅗ',technique='JAMO',is_violation=True)
    path=tmp_path/'result.json';r=ResultManager.export(path,meta,[f,f]);assert len(r['findings'])==1
    assert not path.read_bytes().startswith(b'\xef\xbb\xbf')
    f['technique']='ETC'
    with pytest.raises(Exception):ResultManager.export(path,meta,[f])
