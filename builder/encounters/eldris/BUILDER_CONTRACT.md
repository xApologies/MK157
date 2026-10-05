# eldris atomic group builder contract

## Purpose
This author-facing registry defines reusable *atomic eldris groups*. IDs are editorial handles; they are not a claim about Valnak internal implementation. It does NOT define full encounters, map placement, dungeon populations, spawn schedules, or prose scenes.

Hierarchy:
individual eldris -> atomic group -> encounter composition -> dungeon/domai/trial population.

## Hard constraints
1. Atomic population is 1–4 bodies. Never exceed four inside one atomic-group record.
2. Group IDs are assigned by the highest Genesis basin represented:
   R###, O###, Y###, G###, B###, V###.
3. A higher-rank encounter builder may use any atomic group at or below its legal ceiling.
4. No group may contain an eldris above its ID ceiling.
5. There is no White eldris. White Valnak Normal and Hard Dungeons use the complete R→V atomic library under mastery-level encounter architecture. The W availability key introduces no White eldris or groups. Outside persistent Dungeon ontology and the prohibition on White domai are unchanged.
6. Basin color is ontological Genesis-field identity, not an arbitrary game difficulty tag.
7. Combat-family partition:
   melee = Red / Orange / Green
   Transductionist = Yellow / Blue / Violet
8. Canonical expressions:
   Red physical; Orange intrusion; Yellow ranged force;
   Green juggernaut/persistence threshold; Blue expressed projection;
   Violet high Genesis expression.
9. Do not invent aggro/threat mechanics, MMO roles, health-bar inflation, or illegal higher-rank eldris.
10. The builder may duplicate atomic groups and combine many groups to create large populations.

## Why the registry is exhaustive-but-small
For each ceiling, the library enumerates every unordered basin multiset of population 1–4 whose highest represented basin equals that tier.
This avoids redundant copies: e.g. a pure Red group remains R### and is still legal in Orange through White content.
A Blue encounter can therefore combine R###, O###, Y###, G###, and B### groups.

## Example
A larger encounter containing exactly 25 bodies can be composed from:
2× R004 + 2× O006 + Y012 + G018 + B021
The populations are 2×4 + 2×3 + 4 + 4 + 3 = 25. The highest member is Blue, so this example is legal at a Blue-or-higher permitted ceiling. This is an illustration, not a fixed encounter or spawn schedule.
The encounter builder controls placement, timing, terrain relation, and larger tactical structure.

## Environment independence
Atomic groups are not tied to Deep Caverns, Dune Wastes, Oldgrowth, Overgrown City, Highlands, Marshlands, Frozen Expanse, Broken Coast, or Ruined Citadel.
The same legal group can be placed into different procedural domain realizations.

## Area context
The supplied author area ladder is R5/O13/Y25/G53/B113/V285/W450 mi².
Normal Dungeon average realized areas are locked at Red 5, Orange 13, Yellow 25, Green 53, Blue 113, Violet 285 and White 450 mi². Checkpoint 16 explicitly enables White Valnak Normal content; this does not change the Trial arena or outside ontology.
`BASIN_REFERENCE.csv` preserves the supplied area column and adds explicit rank-enablement and area-scope fields; consumers must honor them. `TIER_AVAILABILITY.json` describes composition ceilings, not which content types exist.
The older flat Normal ~5 / Hard ~7.5–8 mi² estimates are superseded as universal scales. Checkpoint 17 locks Hard to the same average area at every rank and the same legal group vocabulary. Hard deploys more groups at greater population density to create sustained combat, fatigue and coordination pressure. The exact 1.5× multiplier governs completion payout, not map area or runtime. No final population/placement counts are assigned.
Area is total realized environment, not required traversal distance.
Larger maps permit more atomic groups and wider separation; they do not require larger atomic groups.

[Normal Dungeon author scale](../NORMAL_DUNGEON_AUTHOR_SCALE.csv) supplies runtime targets. Dungeon populations are pre-populated, while Trial wave delivery remains distinct. [Current doctrine](../../../live-model/NORMAL_DUNGEONS.md) preserves whole-build capability, no rubber-banding, nine domains and the 68,910-credit White Normal completion base; final encounters and placement remain to be authored.

[Combat reward policy and tables](../../../combat-rewards/README.md) govern Checkpoint 17 payouts and Expedition attrition. `MANIFEST.json` records Hard R→W permissions and `hard_dungeon_areas_mi2`; the Normal area/reference and runtime data remain unchanged.
