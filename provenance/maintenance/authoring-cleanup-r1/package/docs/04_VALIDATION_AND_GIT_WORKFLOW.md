# 04 — Validation and Git workflow

## What this ZIP did and did not test

The package preparation checks validate package contents and the supplied helper on local fixture repositories. Actual MK157 before/after tests belong to execution. Never copy PACKAGE_AUDIT results into a claim that MK157's own validators passed.

## Baseline inventory

Use an external scratch directory for helper output. Example commands are intended for Codex's terminal, not instructions requiring the user to perform command-line work. Replace PACKAGE, REPO and SCRATCH with actual absolute paths.

```
python3 PACKAGE/scripts/verify_package.py PACKAGE
python3 -m unittest discover -s PACKAGE/tests -v
python3 PACKAGE/scripts/cleanup_guard.py snapshot --repo REPO --out SCRATCH/before.json --expected-head ACTUAL_EXECUTION_BASELINE
python3 PACKAGE/scripts/cleanup_guard.py invariants --repo REPO --spec PACKAGE/evidence/CRITICAL_INVARIANTS.json --out SCRATCH/invariants-before.json
```

The helper checks the origin identity, requires clean tracked content for snapshotting, records committed and working bytes/modes, inventories equal Git blobs without deleting them, and checks preservation later. Outputs must be outside the repository. Preserve and report pre-existing untracked files, too; exclude none silently.

On a newer execution baseline, source-verify any changed selected invariant first. Store an explicitly revised invariant spec with source citations and a diff. Do not edit actual data to satisfy the old packet, remove a failed assertion without a documented governing update, or describe the observed-baseline spec as timeless.

## Discover and inspect existing validators

The source route map names candidate commands. The fresh inventory determines the complete actual set. Read each script's CLI and side effects before running it. Identify validators which are active, historical-only, import-time-only or generators.

At minimum inspect the existing Arc 3, Arc 4 handoff, historical Arc 4 Yellow, Yellow director, Arc 5, Arc 6, Arc 7, economic/reward and atomic-library checks. Run the appropriate complete baseline set; do not silently skip a historical check merely because it fails. A historical check may need to run at its historic commit rather than the current tree; label that distinction.

Confirmed current interface for Arc Seven:

```
python3 world-clock/validate_arc7.py --repository REPO
```

Its `--write` flag overwrites `world-clock/ARC7_ECONOMY_AUDIT.json`; omit that flag in this cleanup. It uses `git show` on a historical baseline. A shallow/export-only checkout may need ordinary history fetching. Do not rewrite the validator to remove those checks.

For other validators, infer nothing about flags from their filenames. Read before invoking. Prefer read-only options. Run any command with uncertain writes in a disposable worktree derived from the exact baseline/candidate with required Git history. Record the worktree SHA and command. Do not copy side-effect-generated audit files back over originals.

## Before/after comparison

For each command record: ID, category, script path, arguments, cwd, tested tree/commit, return code, stdout/stderr paths or full text, asserted-check count when actually reported, dependencies, and whether any files changed during execution.

A legitimate pass requires no new failures and no formerly passing command becoming failing. Pre-existing failures must be reported, not hidden. A missing dependency is NOT RUN/BLOCKED, not PASS. For required checks that cannot run, do not call the cleanup fully validated or merge it automatically.

For a failing historical-only check, preserve its original failure evidence and state why it is not a current integration gate. Do not relabel a failing active check as historical merely to pass.

## Preservation gate

After authoring changes:

```
python3 PACKAGE/scripts/cleanup_guard.py check --repo REPO --baseline SCRATCH/before.json --out SCRATCH/preservation.json
python3 PACKAGE/scripts/cleanup_guard.py invariants --repo REPO --spec PACKAGE/evidence/CRITICAL_INVARIANTS.json --out SCRATCH/invariants-after.json
```

The preservation report treats deletion, relocation, symlink replacement, mode changes and non-approved edits as failures. Only README.md and live-model/INDEX.md may change. Their original Git-byte backups must exist at the required maintenance paths. Newly created files must be under the approved new surfaces.

This is a byte/mode gate, not a semantic-content gate. Review every navigation edit and all new canon claims against source evidence. Do not claim that the helper alone proves “no canon changed.”

## Active-link and content gates

Validate local file links, directory links, fragments/Markdown headings, explicit anchors, reference-style links and encoded filenames in every new or edited document. Skip code fences and genuine example placeholders. Use an established project link tool if present; otherwise implement a scoped checker and disclose limitations. Validate pinned GitHub source URLs against exact discovered paths; don't invent a root path from a filename inside an archive.

Measure historical broken links separately without editing immutable sources. Every link reachable from the new active front door must resolve. An archive copy can be linked as a raw historical artifact; its own old relative links must not be presented as a new navigation surface.

Validate all new JSON against the supplied schema contracts or equivalent explicit checks. Verify topic IDs and source references are unique and resolvable, every arc has a grounded source route, and coverage rows reconcile all material within the declared reviewed scope. Check every current assertion against its owner, including exceptions and OPENs.

## Required maintenance records

Store baseline inventory, before/after command records, navigation backups, source coverage, source-status decisions, preservation report, active/historical link findings and completion report under the new maintenance directory. Avoid recursive report hashing: file manifests do not contain their own hash, and the final report does not claim to hash itself. Keep the original baseline records immutable once captured; revised reports get a new filename plus explanation.

## Commit and publish

Inspect the staged diff and run `git diff --check` before an ordinary commit. Confirm no data/source binary, registry, historical package, old validator or unrelated user file is staged. Recheck current remote ancestry before any push.

The default when no existing workflow says otherwise is a maintenance branch and normal push, with no automatic merge. Use existing configured workflow if it explicitly requires a different branch policy. Report exactly whether the work is local, committed, pushed, PR-opened or merged. Network/credential problems mean preserve the local result and give the user its actual state; do not claim publication.

Do not amend an unrelated commit, squash the repository, force-push, delete branches, rewrite history, alter remote URLs, change branch protection, or execute archived import prompts.
