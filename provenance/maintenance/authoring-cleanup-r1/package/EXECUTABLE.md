# EXECUTABLE — MK157 authoring cleanup R1

You are working in `xApologies/MK157`. Execute the following maintenance task; do not stop at a proposal. Read any applicable existing repository/ancestor `AGENTS.md` instructions and `THREAD_DEVELOPMENT_CONSTITUTION.md` first. The existing instruction hierarchy remains binding. This ZIP's documents describe the same task and must be read as a whole.

## Task and authority

Make MK157 easier to recover and write from now that its Arcs 1–7 / Valnak macro scaffold is authorially closed. Build a current, subject-oriented authoring interface above the existing source/data layers. Do not redesign the setting, recompute a new economy, create story scenes, or resolve protected OPEN details.

Observed baseline: `main`, `3a7a62407bf0f950f7b6469e5c67e2d6a3e80e31` (Checkpoint 25 correction). That SHA is a reference, not a rollback target. A newer legitimate checkout must never be reset to it. Follow §0 below on drift.

Read in order:
1. `docs/01_RECRAWL_REPORT.md`.
2. `docs/02_NORMALIZATION_SPEC.md`.
3. `docs/03_AUTHORITY_AND_CANON_GUARDS.md`.
4. `docs/04_VALIDATION_AND_GIT_WORKFLOW.md`.
5. `docs/05_ACCEPTANCE_CHECKLIST.md`.
6. `docs/06_SOURCE_ROUTE_MAP.md` and `docs/07_RECOVERY_AND_ROLLBACK.md`.
7. `evidence/BASELINE.json`, `evidence/CRITICAL_INVARIANTS.json`, the templates and schemas.

## 0. Preflight and recrawl in the execution environment

- Verify the remote is `xApologies/MK157`; do not write to Mk-147, _raeon or _bricked.
- Inspect Git status, current branch, upstream, HEAD and `origin/main`. Fetch normally when credentials/network permit. No reset, clean, force push, history rewrite, or automatic stash.
- Preserve pre-existing user work. A dirty tracked tree, divergent baseline or conflicting authoring files is not permission to discard anything. Use an isolated worktree when safe and permitted by the repository workflow; otherwise stop the unsafe part and produce a precise blocker report.
- Perform a complete local `git ls-tree -r`/tracked-file inventory at the chosen execution baseline. Distinguish active sources, historical packages, reference-only assets, generated data, validators and current authoring pages. Read the active source chain; do not treat a full filename listing as a full semantic review.
- The supplied root tree and route map are starting evidence, not a substitute for this recrawl. Capture the exact actual commit, complete file list, modes, Git blob IDs and SHA-256 values. The helper can produce this inventory.
- If HEAD is a descendant of the observed baseline, read the intervening commits and reconcile the task against newer authority. Record every changed assumption in `BASELINE_DRIFT.md`. A closure or number that changed later is not a defect to be reverted. Do not bypass a failed guard silently.
- If HEAD cannot be reconciled with the observed source, preserve the checkout and report the scope that cannot safely execute. Do not switch to Mk-147 or use chat memory as substitute canon.

## 1. Establish before-state evidence

Run package checksum verification and helper tests outside the working tree. Capture a clean baseline with `cleanup_guard.py snapshot`. Inventory and inspect the existing validators; record exact commands, runtime requirements, side effects, return codes and reports. Execute baseline validators in a disposable worktree when they write reports or their side effects are uncertain. Retain full Git history needed by their `git show` checks.

Record existing failures separately. Never rewrite an old audit to claim that it passed. Before editing either navigation file, preserve its exact Git blob content at:

```
provenance/maintenance/authoring-cleanup-r1/baseline/README.md
provenance/maintenance/authoring-cleanup-r1/baseline/live-model/INDEX.md
```

These are recovery copies, not current entry points. A new archive-side README must explain their status and original locations; do not insert a banner into the byte-exact copies.

## 2. Build the authoring interface

Implement the target in `docs/02_NORMALIZATION_SPEC.md`. Required substance:

