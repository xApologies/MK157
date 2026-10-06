# MK157 — Cleanup R1 completion report

## Actual delivery state

- Observed packet and execution baseline: `3a7a62407bf0f950f7b6469e5c67e2d6a3e80e31`.
- Baseline tree: `d2e80f13b3ea6a3e7a41754acb7897c9b479f29d`.
- Branch: `maintenance/authoring-cleanup-r1`.
- Cleanup implementation commit: `a8c5aa560790673a5e441bbf34ea982a071abb9f`. Pushed to `origin/maintenance/authoring-cleanup-r1`; a subsequent fetch confirmed identical local and remote SHAs. [Delivery evidence](DELIVERY.json) records the verified push. This report is completed in a follow-up documentation commit; Git owns the final branch HEAD. No merge or PR has been made.
- Main is unchanged at the execution baseline; local main and fetched origin/main still matched after publication. No baseline drift was found.
- Overall result: COMPLETE — implemented, validated, committed and published on the maintenance branch; not merged into main.

## Implemented surfaces

The [root README](../../../README.md) and [live-model bridge](../../../live-model/INDEX.md) route through the unchanged constitution into [canon by subject](../../../canon/INDEX.md), [all seven arc dossiers](../../../story/INDEX.md), [data and mirrors](../../../data/INDEX.md), [inheritance](../../../upstream/INHERITANCE.md), and [validation](../../../tools/validation/README.md). Eleven topic views cover characters, Valnak, Transduction/Creation, combat, economy, culture, cards, visuals and OPENs. Root agent guidance is subordinate to the constitution.

Every arc has entry/exit states, causal events, character/ability states, calendar/economic owners, dependencies and local OPENs. Chapter folders contain reading instructions only. Arc One/Two have an explicit RECOVERY_GAP for displaced opening-scene timing; their milestones and closed macro status are recovered. No dates, scenes, dialogue, named peers or chapter counts have been invented.

## File accounting and preservation

The execution inventory contains 543 original tracked files. Only README.md and live-model/INDEX.md are edited. The other 541 original files, all Git modes, data, assets, validators and provenance remain unchanged. The two original navigation blobs have byte-exact backups with a separate [archive explanation](BASELINE_ARCHIVE.md). There are no deletions, renames or mode changes and no pre-existing nonignored untracked work. Ignored inbox material is excluded from staging.

[BASELINE.json](BASELINE.json) contains the full modes/blob IDs/SHA-256 inventory; [PRESERVATION_REPORT.json](PRESERVATION_REPORT.json) lists approved edits, additions and failures. [File accounting](FILE_ACCOUNTING.json): 85 added files, two approved navigation edits, zero deletions, zero renames and zero mode changes. This includes the exact 24-file instruction package and maintenance evidence, not 85 new canon documents.

## Source reconciliation

[SOURCE_COVERAGE.json](SOURCE_COVERAGE.json) accounts for 67 selected source documents, 888 substantive sections, 10,428 fragments and 1,855 grouped status rows. Fragment statuses: 8,002 RESOLVED_CURRENT; 2,062 OPEN; 199 WORKING; 131 SUPERSEDED; 34 HISTORICAL_ONLY; zero UNRESOLVED_REVIEW. Grouping retains every fragment coordinate and digest; mixed source sections keep distinct statuses. [Status decisions](SOURCE_STATUS_DECISIONS.md) record correction scope and [authority ownership](../../../canon/AUTHORITY_MAP.json) maps views to retained owners. A current correction statement may quote an obsolete value without reviving it.

Agent semantic review covered this declared scope, including compatible earlier details and mixed passages. Exact repeated paragraphs were deduplicated for reading; their separate source locations remain represented. This is not a claim to have semantically reread all historical ZIP instructions, PDF images or every generated catalog entry. Existing validators independently cover structured records. All 543 baseline files remain navigable in the [historical index](../../../upstream/HISTORICAL_INDEX.md).

Current CP25 correction governs the White sequence, rewards and gross; CP24 governs the 19-event progression ledger; CP22/23 govern the current Yellow/Arc Five calendar. Old retained projections remain history. Later application benchmarks do not imply mastery. Mk-147 inheritance preserves accepted world/culture but excludes its Kira/Enix identity and Binding-circle causality. Fresh upstream HEADs are null; historically recorded pins and local source snapshots remain separately identified in [SOURCE_PINS.json](../../../upstream/SOURCE_PINS.json).

## Validation

All commands run from the repository root unless their evidence specifies the external package scratch folder. Exact interpreter, absolute arguments, outputs, return codes and side-effect checks are retained in the linked JSON reports; the portable command routes are in [commands.json](../../../tools/validation/commands.json). Write flags were omitted.

