# Requirements status

| Requirement | Implemented and checked | Remaining work |
|---|---|---|
| Independent two-stage modules | TextNormalizer, ScreeningEngine, VerificationEngine, StyleAnalyzer, Crawler, LocationResolver, ResultManager, DesktopGUI | Real-site corpus calibration |
| Four mandatory techniques | Jamo composition, NFKC/confusables, computed CSS and ancestor opacity, geometry and clipping | Broader confusables and complex styles |
| Subpages, boards, queries | Same-origin links, preserved queries, concurrent pages | Click/form navigation and infinite scroll |
| Comments | Rendered DOM and exposed comment links | Interaction-only comments |
| Nested iframes | Recursive inspection, unique paths, absolute src | Relative-src reproduction uses the resolver |
| False-positive reduction | Promotion/public-context rules, links, concealment, negative fixtures | Generalization validation |
| Unique locations | Extraction uniqueness, pre-export text match, browser re-resolution tests | Mutable remote DOM |
| JSON | Local schema, timestamps, UTF-8, deduplication, separate techniques | Official schema and topic confirmation |
| GUI | Threaded scan, stop, counts, filters, sorting, details, export | Large-result UI load testing |
| Time and concurrency | Shared Chromium, worker/page/time limits, media blocking | Full 30-minute load benchmark |
| Access restrictions | Robots checks, auth/CAPTCHA skips, bounded link discovery | Complete block-page recognition |
| Tests | Unit, DOM, browser, GUI, crawl boundaries; 16 expected findings | Competition data and independent PC |
| Windows packaging | PyInstaller with Chromium; historical CLI/GUI checks | Signing, installer, current English rebuild |
| CPU-only operation | No dedicated GPU requirement; browser GPU disabled | Independent physically GPU-free hardware |
| Documentation | Build/user manuals, full source, locked dependencies | Original competition attachments 1-4 |
| Optional AI and ETC | Not implemented | Consider after mandatory quality targets |

Historical evidence is under [validation](validation/); fresh test output is generated in the ignored root `test_evidence/` directory. This table is not a certification of competition compliance.
