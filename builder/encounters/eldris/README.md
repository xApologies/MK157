# eldris atomic group library — Checkpoint 15

Author/builder tooling for composing encounters. The IDs are author handles, not in-world Valnak IDs. Each record contains 1–4 bodies and describes basin composition independently of species, Dungeon domain, map, placement or spawn schedule. Larger populations combine or duplicate groups.

| Highest basin | Groups | Cumulative legal groups |
|---|---:|---:|
| Red | 4 | 4 |
| Orange | 10 | 14 |
| Yellow | 20 | 34 |
| Green | 35 | 69 |
| Blue | 56 | 125 |
| Violet | 84 | 209 |
| White content, where permitted | 0 | 209 |

The 209 groups exhaust every unordered multiset of 1–4 members drawn from R→V. The highest represented basin determines the unique ID tier. There are no White eldris. Basin identity is ontological; capability follows architecture. Melee-family R/O/G and Transductionist-family Y/B/V are composition metadata, not new classes or game statistics.

- [CSV registry](ELDRIS_ATOMIC_GROUPS.csv) and [JSON mirror](ELDRIS_ATOMIC_GROUPS.json): exact supplied records.
- [Tier availability](TIER_AVAILABILITY.json): exact supplied cumulative ID lists.
- [Basin reference](BASIN_REFERENCE.csv): taxonomy and areas, with explicit Dungeon enablement and area scope.
- [Builder contract](BUILDER_CONTRACT.md): legal composition, examples and authoring boundaries.
- [Manifest](MANIFEST.json), [independent audit](AUDIT.json), and [validator](validate_library.py).

Current [combat ecology](../../../live-model/COMBAT_ECOLOGY.md) allows Dungeon ranks R→V, not White. The W availability list serves only content whose existing rules permit White tiers. The full supplied R5/O13/Y25/G53/B113/V285/W450 mi² author ladder is retained; W450 is reference-only and does not change the fixed 9-mi² Trial arena. Exact Hard Dungeon areas remain OPEN. No completed encounters or map placements are defined here.

Reproduce the library audit from this directory with `python validate_library.py`. Add `--output AUDIT.json` to save the report. [Checkpoint 15](../../../live-model/22_CHECKPOINT_15_ELDRIS_ATOMIC_GROUP_LIBRARY.md) and [conflict decisions](../../../provenance/CHECKPOINT_15_CONFLICTS.md) record the integration. Original package files are preserved byte-for-byte in [provenance](../../../provenance/checkpoint-15-package/README.md).
