# Changelog

## [1.0.0] - 2026-11-24

### Changed

- **Breaking:** the repository no longer ships installers or screenshots. Each tool is listed in `toolkit.json` with its official download page, license, platforms, verification steps and safe-use rules.
- README rewritten in English with the toolkit, workflow, safe-use rules and usage.

### Added

- `tools/validate_toolkit.py`, a standard-library validator that rejects missing fields, duplicate ids, non-HTTPS links, direct binary links and committed binaries.
- 14 unit tests and a CI workflow on Python 3.11 to 3.14 with read-only permissions and pinned actions.
- `SECURITY.md`.

### Removed

- FileZilla 3.21.0, HTTrack 3.48.22, Notepad++ 7 and Pixie executables, plus two BMP screenshots.
- Pixie from the toolkit: its publisher serves downloads only over plain HTTP. Browser developer tools cover colour picking.
