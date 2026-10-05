# MK157 — CHECKPOINT 12 PRICING POLICY v2

## Governing purpose
Assign canonical Red base acquisition cost B to:
- all 1,016 Binding records;
- all 229 summoned-entity Binding records;
- all 9 Prime Elementals.

The row-level registries carry the prices. Do not paste thousands of rows into narrative live-model files.

## Existing rank law — unchanged
For each Binding with Red base B:
- Red = B
- Orange = previous × 1.60
- Yellow = previous × 1.80
- Green = previous × 2.10
- Blue = previous × 2.50
- Violet = previous × 3.00
- White = previous × 4.00

Derived prices are whole credits. Use deterministic ROUND_HALF_UP at each rank transition.

## Ordinary acquisition bands
These bands describe Red acquisition friction, NOT power rank, basin identity, rarity color, or class.

1. FOUNDATIONAL — 500–1,000
   Civic/professional primitives; basic direct operations; starter-capable foundations.

2. COMMON_SPECIALIZATION — 1,100–2,400
   Normal specialist tools and focused operational architecture.

3. ADVANCED — 2,500–4,900
   Fields, expanded/multi-target/conditional systems, substantial specialist architecture.

4. POWERFUL — 5,000–9,900
   High-throughput or major combat/control architecture; sophisticated/high-output systems.

5. EXCEPTIONAL — exactly 10,000 maximum ordinary Red anchor for this pass
   Top-tier architectures whose Red form is itself difficult to obtain.

No ordinary summoned entity may exceed 9,900 Red. Prime Elementals alone are explicitly fixed at 10,000 among summon records.

## Hand-locked Binding anchors
- PT-0002 Directed Coherence = 600
- PT-0003 Persistent Coherence = 700
- PT-0001 Coherence Field = 1,800
- GE-0537 Absorption Shield = 10,000 (Checkpoint 13 supersession)
- GE-0043 Genesis Beam = 5,000

These values override classifier output.

## Prime Elementals — LOCK
ALL Prime Elementals PE-001 through PE-009:
Red base B = 10,000 credits.

No Prime-specific premium above 10,000.
Their exceptional status is expressed by prerequisite architecture + the 10,000 acquisition + recursive rank expense.

Prime Red→White ladder:
Red 10,000
Orange 16,000
Yellow 28,800
Green 60,480
Blue 151,200
Violet 453,600
White 1,814,400

Cumulative Red→White = 2,534,480 credits.

illi's White Legacy compresses ACCESS prerequisites; it does not automatically waive the 10,000 Prime acquisition price unless later author canon explicitly creates a subsidy.

## Summoned-entity pricing
All 229 summoned entities represent summon Bindings and receive Red prices.
Ordinary summons must be below 10,000.

Semantic factors:
- control complexity;
- scale;
- manifestation/sustain load;
- breadth of autonomous behavior;
- offensive/defensive consequence;
- persistence;
- mobility;
- distributed/swarm coordination;
- siege/capstone character.

General expectation, not a blind formula:
- small/simple/low-control manifestations: foundational/common;
- ordinary combat specialists: common/advanced;
- high-control, large, swarm, major area/siege manifestations: advanced/powerful;
- no ordinary summon reaches or exceeds Prime's 10,000 lock.

Do not price by elemental mechanism or basin color alone.

## Binding semantic classification
Inspect every record. Price from mechanism and acquisition significance, considering:
- foundational dependency value;
- civic/professional accessibility;
- directed vs field/multi-target geometry;
- control and information complexity;
- sustain/concurrency;
- breadth;
- high-output consequences;
- prerequisite/capstone role.

Prefer prices in 50- or 100-credit increments. Avoid fake precision.

## Absolute firewalls
- Never infer cost from Red/Orange/Yellow/Green/Blue/Violet basin composition.
- Pricing class is not an in-world rank.
- Preserve all basin OPENs and topology.
- Preserve all IDs, recipes, White expressions, statuses, and gates.
- Kira's Black economics remain separate:
  Armor ~1,000 anomalous starter;
  CSR 61,000;
  Genesis Orbs 61,000;
  Halo 61,000;
  Domain 61,000.
  Ordinary registry prices must NOT overwrite these character-specific Black acquisition gates.

## Required registry fields
For Bindings:
pricing_class
red_base_cost
Red Orange Yellow Green Blue Violet White
pricing_status = "LOCKED — Checkpoint 12"

For summons, create pricing mirrors keyed by entity_id with:
entity_id
name
pricing_class
red_base_cost
Red Orange Yellow Green Blue Violet White
pricing_status

For Prime Elementals, create explicit pricing mirror keyed by prime_id.

## Required audit
Verify:
- exactly 1,016 Bindings priced;
- exactly 229 summoned entities priced;
- exactly 9 Prime Elementals priced at 10,000;
- zero null Red costs;
- zero ordinary summons >= 10,000;
- anchors exact;
- rank arithmetic exact;
- CSV/JSON/JSONL Binding mirrors agree;
- no IDs/recipes/basin data lost;
- Kira gates unchanged.

## Reproducible semantic assignment

The operational classifier is preserved in provenance/checkpoint-12-package/SEMANTIC_PRICING.ps1. It examines every record and records its factors/rationale in ../provenance/CHECKPOINT_12_PRICING_DECISIONS.csv. Author anchors override the classifier. Otherwise price uses geometry, focused/expanded scope, sustain, concurrent/distributed control, physiological information precision, spatial constraints, output and autonomous role. Existing price scaffolding and ID sequence never contribute.

Summon scale starts at Tiny 500, Small 1100, Medium 1700, Large 2400, Huge 4000, Variable 2200; control adds 0/250/500/1400/2000/2800 for low through extreme. Moderate/high/very-high/extreme sustain adds 300/600/900/1200. Area/lane control adds 400; aerial pursuit 250; guard/transport/interception 150; siege/high-output assault 700. Distributed saturation adds 800; simple low-control hours-long scouting persistence adds 100. Ordinary prices cap at 9900. Elements, species, visible color and basin data create no price premium. Semantically identical patterns receive equal prices.

Matched summon-Binding names share price decisions; unmatched manifestations use their explicit role and distributed coordination. Ordinary CSR has its own operational registry price and does not overwrite Kira's Black acquisition gate.

ROUND_HALF_UP applies sequentially at every positive-credit transition using decimal arithmetic; the next rank uses the rounded preceding rank. Pricing LOCKED status does not promote an ALPHA mechanism, recipe or topology to canon. Existing status/source strings are preserved even if historical wording mentions OPEN costs; pricing_status and this policy supersede only that price claim.
Checkpoint 13 supersedes only GE-0537 to B=10000, Exceptional, cumulative R–W 2534480. The 45% accepted White-Legacy package deduction is character-specific (pay 55%, HALF_UP independently per list item/rank); ordinary registry prices remain list prices. Prequalification Persistent Coherence is full-price. Kira Black gates remain 61000 each.
