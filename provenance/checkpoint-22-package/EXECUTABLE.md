# EXECUTABLE.md — MK157 CHECKPOINT 22

Repository: `xApologies/MK157`
Observed source HEAD during package construction: `47c412e2e25acaf0bbaf5341e270e52b49d00009` (Checkpoint 21).

This is a cumulative live-model checkpoint. **Pull/re-crawl origin/main first.**
The user may finish pushing the narrow CP21A Orb-date patch before this runs.
If CP21A or any newer non-conflicting commit exists, reconcile; do not roll it back.

## Required integration

1. Read every file in this ZIP.
2. Snapshot/review the current repository before edits.
3. Integrate `CHECKPOINT22_LIVE_MODEL_DELTA.md` as the governing author delta.
4. Replace/reconcile the Yellow director calendar from `YELLOW_DIRECTOR_CALENDAR.csv/json`.
   - Y5D5 is Builder party, NOT W18.
   - exact Orbs = Y6D2.
   - Arc Four closes Y6D3.
   - Arc Five opens Y6D4.
   - add Y6D5/Y6D6 W18 Duo.
   - add Y7D1–D3 raeon personal block.
   - add successful Y7D4 domai with payout OPEN.
   - preserve Auction W7D5–D7.
5. Update active current files, not just an addendum:
   - `live-model/01_KIRA.md`
   - `live-model/04_COMBAT_WORLD.md`
   - `live-model/COMBAT_ECOLOGY.md`
   - `live-model/PARTNERSHIP_AND_CARRY.md`
   - `live-model/ILLI_PROGRESSION.md`
   - `live-model/DOMAI_PARTICIPATION.md`
   - `live-model/SOCIAL_LIFE_AND_FOUNDATIONS.md`
   - relevant economy/purchase schedule only where needed
   - `world-clock/WORLD_CLOCK.md`
   - `world-clock/ARC4_YELLOW_COMBAT_CALENDAR.*` or a superseding current Yellow calendar
   - Arc Four handoff / story clock state
   - `live-model/INDEX.md`, `OPEN.md`, `SUPERSESSIONS.md`
   - root `README.md`
6. Add/promote active reference docs for:
   - Training Yard
   - Builder community
   - Arc Five handoff/roadmap
   - Black systems/mastery doctrine
   - domai group-split economy
   Use sensible repository-native paths and link them from INDEX/README.
7. Builder:
   - preserve 200 `builder/paths` trajectories;
   - do NOT regenerate or reclassify them;
   - add the community/UI doctrine over the existing registry.
8. Black systems:
   - preserve all existing late capabilities;
   - explicitly clarify no ordinary rank ladder / no defined mastery ceiling;
   - acquisition opens system, mastery grows;
   - do not invent finite max capability or new paid Black ranks.
9. Trial:
   - add inter-wave voluntary termination and Training Yard selectable-wave/no-credit mode;
   - do not alter reward CSV;
   - exact standing effect of Training Yard beyond selectable prior-completed waves stays OPEN.
10. Arc Five:
   - Y6D4→G6D2.
   - G6D2 Coherence Prime Red 9,350 unchanged.
   - Kira one-Orb mini-blender develops; W19 Blue Solo clear/W20 reached at an OPEN date.
   - Duo stays W18 clear/W19 fail.
   - no Trio push.
   - Green Dungeon attempts become credible; first clear date OPEN.
11. illi:
   - keep PC Blue, Absorption Red, Beam Green, Genesis Prime Red at Arc Five opening;
   - do NOT invent Genesis Prime rank dates;
   - Coherence Prime motivation is distributed-damage/healer fatigue.
12. domai:
   - group contribution award → equal base split among eligible group members;
   - preserve per-participant 7-day eligibility, one-day lockout, death ×0.8^deaths;
   - optional individual bonus layer remains OPEN;
   - Y7D4 payout remains OPEN.
13. Social:
   - lock first Builder invitation Y5D3 and first Builder party Y5D5;
   - preserve broader Arc Five social-launch direction;
   - preserve the later Project Princess Carry fanaticism already in Git.
14. Preserve registry counts:
   - 1,016 Bindings
   - 229 summons
   - 200 Builder paths
15. Mechanical audit must verify:
   - Yellow director calendar = 49 rows;
   - shared W18 Duo = 6;
   - Kira W18 Solo = 1;
   - Orange clears = 17;
   - Yellow attempts = 4;
   - fixed full-Yellow income excluding domai = illi 71,280 / Kira 80,140;
   - revised Arc Four gross through Y6D3 = illi 58,170 / Kira 67,030;
   - Y5D5 has no Trial credit;
   - Y6D2 exact Orbs;
   - Y6D3 Arc Four close;
   - Y6D4 Arc Five open;
   - G6D2 Coherence Prime unchanged;
   - no invented exact Blue-Solo date / Green-clear date / domai payout.
16. Create Checkpoint 22:
   - live-model addendum;
   - before-review snapshot;
   - reverse diff;
   - coverage manifest;
   - conflict log;
   - integration audit;
   - boundary/open search.
17. `git diff --check`, run relevant existing validators, then commit and push normally to `origin/main`.
18. Verify local HEAD == origin/main.
19. Final report: SHA, changed files, calendar counts/income, key supersessions, preserved OPENs.

Suggested commit:
`Checkpoint 22: integrate Arc Five mastery, Training Yard, Builder community and Yellow social calendar`
