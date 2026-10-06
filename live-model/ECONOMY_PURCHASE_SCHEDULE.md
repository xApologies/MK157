# MK157 — Economy and purchase-schedule handoff

Current authority: Checkpoint 18, cumulative with earlier non-conflicting rules. The 17 illi milestones, their exact progression-cost ledger and W1–35 reward rows are locked; remaining purchase dates and the full income/spending ledger remain OPEN.

## Kira Black acquisition economics — current

Armor of the Abyss remains the approximately 1,000-credit anomalous starter. CSR → Genesis Orbs → Halo → Domain follow in that order, with all four final acquisition prices OPEN for recalibration. Checkpoint 14 supersedes the former flat-price lock and derived totals; no replacement numbers are assigned.

Availability/admissibility, affordability, and competency/discovery/integration after acquisition are separate. Black foundations do not use ordinary paid rank ladders. Ordinary registry prices cannot supply replacement character-specific prices. See [Checkpoint 14](21_CHECKPOINT_14_FULL_RECONCILIATION.md).

## 4. illi Red-season economic objective / White Legacy gate

illi begins with:
**Persistent Coherence — Red**

During Red season, she develops/ranks Persistent Coherence using the ordinary recursive Binding economy.

Ordinary pricing law remains:
Red = B
Orange = previous ×1.60
Yellow = previous ×1.80
Green = previous ×2.10
Blue = previous ×2.50
Violet = previous ×3.00
White = previous ×4.00

For an illustrative B=1,000 Persistent Coherence:
R 1,000
O 1,600
Y 2,880
G 6,048
B 15,120

Cumulative Red-through-Blue investment:
**26,648 credits**

Author shorthand: roughly 27k / just under 30k.

NEW LOCK:
**Persistent Coherence must reach BLUE for illi to qualify for/access her White Legacy trajectory.**

This gives Red season a concrete illi objective, completed in early Orange:
rank Persistent Coherence R -> O -> Y -> G -> B.

Once Blue Persistent Coherence is achieved, the White Legacy becomes available and can prescribe/enable the next major acquisition:
**Absorption Shield**.

Checkpoint 14 locks Blue Persistent Coherence and White Legacy acceptance at Orange W1 D4, then Absorption Shield Red at Orange W2 D3. These supplied milestones constrain the future ledger; the older arbitrary Orange W1 D4 Absorption date remains superseded.

Existing later White-Legacy gates remain:
- Genesis Beam GREEN -> Genesis Prime RED available
- Persistent Coherence GREEN -> Coherence Prime RED available
- Absorption Shield GREEN -> Resonance Prime RED available

The new Blue Persistent Coherence rule is specifically the ENTRY QUALIFICATION for access to the White Legacy trajectory, not a replacement for later individual Prime gates.

## 5. Credit economy doctrine

Credit generation != credit retention.

Credits compete among:
- Binding acquisition;
- Binding rank development;
- equipment;
- rare materials / `vaen`;
- Auction purchases;
- `raeon` cards;
- Genesis Cards;
- other Valnak shopping/leisure.

First-cycle participants are capability-throttled rather than arbitrarily credit-capped.
Most first cycles remain in relatively modest Trial/Dungeon bands for substantial portions of the cycle.
Green Solo permits graduation from first-cycle progression grouping, but early Green is unusual.

Veterans operate in a different economic regime because they bring accumulated:
Bindings, ranks, competency, equipment, experience and carried-forward credits across cycles.

Kira later bends the credit curve because the Orb blender lawfully breaks ordinary Trial scaling, but large Black prices and discretionary spending prevent her ledger from functioning like a simple XP bar.

## 6. Auction as credit sink

Seasonal Auctions are a major discretionary credit sink.

Potential purchases:
- Creator originals
- Valnak one-offs
- Dimensional Rings
- rare equipment
- prepared/infused metals
- rare `vaen`
- Genesis materials
- unusual Alchemical products
- Genesis Cards / special collectibles where appropriate

Illustrative conversational values such as a 100,000-credit Dimensional Ring are NOT locked unless later deliberately priced.

Valnak can reproduce certain rare real-world materials/items for deliberately limited Auction release without making them infinite Shop inventory.

## 12. Next-thread development target

Further development should crawl current Git and continue the **Valnak Calendar / purchase schedule simulation**, treating the supplied Checkpoint 14 milestones as author constraints.

Primary task:
map Kira + illi across:
Season -> Week -> Day

Track:
- current Bindings / ranks;
- next purchase/gate;
- credit earned;
- credit spent;
- ledger balance;
- Solo/Duo/Trio wave progression;
- time consumed by Trials;
- Dungeons;
- raid preparation/attempts;
- `domai` operations;
- social/royal obligations;
- Prism;
- `raeon`;
- Auctions;
- nightly highlights;
- story/arc purpose.

