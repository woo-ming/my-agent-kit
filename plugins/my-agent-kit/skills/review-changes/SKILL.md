---
name: review-changes
description: Review a diff or local code changes for actionable bugs, regressions, and missing behavioral coverage when the user requests code review.
---

Use the comparison the user specifies. Otherwise inspect staged and unstaged tracked changes and list relevant untracked files; do not silently choose a base branch.
Read affected callers and tests where needed to verify an issue.
Prioritize reproducible correctness problems over style preferences.

For each finding, explain severity, file and line, triggering conditions, impact, and a concrete fix direction.
Avoid reporting speculative bugs as established facts. If there are no actionable findings, say so and identify material verification gaps.
Review only; change files when the user also requests fixes. Respond in the user's language.
