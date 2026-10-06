# 01 — Targeted recrawl findings

## Observed source

Repository: `xApologies/MK157`.
Branch: `main`.
Commit: `3a7a62407bf0f950f7b6469e5c67e2d6a3e80e31`.
Git tree: `d2e80f13b3ea6a3e7a41754acb7897c9b479f29d`.
Commit subject: `Checkpoint 25: correct Arc Seven calendar and White core economy`.
Commit timestamp: `2026-10-06T21:48:57Z`.

The branch and non-recursive root tree were read directly through the GitHub connector. A recursive tree was requested but its returned presentation was truncated. Selected authoritative file ranges were then read directly at the pinned commit. A programmatic clone was attempted, but the container could not resolve github.com. Therefore no full working-tree file census, whole-repo duplicate measurement, or actual repository validator run is claimed here. The complete local census and baseline tests are required execution steps for Codex.

## Verified root layout

Four root files: `.gitattributes`, `.gitignore`, `README.md`, `THREAD_DEVELOPMENT_CONSTITUTION.md`.

Eleven root directories: `bindings`, `builder`, `combat-rewards`, `economy`, `live-model`, `prior-checkpoint-source`, `provenance`, `summons`, `trial-rewards`, `visual-references`, `world-clock`.

There is no root `canon/`, `story/`, `data/`, `tools/`, `upstream/`, `AGENTS.md` or `CANON_STATUS.md` at this observed tree. Recheck collisions at execution time.

## Findings and consequences

### F01 — Recovery chronology occupies the front door

The root README is 14,987 Git bytes and walks through Checkpoints 07–25 after its initial links. The live-model index similarly mixes current domain references with historical addenda, old calendars and integration evidence. This structure preserves history well but imposes unnecessary reconstruction work during scene and chapter development.

**Action:** concise root navigation plus current topics and arc workspaces. Keep a linked historical index and the original sources. Do not delete history to simplify reading.

### F02 — A confirmed stale current-navigation label

`live-model/INDEX.md`, source lines 81–83, describes Trial rewards as “exact W1–35 rows; W36+ OPEN.” The current Arc Seven validator explicitly checks `extension_starts=36`, `credits_per_completed_wave=1600`, W96=124,555 and W100=130,955.

**Action:** fix the active label and route to the extension table/current rule. Do not rewrite older checkpoint packages that accurately record the earlier OPEN state.

### F03 — Existing addresses are validator dependencies

`world-clock/validate_arc7.py` reads named `provenance/`, `world-clock/`, `trial-rewards/`, `combat-rewards/`, `bindings/`, `summons/` and `live-model/` paths. It verifies byte-identical source-package membership and manifests, CSV/JSON mirrors, protected baseline hashes, and older files through `git show` at a fixed historical commit.

**Action:** no physical bulk moves, no regenerated manifests, no hash refresh to conceal changes. The safe first cleanup is an authoring facade over existing addresses.

### F04 — Some apparently duplicate files are deliberate proof surfaces

The Arc Seven validator requires its calendar Markdown/CSV to match the correction package and its CSV/JSON data to match structurally. Other historical copies serve as provenance. Filename similarity or equal contents does not establish that a file can be deleted.

**Action:** retain mirrors and originals. The new data index declares their owner and purpose. Codex may measure duplicate bytes for the report, but this pass authorizes no deduplication deletion.

### F05 — Source boundaries already contain narrow later promotions

`live-model/SOURCE_BOUNDARIES.md` initially prohibits inheriting the old schedule PDFs' 31-hour day, then explicitly records the later Checkpoint 10 promotion of 31-hour days and applicable calendar infrastructure. It separately excludes old plots, character identities and Binding-circle causality.

**Action:** reconcile by subject and later explicit authority. Never use an automated “first matching paragraph wins” extraction or flatten all older restrictions into current law.

### F06 — Macro closure is not universal detail closure

The current Arc Seven validator explicitly protects null values for detailed training/purchase dates, support Binding names/counts, final discretionary balances and other unsupplied details. It prohibits an invented Trio and invented Blue/Violet clears.

**Action:** distinguish author-closed macro arcs from local OPEN questions and unwritten chapters. Cleanup is not a creative decision pass.

### F07 — Historical spelling remains in an established filename

The index references `live-model/03_VALNEK_PATHS.md`; the current constitution and source firewall specify Valnak for visible canon.

**Action:** normalize newly written display labels, not immutable filenames or archived bytes. Link to the existing address.

## Recommendation

Perform one non-destructive authoring-surface normalization. Build substantive current pages and seven arc workspaces, shorten navigation, add explicit ownership/coverage and make tests reproducible. Defer physical storage reorganization unless separately authorized with a path/hash migration plan.
