# Historical execution validation report

Date: 2026-10-20 (Australia/Sydney).

These are records of the earlier packaged build. Fresh tests write to the ignored root `test_evidence/` directory. English documentation and UI edits do not retroactively update the historical binary.

| Check | Observation |
|---|---|
| OS | Windows 11 Home x64, 10.0.26200 |
| Python | 3.12.14 |
| Automated tests | 12 passed; [log](validation/pytest.txt) |
| Ground truth | Four local pages, 16 expected technique findings |
| TP / FP / FN | 16 / 0 / 0 |
| Precision / recall | 100% / 100% |
| Screening recall | 100% |
| Source scan duration | `elapsed_sec` in [metrics](validation/metrics.json) |
| Historical packaged scan duration | 6.406 seconds |
| Packaged CLI / GUI startup exit codes | 0 / 0 |
| Packaged ground-truth match | All 16 URL/location/technique tuples |
| External path settings | PLAYWRIGHT_BROWSERS_PATH, PYTHONPATH, PYTHONHOME, and VIRTUAL_ENV removed |
| Dedicated GPU dependency | None required; Chromium used --disable-gpu |

Evidence: [metrics](validation/metrics.json), [pytest log](validation/pytest.txt), [packaged smoke report](validation/packaged_smoke.json), and [packaged results](validation/packaged_result.json). Original Korean evidence is preserved unchanged.

DOM tests cover ancestor clipping, large positive coordinates, legitimate below-fold content, and duplicate iframe src values. Boundary tests cover robots restrictions, authentication screens, 404 responses, redirects, external-origin exclusion, and timeout output. GUI behavior was tested with the source application's Qt event loop; packaged checks separately tested window creation and normal shutdown.

Packaging initially exposed Windows path-length and ICU DLL issues. The full Chromium headless channel and verified native Windows ICU resolved them before the successful historical smoke test.

This is evidence from a small local suite. Original competition attachments, official schema compliance, hidden evaluation data, an independent clean Windows PC, physically GPU-free hardware, and large-scale 30-minute load have not been verified. Full competition compliance is not claimed.