- A short root README, canonical read order, repository map, explicit current-versus-history distinction, and links to story/canon/data/upstream/validation.
- `CANON_STATUS.md` separating macro closure, local OPENs, chapter-work status, source checkpoint, and cleanup revision.
- A compact `AGENTS.md` directing agents to the constitution, current authority map and bounded arc workflow. Do not replace or override any pre-existing agent instructions.
- Topic-organized current canon, complete enough to answer its core questions without walking 25 checkpoints. Reconcile later corrections while retaining every compatible earlier lock.
- Seven arc workspaces populated with recovered, evidenced structure: entry/exit states, major events, character and ability states, calendar references, economic references, continuity dependencies and local OPENs. **No new chapter numbering, scenes, named minor characters, fictional dialogue, durations or events.**
- A navigable reference to each existing authoritative data family, including all original mirrors and command paths. No wholesale rehoming under `data/`.
- A source ownership map and exhaustive source-section coverage ledger for the material admitted to the new current layer. A source section must be reconciled, explicitly historic/superseded, or left unresolved with a reason; it cannot just disappear into a summary.
- An inheritance document that uses MK157's existing source firewall: Mk-147 world/culture where compatible; no Mk-147 Kira/Enix identity or Binding-circle causality.

Treat `canon/` as a resolved authoring view, not a second independent legislature. Existing source documents and data own their facts. The authority map must identify those owners and the new view paths. When views disagree with their sources, that is a maintenance defect, not new canon.

## 3. Clean navigation, not the archive

Rewrite the two navigation files only after before-state copies exist. Replace checkpoint chronology as the primary read route with topic and story routes. Put the full historical checkpoint chronology in a new maintenance history index that links to all retained originals. Do not remove any original checkpoint document or provenance file.

Correct current-navigation descriptions demonstrated to be stale, including the `W36+ OPEN` index description superseded by Checkpoint 25. Preserve that phrase inside historical source documents. Do not globally replace `OPEN`, old names, prices, dates or spellings across the repository.

Leave `live-model/03_VALNEK_PATHS.md` at its existing path even though visible canon says Valnak. The path is an established address; cosmetics do not justify breaking it.

## 4. Validate and review

Run the complete discovered baseline validator set again against the candidate. Review commands before invoking them; do not execute every archived `EXECUTABLE.md`, regeneration script or historical import instruction. Avoid `--write` on current validators where read-only mode exists.

Run the preservation helper: all existing tracked bytes and modes must remain unchanged except the two approved navigation surfaces, whose backups must match baseline Git bytes. Report any added files outside the permitted new surfaces. Re-run the selected invariant checks against the reconciled execution baseline, not blindly against a stale checkpoint.

Validate all new JSON, all new/edited relative links and Markdown anchors, authority ownership, source coverage, current/historical status, arc boundaries and the numerical/categorical guards. A checksum pass does not establish semantic equivalence: perform the human/agent source-section review too.

Historical broken links may remain in byte-exact archives; inventory them separately. There must be no new broken links, and no broken links from the active authoring front door. Existing historical failures are not waived by omission.

Run `git diff --check`. Inspect the exact change set, diff, modes and new file list. Stage only approved paths, never indiscriminately `git add .` in a checkout with other material. Do not weaken tests, replace expected hashes, or rewrite historical audit records to make the cleanup appear green.

## 5. Deliver the implemented cleanup

Follow the configured repository branch/push workflow. Where no workflow specifies otherwise, create a maintenance branch from the verified current canonical baseline, make an ordinary commit, and push that branch with its upstream; do not merge automatically. If an explicit existing policy requires direct main delivery, use only a normal non-force fast-forward push after rechecking the remote. No automatic merge, force push or squash/history rewrite.

Suggested commit subject:
`maintenance: add source-accounted authoring surface for closed Valnak arcs`

Record the actual implementation in `provenance/maintenance/authoring-cleanup-r1/`: baseline inventory, source map/coverage, source-status decisions, before/after tests, preservation report, link report, drift report if any, and completion report. Preserve the relevant instruction files as maintenance provenance without embedding another copy of the whole repository or nesting the ZIP recursively.

Use `templates/CODEX_COMPLETION_REPORT.md`. Include actual source SHA, cleanup commit, branch and push/PR state; counts of additions/edits/deletions; full validation results and any pre-existing failures; remaining blockers; and the new start-here path. Distinguish implementation completed locally from pushed or merged. Do not claim execution when only a plan was produced.

Success is **a populated and validated authoring surface with no lost source material or changed story mechanics**, not a large rename diff and not an empty scaffold.
