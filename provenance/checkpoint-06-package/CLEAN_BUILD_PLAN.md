# MK157 CLEAN BUILD PLAN — CHECKPOINT 06

Target repository: `xApologies/MK157`
Target branch: `main`
Observed main tree SHA before this package: `dad02e4a456cd4b8e5337a5504c93eca70f6970b`

## Goal
Normalize the active repository into one clean current model through Checkpoint 06 while preserving historical provenance.

This is NOT a destructive rewrite of Git history. It is a repository-content cleanup:
- current/live files must agree with current canon;
- old checkpoint handoffs/manifests belong in provenance/archive space;
- provenance may preserve obsolete text, but active navigation must never present it as current;
- generated registries remain infrastructure, not character canon.

## Desired root structure

- `README.md` — current repository entry point only; concise.
- `live-model/` — current cumulative canon/navigation.
- `bindings/` — world-level Binding registry.
- `summons/` — world-level Summoned Entity registry.
- `builder/paths/` — Valnak Builder Path registry.
- `visual-references/` — assets plus explicit current/superseded status.
- `provenance/` — historical checkpoints, manifests, executables, audits, superseded source.
- `.gitignore`, `.gitattributes`.

## Root cleanup
Move historical root handoff artifacts into provenance rather than leaving multiple apparent executables at repository root:
- `EXECUTABLE.md`
- `EXECUTABLE_CHECKPOINT_01.md`
- `EXECUTABLE_CHECKPOINT_02.md`
- `EXECUTABLE_CHECKPOINT_03.md`
- `MANIFEST.json`
- `MANIFEST_CHECKPOINT_02.json`
- `MANIFEST_CHECKPOINT_03.json`
- `MANIFEST_CHECKPOINT_04.json`
- `FILE_INVENTORY.json`

Use a sensible `provenance/historical-root-handoffs/` directory, preserving filenames and bytes where possible. Do not delete historical evidence.

After cleanup, root should not contain stale executables that can be mistaken for the current handoff.

## Current authority
Set active authority everywhere to:
**Checkpoint 06 > 05 > 04 > 03 > 02 > 01** on explicit conflicts; otherwise cumulative.

## Kira biology normalization
The active repository currently still has a stale contradiction:
- `live-model/01_KIRA.md` still says matte-black skin, golden-energy hair, golden eyes.
- `live-model/05_VISUAL_CANON.md` still labels the old black/gold image current.
- newer Checkpoint 03 already supersedes that material.

Normalize active canon to:
- Kira genuinely enters Valnak Afflicted.
- Black interaction restructures/evolves her beyond the pathological Afflicted state.
- permanent biological skin = energized multilayered **WHITE** with extreme apparent Genesis depth;
- permanent biological hair = healthy/full **WHITE** hair;
- eyes = **BLACK** internal depth with Red→Violet spectral/rainbow striation;
- biological symmetry = effectively perfect;
- beauty = exotic/otherworldly but unmistakably human;
- ~5'11", lithe/dense athletic build;
- crystalline Genesis skeletal integration;
- crystalline-Genesis neural integration;
- Black/rainbow belongs principally to Black architecture/battle-state structures rather than permanent pigmentation.

Armor of the Abyss remains liquid/deep Black with buried R→V spectral structure. White biological hair can integrate/reconfigure into armor during manifestation.

## Enix-source firewall
The recovered Enix/Class-2 description is authorized only as biological morphology inspiration.
Do NOT import Enix identity, potion causality, Class-2 terminology/rank ladder, old tattoo ontology, or old setting mechanics.

## Visual cleanup
Keep binary files for provenance unless there is a compelling repository reason to relocate them.

Mark:
- `KIRA_GOLDEN_EYE_REFERENCE.png` — SUPERSEDED / provenance only.
- `KIRA_POST_VALNEK_CANON.png` — historical filename only; black/gold phenotype SUPERSEDED.
- `KIRA_AFFLICTED_REFERENCE.jpeg` — valid pre-transformation reference.
- `ARMOR_OF_THE_ABYSS_REFERENCE.jpeg` — valid working armor reference.
Update `visual-references/INDEX.md` and `live-model/05_VISUAL_CANON.md` so there is no ambiguity.

## Checkpoint 05 infrastructure remains current
Retain:
- `bindings/` — 1,014 Binding candidates.
- `summons/` — 220 Summoned Entity candidates.
- `builder/paths/` — 200 Path candidates.
Do not regenerate these in this cleanup unless validation discovers corruption.

## Canon locks to preserve
- six Transduction domains are primary Binding taxonomy;
- basin colors are structural energy identities only, never domain/element/power labels;
- Coherence/Decoherence foundational set is exactly six current Bindings;
- `maege` spelling;
- `domai` lowercase;
- Valnak spelling;
- Architect is mathematical/topological construction, not padded spell list;
- Summoned entities are non-sentient autonomous manifestations;
- generated Paths do not automatically define Kira or illi.

## Live-model normalization
Update active summary files where needed so a reader does not have to mentally resolve known contradictions:
- `live-model/00_GOVERNANCE.md` authority line if present;
- `live-model/01_KIRA.md` Kira biology and Armor/hair wording;
- `live-model/05_VISUAL_CANON.md`;
- `live-model/INDEX.md`;
- `live-model/SUPERSESSIONS.md`;
- root `README.md`.

Add `live-model/11_CHECKPOINT_06_KIRA_BIOLOGY_FIX.md` as the explicit change record, but make active summaries themselves correct too.

Do NOT flatten every old addendum into one giant file. Current summaries + authority chain + provenance are sufficient.

## README cleanup
Rewrite root README as a concise CURRENT navigation page. Do not keep the long quoted historical README chronology at root. Move historical README material to provenance if needed.

README should clearly say:
- current through Checkpoint 06;
- start with `live-model/INDEX.md`;
- infrastructure registries are `bindings/`, `summons/`, `builder/paths/`;
- provenance is historical and may contain superseded text.

## Validation
Before commit:
1. Parse `bindings/BINDINGS.json`; exactly 1,014 unique IDs/names.
2. Parse `summons/SUMMONED_ENTITIES.json`; exactly 220 unique IDs/names.
3. Parse `builder/paths/PATHS.json`; exactly 200 unique IDs/names.
4. Validate all Path Binding and summon references.
5. Confirm active authority says 06 > 05 > 04 > 03 > 02 > 01.
6. Search ACTIVE files (exclude provenance/prior-checkpoint-source) for stale Kira phenotype:
   - matte-black permanent skin,
   - golden-energy biological hair,
   - golden Eye-of-Mordor eyes,
   - old post-Valnak black/gold image labeled current.
   Any occurrence must either be removed or explicitly marked superseded/historical.
7. Confirm active Kira summary contains WHITE skin, WHITE hair, BLACK/R→V eyes, perfect symmetry.
8. Search active files for forbidden basin→domain mappings.
9. Confirm no root historical executable/manifests remain except files intentionally designated current by the cleanup.
10. `git diff --check`.

## Commit
Suggested:
`Checkpoint 06 clean build: normalize Kira canon and repository authority`

Push normally to `origin main`. Never force-push.
Report commit SHA, moved files, changed files, registry counts, and validation results.
