# Validation routes

Run from the repository root with Python 3 standard library and Git/full local history. [commands.json](commands.json) records the discovered read-only entry points, required paths, dependencies and omitted write flags. `${REPO}` means the absolute repository root. Use UTF-8 output; Windows may need a per-command Git safe.directory entry for this authorized checkout.

The R1 cleanup edited no existing validator or expected value. Before/after evidence captures exact interpreter/arguments, outputs, exit codes and file/status side effects. Do not regenerate an old AUDIT.json as part of navigation maintenance. Historical CP21 validation checks its historical calendar against current unchanged rewards; it does not make CP21 the current Yellow schedule.

| Existing command | Scope |
|---|---|
| [builder/encounters/eldris/validate_library.py](../../builder/encounters/eldris/validate_library.py) | current invariant validator |
| [combat-rewards/validate_rewards.py](../../combat-rewards/validate_rewards.py) | current invariant validator |
| [economy/validate_economy.py](../../economy/validate_economy.py) | current invariant validator |
| [world-clock/validate_arc3.py](../../world-clock/validate_arc3.py) | current invariant validator |
| [world-clock/validate_arc4_handoff.py](../../world-clock/validate_arc4_handoff.py) | current invariant validator |
| [world-clock/validate_arc4_yellow.py](../../world-clock/validate_arc4_yellow.py) | historical CP21 calendar on current tree |
| [world-clock/validate_arc5.py](../../world-clock/validate_arc5.py) | current invariant validator |
| [world-clock/validate_arc6.py](../../world-clock/validate_arc6.py) | current invariant validator |
| [world-clock/validate_arc7.py](../../world-clock/validate_arc7.py) | current invariant validator |
| [world-clock/validate_yellow_director.py](../../world-clock/validate_yellow_director.py) | current invariant validator |

## Cleanup checks

The [preserved package guard](../../provenance/maintenance/authoring-cleanup-r1/package/scripts/cleanup_guard.py) supplies snapshot/check/invariants commands. Its output must be outside the checkout. [Package helper tests](../../provenance/maintenance/authoring-cleanup-r1/HELPER_TESTS.json) retain actual Windows skips. [Authoring-surface validator](validate_authoring.py) checks JSON schemas, section/item coverage, authority owners, seven arc workspaces, local Markdown links/anchors and active navigation. It runs read-only and prints its report to stdout; callers may capture new evidence in the maintenance directory. It does not rewrite old sources or treat archived instructions as active commands.

Evidence: [baseline](../../provenance/maintenance/authoring-cleanup-r1/BASELINE.json), [before](../../provenance/maintenance/authoring-cleanup-r1/VALIDATION_BEFORE.json), [after](../../provenance/maintenance/authoring-cleanup-r1/VALIDATION_AFTER.json), [preservation](../../provenance/maintenance/authoring-cleanup-r1/PRESERVATION_REPORT.json), [links](../../provenance/maintenance/authoring-cleanup-r1/LINK_REPORT.json), [completion](../../provenance/maintenance/authoring-cleanup-r1/COMPLETION_REPORT.md).

Historical broken links (including byte-exact backup links retaining their original base) are inventoried separately; no active front-door link failure is accepted. External pinned URLs are structurally checked against local recorded metadata, not asserted freshly reachable. Git mode preservation is checked; physical executable-bit and symlink fixture tests are unavailable on this Windows environment and disclosed as skips.

## Later author promotions

[Promotion registry](../../canon/PROMOTIONS.json) and [promotion accounting validator](validate_promotions.py) account for later explicit author decisions without rewriting R1 evidence. Run `python tools/validation/validate_authoring.py --repository .` and `python -m unittest discover -s tools/validation -v`; both remain read-only. The ten original numeric/calendar validators remain unchanged.

Each promotion preserves its exact supplied package, pins its pre-edit commit, records before/after SHA-256 for every changed baseline file, and maps every delta section/paragraph to a current owner or view with CURRENT/WORKING/OPEN qualifications. Every other baseline file must retain its bytes. Only those declared replacements let the R1 section audit read its original Git revision; unaccounted edits still fail. Changed source files join the active link audit. Paragraph partition/digests test complete accounting, not semantic equivalence; human-readable decisions and remaining conflicts are recorded in each integration manifest. Do not treat a historical PASS as new execution evidence.
