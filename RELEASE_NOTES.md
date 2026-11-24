# Release Notes: 1.0.0

The repository becomes a curated, verifiable website toolkit instead of a folder of copied installers.

## Highlights

- `toolkit.json` lists Notepad++, HTTrack and FileZilla Client with official download pages, licenses, platforms, verification steps and safe-use rules.
- `tools/validate_toolkit.py` rejects missing fields, duplicate ids, non-HTTPS links, direct binary links and any committed binary.
- 14 unit tests and CI on Python 3.11 to 3.14 with pinned actions and read-only permissions.

## Breaking changes

- The bundled FileZilla, HTTrack, Notepad++ and Pixie executables and the BMP screenshots are gone. Install each tool from its publisher. Delete any installer previously downloaded from this repository.
- Pixie is no longer listed, because its publisher serves downloads only over plain HTTP.

See [CHANGELOG.md](CHANGELOG.md) and [SECURITY.md](SECURITY.md).
