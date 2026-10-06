# 02 — Implementation specification

## Principle: one factual owner, many useful views

The new view must let an author answer “what is true now?” without reading the entire checkpoint chain, while preserving a route to the exact evidence for every lock. It does not replace the detailed source corpus with shortened summaries.

Default write scope:

- Eligible existing edits: `README.md`, `live-model/INDEX.md`, navigation only.
- Existing sources/data/scripts/assets/constitution: byte- and mode-preserved.
- New material: `canon/`, `story/`, `data/`, `tools/`, `upstream/`, root `AGENTS.md`, root `CANON_STATUS.md`, and `provenance/maintenance/authoring-cleanup-r1/`.
- No tracked deletions or renames. No regenerated existing catalogs or audit JSON.

Do not create a parallel replacement copy of `bindings/BINDINGS.json` under data, for example. `data/INDEX.md` points to its canonical location and describes the mirrors. Do not silently turn generated Binding, summon or Legacy candidates into character canon.

## Target author-facing layout

```
README.md                         # compact front door
CANON_STATUS.md                   # source baseline, closure and local OPENs
AGENTS.md                         # read order and maintenance behavior
THREAD_DEVELOPMENT_CONSTITUTION.md # existing; unchanged
canon/
  INDEX.md
  AUTHORITY_MAP.json
  characters/KIRA.md
  characters/ILLI.md
  characters/ELARA.md
  VALNAK.md
  TRANSDUCTION.md
  COMBAT.md
  ECONOMY.md
  WORLD_AND_CULTURE.md
  CARDS.md
  VISUALS.md
  OPEN.md
story/
  INDEX.md
  ARC_MAP.json
  ARC_01/ARC.md
  ARC_01/chapters/README.md
  ... same two-file shape through ARC_07 ...
data/
  INDEX.md                        # routes; does not duplicate data
upstream/
  INHERITANCE.md
  SOURCE_PINS.json
  HISTORICAL_INDEX.md             # linked historical route, no relocation
tools/
  validation/README.md
  validation/commands.json        # discovered, inspected commands
provenance/maintenance/authoring-cleanup-r1/
  baseline/...
  BASELINE.json
  SOURCE_COVERAGE.json
  SOURCE_STATUS_DECISIONS.md
  PRESERVATION_REPORT.json
  VALIDATION_BEFORE.json
  VALIDATION_AFTER.json
  LINK_REPORT.json
  COMPLETION_REPORT.md
```

This is the default target, not permission to overwrite a later existing structure. If the execution checkout already has an accepted authoring layout, extend that layout rather than duplicate it; document the mapping and adjust the helper policy explicitly with source evidence.

## Root README

Aim for one useful screenful to a short page, not another growing checkpoint diary. Include project purpose, source baseline, next creative phase, start-here sequence, current/historical distinction, the seven-arc story route, data and validation links, and the source firewall. Link the development constitution prominently. A short factual current-state summary is appropriate, but lists of every credit total and prior checkpoint belong elsewhere.

## CANON_STATUS

Keep separate fields for:
- Canon source checkpoint/commit.
- Maintenance revision (this cleanup is not automatically “Checkpoint 26”).
- Authorial macro closure of Arcs 1–7 / Valnak.
- Local protected OPEN facts.
- Actual chapter/scene/prose status discovered in Git.
- Verified execution baseline and upstream pins, with unavailable pins explicitly null.

Do not assign LOCKED to every field because an arc is authorially closed. Do not mark a chapter written because an outline exists.

## Topic pages

Each topic needs: current scope; reconciled assertions; required qualifications and exceptions; selected examples already in canon; related current sources/data; explicitly superseded alternatives; protected OPENs; and a source-accounted ownership table.

Use the template as structure, not filler text. Each core claim needs its factual owner and source heading or stable item identifier. Preserve distinctions such as basin versus domain, Kira's Black identity versus seasonal color, generic catalogs versus character builds, and fixed gross versus actual bank balances.

The author should not have to inspect 25 addenda for common questions, but one new page need not repeat every registry row. Full catalogs stay directly accessible under their original addresses.

## Authority map and coverage

`canon/AUTHORITY_MAP.json` maps topic IDs to authoritative source paths, source sections, view paths and data owners. Include source statuses and the reason a later rule governs. It must not replace a nuanced source order with one simplistic global “newest file wins” rule.

`SOURCE_COVERAGE.json` accounts for every substantive section of the selected current source chain, including compatible earlier sections that remain authoritative. Each row is one of `RESOLVED_CURRENT`, `HISTORICAL_ONLY`, `SUPERSEDED`, `WORKING`, `OPEN`, or `UNRESOLVED_REVIEW` and provides a reason and destination or governing supersession.

Do not mark an entire 20-page checkpoint covered merely because one sentence was quoted. Section-level coverage is the minimum; split mixed sections into claim/item-level rows when they contain different statuses. Every resolved row must reach a usable destination or a directly linked full-detail canonical owner. No silent loss of detail.

`UNRESOLVED_REVIEW` is not completed reconciliation. Report it as a blocker to claiming full coverage for that topic. The repository can still receive verified additive navigation for independently resolved topics, but the completion report must say exactly what remains incomplete.

## Arc workspaces

Each ARC.md consolidates already established entry/exit conditions, chronology, major event order, principal character states, capabilities/purchases, economy links, relationships/social life, negative space/recovery windows, transitions and protected OPENs.

Identify whether a fact is a locked event, an illustrative possibility, an undated opportunity or a protected unknown. For Arcs 1–2, recover sources rather than inventing names or dates by analogy with later arcs. A source gap is `RECOVERY_GAP`, not evidence that the author reopened the arc.

For each later arc, link the existing authoritative calendar and ledger rather than manually creating new “canonical” numeric mirrors. Overlapping seasonal and arc calendars must be labeled as different views of the same events; never sum them as disjoint earnings.

The chapters directory gets a real explanatory README, not invented chapter files. Explain how to create future chapter outlines without moving macro locks. Do not invent chapter counts, cliffhangers, scene timing or emotional conclusions in a cleanup.

## History navigation

The history index classifies retained checkpoint addenda, original packages, correction packages, baseline archives and validation records. Link every original represented by the old active index. Existing `provenance/` and `prior-checkpoint-source/` remain where they are.

The new live-model index becomes a compact bridge: current authoring routes, existing factual owners, and the historical index. Its description of historical documents must not imply they all remain fully current.

## Upstream model

MK157's own SOURCE_BOUNDARIES and supersessions govern inheritance. Record the repository name, role, exact source path, relevant pin when actually checked, permitted scope and explicit exclusions. Do not assert that upstream HEADs have been audited in this package. Do not pin them to historical hashes recovered only from chat as though freshly verified.

## No cosmetic mass migration

Preserve `.gitattributes`, `.gitignore`, all old script paths, all registry IDs, visual filenames, source manifests and original encodings. Do not normalize all newline styles. Retain CSV/JSON/JSONL/Markdown mirrors where required. Prefer regular Markdown links over symlinks for cross-platform portability.
