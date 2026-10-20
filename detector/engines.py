import re
from .text import TextNormalizer, KEYWORDS

class StyleAnalyzer:
    @staticmethod
    def techniques(style):
        result = []
        if style.get('opacity', 1) <= .02 or style.get('alpha', 1) <= .02 or style.get('sameColor', False):
            result.append('TRANSPARENT')
        if any(style.get(k, False) for k in ('displayNone', 'invisible', 'tiny', 'clipped', 'outside')):
            result.append('OFFSCREEN')
        return result

class ScreeningEngine:
    def __init__(self, keywords=KEYWORDS):
        self.keywords = tuple(TextNormalizer.normalize(k)[0] for k in keywords)

    def screen(self, element):
        normalized, jamo, homo = TextNormalizer.normalize(element['text'])
        techniques = StyleAnalyzer.techniques(element['style'])
        if jamo: techniques.append('JAMO')
        if homo: techniques.append('HOMOGLYPH')
        matched = [k for k in self.keywords if k in normalized]
        if not (matched or techniques): return None
        return dict(element, normalized=normalized, techniques=techniques, keywords=matched)

class VerificationEngine:
    def verify(self, candidate):
        if not candidate['keywords']: return []
        text = candidate['normalized']
        context = TextNormalizer.normalize(candidate.get('context', ''))[0]
        promo = bool(re.search('가입|보너스|첫충|충전|환전|배당|무료머니|추천코드|지급|bonus|signup|jackpot', text))
        public = bool(re.search('예방|신고|근절|위험|중독|상담|단속|피해|금지|보도|교육', text))
        linked = bool(candidate.get('external'))
        conceal = any(t in candidate['techniques'] for t in ('TRANSPARENT', 'OFFSCREEN'))
        obfuscated = any(t in candidate['techniques'] for t in ('JAMO', 'HOMOGLYPH'))
        score = 2 + 3*promo + linked + conceal + obfuscated - 5*public
        # Nearby text can corroborate but cannot alone convert public guidance into advertising.
        if not public and re.search('보너스|첫충|추천코드', context): score += 1
        candidate['verification'] = {'score': score, 'promotional': promo, 'public_information': public}
        return sorted(set(candidate['techniques'])) if score >= 4 else []
