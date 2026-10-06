# 07 — Recovery and rollback

This pass should be reversible without touching story data because it changes only two old navigation surfaces and adds new authoring/maintenance files.

## Before commit

Keep external before-state evidence and exact baseline SHAs. If validation fails, inspect the individual introduced change. Revert only the cleanup's own edits/additions that caused the failure; do not reset the entire repository or remove pre-existing user work. Keep failure reports. Do not “fix” old source packages to match an accidental move.

If an old validator depends on an affected navigation file in a way that prevents the allowed edit, report that dependency. Do not expand the edit scope to rewrite tests without a separate justified plan. Verified additive pages can still be preserved as a partial result.

## After commit

A normal `git revert <cleanup-commit>` may be an appropriate rollback only after reviewing later dependent work and the current branch status. Do not force-rewrite published history. Do not automatically revert a cleanup if later chapter work depends on its paths; first produce an explicit compatibility plan.

## Drift or concurrent writes

If remote main moves during implementation, fetch and compare. Reconcile in the configured normal workflow; never overwrite newer author decisions. If the change affects authority, calendar/economy facts or existing authoring paths, repeat the relevant source and invariant review against the new baseline. Report the exact commits and scope.

## Audit authenticity

Preserve original evidence as captured. Any correction to a maintenance report must state the reason and previous filename/hash, rather than silently rewriting the baseline. Do not fabricate successful runtime checks in an environment missing required tools or Git history.

## Future physical cleanup

Moving existing storage paths is a separate maintenance operation. It would require a complete old→new path map, immutable-byte accounting, preserved historical Git addresses, link updates, code path adaptation, manifest design and before/after validation. It is intentionally not authorized by R1.
