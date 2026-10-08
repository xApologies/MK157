# Known stale/missing current Git items from post-push audit

1 `world-clock/WORLD_CLOCK.md` still contains stale Checkpoint19 current-readable claims:
R5D4 eliminated; O5D1 qualification; O5D6 elimination; O7D5 championship viewing. Clean/supersede for Red/Orange.

2 `story/ARC_02/ARC.md` still contains an earlier scaffold sentence saying R5D4 raeon participation/elimination, while later text says OPEN. Remove contradiction; current = OPEN.

3 `live-model/04_COMBAT_WORLD.md` retains stale wording that O4D2 paid Red must be a distinct unpaid boss from O1D6. Current = both Reds paid O1D6; O4D2 Red repeats unpaid; Black Orchard +3,750 only.

4 `world-clock/ARC3_ECONOMY_AUDIT.json` is stale:
- event kind counts still include Tournament=2 and Recovery/Tournament=1;
- Raid income still 6,250 each;
- deterministic gross still 58,885 illi /83,915 Kira;
- tournament_dates still old R5D4/O5D1/O5D6/O7D5;
- raid_eligibility_constraint still says O4D2 needs distinct unpaid Red;
- hashes correspond to old source state.
Regenerate this audit from CURRENT calendars. Current ARC3 calendar prose reports corrected deterministic gross 56,385 illi /81,415 Kira, but validator/audit must compute it.

5 Ensure CSV/JSON/MD mirrors agree for RED_TO_ORANGE and ARC3_ORANGE.

6 Current Git lacks first-class Kira pre-CSR running ledger despite all source events/reward tables existing. Add it per KIRA_LEDGER_SPEC.

7 Do not treat historical provenance packages as current authority, but preserve them.
