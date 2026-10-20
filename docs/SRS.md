# Software Requirements Specification (SRS)
## Public Website Illegal Advertisement Detection System

**Project Name:** Public Web Ad Detector
**Target:** 행정안전부·NIA 「공공 웹사이트 불법광고 탐지 도구 개발 공모전」
**Development Priority:** Detection Accuracy → Detection Coverage → Execution Speed → Usability

---

# 1. Project Objective

Develop a Windows 11 desktop application that automatically detects and classifies illegal advertisements embedded or concealed within public websites.

The system shall implement a **Two-Stage Detection Pipeline**:

1. **Screening:** Rapidly identify potentially suspicious web elements with high recall.
2. **Verification:** Perform detailed analysis of suspicious elements, eliminate false positives, classify detection techniques, and determine their precise locations.

The system must scan subpages, bulletin boards, comments, and nested iframes originating from a user-provided URL.

The final software must comply with all technical and submission requirements described in the attached competition guidelines.

# 2. Technical Architecture

## 2.1 Technology Stack

Use the following technologies unless a technically justified alternative offers better performance.

| Component | Technology |
|---|---|
| Main Language | Python 3.11+ |
| Web Crawling | Playwright, httpx |
| HTML Parsing | BeautifulSoup / lxml |
| Text Processing | Unicode normalization, regex |
| CSS Inspection | Playwright DOM API |
| Optional AI | External LLM API |
| GUI | PySide6 |
| Output | JSON |
| Packaging | PyInstaller |
| Target OS | Windows 11 |

The final application must operate on a standard CPU-based PC without a dedicated GPU.

Do not make AI API availability a prerequisite for core detection.

## 2.2 System Modules

Implement the following independent modules:

- `Crawler`: Discovers and visits webpages.
- `ScreeningEngine`: Extracts suspicious elements.
- `VerificationEngine`: Performs detailed classification.
- `TextNormalizer`: Processes obfuscated text.
- `StyleAnalyzer`: Examines computed CSS and element geometry.
- `LocationResolver`: Generates unique CSS selectors.
- `ResultManager`: Validates and exports detection results.
- `DesktopGUI`: Provides scanning controls and result visualization.

Each module must be independently testable.

# 3. Stage 1 — Screening Engine

## 3.1 Objective

Maximize recall while minimizing computational overhead.

False positives during screening are acceptable. False negatives should be minimized.

## 3.2 Crawling Requirements

The crawler shall:

1. Accept one entry URL from the user.
2. Discover internal hyperlinks and subpages.
3. Traverse bulletin boards, posts, and comment sections.
4. Inspect iframe contents, including nested iframes.
5. Support JavaScript-rendered content.
6. Track visited URLs to prevent redundant crawling.
7. Support concurrent page processing.
8. Handle network errors, redirects, and timeouts.
9. Preserve query parameters that identify distinct pages.
10. Avoid uncontrolled crawling into unrelated external websites.

Use a shared browser instance and a configurable number of concurrent workers.

Do not bypass authentication, CAPTCHA, access controls, or anti-bot restrictions.

## 3.3 Suspicious Element Screening

Inspect text-bearing DOM elements for the following indicators.

**A. Suspicious keywords**

Examples:

- 카지노
- 도박
- 토토
- 슬롯
- 바카라
- 불법 베팅
- 성인사이트
- 첫충
- 먹튀검증

Maintain an extensible keyword dictionary.

**B. Obfuscated text**

Identify potentially suspicious strings containing:

- Mixed Unicode scripts
- Fullwidth characters
- Confusable Unicode characters
- Decomposed Hangul jamo
- Unusual character separators

**C. Hidden text**

Identify potential concealment through:

- `opacity: 0`
- `color: transparent`
- Foreground/background color similarity
- `display: none`
- Extremely small font sizes
- Off-screen positioning
- Zero-sized or clipped regions

**D. Suspicious hyperlinks**

Inspect external URLs, unusual anchor text, and hidden links.

External hyperlinks alone must not be treated as illegal advertisements.

## 3.4 Screening Output

Each suspicious candidate shall contain:

- Source page URL
- DOM element reference
- Original text
- Normalized text
- Preliminary detection indicators
- Computed style information
- Parent and nearby element context
- iframe ancestry, if applicable

The screening engine shall pass all relevant candidates to the verification engine.

Do not discard candidates solely because a keyword is absent. CSS-based concealment must be detected independently.

# 4. Stage 2 — Verification Engine

## 4.1 Objective

Determine whether each candidate represents an illegal advertisement and identify the associated concealment or obfuscation technique.

The four mandatory detection categories must be supported.

## 4.2 HOMOGLYPH Detection

Detect advertisements employing visually confusable characters.

Examples:

- `ｃａｓｉｎｏ` → `casino`
- Fullwidth Latin characters
- Cyrillic characters resembling Latin characters
- Mixed-script advertising text

Implementation:

1. Preserve original text.
2. Apply Unicode normalization to a separate copy.
3. Apply a controlled confusable-character mapping.
4. Compare normalized text against advertising indicators.
5. Confirm that a relevant character-obfuscation technique exists.
6. Return `HOMOGLYPH` when advertisement and technique conditions are satisfied.

Do not classify ordinary multilingual content as an advertisement solely because it contains non-ASCII characters.

## 4.3 JAMO Detection

Detect Hangul advertising expressions split into jamo.

Example:

`ㅋㅏㅈㅣㄴㅗ` → `카지노`

Implementation:

1. Identify Hangul jamo sequences.
2. Recompose valid syllables.
3. Support common spacing and separator obfuscation.
4. Perform advertisement classification on the reconstructed text.
5. Retain the original text for output.

Return `JAMO` when appropriate.

## 4.4 TRANSPARENT Detection

Detect advertisements concealed through transparent styling.

Inspect actual computed styles rather than relying exclusively on inline CSS.

Indicators include:

- Zero or near-zero effective opacity
- Transparent text color
- Text and background colors that are visually indistinguishable

Account for inherited opacity and relevant ancestor elements.

Return `TRANSPARENT` when a concealed element contains illegal advertising content.

## 4.5 OFFSCREEN Detection

Detect advertisements concealed outside the visible webpage or through extremely small or hidden elements.

Indicators include:

- Large negative coordinates
- `display: none`
- Font size approximately 0–1 px
- Positioning outside visible page boundaries
- Other geometry-based concealment techniques

Use element geometry and computed styles.

Avoid misclassifying legitimate hidden menus, accessibility text, and responsive interface elements.

Return `OFFSCREEN` when appropriate.

## 4.6 Advertisement Classification

A suspicious element must not automatically be considered an illegal advertisement.

For example:

- "불법 도박을 예방합시다" — potentially legitimate public information.
- "카지노 가입 시 보너스 지급" — potentially promotional advertising.

Use a combination of:

- Keyword patterns
- Promotional language
- Nearby context
- Link characteristics
- Obfuscation indicators
- Concealment techniques

Develop a deterministic scoring or rule-based verification mechanism first.

Optional AI-based verification may be implemented only for ambiguous cases.

If external AI is used:

- Make calls asynchronously.
- Cache repeated classification results.
- Support configurable API credentials through `.env`.
- Never hardcode API keys.
- Keep the core system functional if the AI service is unavailable.

# 5. Detection Location and Classification

Every verified finding must provide an accurate and uniquely identifying element location.

Generate CSS selectors using:

1. Element tag names and classes.
2. Parent-child relationships separated by ` > `.
3. `nth-of-type()` where needed.
4. Attribute selectors where appropriate.

For iframe elements, use:

`iframe[src="ABSOLUTE_URL"] >>> element-selector`

For nested iframes, repeat the ` >>> ` separator.

**Important:** Verify that each generated selector resolves to exactly one intended element.

Use absolute iframe URLs, even if the original HTML uses relative paths.

If one DOM element uses multiple mandatory techniques, create a separate finding for each technique.

# 6. Output Requirements

## 6.1 Mandatory Result File

Generate `result.json` in UTF-8 without BOM.

The top-level object must contain `meta` and `findings`.

Use the following structure:

```json
{
  "meta": {
    "topic": "TOPIC",
    "entry_url": "https://example.go.kr",
    "started_at": "2026-10-22T10:00:00+09:00",
    "finished_at": "2026-10-22T10:01:30+09:00",
    "elapsed_sec": 90,
    "tool_version": "1.0.0"
  },
  "findings": [
    {
      "id": "f_001",
      "url": "https://example.go.kr/board/view?id=10",
      "is_violation": true,
      "location": "div.board > span.hidden",
      "evidence_text": "ㅋㅏㅈㅣㄴㅗ",
      "technique": "JAMO"
    }
  ]
}
```

The four permitted mandatory technique codes are:

- `HOMOGLYPH`
- `JAMO`
- `TRANSPARENT`
- `OFFSCREEN`

The `topic` value must follow the organizer's published schema; its examples use `TOPIC`.

Additional requirements:

- `findings` must be an array, even if empty.
- Each finding must have a unique ID.
- Preserve the original, unnormalized evidence text.
- Use valid ISO 8601 timestamps.
- Measure actual elapsed time.
- Include all detected subpages in one findings array.
- Deduplicate identical `(url, location, technique)` combinations.
- Preserve distinct URLs with different query parameter values.
- Do not replace multiple techniques with a combined code.

Before exporting, validate the entire JSON structure programmatically.

## 6.2 Optional Extended Detection

Implement additional techniques only after the four mandatory categories are working reliably.

Potential extensions include:

- Suspicious image-based advertising
- Hidden malicious redirects
- Encoded advertising text
- Dynamically injected promotional content

Save additional findings in `result_extra.json`.

Use `technique: "ETC"` and describe the additional type using `extra_finding`, as specified in the competition guidelines.

Do not mix additional categories into the mandatory result file.

# 7. Graphical User Interface