| Command/check | Before | After / scope | Evidence |
|---|---|---|---|
| `python -X utf8 builder/encounters/eldris/validate_library.py --directory builder/encounters/eldris` | PASS | PASS; atomic library | [before](VALIDATION_BEFORE.json), [after](VALIDATION_AFTER.json) |
| `python -X utf8 combat-rewards/validate_rewards.py --directory combat-rewards --repository .` | PASS | PASS; reward tables/policy | [after](VALIDATION_AFTER.json) |
| `python -X utf8 economy/validate_economy.py --repository .` | PASS | PASS; pricing and economic data | [after](VALIDATION_AFTER.json) |
| `python -X utf8 world-clock/validate_arc3.py --repository .` | PASS | PASS; Arc Three | [after](VALIDATION_AFTER.json) |
| `python -X utf8 world-clock/validate_arc4_handoff.py --repository .` | PASS | PASS; Arc Four handoff | [after](VALIDATION_AFTER.json) |
| `python -X utf8 world-clock/validate_arc4_yellow.py --repository .` | PASS | PASS; historical CP21 scope, not current Yellow authority | [after](VALIDATION_AFTER.json) |
| `python -X utf8 world-clock/validate_yellow_director.py --repository .` | PASS | PASS; current Yellow | [after](VALIDATION_AFTER.json) |
| `python -X utf8 world-clock/validate_arc5.py --repository .` | PASS | PASS; locked Arc Five | [after](VALIDATION_AFTER.json) |
| `python -X utf8 world-clock/validate_arc6.py --repository .` | PASS | PASS; graduation/Arc Six | [after](VALIDATION_AFTER.json) |
| `python -X utf8 world-clock/validate_arc7.py --repository .` | PASS | PASS; corrected finale | [after](VALIDATION_AFTER.json) |
| `verify_package.py PACKAGE` | PASS, 23 manifest entries | Exact 24-file package retained including manifest | [package check](PACKAGE_CHECK.json) |
| `python -X utf8 -m unittest discover -s PACKAGE/tests -v` | 17 PASS, 2 SKIP | Physical executable-bit and native-symlink fixtures skipped on Windows; no failures | [helper tests](HELPER_TESTS.json) |
| `cleanup_guard.py snapshot --repo REPO --out EXTERNAL --expected-head BASE` | Clean inventory | 543 baseline files | [baseline](BASELINE.json) |
| `cleanup_guard.py check --repo REPO --baseline BASELINE.json --out EXTERNAL` | N/A | PASS; bytes, modes, allowed paths and backups | [report](PRESERVATION_REPORT.json), [exact command](PRESERVATION_REPORT_EXECUTION.json) |
| `cleanup_guard.py invariants --repo REPO --spec CRITICAL_INVARIANTS.json --out EXTERNAL` | PASS, 33 assertions | PASS, 33 assertions | [before](INVARIANTS_BEFORE.json), [after](INVARIANTS_AFTER.json), [exact command](INVARIANTS_AFTER_EXECUTION.json) |
| `python -X utf8 -m unittest discover -s tools/validation -v` | N/A | PASS, 7 parser/schema/coverage regression fixtures | [execution](AUTHORING_TESTS.json) |
| `python -X utf8 tools/validation/validate_authoring.py --repository .` | N/A | PASS; all new JSON, supplied schema keyword subset, coverage partition/digests, owner paths, arc boundaries, local links/anchors | [authoring audit](AUTHORING_VALIDATION.json), [links](LINK_REPORT.json) |
| `git diff --check` and staged equivalent | Clean baseline | PASS; new generated files use LF, exact archives retain their original bytes | [Delivery evidence](DELIVERY.json) |

No original validator or expected hash was changed. All ten reruns were read-only, with no file or status side effects. Active authoring links and anchors have zero failures. Historical inventory contains 44 broken links in retained baseline source snapshots and 317 relative links in byte-exact navigation backups at their relocated addresses; their original-base copies were preserved deliberately. No instruction-package link failures were found. These 361 historical references are listed individually in the link report. External URLs were not network-tested. Physical executable-bit/symlink tests were unavailable; Git mode preservation was checked.

## Unchanged canon anchors

Macro closure is distinct from local OPENs and unwritten chapters. Gross income, progression reserves and actual bank balances stay separate. Trial W36+ pays 1,600 per completed wave; White W1 follows Solo96 → recovery → Duo100 → recovery → Solo100. Fixed White gross remains 63,933,340 Kira / 63,677,830 illi; illi's remaining bill remains 9,513,297. No new combat, direct wealth transfer, mastery ceiling or prerequisite grant is inferred. Selected numerical/categorical guards and full original-source preservation complement the semantic review.

## Remaining work and next entry

No protected OPEN was resolved. Exact displaced early scene placement, unprovided purchase dates, private spending/balances, detailed mastery and named minor roles still need author input when relevant. Physical source migration was deliberately outside this cleanup. Begin at [README.md](../../../README.md), then [Arc One](../../../story/ARC_01/ARC.md). New chapter drafting was not part of this task.
