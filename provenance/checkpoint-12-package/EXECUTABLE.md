# EXECUTABLE.md — MK157 CHECKPOINT 12 COMPLETE PRICING PASS v2

## Invocation
Unpack this pouch into a temporary working directory.
Execute this document against the current default branch of:
xApologies/MK157

No additional prompt is required.

## 0. Safety / authority
Git is authoritative.
Start by reading:
- README.md
- THREAD_DEVELOPMENT_CONSTITUTION.md
- live-model/INDEX.md
- live-model/SUPERSESSIONS.md
- live-model/OPEN.md
- live-model/18_CHECKPOINT_11_ECONOMY_CARDS_HANDOFF.md
- live-model/ECONOMY_PURCHASE_SCHEDULE.md
- bindings/README.md
- bindings/CANON_LOCKS.md
- bindings/PRICING_MODEL.md
- bindings/BINDINGS.csv
- bindings/BINDINGS.json
- bindings/BINDINGS.jsonl
- summons/README.md
- summons/SUMMONED_ENTITIES.csv
- summons/SUMMONED_ENTITIES.json
- summons/SUMMONED_ENTITIES.jsonl
- summons/PRIME_ELEMENTAL_TAXONOMY.csv
- summons/PRIME_ELEMENTAL_RECIPES.md
- summons/ILLI_WHITE_LEGACY_GATES.json

Then read PRICING_POLICY.md from this pouch.

If repository authority is newer than Checkpoint 11, reconcile rather than overwrite newer canon.

## 1. Preserve before mutation
Record hashes/counts for all registry files.
The pass MUST preserve:
- 1,016 Binding IDs;
- 229 summoned entity IDs;
- PE-001..PE-009;
- six-domain taxonomy;
- basin firewall;
- recipes and illi overrides;
- White expressions;
- statuses/source lineage;
- Checkpoint 11 calendar/economy;
- Kira's 61,000 Black acquisition gates.

## 2. Reprice all Bindings
The existing registry contains numeric scaffolding created before an accepted deterministic pricing convention. Do not treat that scaffolding as governing canon.

Semantically classify all 1,016 Bindings using PRICING_POLICY.md.
Assign:
- pricing_class;
- canonical red_base_cost B;
- recomputed Red..White ladder;
- pricing_status = LOCKED — Checkpoint 12.

Apply hand-locked anchors exactly.

Use meaningful 50/100-credit increments and avoid ID-sequence pricing.

## 3. Price all summoned-entity Bindings
Semantically classify all 229 SUMMONED_ENTITIES records.
Create:
- summons/SUMMON_PRICING.csv
- summons/SUMMON_PRICING.json
- summons/SUMMON_PRICING.jsonl

Each must contain the full 229-record price atlas keyed by entity_id.

Ordinary summons MUST be below 10,000 Red.
Use scale/control/load/persistence/role to distinguish prices.
Do not infer price from element name or basin colors.

## 4. Prime Elemental lock
Create:
- summons/PRIME_ELEMENTAL_PRICING.csv
- summons/PRIME_ELEMENTAL_PRICING.json

PE-001..PE-009 all have:
B = 10,000.

Derived ladder exactly:
R 10000
O 16000
Y 28800
G 60480
B 151200
V 453600
W 1814400
cumulative 2534480

Do not introduce 25k/30k Prime prices.
Do not vary Prime Red price by Prime type.

## 5. Pricing documentation
Update bindings/PRICING_MODEL.md to establish:
- five ordinary Red acquisition bands;
- semantic pricing doctrine;
- deterministic rounding;
- Prime 10,000 lock;
- ordinary summons <10,000;
- basin firewall;
- Kira firewall.

Update bindings/README.md and summons/README.md only as needed for discoverability.

## 6. Audit
Create/update:
- bindings/PRICING_AUDIT.json
- summons/PRICING_AUDIT.json

Audit must include:
- total record counts;
- counts by pricing class;
- min/median/max B;
- counts by domain/entity type;
- anchor checks;
- Prime checks;
- arithmetic checks;
- null-price count;
- mirror equality;
- preserved ID/recipe/basin/status checks.

Flag suspicious distributions for review. Do not silently repair unrelated canon.

## 7. Live-model integration
Create the next numbered checkpoint addendum for the pricing pass.
Integrate minimally into:
- live-model/INDEX.md
- live-model/SUPERSESSIONS.md
- live-model/OPEN.md
- live-model/ECONOMY_PURCHASE_SCHEDULE.md where relevant
- README.md
- THREAD_DEVELOPMENT_CONSTITUTION.md if the pricing grammar belongs there

Do NOT duplicate the complete 1,245-row ordinary registry into narrative live-model prose.
Row-level prices live in registries.

Supersede prior statements that pricing convention/base prices are OPEN only where this pass actually resolves them.
Do not resolve unrelated OPEN items.

## 8. Provenance
Create a Checkpoint 12 provenance package/coverage manifest/audit consistent with existing repository practice.
Preserve the exact input pouch or equivalent executable/policy evidence in provenance.

## 9. Final validation and commit
Before commit verify:
- 1,016/1,016 Bindings priced;
- 229/229 summoned entities priced;
- 9/9 Prime Elementals at exactly 10,000;
- ordinary summons all <10,000;
- PT-0002=600;
- PT-0003=700;
- PT-0001=1800;
- GE-0537=3000;
- GE-0043=5000;
- all rank ladders mathematically valid;
- Kira's four post-Armor Black gates remain 61,000;
- no basin/color pricing inference;
- no lost registry records.

Commit the completed integration.

Final Codex report must include:
commit hash;
files changed;
class distributions;
Binding/summon/Prime counts;
min/median/max Red prices;
anchor verification;
Prime verification;
audit result.