Immediate economic goals:
- Recalibrate Kira's four post-Armor Black prices; ordinary registry prices do not substitute for them.
- Model illi's supplied milestone dates, including Blue Persistent Coherence qualification and White Legacy acceptance.
- Solve the remaining income, spending and purchase schedule without inventing post-Violet-W2 rank dates.

## 13. Protected OPEN items

Do not silently decide:
- exact Genesis Card set sizes/rarities/prices;
- exact `raeon` individual card prices;
- exact Auction item prices;
- exact Kira discretionary purchases;
- exact illi discretionary purchases;
- exact Red-season credit income until actual runs and other income are modeled;
- illi rank dates after the supplied Violet W2 D2 milestone;
- exact day Kira buys CSR;
- exact standard card dimensions beyond the working trading-card form factor.
## Checkpoint 12 canonical inputs

Current ordinary prices are in the [Binding registry](../bindings/BINDINGS.json), [summon price atlas](../summons/SUMMON_PRICING.json) and [Prime price atlas](../summons/PRIME_ELEMENTAL_PRICING.json). Checkpoint 18 prices Persistent Coherence by its Foundational class: B=1700, R 1700/O 2720/Y 4896/G 10282/B 25705; cumulative R-through-Blue **45,303**, or **43,603** after Red. The above B=1000 calculation remains historical illustration only. Absorption Shield and all Primes are Exceptional B=17000; Genesis Beam is Powerful B=11000; White Legacy access compression is separate from the Checkpoint 13 45% package deduction; illi pays 55% after acceptance.

Kira's CSR/Genesis Orbs/Halo/Domain final prices are OPEN for recalibration under Checkpoint 14. The old flat-price claim is SUPERSEDED; Armor remains approximately 1,000. Ordinary list prices and all unrelated canon remain governed by their existing rules.

## Checkpoint 13 list prices, Legacy subsidy and Trial target

## 1. Absorption Shield repricing — LOCK
GE-0537 Absorption Shield:
Red base B = 17,000 credits (Checkpoint 18 fixed Exceptional anchor).
Pricing class = Exceptional.

Checkpoint 13 first moved GE-0537 to Exceptional; Checkpoint 18 now fixes that class at 17,000. Its class/mechanism is unchanged.
Recompute its ordinary R→W ladder using sequential ROUND_HALF_UP:
R 17,000
O 27,200
Y 48,960
G 102,816
B 257,040
V 771,120
W 3,084,480
cumulative 4,308,616.

Rationale: high-rank Absorption is defining combat-helkir prevention architecture. Preventing catastrophic injury can dominate repairing it after the fact.

## 2. illi White Legacy economic subsidy — LOCK
White Legacy provides BOTH:
1. prerequisite/recipe compression already established; and
2. 45% price deduction on purchases and rank upgrades that belong to the accepted White-Legacy package.

Participant pays 55% of ordinary list price:
P_legacy = 0.55 * P_list.

Use deterministic whole-credit HALF_UP if a discounted price is fractional.

Persistent Coherence R→Blue is paid at FULL PRICE because illi has not yet qualified/accepted the White Legacy.
PT-0003 canonical ladder remains:
1700 / 2720 / 4896 / 10282 / 25705; cumulative 45,303 (Checkpoint 18).
After Red is already paid, remaining O→Blue = 43,603.

Blue Persistent Coherence unlocks White Legacy access.
After acceptance:
Absorption Shield Red list 17,000 → illi price 9,350 (Checkpoint 18).

The 45% deduction applies to the accepted Legacy package, including later ranks and Prime purchases. It does not grant omitted prerequisite Bindings as usable abilities.

Discount each ordinary list purchase/upgrade independently using whole-credit HALF_UP; do not recursively discount already discounted prior ranks. Prequalification Persistent Coherence through Blue remains full price. Membership of any additional Legacy package architecture remains OPEN; no discretionary shopping discount is inferred.

## 3. illi White-Legacy package / causal progression — preserve
Visible developmental package after qualification:
- Absorption Shield
- Genesis Beam
- Genesis Prime Elemental
- Coherence Prime Elemental
- Resonance Prime Elemental / Juggernaut

Individual compressed Prime gates remain:
Genesis Beam GREEN → Genesis Prime RED
Persistent Coherence GREEN → Coherence Prime RED
Absorption Shield GREEN → Resonance Prime RED

Prime ordinary Red base is 17,000. White-Legacy price at Red = 9,350 (Checkpoint 18).

## 4. Kira + illi three carry regimes — LOCK narrative/economic model
Phase I — Armor carries:
Early partnership is enabled by Armor of the Abyss's exceptional persistence.

