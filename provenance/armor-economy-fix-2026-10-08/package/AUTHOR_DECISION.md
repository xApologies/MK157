# MK157 — SURGICAL KIRA ARMOR ECONOMY FIX

Target repository:
xApologies/MK157

Make ONE canonical economic correction:

Kira's initial purchase of Armor of the Abyss costs exactly 2,000 credits.

This supersedes all prior language describing the initial Armor price as:
- approximately 1,000 credits;
- unquantified;
- OPEN;
- an unknown debit.

## REQUIRED UPDATES

1. Set the canonical Armor of the Abyss acquisition price to:

   2,000 credits

2. Kira's existing 2,000-credit entry grant is spent entirely on Armor of the Abyss.

   Entry grant:          +2,000
   Armor of the Abyss:   -2,000
   Post-Armor balance:        0

3. Update Kira's credit ledger and all CURRENT economic owners accordingly.

   The Armor transaction must become an exact 2,000-credit progression expenditure rather than an unquantified debit.

4. Preserve all subsequent dated combat income exactly as currently authored.

5. Preserve the mechanically reconstructed pre-CSR combat gross:

   63,705 credits

6. Immediately before CSR on O2D3, Kira's available balance should therefore be:

   63,705 credits

   because the original 2,000 grant has already been completely consumed by Armor.

7. CSR remains:

   Orange W2 D3
   Continuous Spatial Resolution
   Cost: 61,017 credits

8. Therefore the exact post-CSR balance becomes:

   63,705 - 61,017 = 2,688 credits

   LOCK:

   Kira post-CSR balance O2D3 = 2,688 credits

9. Update at minimum:
   - economy/KIRA_BLACK_ACQUISITION_PRICES.json
   - world-clock/KIRA_CREDIT_LEDGER.csv
   - world-clock/KIRA_CREDIT_LEDGER.json
   - any CURRENT Kira/economy/live-model owner that still calls Armor approximately 1,000, unquantified, or OPEN
   - any validator/audit whose expected Kira balance changes because the Armor debit is now exact

10. Do NOT change:
   - CSR price
   - CSR date
   - any Trial
   - any Dungeon
   - any Raid
   - any domai
   - any reward
   - any other purchase
   - any social-calendar event
   - any raeon tournament scheduling
   - any later-season calendar
   - Kira's 63,705 pre-CSR COMBAT GROSS

11. Preserve historical provenance files as historical evidence. Do not rewrite old packages merely to erase previous values. Current authoritative owners must supersede them.

## VALIDATE

After making the changes, mechanically verify:

Entry grant = 2,000
Armor cost = 2,000
Post-Armor balance = 0

Pre-CSR combat gross = 63,705
Pre-CSR available balance = 63,705

CSR cost = 61,017
Post-CSR balance = 2,688

All existing Red/Orange calendar events and rewards must remain unchanged.

Run all relevant economy/calendar validators.

Then:
- commit the change;
- PUSH to GitHub;
- fetch/read remote HEAD after the push;
- verify the remote repository contains the corrected values.

Report:
- commit SHA;
- exact files changed;
- validator results;
- confirmation that remote HEAD has:
  Armor = 2,000
  post-Armor = 0
  pre-CSR = 63,705
  CSR = 61,017
  post-CSR = 2,688

Do not perform any unrelated cleanup or refactoring.
