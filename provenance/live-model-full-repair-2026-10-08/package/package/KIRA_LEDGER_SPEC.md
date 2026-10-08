# KIRA CREDIT LEDGER — REQUIRED RECONSTRUCTION

Create a first-class machine-readable ledger, preferably:
`world-clock/KIRA_CREDIT_LEDGER.csv`
and JSON mirror, plus validator.

Scope first required proof: R1D1 through O2D3.

Columns at minimum:
season,week,day,event,source_kind,kira_credits_earned,kira_progression_spend,kira_actual_surplus_earned,kira_minimum_running_gross,kira_actual_running_gross,notes/source.

Rules:
- derive Trial rewards from trial-rewards/TRIAL_WAVE_CREDITS.csv;
- derive Dungeon rewards from combat-rewards/DUNGEON_REWARDS.csv;
- derive Raid rewards from combat-rewards/RAID_BOSS_REWARDS.csv;
- shared paid event gives Kira same per-participant completion reward unless source explicitly differs;
- Kira-only Solo rewards belong to Kira;
- illi-only Solo rewards do NOT belong to Kira;
- failed encounters pay only when an authoritative partial-progress rule supplies an exact reward; otherwise zero/OPEN as current source requires;
- R4D5 Burrower +2,500 = authored actual/discretionary surplus;
- O1D6 second Red (Triumvirate) +2,500 = authored actual/discretionary surplus;
- do not fabricate domai payout.
- CSR spend 61,017 occurs O2D3.
- If Armor/starter purchase is a locked pre-CSR spend in an authoritative source, represent it explicitly; if not numerically locked, do not invent it.

CRITICAL: validator must recompute Kira row-by-row from source tables. Never derive Kira from illi totals.

Expected authored combat-gross checkpoint before CSR from current live model is 63,705 credits. Validator must independently reproduce or flag mismatch, with a per-row diff. Do not hard-code 63,705 as a substitute for computation.

CSR affordability invariant:
actual/progression-eligible Kira funds immediately before O2D3 CSR must be >=61,017 using only sourced transactions. If a locked pre-CSR spend makes that false, FAIL and report exact row causing it; do not alter calendar automatically.
