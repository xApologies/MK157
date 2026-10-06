# Combat reward economy — Checkpoint 18

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

Expedition/Hard Raid is an attrition expedition. Intervening eldris are the path to the next boss reward. An eliminated participant remains out for that expedition attempt, with **no mid-run replacement**. Remaining participants may continue short-handed or abandon. No additional resurrection or re-entry rules are supplied.

## Valnak domai rewards — OPEN BY DESIGN

There is **no fixed rank reward table and no deterministic formula**. Valnak evaluates validated contribution in the existing local participation ledger. Author-facing awards may be assigned contextually **per incursion and per participant**, supporting story/economic pacing.

Contribution may include eldris kills, healing/support, control, operational contribution, core assault and other validated participation. The core-break bonus concept remains valid; its exact amount/formula remains OPEN. This flexibility is deliberate rather than missing data.

Existing Valnak domai ranks remain R→V. The main White Crystal's break ends the training encounter. Outside domai ontology, including progressive unraveling after core break, is unchanged.

## Preservation and audit

Recalibrated W1–35 Trial rows total **26,955**; the repriced 17-event illi ledger totals **250,884** expenditure. Their rules/dates, Project Princess Carry, atomic group records, cumulative availability, White Normal content, outside ontology and unrelated canon are preserved. The supplied 59-day combat calendar adds required progression income; all existing milestone dates remain unchanged.

Run `python combat-rewards/validate_rewards.py` from the repository root; add `--output combat-rewards/AUDIT.json` to save the report. The validator checks both CSVs against JSON and the exact supplied values, every 1.5× relationship with whole-credit HALF_UP, both Raid totals, Hard/Normal area equality and the OPEN BY DESIGN domai boundary. [Checkpoint 18](../live-model/25_CHECKPOINT_18_MASTER_LIVE_MODEL.md), [reverse diff](../provenance/CHECKPOINT_18_REVERSE_DIFF.csv), [coverage](../provenance/CHECKPOINT_18_COVERAGE_MANIFEST.csv) and [integration audit](../provenance/CHECKPOINT_18_AUDIT.json) document the complete reconciliation.

Checkpoint 18 does **not** halve Valnak domai awards. [Participation rules](../live-model/DOMAI_PARTICIPATION.md) lock seven days from first validated kill, conquest within that window even after departure, one full day of same-domai lockout after exit/death, and cumulative validated award ×0.8^deaths. Scoring remains OPEN BY DESIGN; the multiplier constrains an eventual contextual award without defining it.
