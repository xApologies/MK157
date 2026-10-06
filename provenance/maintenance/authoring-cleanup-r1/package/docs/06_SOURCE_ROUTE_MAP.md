# 06 — Source routes for Codex's local crawl

All paths are relative to MK157. These routes come from the current/previously fetched index and observed validator references. The full execution inventory must confirm them; this list is neither a complete file census nor a claim that every file below was reread in full for this packet.

## Start here

`THREAD_DEVELOPMENT_CONSTITUTION.md`; `live-model/INDEX.md`; `live-model/SUPERSESSIONS.md`; `live-model/OPEN.md`; `live-model/SOURCE_BOUNDARIES.md`; `live-model/32_CHECKPOINT_25_ARC7_FINALE.md`; `world-clock/ARC7_HANDOFF.md`; `provenance/CHECKPOINT_25_CONFLICTS.md`.

Then traverse earlier active topic sources and checkpoint addenda cumulatively. Do not read only the latest checkpoint: it is a delta plus reconciliation, not the whole novel.

## Topic-to-owner starting routes

| New author topic | Existing routes to inspect |
|---|---|
| Kira | `live-model/01_KIRA.md`, `05_VISUAL_CANON.md`, `11_CHECKPOINT_06_KIRA_BIOLOGY_FIX.md`, `BLACK_SYSTEMS_MASTERY.md`, `TRAINING_YARD.md`, `32_CHECKPOINT_25_ARC7_FINALE.md` |
| illi | `live-model/ILLI_PROGRESSION.md`, `PARTNERSHIP_AND_CARRY.md`, `PRIME_ELEMENTALS.md`, `03_VALNEK_PATHS.md`; `world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json` |
| Elara | `live-model/03_VALNEK_PATHS.md`, current checkpoint addenda and Arc Seven author-understory/administration boundaries |
| Valnak | `live-model/03_VALNEK_PATHS.md`, `VALNAK_CITY_CULTURE_TRANSPORT.md`, `WORLD_CLOCK.md`, `STORY_CLOCK_STATE.md`; `world-clock/WORLD_CLOCK.md` |
| Transduction | constitution; `bindings/CANON_LOCKS.md`, `bindings/PRICING_MODEL.md`, `summons/README.md`, `live-model/PRIME_ELEMENTALS.md`, `CREATOR_CRAFTSMAN.md`, `builder/COMMUNITY.md` |
| Combat | `live-model/COMBAT_ECOLOGY.md`, `COMBAT_THRESHOLDS.md`, `TRIAL_ARENA.md`, `NORMAL_DUNGEONS.md`, `ELDRIS_REFERENCE.md`, `DOMAI_PARTICIPATION.md`; `builder/encounters/eldris/BUILDER_CONTRACT.md` |
| Economy | `live-model/ECONOMY_PURCHASE_SCHEDULE.md`; `economy/`; `bindings/PRICING_CLASS_MATRIX.json`; `trial-rewards/`; `combat-rewards/`; dated character ledgers |
| World/culture | `live-model/02_COSMOLOGY.md`, `SOCIAL_LIFE_AND_FOUNDATIONS.md`, `AITHREN_VAELUM_ACCORD.md`, `PRISM.md`, `PLANETARY_CALENDAR.md`, `SOURCE_BOUNDARIES.md` |
| Cards | `live-model/RAEON.md`, `GENESIS_CARDS.md`; `economy/ADVANCED_CARD_PRICES.json`; specific Arc Three purchase exception |
| Visuals | `live-model/05_VISUAL_CANON.md`; `visual-references/INDEX.md`, `CITY_LOCATION_REGISTRY.csv`; approved maps versus excluded concept imagery |
| Local unknowns | `live-model/OPEN.md`, latest checkpoint protected OPEN sections, arc handoffs, source-specific unresolved flags |

For shorthand filenames in the right column, retain the directory established by the first path in that group; verify the actual path before linking. The execution output must contain full relative paths, not ambiguous shorthand.

## Arc source routes

**Arcs 1–2:** recover exact boundaries/events from `live-model/STORY_CLOCK_STATE.md`, the constitution, early addenda (especially CP08 Day 1–2 runtime), `prior-checkpoint-source/LIVE_MODEL_03_SYSTEMS_STORY.md`, and later explicit arc-boundary reconciliations. Read supersessions before promoting any older story detail. Do not substitute MK147's Arcs 1–4 or the old Open Blank 66 narrative. Missing precision is a recovery gap, not permission to invent.

**Arc 3:** `live-model/26_CHECKPOINT_19_ARC_THREE.md`; CP20 boundary/card correction; `world-clock/ARC3_ORANGE_CALENDAR.md`; `ARC3_ECONOMY_AUDIT.json`; `economy/KIRA_BLACK_ACQUISITION_PRICES.json`.

**Arc 4:** CP20/21 historical development reconciled by CP22; `world-clock/ARC4_HANDOFF.md`; current `YELLOW_DIRECTOR_CALENDAR.md`. Clearly distinguish the superseded `ARC4_YELLOW_COMBAT_CALENDAR.md` from the later director calendar, and distinguish full-Yellow from Arc Four totals.

**Arc 5:** `live-model/29_CHECKPOINT_22_ARC5_SOCIAL_MASTERY.md` for compatible social/mastery doctrine; `30_CHECKPOINT_23_ARC5_COMBAT_CALENDAR.md` for full combat lock; `world-clock/ARC5_DIRECTOR_CALENDAR.md`; `ARC5_HANDOFF.json`; Training Yard and Builder community.

**Arc 6:** `live-model/31_CHECKPOINT_24_ARC6_GRADUATION.md`; `world-clock/ARC6_DIRECTOR_CALENDAR.md`; `ARC6_HANDOFF.md`; `ARC6_ILLI_CREDIT_LEDGER.json`; revised `ILLI_AUTHOR_PROGRESSION_LEDGER.json`.

**Arc 7:** `live-model/32_CHECKPOINT_25_ARC7_FINALE.md`; `world-clock/ARC7_REVISED_DIRECTOR_CALENDAR.md`; `ARC7_HANDOFF.json`; `ARC7_TRIAL_LEDGER.json`; `ARC7_DOMAI_CORE_LEDGER.json`; `ARC7_ECONOMY_AUDIT.json`; `economy/ILLI_REMAINING_WHITE_BILL.json`; `provenance/CHECKPOINT_25_CONFLICTS.md`.

## Data families to expose without moving

`bindings/BINDINGS.{json,csv,jsonl}` and pricing model/matrix; summons registry and Prime pricing; `builder/paths/PATHS.{json,csv,jsonl}`; atomic group library and availability; Trial base/extended rewards; combat reward tables; domai group/core/participation/spatial data; seasonal and arc calendars; character ledgers; visual/location registries.

Record each family's owner, mirrors, generated/candidate status and validator. Do not infer all files are generated from JSON: inspect the existing workflow to determine direction.

## Validator discovery starting points

`world-clock/validate_arc3.py`, `validate_arc4_handoff.py`, `validate_arc4_yellow.py`, `validate_yellow_director.py`, `validate_arc5.py`, `validate_arc6.py`, `validate_arc7.py`; `economy/validate_economy.py`; `combat-rewards/validate_rewards.py`; `builder/encounters/eldris/validate_library.py`.

Use the full local file inventory to discover any additional checks under bindings, summons, provenance or other paths. Their presence does not automatically make archived generators executable maintenance steps.
