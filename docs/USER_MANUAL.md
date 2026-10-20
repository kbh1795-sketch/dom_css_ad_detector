# User manual

## Output location and startup

**Default outputs are `result.json` and `scan_details.json` beside the executable.** When running from source, they are saved beside `main.py`. The directory must be writable, and a subsequent scan replaces files with the same names. The GUI lets you change the destination.

On Windows 11 x64, extract the complete distribution and run `PublicWebAdDetector.exe`. Keep `_internal` beside it. The packaged application does not need a separate Python installation or dedicated GPU. A console window may accompany the GUI because CLI mode is also supported.

1. Enter a URL you are authorized to inspect.
2. Set **Max pages** and **Workers**. Defaults are 200 pages and 3 workers; these limits do not imply complete site coverage.
3. Set **Official topic** only after checking the competition schema. `TOPIC` is currently the SRS example value.
4. Select **Start scan** to view page, candidate, finding, and elapsed-time counts.
5. Select **Stop** to cancel active work and save confirmed partial results. Keep the window open until saving finishes.
6. Filter or sort the results. Select a row to inspect context, computed styles, keyword matches, and verification scores. Copy URLs/selectors or export to another JSON file.

## Interpreting output

`result.json` is UTF-8 without a BOM and contains `meta` and `findings`. It preserves original evidence and emits a separate row for each observed mandatory technique: `HOMOGLYPH`, `JAMO`, `TRANSPARENT`, or `OFFSCREEN`. An empty array means no confirmed mandatory-technique findings, not that the entire site is clean.

`scan_details.json` includes status (`completed`, `stopped`, `timeout`, or `failed`), visited URLs, errors/skips, context, and styles. Always review errors and coverage alongside findings. This file is separate from the mandatory result schema.

Nested locations use `iframe[src="ABSOLUTE_URL"] >>> element-selector`. Since raw HTML may contain a relative `src`, reproduce locations with `LocationResolver.resolve(page, location)`. It compares the browser-resolved `iframe.src` and verifies uniqueness at every step. `>>>` is not a standard CSS operator.

## Command line and configuration

```powershell
.\PublicWebAdDetector.exe --url https://example.go.kr --output .\result.json --config .\config.example.json
```

`timeout_seconds` defaults to 1740 and must not exceed 1800. The default leaves room for startup and cleanup. Increasing `settle_ms` waits longer for late DOM injection but slows scanning. A `keywords` string array replaces the default dictionary.

Only links matching the entry URL's scheme, host, and port are followed. Readable embedded frames are inspected, including cross-origin frames, but unrelated external links are not crawled. Images, media, and web fonts are blocked. Authentication and CAPTCHA are not bypassed.

Result files are written through a temporary file and atomically replaced. Forced process termination or power loss does not guarantee partial output from the current scan. Source-only UI changes do not update previously built executables; rebuild for the current English interface.
