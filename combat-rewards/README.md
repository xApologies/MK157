# Combat reward economy — Checkpoint 18

> Checkpoint 24 current progression: 19 events, 292,772 total through B6D3. Earlier checkpoint sections below retain development history; any 17-event/250,884 or Violet-endpoint projection is superseded by the [current illi ledger](../world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json). Arc Five dates/outcomes through G6D2 remain locked.

These are the locked Valnak Dungeon completion and Raid major-boss payouts. [Dungeon CSV](DUNGEON_REWARDS.csv), [Raid CSV](RAID_BOSS_REWARDS.csv) and [JSON mirror](COMBAT_REWARD_TABLES.json) contain the exact values. The [source delta](../provenance/checkpoint-18-package/MASTER_LIVE_MODEL_DELTA.md) is preserved verbatim.

## Dungeon completion rewards

| Rank | Normal credits | Hard credits (×1.5) |
|---|---:|---:|
| Red | 395 | 593 |
| Orange | 1,020 | 1,530 |
| Yellow | 2,305 | 3,458 |
| Green | 4,550 | 6,825 |
| Blue | 7,800 | 11,700 |
| Violet | 13,750 | 20,625 |
| White | 34,455 | 51,683 |

Checkpoint 18 halves the prior deterministic Normal payouts. White Normal is **34,455 = 26,955 + 7,500**. Hard completion is **1.5× recalibrated Normal, whole-credit HALF_UP** at every rank; Red 592.5→593, Yellow 3457.5→3458 and White 51682.5→51683 demonstrate the rounding rule. These completion values do not supply Dungeon party-distribution, partial-progress, boss/contribution or first-clear bonus formulas; those unsupplied details remain OPEN. Existing partial-progress credit and completion-weighted economics are preserved.

## Hard Dungeon ecology

Normal and Hard Valnak Dungeons both span R→W and use the same cumulative rank-legal eldris palettes: R, R+O, R+O+Y, R→G, R→B, R→V, and R→V at White. **No White eldris exist.** Both use the unchanged **209 atomic groups**, each containing 1–4 bodies.

Hard uses the same average area ladder as Normal: **5 / 13 / 25 / 53 / 113 / 285 / 450 mi²**, respectively. Hard increases population density and the number of deployed legal groups, creating more sustained combat, fatigue and coordination pressure. The **1.5× multiplier applies to payout, not map area**. This supersedes the former blanket larger-map description and unresolved Hard average areas. Exact realization geometry, population/placement counts and Hard runtime targets remain OPEN; no runtime multiplier follows from payout. The [Normal runtime targets](../builder/encounters/NORMAL_DUNGEON_AUTHOR_SCALE.csv) remain unchanged.

## Raid major-boss rewards

| Boss rank | Normal credits | Expedition/Hard credits (×1.5 HALF_UP) |
|---|---:|---:|
| Red | 2,500 | 3,750 |
| Orange | 3,750 | 5,625 |
| Yellow | 5,000 | 7,500 |
| Green | 7,500 | 11,250 |
| Blue | 11,250 | 16,875 |
| Violet | 17,500 | 26,250 |
| One boss at each R→V rank | **47,500** | **71,250** |

The totals sum one boss at each listed rank. The mature standalone roster is R/O/Y/G/B/V; the existing First-Cycle standalone roster **R/R/O/O/Y/G** is preserved. The rank table does not replace that roster or promise every participant a six-boss total. Expedition remains the full six-wing progression, without first-cycle downscaling.

The major completion reward is earned **once per participant per boss per season**. Repeat assistance/practice/social kills remain legal and do not repeat the major payout for that participant. The unit is a boss, not a shared same-rank allowance. Existing season reset and 12 major opportunities (six standalone plus six Expedition bosses) remain. Participant maximum stays ten; smaller groups remain legal.

