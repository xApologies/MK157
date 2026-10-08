# EXECUTABLE — MK157 R2/R3 cumulative reverse-diff pouch

Target: xApologies/MK157

Completion means: INTEGRATE -> REVERSE-DIFF -> VALIDATE -> STAGE -> COMMIT -> PUSH -> VERIFY REMOTE.
Do not stop with uncommitted/unpublished changes.

Read current Git authority first, especially THREAD_DEVELOPMENT_CONSTITUTION.md, story/ARC_02/ARC.md,
live-model/{WORLD_CLOCK,STORY_CLOCK_STATE,03_VALNEK_PATHS,04_COMBAT_WORLD,VALNAK_CITY_CULTURE_TRANSPORT,RAEON,PRISM}.md,
builder/COMMUNITY.md, combat-rewards/README.md, and world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.csv.

Integrate this pouch as a delta. Preserve newer authority and LOCKED/WORKING/OPEN distinctions.
Do not move existing mandatory combat or Binding-purchase dates.

MANDATORY REVERSE DIFF:
After editing, compare every decision in REVERSE_DIFF.csv against the resulting repository.
Mark PRESENT/PARTIAL/MISSING/CONFLICT/SUPERSEDED. Resolve all unintended gaps before commit.
In particular search globally for governing 25:00 Highlight references and supersede them with 27:00.

Run applicable repository validators. Then stage intended changes, commit, push current branch to configured
GitHub remote, and verify remote contains the commit and git status is clean/synchronized.

Final report: commit SHA, branch, remote, files changed, reverse-diff counts, validation results, final git status.
