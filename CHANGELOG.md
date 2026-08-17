# Changelog

## [0.1.1] - 2026-08-18

### Fixed

- Fixed stale `open` status causing repeated double-boot warnings.
  When confirming a double boot, stale `open` statuses in recent Wenvi
  JSON files are now changed to `close`.
- Fixed editing failing when the target editable element is outside
  the visible viewport.
  Explicitly requested editable elements can now be found even when
  they are offscreen. Wenvi also scrolls the target element into view
  when necessary.

## [0.1.0] - 2026-03-03

Initial release.

### Features

- Edit browser-editable elements (textareas, inputs, and contenteditable
  regions) using Neovim.
- Automatically sync edited content back to the browser.
- Save edit buffers in `dataHome` for search and diff.
- Organize saved files by domain and page title.
