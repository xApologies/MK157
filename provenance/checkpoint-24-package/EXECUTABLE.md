# EXECUTABLE.md — MK157 CHECKPOINT 24 ARC SIX MASTER UPDATE

Repository: `xApologies/MK157`
Observed remote baseline during package build:
`ec3274b8f5026cd2cd6aa2bfb076383e3a863311` — Checkpoint 23: lock Arc Five combat calendar and progression

This is the final large checkpoint from the current thread.

## Mandatory procedure

1. Pull/re-crawl newest `origin/main` before editing.
2. If newer non-conflicting work exists, reconcile it; do not roll back.
3. Read every file in this ZIP.
4. Treat `CHECKPOINT24_LIVE_MODEL_DELTA.md` as author authority on explicit conflicts.
5. Integrate `ARC6_DIRECTOR_CALENDAR.csv/json` as the **fully locked Arc Six** schedule G6D3→B6D3.
6. Replace/update the active illi progression ledger using `ILLI_PROGRESSION_LEDGER_REPLACEMENT.csv/json`.
   - It now contains **19 events**.
   - full cumulative progression spend through B6D3 = **292,772**.
7. Explicitly supersede old projected dates:
   - G6D4 Absorption O
   - G7D2 Absorption Y
   - V1D3 Absorption G
   - V2D2 Resonance Prime R
8. New progression sequence must be:
   - G6D4 Genesis Prime O
   - G7D2 Genesis Prime Y
   - B1D3 Absorption O
   - B2D4 Absorption Y
   - B5D6 Absorption G
   - B6D3 Resonance Prime R
9. Lock illi sandbox graduation:
   - B1D1 W13 Green Solo clear / W14 fail.
10. Lock Kira Halo:
   - B1D5, 61,017.
   - Domain remains Late Violet exact day OPEN.
11. Lock specific domai awards:
   - G6D3 Orange = 30,000 each (60,000 collective Kira+illi unit).
   - B5D4 Yellow = 15,000 each (30,000 collective).
   - Do NOT convert these to general rank reward tables.
12. Integrate veteran-rookie ecology:
   - eligibility != credibility;
   - PUG rejection is normal;
   - no item-level system;
   - Green primary, Blue push, Violet not attempted;
   - Normal R/O/Y clear, Green wall;
   - Hard R/O clear, eventual Hard Y clear, no Hard Green.
13. Integrate Duo progression and runtime:
   - G6D7 W18 clear/W19 fail;
   - B2D1–2 W19 clear/W20 fail;
   - B6D1–2 W20 clear/W21 fail;
   - deep Blue runs are multi-day.
14. Preserve Arc Five FULL LOCK byte/semantic authority except where Arc Six begins after G6D2.
15. Update active current files, including where relevant:
   - root README
   - live-model/INDEX.md
   - live-model/ILLI_PROGRESSION.md
   - live-model/PRIME_ELEMENTALS.md
   - live-model/PARTNERSHIP_AND_CARRY.md
   - live-model/COMBAT_ECOLOGY.md
   - live-model/01_KIRA.md
   - live-model/DOMAI_PARTICIPATION.md
   - live-model/OPEN.md
   - live-model/SUPERSESSIONS.md
   - world-clock/WORLD_CLOCK.md
   - world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.csv/json
   - story/arc handoff/state files
16. Add current Arc Six calendar/handoff files under `world-clock/` and/or `live-model/` using repository conventions.
17. Mechanical audit must reproduce:
   - Kira Arc Six gross **148,600**
   - illi Arc Six gross **157,065**
   - illi Arc Six progression spend **149,675**
   - illi ending earmarked reserve **7,390**
   - cumulative illi progression spend **292,772**
   - Orange domai 30,000 each
   - Yellow domai 15,000 each
18. Raid audit:
   - B2D3 Normal R/O/Y first seasonal major rewards = 11,250 each.
   - B3D2 Hard R/O first seasonal major rewards = 9,375 each.
   - B4 Hard R/O repeats pay zero.
   - B5D3 Hard Yellow first major reward = 7,500 each.
   - never double-pay repeated bosses.
19. Dungeon runtime audit:
   - Yellow 5–10h
   - Green 12–21h
   - Blue 25–42h
   - Blue attempts retain two-day blocks.
20. Preserve Builder nights/social economy and Project Princess Carry.
21. Do NOT invent Kira two-Orb maturity, Violet Dungeon clears, Green Raid clears, Trio, or exact future Domain day.
22. Create Checkpoint 24 addendum, before-review snapshot, reverse diff, coverage manifest, conflicts, boundary/open search and integration audit.
23. Run existing economy/reward/calendar validators plus `git diff --check`.
24. Commit and push normally to `origin/main`; never force-push.
25. Verify local HEAD == origin/main and report remote SHA, changed files, ledger totals and all supersessions.

Suggested commit:
`Checkpoint 24: lock Arc Six graduation, veteran progression and revised illi ledger`
