# EXECUTABLE — MK157 CHECKPOINT 09 FULL CONTINUATION

Codex: integrate this package into `xApologies/MK157`.

Baseline used to build this package:
`1f7585eae09df24fb9d7c17d74955c8dbbdeaa3c` — "Checkpoint 08: integrate live-model delta, Prime Elementals, and Legacy rules"

If repository HEAD has advanced, crawl the new HEAD first and reconcile rather than blindly overwriting newer work.

## Mission

Checkpoint 09 exists specifically because prior ZIP -> Codex -> Git updates lost too much of the live model.

DO NOT reduce this package to a short summary.

The integration succeeds only when every requirement in `COVERAGE_MANIFEST.csv` is either:
1. mapped to an actual Git destination, or
2. explicitly reported unresolved/conflicting.

## Required read order

1. `README.md`
2. `16_CHECKPOINT_09_WORLD_CLOCK_CONTINUATION.md`
3. `01_CREATOR_CRAFTSMAN_CONTINUITY.md`
4. `02_VALNAK_CITY_CULTURE_TRANSPORT.md`
5. `03_RAEON_FLAGSHIP_AND_TOURNAMENT.md`
6. `04_COMBAT_ECOLOGY.md`
7. `05_WORLD_CLOCK.md`
8. `06_PRISM_TRACKING_MODEL.md`
9. `07_STORY_CLOCK_STATE.md`
10. `08_SOURCE_BOUNDARIES.md`
11. `GIT_GAP_AUDIT.md`
12. `COVERAGE_MANIFEST.csv`
13. supporting CSVs and visual references
14. upstream snapshots for provenance

## Authority

After successful integration:
**09 > 08 > 07B/07 > 06 > 05 > 04 > 03 > 02 > 01** on explicit conflicts.
Non-conflicting detail accumulates.

## Required repository integration

### A. Governance / constitution
Update:
- `README.md`
- `THREAD_DEVELOPMENT_CONSTITUTION.md`
- `live-model/00_GOVERNANCE.md`
- `live-model/INDEX.md`
- `live-model/SUPERSESSIONS.md`
- `live-model/OPEN.md`

Required active lexical corrections:
- canonical active monster word is lowercase `eldris`;
- `domai`, `raeon`, `vaen`, `maege`, `maegi` follow Checkpoint 09;
- spelling-by-letter all-caps is not canonical capitalization.

Historical provenance may retain source casing.

Add explicit external-reference authority for `_bricked`, `_raeon`, `Mk-147` with MK157 conflict precedence.

### B. Checkpoint
Add exact package master:
`live-model/16_CHECKPOINT_09_WORLD_CLOCK_CONTINUATION.md`

### C. Discoverable domain files
Create or update discoverable live-model domain files so a new thread does NOT need to read one 37k-character checkpoint to recover basics.

At minimum provide dedicated current files for:
- Creator/Craftsman;
- Valnak city/culture/transport;
- `raeon`;
- World Clock;
- Prism;
- Dungeon/Raid/`domai` combat ecology.

Exact filenames may follow repository style, but INDEX must expose them.

Do not discard exhaustive detail from the package when creating these files.

### D. Existing character / Valnak / combat summaries
Merge relevant current canon into:
- `live-model/01_KIRA.md` — Kira Creator/mail identity; Eternal Champion;
- `live-model/03_VALNEK_PATHS.md` — city, transport, culture, cohort/ecology where appropriate;
- `live-model/04_COMBAT_WORLD.md` — Guardian, Dungeons, Hard Dungeons, raids, `domai`, lowercase `eldris`.

Preserve Checkpoint 08 Black/White progression rules.

### E. World Clock files
Add a `world-clock/` directory (or equivalently discoverable current location) containing:
- `WORLD_CLOCK.md`
- `WORLD_CLOCK_TEMPLATE.csv`
- `PRISM_TEAM_TRACKER.csv`

Copy 37 team placeholders exactly; do NOT invent team names/rosters yet.

Prism:
- standings = wins/losses;
- 37 tracked teams;
- ~20 moving competitive bubble;
- Top 16 postseason;
- 16 -> 8 -> 4 -> 2 -> Champion;
- exact schedule/tiebreaks/team size OPEN.

