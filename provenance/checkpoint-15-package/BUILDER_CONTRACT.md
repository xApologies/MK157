# ELDRIS ATOMIC GROUP BUILDER CONTRACT

## Purpose
This registry defines reusable *atomic eldRIS groups*. It does NOT define full encounters, map placement, dungeon populations, spawn schedules, or prose scenes.

Hierarchy:
individual eldRIS -> atomic group -> encounter composition -> dungeon/domai/trial population.

## Hard constraints
1. Atomic population is 1–4 bodies. Never exceed four inside one atomic-group record.
2. Group IDs are assigned by the highest Genesis basin represented:
   R###, O###, Y###, G###, B###, V###.
3. A higher-rank encounter builder may use any atomic group at or below its legal ceiling.
4. No group may contain an eldRIS above its ID ceiling.
5. There is no White eldRIS. White encounter builders use the complete R→V atomic library.
6. Basin color is ontological Genesis-field identity, not an arbitrary game difficulty tag.
7. Combat-family partition:
   melee = Red / Orange / Green
   Transductionist = Yellow / Blue / Violet
8. Canonical expressions:
   Red physical; Orange intrusion; Yellow ranged force;
   Green juggernaut/persistence threshold; Blue expressed projection;
   Violet high Genesis expression.
9. Do not invent aggro/threat mechanics, MMO roles, health-bar inflation, or illegal higher-rank eldRIS.
10. The builder may duplicate atomic groups and combine many groups to create large populations.

## Why the registry is exhaustive-but-small
For each ceiling, the library enumerates every unordered basin multiset of population 1–4 whose highest represented basin equals that tier.
This avoids redundant copies: e.g. a pure Red group remains R### and is still legal in Orange through White content.
A Blue encounter can therefore combine R###, O###, Y###, G###, and B### groups.

## Example
A larger encounter requiring ~30 bodies might be composed from:
2× R004 + 2× O006 + Y012 + G018 + B021
subject to the actual row populations.
The encounter builder controls placement, timing, terrain relation, and larger tactical structure.

## Environment independence
Atomic groups are not tied to Deep Caverns, Dune Wastes, Oldgrowth, Overgrown City, Highlands, Marshlands, Frozen Expanse, Broken Coast, or Ruined Citadel.
The same legal group can be placed into different procedural domain realizations.

## Area context
Normal Dungeon average realized areas currently locked author-side:
Red 5 mi²; Orange 13; Yellow 25; Green 53; Blue 113; Violet 285; White 450.
Area is total realized environment, not required traversal distance.
Larger maps permit more atomic groups and wider separation; they do not require larger atomic groups.
