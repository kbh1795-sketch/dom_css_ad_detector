# GitHub publishing guide

The repository root contains the application source. Do not upload the surrounding workspace, intermediate files, or complete distribution archives as source commits.

Clone the GitHub repository before applying a prepared source bundle. Preserve `.git/` and the existing `LICENSE`; review any files you have already edited before replacing them.

Commit source, fixtures, documentation, diagrams, and historical validation records. `.gitignore` excludes executables, Chromium, virtual environments, caches, fresh scan/test output, and environment files. Attach large binary archives separately to GitHub Releases.

Before committing, review `git status --short` and `git diff --cached --stat`. Project licensing does not replace dependency licenses and notices.

GitHub renders the root `README.md` below the file list on the repository's default branch. A direct [README section link](https://github.com/kbh1795-sketch/dom_css_ad_detector#readme) opens that section. If an older version is shown, verify the selected branch and reload the page.
