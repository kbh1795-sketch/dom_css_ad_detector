import re
import unicodedata
from functools import lru_cache

KEYWORDS = ('카지노', '도박', '토토', '슬롯', '바카라', '베팅', '성인사이트', '첫충', '먹튀검증', 'casino', 'betting', 'baccarat', 'slots')
CONFUSABLES = str.maketrans(dict(zip('аесорхуіјѕΑΒΕΖΗΙΚΜΝΟΡΤΧ', 'aecopxyijsABEZHIKMNOPTX')))
L = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
V = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
T = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'

class TextNormalizer:
    @staticmethod
    @lru_cache(maxsize=16384)
    def normalize(text):
        original = text
        text = unicodedata.normalize('NFKC', text).translate(CONFUSABLES).lower()
        # Compatibility and conjoining jamo share a compatibility representation.
        chars = []
        for c in text:
            d = unicodedata.decomposition(c)
            if 0x1100 <= ord(c) <= 0x11ff:
                found = next((x for x in L + V + T[1:] if unicodedata.normalize('NFKD', x) == c), c)
                chars.append(found)
            else:
                chars.append(c)
        text = re.sub(r'[\s\W_\u200b-\u200f\ufeff]+', '', ''.join(chars))
        out, i = [], 0
        while i < len(text):
            if i + 1 < len(text) and text[i] in L and text[i+1] in V:
                a, b, final = L.index(text[i]), V.index(text[i+1]), 0
                i += 2
                if i < len(text) and text[i] in T[1:] and not (i+1 < len(text) and text[i+1] in V):
                    final = T.index(text[i]); i += 1
                out.append(chr(0xac00 + (a*21+b)*28+final))
            else:
                out.append(text[i]); i += 1
        normalized = unicodedata.normalize('NFC', ''.join(out))
        jamo = bool(re.search('[\u1100-\u11ff\u3130-\u318f]', original))
        homo = any(unicodedata.east_asian_width(c) == 'F' or c.translate(CONFUSABLES) != c for c in original)
        return normalized, jamo, homo
