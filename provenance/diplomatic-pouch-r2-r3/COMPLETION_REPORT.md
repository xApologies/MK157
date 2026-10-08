# R2/R3 cumulative pouch — integration audit

Baseline: `b7fef052b2f6f3855555be8ef0b9ae75cf0ce090` on `main`; remote `origin` (`https://github.com/xApologies/MK157.git`).

The supplied delta is integrated. All 36 decisions are PRESENT with WORKING, OPEN and conditional qualifications preserved. Seven content documents (18 sections / 43 paragraphs) and all ten exact package files are accounted for. No new numbered checkpoint, chapter, required combat event or Binding date is created.

All ten repository validator routes pass, as do authoring validation, 17 unit tests and 33 selected critical canon assertions. Active links have zero broken references; historical broken references remain separate evidence. Validation ran read-only. Whitespace checks pass; no file was deleted or renamed. All prior provenance, fixed combat/purchase/reward data and source corpus bytes survive. The weekly template changes only 49 Highlights timestamps to 27:00.

Publication: this is precommit evidence. The current executable requires a commit and push to the existing branch. Actual resulting SHA and fetched remote synchronization are reported after publication, not asserted by this precommit snapshot.

Review: [reverse diff](REVERSE_DIFF.csv), [integration manifest](INTEGRATION.json), [preservation](PRESERVATION.json), [clock audit](CLOCK_AUDIT.json), [fresh validation](VALIDATION_AFTER.json), [critical invariants](CRITICAL_INVARIANTS.json).

Remaining: the R1D2/R1D3 friendship chronology RECOVERY_GAP; qualified property lifecycle, daily prizes, Prism routing, scene timings and Raid environment; unknown names/equipment/legal/UI/bracket details; unscheduled A/B Raid mappings/additional clears and actual wallets. Conditional additional Red+Orange first-clears yield 6,250 each if later authored; no such clears are booked.

Files modified:

- `CANON_STATUS.md`
- `README.md`
- `THREAD_DEVELOPMENT_CONSTITUTION.md`
- `builder/COMMUNITY.md`
- `canon/AUTHORITY_MAP.json`
- `canon/CARDS.md`
- `canon/COMBAT.md`
- `canon/ECONOMY.md`
- `canon/INDEX.md`
- `canon/OPEN.md`
- `canon/PROMOTIONS.json`
- `canon/TRANSDUCTION.md`
- `canon/VALNAK.md`
- `canon/WORLD_AND_CULTURE.md`
- `canon/characters/ILLI.md`
- `canon/characters/KIRA.md`
- `combat-rewards/README.md`
- `live-model/03_VALNEK_PATHS.md`
- `live-model/04_COMBAT_WORLD.md`
- `live-model/ECONOMY_PURCHASE_SCHEDULE.md`
- `live-model/INDEX.md`
- `live-model/OPEN.md`
- `live-model/PRISM.md`
- `live-model/RAEON.md`
- `live-model/STORY_CLOCK_STATE.md`
- `live-model/SUPERSESSIONS.md`
- `live-model/VALNAK_CITY_CULTURE_TRANSPORT.md`
- `live-model/WORLD_CLOCK.md`
- `story/ARC_02/ARC.md`
- `story/INDEX.md`
- `tools/validation/README.md`
- `world-clock/ARC5_DIRECTOR_CALENDAR.md`
- `world-clock/WORLD_CLOCK.md`
- `world-clock/WORLD_CLOCK_TEMPLATE.csv`
- `world-clock/validate_arc3.py`
- `world-clock/validate_arc5.py`
- `world-clock/validate_arc6.py`
- `world-clock/validate_arc7.py`

Files added:

- `provenance/diplomatic-pouch-r2-r3/BASELINE.json`
- `provenance/diplomatic-pouch-r2-r3/CLOCK_AUDIT.json`
- `provenance/diplomatic-pouch-r2-r3/COMPLETION.json`
- `provenance/diplomatic-pouch-r2-r3/COMPLETION_REPORT.md`
- `provenance/diplomatic-pouch-r2-r3/CRITICAL_INVARIANTS.json`
- `provenance/diplomatic-pouch-r2-r3/INTEGRATION.json`
- `provenance/diplomatic-pouch-r2-r3/PRESERVATION.json`
- `provenance/diplomatic-pouch-r2-r3/REVERSE_DIFF.csv`
- `provenance/diplomatic-pouch-r2-r3/REVERSE_DIFF_AUDIT.json`
- `provenance/diplomatic-pouch-r2-r3/VALIDATION_AFTER.json`
- `provenance/diplomatic-pouch-r2-r3/VALIDATION_BEFORE.json`
- `provenance/diplomatic-pouch-r2-r3/package/CITY_STACK.md`
- `provenance/diplomatic-pouch-r2-r3/package/EXECUTABLE.md`
- `provenance/diplomatic-pouch-r2-r3/package/GHOST_BASE_BUILDER.md`
- `provenance/diplomatic-pouch-r2-r3/package/MANIFEST.json`
- `provenance/diplomatic-pouch-r2-r3/package/MASTER_DELTA.md`
- `provenance/diplomatic-pouch-r2-r3/package/PRISM_DELTA.md`
- `provenance/diplomatic-pouch-r2-r3/package/R2_WEEK2_DELTA.md`
- `provenance/diplomatic-pouch-r2-r3/package/R3_RAID_ROSTER.md`
- `provenance/diplomatic-pouch-r2-r3/package/RAEON_DAILY.md`
- `provenance/diplomatic-pouch-r2-r3/package/REVERSE_DIFF.csv`
- `tools/validation/test_clock_promotion.py`
- `tools/validation/validate_clock_promotion.py`
