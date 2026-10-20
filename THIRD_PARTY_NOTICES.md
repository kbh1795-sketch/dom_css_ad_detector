# Third-party components

This source repository uses Python, Qt/PySide6, Playwright, Chromium, and Python dependencies; it does not vendor their binaries. A packaged Windows release bundles those components separately from the application source. Chromium retains its own license material inside the browser distribution.

Before distributing a built release, run `python -m tests.collect_licenses` in the build environment and include the generated `third_party_licenses` directory and this notice alongside the executable. Review the original component licenses; this generated inventory is supporting material, not a replacement for their terms.

- Python: https://www.python.org/psf/license/
- PySide6 / Qt for Python: https://doc.qt.io/qtforpython-6/licenses.html
- Qt: https://www.qt.io/licensing/open-source-lgpl-obligations
- Playwright: https://github.com/microsoft/playwright-python/blob/main/LICENSE
- Chromium: https://chromium.googlesource.com/chromium/src/+/HEAD/LICENSE
- PyInstaller: https://pyinstaller.org/en/stable/license.html

Qt libraries are dynamically linked and shipped as separate files in `_internal/PySide6`. The complete application source and dependency versions are provided, and the application can be rebuilt with replacement compatible Qt/PySide6 libraries. The application source is licensed under the MIT License in the root LICENSE file. This does not relicense third-party components. Any competition-specific distribution terms remain to be reviewed against the missing official guidelines.