### F. Location registry / visual assets
Preserve current base Valnak map already in Git.

Add:
- `visual-references/VALNAK_CITY_MAP_001_RAEON_FLAGSHIP.png`
- `visual-references/VALNAK_DUNGEON_DOMAI_BASE_MAP.jpeg`
- a location registry derived from `CITY_LOCATION_REGISTRY.csv`

Marker 001 is the `raeon` flagship.
001-A rooftop restaurant and 001-B Champion Tables may be registry child records without additional map markers.

Update `visual-references/INDEX.md`.

The clean Dungeon/Domai domain map is a BASE geography.
DO NOT import the node-filled concept image that is not in this package.

### G. `raeon`
Record direct inheritance:
- MK-147 physical maege-glass implementation;
- `_raeon` current detailed mechanics;
- external authorized publisher;
- Valnak Cycle-exclusive set every ~23 years;
- Node collection/deck module;
- flagship;
- Weeks 5–7 tournament / Week 7 final.

Do not freeze unnecessary `_raeon` implementation details into MK157 if they can remain upstream authority.

### H. Creator/Craftsman
Integrate `01_CREATOR_CRAFTSMAN_CONTINUITY.md` at full substantive resolution.

Do NOT reduce to "Craftsman's Row exists."

Must remain recoverable:
- primary Creation route;
- Trial progression;
- 64 smithies;
- persistent shops;
- commissions;
- spectator culture;
- conductor-of-matter smithing;
- Kira mail identity;
- originals/reproduction/Auction distinction;
- rune-carver civic sigils;
- discovery loop.

### I. Combat ecology
Integrate:
- no taunt/aggro/threat;
- Guardian;
- helkir value;
- flexible five-person composition;
- completion-weighted Dungeon economy;
- Red->Violet Dungeon rank law;
- cumulative `eldris` palette;
- Normal ~5 sq mi / Hard ~7.5–8 sq mi working scale;
- procedural realization;
- nine domains;
- adaptive Node allocation;
- 10-person raid cap;
- 6 standalone + 6 Expedition bosses;
- mature and first-cycle standalone rosters;
- per-boss once-per-season major rewards;
- outside vs Valnak `domai` distinction.

### J. Upstream inheritance
Use package snapshots for traceability and, where useful, verify against live upstream GitHub repositories:
- `xApologies/Mk-147`
- `xApologies/_raeon`
- `xApologies/_bricked`

Do not import unrelated source material.

### K. Source quarantine
`MASTER_schedule.pdf` and `Calendar - Kira.pdf` are methodology examples only.
`Open Blank 66(1).pdf` is historical reference only; current carriage rules govern.

Do not import old plot/cosmology from those files.

## Reverse coverage audit — REQUIRED

After integration, update/copy `COVERAGE_MANIFEST.csv` into provenance and fill:
- `integration_status`
- `actual_git_destination`
- `notes`

No row may remain PENDING on a successful run.

If a row cannot be integrated, status it CONFLICT or OPEN and explain.

Then create:
`provenance/CHECKPOINT_09_AUDIT.json`

Audit must include:
- baseline and final commit/hash if available;
- current authority chain;
- changed files;
- all coverage rows accounted for;
- visual assets present and hashed;
- 37 Prism team tracker rows preserved;
- 49 World Clock week rows preserved;
- lowercase `eldris` active-canon normalization check;
- preexisting Binding/summon/Legacy registries unchanged unless required by an explicit Checkpoint 09 rule (no new Binding registry work is requested here);
- source-quarantine check;
- conflict list;
- OPEN list.

## Critical non-inventions

Do NOT invent:
- Prism team names or rosters;
- Prism team size/positions;
- Prism scoring formula;
- exact Prism playoff-week schedule;
- `raeon` publisher name/legal structure;
- exact `raeon` bracket size;
- Dungeon credit table;
- raid credit values;
- `domai` scaling formula;
- special events calendar;
- carriage propulsion;
- future map serials after 001;
- new Bindings or summons;
- a White `eldris`;
- White-ranked Dungeons.

## Completion criterion

A brand-new MK157 thread must be able to crawl Git and recover all Checkpoint 09 systems without asking the user to reconstruct this conversation.