Phase II — illi prevention carries/extents the Duo:
After White-Legacy access, Absorption Shield materially extends Kira's operating window.
Kira's CSR mobility + Armor + illi prevention increase Duo depth and credit generation.
Absorption remains economically valuable, but the locked Checkpoint 14 schedule intentionally defers its ranks until after late-Green Coherence Prime; prerequisite availability does not force immediate purchase.

Phase III — Kira CARRIES after Orb blender maturation:
Genesis Orbs arrive late Yellow; acquisition is not mastery.
One-Orb crude/orbit use develops toward two-Orb patterned control.
Around mid-Green, mature two-Orb blender is the major economic inversion.
Most incoming eldris are destroyed before reaching the center; attacks that penetrate Orb exclusion meet illi Absorption, then Armor.
Kira's Trial-breaking throughput then accelerates illi's White-Legacy credit generation dramatically.

Canonical mature defensive stack remains:
Orb exclusion → illi Absorption/prevention → Armor of the Abyss → Kira.

This is a coupled positive feedback system, not generic veteran boosting.

## Exact Trial reward schedule

Checkpoint 18 recalibrates the exact [W1–35 reward rows](../trial-rewards/TRIAL_WAVE_CREDITS.csv), totaling 26,955 per eligible participant. Completed waves pay; the failed next wave does not. Solo/Duo/Trio share the schedule; legitimate repeats pay again. W36+ remains OPEN. Earlier ~55,000 and Checkpoint 14's 53,910 are historical pre-recalibration values; the rejected high-output table stays rejected. [Reward economy context](../trial-rewards/README.md) preserves the ~156-hour estimate and career/multi-cycle White-mastery design.


## Commodity economy — LOCK doctrine; prices mostly OPEN
Credits are not XP. Non-Binding sinks intentionally compete with progression.
Veterans with mature builds may value collectibles/equipment/leisure over marginal power.
Genesis Cards range from accessible thousands to rare/cycle-exclusive million-credit commodities based on scarcity/provenance/demand/edition/manifold/artistry; no universal color-price formula.
raeon specialty/cycle cards can also become expensive.
Auction is a top-end sink for rare equipment, Creator originals, materials, cards, Dimensional Rings and one-offs.
Illustrative White Fireball 1.3M/3M, Dimensional Ring 2M, and Valnak-made princess tiara are examples only unless later locked.

[illi progression](ILLI_PROGRESSION.md) provides 17 dated author milestones; post-Violet-W2 rank dates remain OPEN. [Partnership/economy](PARTNERSHIP_AND_CARRY.md) preserves independent schedules, discretionary spending and Project Princess Carry. These are story constraints, not a fabricated income simulation.

## Checkpoint 16 progression ledger and Normal Dungeon base

The [illi author ledger](../world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.csv) preserves all 17 milestone dates and totals **250,884 credits** in progression expenditure by Violet W2 D2. Full-price prequalification Persistent Coherence and independent 55%-of-list package purchases match the established pricing rules. This is not literal bank balance or gross earnings; discretionary spending remains separate.

White Valnak Normal Dungeon successful-completion base is **34,455 = 26,955 + 7,500 credits**. Reliable Dungeon clears should generally outperform equivalent Trial farming in credits/hour, with failure/procedural/coordination risk preserving Trial value. Checkpoint 18 recalibrates the [complete Normal/Hard Dungeon completion and Raid major-boss payouts](../combat-rewards/README.md). Hard rewards are 1.5× Normal rounded HALF_UP; Hard Dungeon average areas match Normal and pressure increases through density/deployed groups. Raid rewards remain once per participant per boss per season; Expedition elimination persists for the attempt with no mid-run replacement. Dungeon distribution, partial-progress, boss/contribution and first-clear bonus formulas remain OPEN. Valnak domai awards are contextual per incursion/per participant and OPEN BY DESIGN; no rank table or deterministic formula is assigned, and the core-break amount/formula remains OPEN. The [Normal Dungeon scale](../builder/encounters/NORMAL_DUNGEON_AUTHOR_SCALE.csv) supplies authored runtime targets, not fixed stopwatch laws.

The World Clock + character + economy calendar is ready for authored content placement. Purchases must be economically plausible against the ledger's progression-capital breakpoints, without micro-accounting every discretionary purchase. No new income schedule, encounter placement or post-Violet-W2 rank date is invented here.

[Checkpoint 18 combat calendar](25_CHECKPOINT_18_MASTER_LIVE_MODEL.md) governs the 59 supplied Red→O2D3 rows, retaining 21 NO REQUIRED COMBAT days and all milestone dates. Starter grant 2,000; illi combat income 52,695 through O2D2; PC Blue/Legacy leaves 952 at O1D4 and Absorption Red leaves 42 at O2D3. Discretionary spending and later income remain separate/OPEN.
