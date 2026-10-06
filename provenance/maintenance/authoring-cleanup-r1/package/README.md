# MK157 — Authoring-surface cleanup R1

**Codex entry point: `EXECUTABLE.md`.**

Unpack this package outside the repository working tree. Ask Codex to read and execute `EXECUTABLE.md` against `xApologies/MK157`. The complete implementation instruction set is inside the package; a separate long prompt is unnecessary.

This package is a maintenance handoff, not a replacement repository, new chapter draft, or new canon checkpoint. It was prepared after a fresh read of the MK157 `main` branch, its root tree, its navigation and authority documents, and the current Arc Seven validator. The observed source was Checkpoint 25, commit `3a7a62407bf0f950f7b6469e5c67e2d6a3e80e31`.

## Outcome

Provide a usable authoring front door: current canon by subject, a bounded workspace for each of Arcs 1–7, clear pointers to authoritative calendars/data, and a compact source-authority map. Keep the existing working data and historical archive intact.

The implementation must produce substantive, source-accounted current-state pages, not merely an empty folder tree or a few generic summaries. Conversely, it must not copy every historical checkpoint into the new author-facing layer or manufacture chapter content.

## Important scope adjustment after recrawl

Do **not** physically move the existing registries, calendars, validators, checkpoint addenda, provenance packages, or visual assets in this pass. The current validators contain exact paths, byte-preservation checks, and Git-history dependencies. The earlier example tree was a conceptual proposal, not permission for a mass relocation. `data/` and `tools/` are navigation/orchestration layers over those existing paths.

Only two existing tracked files are eligible for navigation-only edits in the default plan: `README.md` and `live-model/INDEX.md`. Preserve their pre-cleanup Git bytes in a new maintenance archive before editing. All other existing tracked files remain unchanged. If the execution checkout is newer or already contains authoring files, follow the drift and collision procedure rather than overwriting them.

## Contents

- `EXECUTABLE.md`: ordered implementation workflow.
- `docs/`: findings, target layout, authority rules, validation, acceptance, source routes and recovery.
- `evidence/`: observed baseline, root inventory, reviewed-source metadata and machine-checkable canon anchors.
- `templates/`: working templates for arc pages, topic pages and completion reporting.
- `scripts/cleanup_guard.py`: local Git inventory, preservation and selected-invariant checks; no commit/push/delete operations.
- `scripts/verify_package.py`: package checksum verification.
- `tests/`: isolated tests of the supplied preservation helper.
- `schemas/`: structural contracts for the authority map and coverage ledger.
- `PACKAGE_MANIFEST.json` and `PACKAGE_AUDIT.json`: package integrity and actually performed checks.

## Reading the audit honestly

The supplied helper is tested against disposable local Git fixtures. The actual MK157 repository validators have **not** been run by the package author: the container could not resolve GitHub for a local clone. Connector reads succeeded. Codex must run before-and-after validation in its checkout and report actual results. No full-file census, complete duplicate census, semantic-completeness certificate, or successful cleanup commit is asserted by this ZIP.
