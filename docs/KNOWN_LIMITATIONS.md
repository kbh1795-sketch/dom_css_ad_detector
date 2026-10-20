# Known limitations

## Compliance and environment

- Implementation started from the supplied SRS. Competition PDF attachments 1-4 and the official JSON schema were not verified. `TOPIC` is provisional; the shipped schema is a local SRS-derived schema.
- The historical executable was tested in the Windows 11 development environment, not on an independently provisioned PC. Code signing, an installer, and product-specific antivirus/SmartScreen behavior are outside the verified scope.
- Chromium runs with `--disable-gpu`. A dedicated GPU is not required, but an independent physically GPU-free machine was not tested.

## Detection and coverage

- Perfect results on 16 local expected findings do not estimate competition performance. External ground truth, tens of thousands of pages, and full 30-minute load benchmarks have not been evaluated.
- Confusable-character and keyword dictionaries are limited. Creative misspellings, text split across HTML tags, pseudo-elements, Shadow DOM, canvas, image text, encoded content, and redirect advertising can be missed.
- The crawler inspects rendered DOM and links exposed through `href`. It does not automatically log in, submit searches, click pagination or comments, press load-more buttons, or trigger infinite scrolling.
- Links are restricted to the same origin. Domain aliases and subdomains are not automatically added. Embedded frames are inspected recursively; unrelated external links inside them are not followed.
- Color comparison uses the closest opaque ancestor background or white. Images, gradients, alpha compositing, transforms, and complex clipping are not fully modeled. Ordinary below-fold content is not automatically considered off-screen concealment.
- Rule-based scoring cannot perfectly distinguish advertising from public information. Ads containing prevention terminology may be missed, while legitimate quotations may be flagged. Nearby context is length-limited.
- The DOM may change after location verification. Full page snapshots are not preserved. Absolute iframe paths require the supplied URL-aware resolver.
- Links beyond `max_pages` are not visited. Review the visited list; reaching the limit does not establish full coverage.
- Page/frame errors are recorded while other work continues. The entry origin's robots.txt is checked; if it is unreachable, an error is recorded and accessible public pages may still be scanned.
- No authentication/CAPTCHA bypass, AI classification, `ETC` output, legal adjudication, or image OCR is provided.

## Execution and distribution

Results are saved at completion, stop, or timeout, with no periodic forced-termination checkpoint. Distribute Chromium and libraries with the executable. Use a writable output directory. The GUI displays an indeterminate progress bar with actual counts because the total number of discoverable URLs is unknown.

The repository's English interface requires a new build. Historical executable validation records describe the earlier packaged build, not an English binary release.
