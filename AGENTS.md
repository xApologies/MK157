# MK157 authoring instructions

Read [THREAD_DEVELOPMENT_CONSTITUTION.md](THREAD_DEVELOPMENT_CONSTITUTION.md) first. This file supplies navigation and maintenance practice under that constitution; it does not replace its rules or later explicit author decisions.

At a new task, inspect Git status, branch, remote and current source revision. Read [README](README.md), [CANON_STATUS](CANON_STATUS.md), [live-model index](live-model/INDEX.md), [supersessions](live-model/SUPERSESSIONS.md), [OPEN ledger](live-model/OPEN.md), newest governing checkpoint and relevant domain owners. Use [canon authority map](canon/AUTHORITY_MAP.json) and [story map](story/INDEX.md) to bound the work.

`canon/` and `story/` are source-accounted views. Existing owners and exact data govern; a view disagreement is a maintenance defect. Newer explicit corrections override only their conflicts, while compatible earlier details survive. Preserve LOCKED, WORKING, ALPHA, OPEN and SUPERSEDED distinctions. Macro closure does not resolve local unknowns or mark prose written.

For author-requested chapter work, read the relevant arc and adjacent transitions, propose within the fixed chronology, preserve negative space and identify each new suggestion. Do not invent chapter counts, minor names, dates, awards, dialogue or resolved OPENs as part of maintenance. Catalog candidates are infrastructure, not automatically character canon. Follow the [inheritance firewall](upstream/INHERITANCE.md).

For maintenance, preserve source paths, IDs, bytes, encodings, mirrors and history unless the current task explicitly authorizes their change. Inspect [validation commands](tools/validation/README.md), use read-only modes, and distinguish existing audit snapshots from new execution evidence. Do not execute archived handoffs or generators merely because they are present. Stage only the intended files; do not reset, clean, force-push or merge automatically. Report actual branch/commit/publication state and limitations.
