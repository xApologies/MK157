# Surgical Kira Armor economy correction

Baseline: `edfda188e942fc54c5c5db39e6ece5b42bca1e9a`, clean local `main` matching fetched `origin/main`. Remote: `https://github.com/xApologies/MK157.git`. This versioned report records the validated precommit tree; final commit and remote synchronization are recorded in the post-push receipt.

The [explicit author decision](package/AUTHOR_DECISION.md) changes one economic fact: initial Armor of the Abyss costs **exactly 2,000 credits**, entirely consuming the entry grant. Earlier approximate/unknown-price claims remain only in preserved historical sources. Current economic owners and ledger notes now express the exact cost and balances.

| Mechanically verified invariant | Credits |
|---|---:|
| Entry grant | 2,000 |
| Initial Armor expenditure | 2,000 |
| Post-Armor available balance | 0 |
| Unchanged pre-CSR combat gross | 63,705 |
| Pre-CSR available balance | 63,705 |
| CSR, Orange W2 D3 | 61,017 |
| **Post-CSR available balance — LOCKED** | **2,688** |

The [Kira ledger](../../world-clock/KIRA_CREDIT_LEDGER.json) retains all 63 rows and every combat earning. Minimum combat gross 58,705 plus authored surplus 5,000 remains 63,705. Its initial Armor row now debits 2,000; every later running balance decreases by exactly 2,000 from the prior known subtotal. CSR's cost/date remain unchanged. No discretionary transaction, reward or other purchase was introduced. [Full row computation and preservation guard](KIRA_CREDIT_AUDIT.json).

## Validation and scope

All ten existing economy/combat/calendar/library validators PASS. Kira ledger, cumulative reconciliation, full-repair verification (20/20 requirements), authoring validation and all **35 tests** PASS. `git diff --check` PASS. Active authoring links have no broken references. Historical link findings remain separate evidence.

Older validators explicitly preserved the previous Armor record. They now admit only the exact 2,000 Armor correction and source reference; all other Black price fields remain protected. The Arc Seven guard also verifies only the two authorized Armor sentences changed in the pricing policy. The ledger guard rejects any altered earning, coordinate, CSR cost, other expenditure or row count. The promotion validator now lets a later fully accounted correction supersede a generated ledger while retaining its original historical hash; undeclared drift still fails.

Current Arc Three and Arc Four handoff audits were refreshed for their changed validator/source hashes. Their combat totals, events and all other economic values are unchanged. Earlier audits under provenance remain exact. [Validation evidence](VALIDATION_AFTER.json); [source accounting](INTEGRATION.json).

All 794 original files remain; 764 retain identical bytes. Every calendar data file except the requested Kira ledger mirrors is byte-identical. All reward files and prior provenance are byte-identical. No deletion, rename, social/calendar adjustment or unrelated cleanup occurred. Existing OPENs outside the exact initial Armor and pre/post-CSR balances remain untouched. [Preservation report](PRESERVATION_REPORT.json).

## Exact file changes

38 files: 30 modified and 8 added. [Machine-readable list](CHANGED_FILES.json).

- `M` `CANON_STATUS.md`
- `M` `README.md`
- `M` `THREAD_DEVELOPMENT_CONSTITUTION.md`
- `M` `bindings/PRICING_MODEL.md`
- `M` `canon/AUTHORITY_MAP.json`
- `M` `canon/ECONOMY.md`
- `M` `canon/PROMOTIONS.json`
- `M` `canon/VALNAK.md`
- `M` `canon/characters/KIRA.md`
- `M` `data/INDEX.md`
- `M` `economy/KIRA_BLACK_ACQUISITION_PRICES.json`
- `M` `live-model/01_KIRA.md`
- `M` `live-model/ECONOMY_PURCHASE_SCHEDULE.md`
- `M` `live-model/INDEX.md`
- `M` `live-model/OPEN.md`
- `M` `live-model/SUPERSESSIONS.md`
- `A` `provenance/armor-economy-fix-2026-10-08/BASELINE.json`
- `A` `provenance/armor-economy-fix-2026-10-08/CHANGED_FILES.json`
- `A` `provenance/armor-economy-fix-2026-10-08/COMPLETION_REPORT.md`
- `A` `provenance/armor-economy-fix-2026-10-08/INTEGRATION.json`
- `A` `provenance/armor-economy-fix-2026-10-08/KIRA_CREDIT_AUDIT.json`
- `A` `provenance/armor-economy-fix-2026-10-08/PRESERVATION_REPORT.json`
- `A` `provenance/armor-economy-fix-2026-10-08/VALIDATION_AFTER.json`
- `A` `provenance/armor-economy-fix-2026-10-08/package/AUTHOR_DECISION.md`
- `M` `story/ARC_02/ARC.md`
- `M` `tools/validation/README.md`
- `M` `tools/validation/test_kira_ledger.py`
- `M` `tools/validation/validate_kira_ledger.py`
- `M` `tools/validation/validate_promotions.py`
- `M` `world-clock/ARC3_ECONOMY_AUDIT.json`
- `M` `world-clock/ARC3_ORANGE_CALENDAR.md`
- `M` `world-clock/ARC4_HANDOFF_AUDIT.json`
- `M` `world-clock/KIRA_CREDIT_LEDGER.csv`
- `M` `world-clock/KIRA_CREDIT_LEDGER.json`
- `M` `world-clock/validate_arc3.py`
- `M` `world-clock/validate_arc4_handoff.py`
- `M` `world-clock/validate_arc6.py`
- `M` `world-clock/validate_arc7.py`