Expedition/Hard Raid uses the same seasonal bosses as Normal in a continuous hostile environment. [Current complete doctrine](../live-model/COMBAT_ECOLOGY.md#october-8-cumulative--hard-raid-doctrine) locks roster, death/exit re-instancing, no re-entry/replacement, no systemic fatigue reset, complete-attempt restart without checkpoints, and persistent reward eligibility. Ordinary in-instance rest is not a systemic reset; accessibility follows build depth, not an availability gate.

## Valnak domai rewards — OPEN BY DESIGN

There is **no fixed rank reward table and no deterministic formula**. Valnak evaluates validated contribution in the existing local participation ledger. Author-facing awards may be assigned contextually **per incursion and per participant**, supporting story/economic pacing.

Contribution may include eldris kills, healing/support, control, operational contribution, core assault and other validated participation. The core-break bonus concept remains valid; its exact amount/formula remains OPEN. This flexibility is deliberate rather than missing data.

Existing Valnak domai ranks remain R→V. The main White Crystal's break ends the training encounter. Outside domai ontology, including progressive unraveling after core break, is unchanged.

## Preservation and audit

Recalibrated W1–35 Trial rows total **26,955**; the repriced 17-event illi ledger totals **250,884** expenditure. Their rules/dates, Project Princess Carry, atomic group records, cumulative availability, White Normal content, outside ontology and unrelated canon are preserved. The supplied 59-day combat calendar adds required progression income; all existing milestone dates remain unchanged.

Run `python combat-rewards/validate_rewards.py` from the repository root; add `--output combat-rewards/AUDIT.json` to save the report. The validator checks both CSVs against JSON and the exact supplied values, every 1.5× relationship with whole-credit HALF_UP, both Raid totals, Hard/Normal area equality and the OPEN BY DESIGN domai boundary. [Checkpoint 18](../live-model/25_CHECKPOINT_18_MASTER_LIVE_MODEL.md), [reverse diff](../provenance/CHECKPOINT_18_REVERSE_DIFF.csv), [coverage](../provenance/CHECKPOINT_18_COVERAGE_MANIFEST.csv) and [integration audit](../provenance/CHECKPOINT_18_AUDIT.json) document the complete reconciliation.

Checkpoint 18 does **not** halve Valnak domai awards. [Participation rules](../live-model/DOMAI_PARTICIPATION.md) lock seven days from first validated kill, conquest within that window even after departure, one full day of same-domai lockout after exit/death, and cumulative validated award ×0.8^deaths. Scoring remains OPEN BY DESIGN; the multiplier constrains an eventual contextual award without defining it.

## Checkpoint 22 domai allocation clarification

[Group economy](DOMAI_GROUP_ECONOMY.md) / [structured clarification](DOMAI_GROUP_ECONOMY.json) governs aggregate group contribution → equal eligible base shares → individual death multipliers. The CP18 participant rule’s validated award is that participant’s base share under CP22. Its first-kill seven-day eligibility, same-domai one-day lockout and ×0.8^deaths are unchanged. Optional bonuses and fractional rounding remain OPEN. Trial/Dungeon/Raid tables are byte-identical; Y7D4 domai amount is OPEN and excluded from fixed Yellow gross.

## Checkpoint 25 separate core layer

Ordinary domai contributions remain contextual OPEN BY DESIGN. [Registered two-person core awards](DOMAI_CORE_AWARDS.json) now lock R/O/Y/G collective 1M/2.3M/3.7M/5M, split equally. Blue/Violet successful core awards remain OPEN. Existing participant eligibility, recovery, death multiplier and fixed Dungeon/Raid tables are preserved. [Spatial metric](DOMAI_SPATIAL_METRIC.csv) uses equivalent radius only as author traversal scale; [doctrine](../live-model/DOMAI_PARTICIPATION.md).

## R2/R3 cumulative income and narrative doctrine

The combat/purchase calendar is a **minimum guaranteed progression-income spine**, not a closed wallet or earnings ceiling. Extra legitimate income can come from optional Trials, Dungeons/Raids, `raeon`, Prism, crafting and other established activity. This broadens the earlier incidental shallow-Trial doctrine without inserting required events. Extra income does not automatically move locked Binding purchase dates earlier. Actual wallet bookkeeping is deferred to the later chapter-outline pass. Surplus may fund cards, clothes/formalwear, residence work, food/abecca, entertainment and gifts; existing progression-financing restrictions remain.

Raid major payout remains once per participant per **specific boss per season**, with the existing Normal/Expedition opportunity distinction preserved. Distinct same-rank bosses can each pay once. If later story supplies an additional Red and an additional Orange Normal first-clear, each girl earns **2,500 + 3,750 = 6,250**, or **12,500 combined**, as wallet/social surplus. These additional clears are conditional, not booked events or present balances; do not erase surplus through the formal progression ledger or advance Binding dates.

OPEN/recovery days may pass off-page. Calendar is macro time; narrative selects meaningful intersections. No chapter count is assigned.

[Master source](../provenance/diplomatic-pouch-r2-r3/package/MASTER_DELTA.md); [conditional Raid scope](../provenance/diplomatic-pouch-r2-r3/package/R3_RAID_ROSTER.md#red-season-character-reward-handling). Checkpoint 25 and compatible earlier locks still govern their scopes; this is not a numbered checkpoint.

## October 8 — authored bonus clears and Solo accounting

The existing Red→O2D3 ledger remains the minimum progression scaffold. R4D5 Burrower (Red B) now clears for **2,500 per girl** in separate actual/discretionary wallet surplus. O1D6’s newly authored Sixfold (Red A) plus Triumvirate (Red B) clears each pay 2,500; the existing minimum row covers one Red only. The new source calls the second Red a further 2,500 per girl wallet surplus. Black Orchard fails and gives no Orange major reward.

The cumulative Red/Orange reconciliation resolves O4D2: Black Orchard pays3,750 each; Red repeats pay0 after both Reds paid O1D6. Current Arc Three minimum gross is56,385 illi /81,415 Kira. The earlier second-Red2,500 stays O1D6 actual/discretionary surplus; no duplicate reward remains. Black Orchard Orange-A clears O4D2; any Red warm-up is unpaid. The current39-row minimum total decreases2,500 per girl, without reclassifying O1D6’s already-earned discretionary2,500 as another reward. No third Red, mode swap or deferred-payment device is created. Earlier optional extra Red+Orange examples stay conditional; no unsupplied Orange clear follows.

Trial table audit: completed W1 pays 50, W1–W2 totals 140, W1–W3 totals 255; failed next waves pay zero. R2D5’s W2 clear remains 140 and is a bad run, not a ceiling. R4D1’s minimum 255 does not establish the final depth of its now-variable Orange-pressure run. Optional R6D4/R7D5/O1D4 efforts have no authored exact results and receive no guessed credits. All progression-spend values remain fixed; only the explicitly corrected PC Blue/Legacy O1D3 and Absorption O2D2 dates move. Actual/discretionary wallet closure awaits later outline accounting.

[Author locks](../provenance/diplomatic-pouch-2026-10-08/package/package/00_CONFLICTS_AND_LOCKS.md); [Orange Week One](../provenance/diplomatic-pouch-2026-10-08/package/package/03_ORANGE_W1.md); [conflict audit](../provenance/diplomatic-pouch-2026-10-08/CONFLICTS.json).

## October 8 cumulative — reconciled economy

Current Arc Three O2D4–O7D7 minimum gross: **56,385 illi /81,415 Kira**; Kira-only Solo remains25,030. O4D2 pays only Black Orchard **3,750 each**; both Normal Reds already paid O1D6, whose actual5,000 includes2,500 booked+2,500 discretionary. R4D5 Burrower’s2,500 remains discretionary. Never add the same second-Red reward twice.

PC Blue/White Legacy now O1D3 for25,705, post-balance952; Absorption Red O2D2 for9,350, post-balance42. Their minimum prebalances26,657/9,392 and total progression spend stay unchanged. CSR purchase O2D3 costs Kira61,017. Optional illi W7/W8 Solo credits remain OPEN. The conditional86,000−81,415=**4,585** card-funding difference assumes no opening funds/other income/prior spending; it is no canonical debt or invented award. Actual wallets and contextual domai payout remain OPEN. [Explicit correction](../provenance/diplomatic-pouch-2026-10-08/package/red-orange-reconciliation/package/ORANGE_W1_W4.md), [current calendar](../world-clock/ARC3_ORANGE_CALENDAR.md).