Develop a functional desktop GUI.

## 7.1 Main Screen

Provide:

- Target URL input
- Start scanning button
- Stop scanning button
- Scan progress indicator
- Number of visited pages
- Number of suspicious candidates
- Number of confirmed findings
- Elapsed execution time

## 7.2 Results Screen

Display a sortable findings table containing:

- Finding ID
- Page URL
- Detection technique
- Original evidence text
- CSS element location
- Verification result

When selecting a finding, show additional evidence including its surrounding context and relevant style attributes.

Provide filtering by technique, exporting results, and copying URLs/selectors.

The interface should remain responsive during crawling and analysis.

# 8. Performance Requirements

The organizer's evaluation imposes a **30-minute timeout ceiling**.

Optimize performance under this constraint.

The system shall:

1. Reuse browser instances.
2. Process independent pages concurrently.
3. Avoid repeated navigation.
4. Cache normalized text and verification results.
5. Limit unnecessary AI calls.
6. Avoid loading large media resources unless required for analysis.
7. Prioritize pages likely to contain user-generated content when necessary.
8. Save valid outputs when scanning completes or is stopped.

The first-stage screening process must be inexpensive enough to examine a large number of DOM elements.

Use configurable crawling limits and worker counts rather than hardcoded assumptions about the evaluation website.

**Important:** Prioritization must not permanently exclude pages merely because they lack suspicious keywords.

# 9. Testing and Validation

Develop a local test website that reproduces the competition's four mandatory detection cases.

Include at least:

- HOMOGLYPH positive cases
- JAMO positive cases
- TRANSPARENT positive cases
- OFFSCREEN positive cases
- Cases combining multiple techniques
- Legitimate content containing suspicious keywords
- Legitimate hidden UI elements
- Nested iframe cases
- Multiple bulletin-board pages
- Query-string variations
- Empty-result cases

Maintain a ground-truth dataset mapping each illegal advertisement to its expected URL, DOM location, and technique.

Evaluate:

**Recall**

\[
Recall=\frac{TP}{TP+FN}
\]

**Precision**

\[
Precision=\frac{TP}{TP+FP}
\]

**Execution Time**

Measure from scan start to scan completion.

Track first-stage recall separately from final-stage precision and recall.

Implement automated regression tests to prevent performance degradation following code changes.

Validate that every emitted CSS selector points to the intended DOM element.

# 10. Packaging and Delivery

The final submission must include:

1. Windows 11 executable (`.exe`).
2. Complete source code.
3. Installation/build instructions.
4. User manual.
5. Python dependency specifications.
6. Configuration examples.
7. Test cases and test execution instructions.

The application must run on a CPU-only Windows 11 PC.

Package the software using PyInstaller or an equivalent tool.

Ensure that `result.json` and, when applicable, `result_extra.json` are generated alongside the executable by default.

If a different output directory is used, document it on the first page of the user manual.

No developer-specific absolute paths or hardcoded secrets are permitted.

If an external AI API is used, document its provider, model, environment variable name, and configuration procedure. Replacing the API key must not require rebuilding the executable.

# 11. Development Priorities

Implement incrementally.

**Phase 1 — Core Engine**

- Project skeleton
- URL crawling
- HTML/DOM extraction
- Four mandatory detection techniques

**Phase 2 — Verification**

- Advertisement classification
- False-positive reduction
- Unique CSS selector generation
- iframe handling

**Phase 3 — Competition Compliance**

- `result.json` export
- Schema validation
- Windows executable packaging
- CPU-only compatibility

**Phase 4 — Quality and Performance**

- Benchmark suite
- Concurrent crawling
- GUI completion
- Performance optimization

**Phase 5 — Optional Enhancements**

- AI-assisted classification
- Additional detection categories
- Extended reporting functionality

Mandatory competition requirements take precedence over optional features.

# 12. Instructions to Codex

Implement the complete application according to this specification.

Follow these rules:

1. Begin by analyzing the attached competition PDF, especially Attachments 1–4.
2. Treat the organizer's requirements as authoritative where they differ from this specification.
3. Produce a modular, maintainable Python project.
4. Implement real detection functionality, not placeholder demonstrations.
5. Implement unit and integration tests.
6. Construct a representative local test website.
7. Run the tests and report measured detection metrics.
8. Validate the competition JSON output schema.
9. Build the Windows executable in a compatible Windows environment.
10. Document any incomplete requirement or unresolved technical limitation.

Before implementing optional AI features or additional detection categories, ensure the four mandatory techniques pass the local test suite.

**Definition of Done**

The project is complete only when:

- All four mandatory detection techniques are implemented and tested.
- The crawler supports subpages and nested iframes.
- Findings provide correct URLs, uniquely identifying selectors, and technique codes.
- Valid `result.json` output is generated.
- The GUI is functional.
- The packaged application has been verified on Windows 11 without a GPU.
- Full source code, build manual, and user manual are ready for submission.
- Test evidence and known limitations are documented.

Do not claim compliance or successful testing without execution evidence.
