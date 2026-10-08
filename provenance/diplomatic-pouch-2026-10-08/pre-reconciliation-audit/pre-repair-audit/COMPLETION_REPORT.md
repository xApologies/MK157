# October 8 diplomatic pouch — pending author reconciliation

Status: **integrated locally; not staged, committed or pushed**. Publication remains blocked by the O1D6/O4D2 Red Raid reward collision.

Baseline and fetched origin/main: `d2e6a9eded93b0cc4061952a8e381875f06d86c9`; branch `main`, remote `origin` (`https://github.com/xApologies/MK157.git`).

All supplied files were read, including the map. The integration names Kira’s household and Kaevren, preserves the unnamed leader, adds the bow/PC and Red/Orange scene directions, develops all six Orange Raid bosses, and moves the old southern festival venue from 007 to unused 008 while assigning 007 to the bookstore. The original package, maps and historical provenance remain intact.

Reverse diff: 65 decisions, 63 PRESENT and 2 CONFLICT entries describing one unique payout issue. W2/W3 reward sums were audited; no optional Solo income was guessed. All existing numeric calendars and later arc dossiers remain byte-identical.

Problem: both Orange-season Red bosses clear and pay on O1D6, while current O4D2 also includes a 2,500 Red first-clear per girl. That cannot satisfy once-per-specific-boss-per-season eligibility. The author has been asked whether to make O4D2’s Red repeat unpaid and recalculate affected totals, or explicitly retain the discrepancy OPEN for publication without changing the existing totals. No answer has been assumed.

Validation: all 10 repository routes, authoring validation, 19 unit tests, 33 selected critical assertions and whitespace checks pass. There are zero broken active links; these checks do not resolve the narrative/economic conflict. No file was deleted or renamed. Nine content checksums match; only the checksum list’s self-entry is stale and preserved as supplied.

Evidence: [integration](INTEGRATION.json), [reverse diff](REVERSE_DIFF.csv), [conflicts](CONFLICTS.json), [reward audit](REWARD_AUDIT.json), [locations](LOCATION_AUDIT.json), [fresh validation](VALIDATION_AFTER.json), [preservation](PRESERVATION.json).

Remaining OPENs include the prior Arc-One paid-combat RECOVERY_GAP, leader name, Kaevren surname, optional Solo results/credits, exact first-domai overnight staging, Weaver material, qualified social attendance/times and all compatible earlier unknowns.

Files modified:

- `CANON_STATUS.md`
- `README.md`
- `THREAD_DEVELOPMENT_CONSTITUTION.md`
- `canon/AUTHORITY_MAP.json`
- `canon/COMBAT.md`
- `canon/ECONOMY.md`
- `canon/INDEX.md`
- `canon/OPEN.md`
- `canon/PROMOTIONS.json`
- `canon/VISUALS.md`
- `canon/WORLD_AND_CULTURE.md`
- `canon/characters/ILLI.md`
- `canon/characters/KIRA.md`
- `combat-rewards/README.md`
- `live-model/01_KIRA.md`
- `live-model/03_VALNEK_PATHS.md`
- `live-model/04_COMBAT_WORLD.md`
- `live-model/DOMAI_PARTICIPATION.md`
- `live-model/ECONOMY_PURCHASE_SCHEDULE.md`
- `live-model/ILLI_PROGRESSION.md`
- `live-model/INDEX.md`
- `live-model/OPEN.md`
- `live-model/RAEON.md`
- `live-model/STORY_CLOCK_STATE.md`
- `live-model/SUPERSESSIONS.md`
- `live-model/VALNAK_CITY_CULTURE_TRANSPORT.md`
- `live-model/WORLD_CLOCK.md`
- `story/ARC_01/ARC.md`
- `story/ARC_02/ARC.md`
- `story/INDEX.md`
- `tools/validation/README.md`
- `tools/validation/validate_authoring.py`
- `tools/validation/validate_promotions.py`
- `visual-references/CITY_LOCATION_REGISTRY.csv`
- `visual-references/INDEX.md`

Files added:

- `provenance/diplomatic-pouch-2026-10-08/BASELINE.json`
- `provenance/diplomatic-pouch-2026-10-08/CHECKLIST_AUDIT.json`
- `provenance/diplomatic-pouch-2026-10-08/CHECKSUM_REVIEW.json`
- `provenance/diplomatic-pouch-2026-10-08/COMPLETION.json`
- `provenance/diplomatic-pouch-2026-10-08/COMPLETION_REPORT.md`
- `provenance/diplomatic-pouch-2026-10-08/CONFLICTS.json`
- `provenance/diplomatic-pouch-2026-10-08/CRITICAL_INVARIANTS.json`
- `provenance/diplomatic-pouch-2026-10-08/INTEGRATION.json`
- `provenance/diplomatic-pouch-2026-10-08/LOCATION_AUDIT.json`
- `provenance/diplomatic-pouch-2026-10-08/PRESERVATION.json`
- `provenance/diplomatic-pouch-2026-10-08/REVERSE_DIFF.csv`
- `provenance/diplomatic-pouch-2026-10-08/REWARD_AUDIT.json`
- `provenance/diplomatic-pouch-2026-10-08/VALIDATION_AFTER.json`
- `provenance/diplomatic-pouch-2026-10-08/VALIDATION_BEFORE.json`
- `provenance/diplomatic-pouch-2026-10-08/package/EXECUTABLE.md`
- `provenance/diplomatic-pouch-2026-10-08/package/README.md`
- `provenance/diplomatic-pouch-2026-10-08/package/SHA256SUMS.txt`
- `provenance/diplomatic-pouch-2026-10-08/package/package/00_CONFLICTS_AND_LOCKS.md`
- `provenance/diplomatic-pouch-2026-10-08/package/package/01_CHARACTER_SOCIAL.md`
- `provenance/diplomatic-pouch-2026-10-08/package/package/02_RED_W3_W7.md`
- `provenance/diplomatic-pouch-2026-10-08/package/package/03_ORANGE_W1.md`
- `provenance/diplomatic-pouch-2026-10-08/package/package/04_ORANGE_RAID_ROSTER.md`
- `provenance/diplomatic-pouch-2026-10-08/package/package/05_AUDIT_CHECKLIST.md`
- `provenance/diplomatic-pouch-2026-10-08/package/visual-references/VALNAK_MAP_007_BOOKSTORE.jpeg`
- `tools/validation/test_city_relocation.py`
- `visual-references/VALNAK_MAP_007_BOOKSTORE.jpeg`
