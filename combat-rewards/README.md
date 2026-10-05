# Combat reward economy — Checkpoint 17

These are the locked Valnak Dungeon completion and Raid major-boss payouts. [Dungeon CSV](DUNGEON_REWARDS.csv), [Raid CSV](RAID_BOSS_REWARDS.csv) and [JSON mirror](COMBAT_REWARD_TABLES.json) contain the exact values. The [source delta](../provenance/checkpoint-17-package/COMBAT_REWARD_ECONOMY_DELTA.md) is preserved verbatim.

## Dungeon completion rewards

| Rank | Normal credits | Hard credits (×1.5) |
|---|---:|---:|
| Red | 790 | 1,185 |
| Orange | 2,040 | 3,060 |
| Yellow | 4,610 | 6,915 |
| Green | 9,100 | 13,650 |
| Blue | 15,600 | 23,400 |
| Violet | 27,500 | 41,250 |
| White | 68,910 | 103,365 |

The recovered Normal rows resolve the Red→Violet payout OPENs. White Normal remains **68,910 = 53,910 + 15,000**. Hard completion pays exactly **1.5×** Normal at every rank. These completion values do not supply Dungeon party-distribution, partial-progress, boss/contribution or first-clear bonus formulas; those unsupplied details remain OPEN. Existing partial-progress credit and completion-weighted economics are preserved.

## Hard Dungeon ecology

Normal and Hard Valnak Dungeons both span R→W and use the same cumulative rank-legal eldris palettes: R, R+O, R+O+Y, R→G, R→B, R→V, and R→V at White. **No White eldris exist.** Both use the unchanged **209 atomic groups**, each containing 1–4 bodies.

Hard uses the same average area ladder as Normal: **5 / 13 / 25 / 53 / 113 / 285 / 450 mi²**, respectively. Hard increases population density and the number of deployed legal groups, creating more sustained combat, fatigue and coordination pressure. The **1.5× multiplier applies to payout, not map area**. This supersedes the former blanket larger-map description and unresolved Hard average areas. Exact realization geometry, population/placement counts and Hard runtime targets remain OPEN; no runtime multiplier follows from payout. The [Normal runtime targets](../builder/encounters/NORMAL_DUNGEON_AUTHOR_SCALE.csv) remain unchanged.

## Raid major-boss rewards

| Boss rank | Normal credits | Expedition/Hard credits (×1.5) |
|---|---:|---:|
| Red | 5,000 | 7,500 |
| Orange | 7,500 | 11,250 |
| Yellow | 10,000 | 15,000 |
| Green | 15,000 | 22,500 |
| Blue | 22,500 | 33,750 |
| Violet | 35,000 | 52,500 |
| One boss at each R→V rank | **95,000** | **142,500** |

The totals sum one boss at each listed rank. The mature standalone roster is R/O/Y/G/B/V; the existing First-Cycle standalone roster **R/R/O/O/Y/G** is preserved. The rank table does not replace that roster or promise every participant a six-boss total. Expedition remains the full six-wing progression, without first-cycle downscaling.

The major completion reward is earned **once per participant per boss per season**. Repeat assistance/practice/social kills remain legal and do not repeat the major payout for that participant. The unit is a boss, not a shared same-rank allowance. Existing season reset and 12 major opportunities (six standalone plus six Expedition bosses) remain. Participant maximum stays ten; smaller groups remain legal.

Expedition/Hard Raid is an attrition expedition. Intervening eldris are the path to the next boss reward. An eliminated participant remains out for that expedition attempt, with **no mid-run replacement**. Remaining participants may continue short-handed or abandon. No additional resurrection or re-entry rules are supplied.

## Valnak domai rewards — OPEN BY DESIGN

There is **no fixed rank reward table and no deterministic formula**. Valnak evaluates validated contribution in the existing local participation ledger. Author-facing awards may be assigned contextually **per incursion and per participant**, supporting story/economic pacing.

Contribution may include eldris kills, healing/support, control, operational contribution, core assault and other validated participation. The core-break bonus concept remains valid; its exact amount/formula remains OPEN. This flexibility is deliberate rather than missing data.

Existing Valnak domai ranks remain R→V. The main White Crystal's break ends the training encounter. Outside domai ontology, including progressive unraveling after core break, is unchanged.

## Preservation and audit

W1–35 Trial rows still total **53,910**; the 17-event illi progression ledger still totals **130,261** expenditure. Their rules/dates, Project Princess Carry, atomic group records, cumulative availability, White Normal content, outside ontology and unrelated canon are preserved. No new income calendar or purchase dates are assigned.

Run `python combat-rewards/validate_rewards.py` from the repository root; add `--output combat-rewards/AUDIT.json` to save the report. The validator checks both CSVs against JSON and the exact supplied values, every 1.5× relationship using integer arithmetic, both Raid totals, Hard/Normal area equality and the OPEN BY DESIGN domai boundary. [Checkpoint 17](../live-model/24_CHECKPOINT_17_COMBAT_REWARD_ECONOMY.md), [reverse diff](../provenance/CHECKPOINT_17_REVERSE_DIFF.csv), [coverage](../provenance/CHECKPOINT_17_COVERAGE_MANIFEST.csv) and [integration audit](../provenance/CHECKPOINT_17_AUDIT.json) document the complete reconciliation.
