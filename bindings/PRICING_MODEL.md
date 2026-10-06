# MK157 — Checkpoint 18 pricing policy

All **1,016 Bindings**, **229 summoned-entity pricing records** (including nine Primes), and **nine dedicated Prime pricing records** use fixed Red anchors by their **existing semantic pricing_class**. The dedicated Prime atlas mirrors those nine entities; it adds no new entities. Checkpoint 18 supersedes previous bands, microprices, numeric hand anchors and the old 9,900/10,000 summon limits. Class assignments, IDs, mechanisms, recipes, basin requirements, White expressions, lineage and non-price statuses are preserved.

## Fixed class matrix

| Existing class | Red | Orange | Yellow | Green | Blue | Violet | White |
|---|---:|---:|---:|---:|---:|---:|---:|
| FOUNDATIONAL | 1,700 | 2,720 | 4,896 | 10,282 | 25,705 | 77,115 | 308,460 |
| COMMON_SPECIALIZATION | 3,100 | 4,960 | 8,928 | 18,749 | 46,873 | 140,619 | 562,476 |
| ADVANCED | 5,700 | 9,120 | 16,416 | 34,474 | 86,185 | 258,555 | 1,034,220 |
| POWERFUL | 11,000 | 17,600 | 31,680 | 66,528 | 166,320 | 498,960 | 1,995,840 |
| EXCEPTIONAL | 17,000 | 27,200 | 48,960 | 102,816 | 257,040 | 771,120 | 3,084,480 |

[CSV](PRICING_CLASS_MATRIX.csv) and [JSON](PRICING_CLASS_MATRIX.json) preserve the supplied matrix. Each subsequent rank uses the rounded preceding rank, multiplying sequentially by **1.60 / 1.80 / 2.10 / 2.50 / 3 / 4** with decimal **ROUND_HALF_UP** to whole credits. Do not round only the final result or use ties-to-even rounding.

## Semantics and protected fields

Foundational means civic/basic direct operations; Common Specialization means focused specialist architecture; Advanced covers fields, expanded/multi-target/conditional architecture; Powerful covers major throughput/control architecture; Exceptional covers difficult defining architectures. These describe acquisition significance, not in-world rank, rarity color or basin identity. Historical classification reasoning remains in [Checkpoint 12 decisions](../provenance/CHECKPOINT_12_PRICING_DECISIONS.csv); do not rerun the classifier or assign different classes in this update.

Mechanism, geometry, scope, information/control complexity, sustain/concurrency, breadth, autonomy and prerequisite/capstone role informed those classes. Species, elemental name, ID sequence and basin color do not price a Binding. Identical classes now intentionally share prices; name matching cannot override an existing class.

Persistent Coherence PT-0003 and Directed Coherence PT-0002 are Foundational (Red 1,700); Coherence Field PT-0001 is Common Specialization (3,100); Genesis Beam GE-0043 is Powerful (11,000); Absorption Shield GE-0537 is Exceptional (17,000). All nine Primes PE-001–009 remain Exceptional, Red 17,000, cumulative R→W list cost **4,308,616**. No additional Prime premium.

Pricing LOCKED does not promote ALPHA mechanisms/recipes or resolve basin topology/White-expression OPENs. Historical non-price status strings may mention older cost OPENs; current pricing_status governs price only.

## Entry and White Legacy

Starter grant is **2,000 credits**. Full-price Foundational PC R→Blue costs **45,303** (43,603 remaining after Red). Accepted White-Legacy package purchases/upgrades pay **55%** of each ordinary list price, independently rounded HALF_UP. Prerequisite/access compression remains separate. Do not recursively discount discounted ranks or grant omitted prerequisite Bindings. Prequalification PC stays full price. Absorption Shield Red and each Prime Red cost illi **9,350** after acceptance. Additional package membership and discretionary discounts remain OPEN.

The [19-event ledger](../world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.csv) retains the first 13 events through G6D2 and totals **292,772** progression expenditure after Checkpoint 24’s six-event Arc Six tail. The earlier 17-event/250,884 projection is superseded. This is not total income or bank balance. The [early combat calendar](../world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.md) supplies a separate progression balance scaffold.

Kira's Black acquisition gates remain separate: Armor is the approximately 1,000-credit anomaly; Checkpoint 19 locks CSR/Genesis Orbs/Halo/Domain at 61,017 credits each in their character-specific post-Armor acquisition tier ([price record](../economy/KIRA_BLACK_ACQUISITION_PRICES.json)). The starter grant does not reprice Armor. Ordinary registry prices do not determine her Black gates.

## Mirrors and validation

Bindings retain nested rank_costs and explicit Red–White fields in JSON/JSONL; CSV mirrors existing fields and prices. Summon pricing is keyed by entity_id and Prime pricing by prime_id. pricing_status is `LOCKED — Checkpoint 18`. Entity profiles, recipes and illi prerequisite gates remain unchanged.

Run `python economy/validate_economy.py` from the repository root. It checks counts, classes/anchors, every recursive ladder, all mirrors, non-price fields against the baseline commit, the illi ledger, rewards and all 59 calendar balances/gates. [Binding audit](PRICING_AUDIT.json), [summon audit](../summons/PRICING_AUDIT.json) and [Checkpoint 18 audit](../provenance/CHECKPOINT_18_AUDIT.json) preserve the results.
