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

[Promotion registry](../../canon/PROMOTIONS.json) and [promotion accounting validator](validate_promotions.py) account for later explicit author decisions without rewriting R1 evidence. Run `python tools/validation/validate_authoring.py --repository .` and `python -m unittest discover -s tools/validation -v`; both remain read-only. All ten numeric/calendar routes retain their numerical assertions; R2's two narrowly scoped preservation changes are documented below.

Each promotion preserves its exact supplied package, pins its pre-edit commit, records before/after SHA-256 for every changed baseline file, and maps every delta section/paragraph to a current owner or view with CURRENT/WORKING/OPEN qualifications. Every other baseline file must retain its bytes. Only those declared replacements let the R1 section audit read its original Git revision; unaccounted edits still fail. Changed source files join the active link audit. Paragraph partition/digests test complete accounting, not semantic equivalence; human-readable decisions and remaining conflicts are recorded in each integration manifest. Do not treat a historical PASS as new execution evidence.

Arc One R2 adds multiple source documents (including introductory tables), CSV row accounting, and a narrow city-preservation exception in the Arc Five/Seven validators. Only the city prose file and location registry can use that exception, and their complete promotion chain must pass; numeric/calendar assertions are unchanged. Original registry rows are preserved, and all six supplied rows must match the current registry exactly. [R2 integration](../../provenance/diplomatic-pouch-arc1-r2/INTEGRATION.json) records its review and qualifications.

## R2/R3 clock and bounded prose correction

The cumulative pouch authorizes Highlights 25:00 → 27:00. [Clock promotion guard](validate_clock_promotion.py) first validates the complete source/promotion chain, then permits exactly that byte substitution in all 49 weekly rows, preserving every other cell and row order. Arc Three/Six/Seven comparisons apply the verified timestamp to a copy of their historical baseline before their unchanged standing-track and character-overlay checks. No combat or purchase values are exempted.

The same guard permits only append-preserving PRISM/Builder prose and the single timestamp replacement in the Arc Five calendar explanation. Historical CP11 master/provenance remains exact evidence, explicitly superseded by the current World Clock and supersession ledger. [Negative fixtures](test_clock_promotion.py) reject wrong/partial timestamps, changed character cells, reordered rows, edited prior prose and unrelated-file exceptions. All existing validators remain read-only. The cumulative [reverse diff](../../provenance/diplomatic-pouch-r2-r3/REVERSE_DIFF.csv) accounts for all 36 decisions; its PRESENT statuses retain explicit WORKING/OPEN/conditional qualifications.

## October 8 city serial relocation

The promotion audit now accounts for the author-directed 007→008 festival relocation before comparing earlier supplied registry rows with the current registry. It requires the old row in the new promotion’s baseline, an unused 008, exact preservation of every venue field except the serial and its textual note reference, a source-accounted reason and the relocated current row. All other historical supplied rows must still match. The visual index may append the new author overlay while preserving its original prefix; earlier image bytes are untouched. Negative tests reject other serial moves, replaced venues, changed fields and applying a future source correction backward. This is source reconciliation, not permission to disregard registry drift.

## October 8 Arc One/Two repair annotations

The [repair source](../../provenance/diplomatic-pouch-2026-10-08/package/arc1-arc2-repair/package/REPAIR_DELTA.md) and [165-item reverse diff](../../provenance/diplomatic-pouch-2026-10-08/REPAIR_REVERSE_DIFF.csv) supplement the pending October 8 integration. Both original packages and the pre-repair audit remain preserved. The clock promotion guard also admits append-only annotations in exactly the Red→Orange and Arc Three calendar Markdown owners after complete source/promotion validation. It preserves every preceding byte and exempts no CSV/JSON, combat reward, balance, purchase date or later calendar. Negative fixtures reject changed original values, line-ending rewrites and unrelated paths.

The [17-item repair review](../../provenance/diplomatic-pouch-2026-10-08/REPAIR_VERIFY_AFTER.json) records resulting owner evidence, including optional Solo OPENs and the O4D2 payment conflict. A numeric or link-validation PASS does not resolve that semantic conflict or prove publication; working-tree execution and post-push remote verification are separate evidence.

## October 8 cumulative Red/Orange validation

[The reconciliation validator](validate_red_orange_reconciliation.py) checks ten current data files against explicit transformations of the fetched d2e6a9e baseline. It permits only the authored purchase-date/cell corrections, scoped Red/Orange personal-clock cells, O4D2 Orange-only payment and the dependent Arc Four funding summary. Every other field/row must match, CSV/JSON mirrors must agree, all35 Yellow–White clock rows and standing schedule fields remain exact, and fixed reward tables are unchanged. Four negative fixtures reject duplicate Red income, guessed optional credits, removed paid Duos, altered later purchases/costs, global schedule changes and reordered rows.

The existing economy/Arc Three validators recompute the corrected balances and56,385/81,415 totals. Later checkpoint validators first run the new full correction guard, then compare their historical clock views with only the already-validated Red/Orange cells restored for that old comparison. CP24’s historical early ledger is transformed only for the three date rows; all later events/costs remain exact. Historical audit JSON/source packages stay unchanged. Current calendar prose and the dependent Arc Four explanation are explicit source-accounted corrections, superseding the earlier repair’s append-only/no-arithmetic-change assumption.

Run the ten existing routes, `python tools/validation/validate_red_orange_reconciliation.py`, the authoring validator and unit discovery. New execution evidence belongs in the current [reconciliation report](../../provenance/diplomatic-pouch-2026-10-08/RECONCILIATION.json); prior audit snapshots are not proof of current state.

## October 8 full repair and Kira ledger

[Kira validation](validate_kira_ledger.py) independently reconstructs the dated Kira ledger from Trial, Dungeon and Raid CSV reward tables and her own calendar events. It excludes illi-only Solos, separates two authored Red surpluses from minimum income, records the sourced 2,000 grant and exact 2,000 Armor debit (post-Armor zero), and charges CSR 61,017 on O2D3 (63,705 before / 2,688 after, author-locked). It compares every field of both ledger mirrors and fails with row differences or an explicit affordability failure; 63,705 is a source checkpoint tested after computation.

`python tools/validation/validate_kira_ledger.py` and `python tools/validation/validate_full_repair.py` are read-only. The latter checks the 20 package requirements, current stored audits against fresh calculations, unchanged calendars and historical sources, and stale current-owner phrases. Run all ten existing validators, authoring validation and unit discovery too. The full repair explicitly authorizes regenerating the current Arc Three, early economy/calendar and dependent Arc Four handoff audits; exact prior snapshots remain in the new provenance folder. Historical numbered checkpoints and other historical audits remain preserved evidence, not new execution proof.
