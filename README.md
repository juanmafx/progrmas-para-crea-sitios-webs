# website-toolkit

A curated, verifiable toolkit for building and maintaining small websites on a Windows or Linux workstation: edit, mirror and deploy.

The repository holds a machine-readable manifest of three tools, a validator and its tests. It does not redistribute any installer. Every entry points to the publisher's official page and says how to verify the download before running it.

## Why it exists

The 2016 version of this repository shipped vendor installers and screenshots directly. Redistributing third-party binaries is a supply-chain and licensing risk: nobody can tell whether a copied `.exe` still matches what the publisher signed, and old builds never receive security fixes. Version 1.0.0 replaces the binaries with links to the official source and verification steps, and the validator fails the build if a binary is ever committed again.

## The toolkit

| Tool | Stage | What it is for | License | Platforms |
|---|---|---|---|---|
| [Notepad++](https://notepad-plus-plus.org/) | Edit | Edit HTML, CSS, JavaScript and server-side files | GPL-3.0-or-later | Windows |
| [HTTrack](https://www.httrack.com/) | Mirror | Make an offline copy of a site you own or may copy | GPL-3.0-or-later | Windows, Linux |
| [FileZilla Client](https://filezilla-project.org/) | Deploy | Upload and synchronise files over SFTP or FTPS | GPL-2.0-or-later | Windows, macOS, Linux |

Full details, including verification and safe-use rules for each tool, are in [`toolkit.json`](toolkit.json).

## Workflow

```
edit (Notepad++) -> preview locally -> deploy (FileZilla, SFTP) -> mirror for backup or audit (HTTrack)
```

For colour picking, use the colour picker built into Firefox or Chrome developer tools. Pixie, listed in the 2016 version, was dropped because its publisher serves downloads only over plain HTTP, so a download cannot be checked against a trusted source.

## Safe-use rules

1. Download only from the publisher page listed in the manifest, then verify the hash or signature it publishes.
2. Deploy over SFTP or explicit FTPS. Plain FTP sends credentials in clear text.
3. Do not let an FTP client store passwords without a master password.
4. Mirror only sites you own or have written permission to copy, respect `robots.txt` and rate-limit the crawl.
5. Prefer the operating system's package manager on Linux (`apt install filezilla httrack`).

## Usage

Requirements: Python 3.11 or newer. No third-party packages.

```bash
python3 tools/validate_toolkit.py          # validate toolkit.json and check for bundled binaries
python3 -m unittest discover -s tests -v   # run the test suite
```

The validator checks that each entry has every required field, that ids are unique, that categories and platforms come from a fixed list, that every link is absolute HTTPS and points to a page rather than a binary, and that no installer, archive or image dump is committed.

## Architecture

```
toolkit.json                 manifest (data, schema_version 1)
tools/validate_toolkit.py    validator, standard library only
tests/                       unittest suite, 14 tests
.github/workflows/ci.yml     runs the validator and tests on Python 3.11 to 3.14
```

There is no database, service or user input, so there is no SQL schema and no attack surface beyond the CI job, which runs with read-only permissions and pinned actions.

## Adding a tool

Add an object to `tools` in `toolkit.json` with every required field, link to the publisher page, describe how to verify the download, then run the validator and the tests.

## Project history

Created in 2016 as a Spanish-language collection of website tools with bundled installers. Rebuilt in 2026 as an English, binary-free, validated toolkit. See [CHANGELOG.md](CHANGELOG.md).
