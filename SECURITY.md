# Security

## Scope

This repository contains a JSON manifest, a validator and tests. It stores no credentials, personal data or executables, and it runs no service.

## Audit, 2026-11-24

| Check | Result |
|---|---|
| Bundled third-party executables | Removed. Versions up to 2016 shipped four Windows installers, outdated and without a verifiable signature chain. The validator now fails CI if a binary is committed. |
| Secret scan (gitleaks, full history) | No findings |
| Links | All HTTPS, all pointing to publisher pages |
| CI | `permissions: {}` at workflow level, read-only per job, actions pinned by commit SHA, checkout without persisted credentials |

Anyone who downloaded an installer from an earlier version of this repository should delete it and install the current release from the publisher.

## Reporting

Open a GitHub issue for problems with the manifest. For anything sensitive, use GitHub's private vulnerability reporting on this repository.
