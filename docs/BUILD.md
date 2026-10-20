# Installation, builds, and validation

Use Windows 11 x64 and Python 3.11 or later. The historical packaged build used Python 3.12.14. Run all commands from the repository root.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe main.py
```

`requirements-lock.txt` records exact versions in the validated environment. If a wheel is unavailable for your Python version, use `requirements.txt` and rerun the tests.

## Windows executable

```powershell
.\build.ps1 -Python .\.venv\Scripts\python.exe
```

Distribute the entire `release/PublicWebAdDetector` directory. Copying the executable alone is not supported. Bundled Chromium and libraries require several hundred megabytes. Build on Windows; PyInstaller produces artifacts for the current operating system. Follow your organization's approved PowerShell execution policy.

Use `-BrowserPath` to reuse a Playwright browser directory, and `-DistPath` or `-WorkPath` to change build directories.

The final build step checks Qt's ICU imports. If an unrelated build-host ICU library shadows Windows' native ICU, the helper verifies that the system library exports the required symbols before removing only the incompatible bundled DLL. This was necessary in the historical Windows 11 build; CLI and GUI startup passed after the fix.

Before redistributing binaries, run `python -m tests.collect_licenses` in the build environment and include the generated licenses and `THIRD_PARTY_NOTICES.md`. Consult the component licenses for their distribution requirements.

## Local fixture server

```powershell
.\.venv\Scripts\python.exe -m tests.server
# In a second terminal:
.\release\PublicWebAdDetector\PublicWebAdDetector.exe --url http://127.0.0.1:8765/ --output .\test-result.json
```

`tests/ground_truth.json` defines 16 expected URL, location, and technique tuples. Integration tests cover all four mandatory techniques, combined techniques, injected DOM content, legitimate public information, hidden menus, nested iframes, distinct query strings, empty results, and stop handling. Emitted locations are resolved again in a browser and compared with their original text. GUI tests use the real Qt event loop to exercise scanning, filtering, selection, copying, evidence display, and saved output.

Precision is TP/(TP+FP); recall is TP/(TP+FN). Screening recall counts expected rows whose `(URL, location)` survives screening, including multiple technique rows for the same element. `test_evidence/metrics.json` measures the browser scan duration, not total pytest duration. Fresh outputs are ignored by Git. Historical records are in [validation](validation/).

After a build, explicitly run the packaged smoke test:

```powershell
.\.venv\Scripts\python.exe -m tests.package_smoke
```

It tests the default `release/` path, the executable's default output directory, bundled-browser scanning, and GUI startup with external runtime path variables removed. Its fixture outputs beside the executable are removed after a successful check.

## Before competition submission

Compare the original competition attachments 1-4 with the implementation, especially `topic`, filenames, technique codes, schema, and evaluation URL rules. Recheck on an independent Windows 11 PC and measure performance on evaluation data. Optional AI and `ETC` findings are not implemented.
