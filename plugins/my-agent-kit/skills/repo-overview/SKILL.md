---
name: repo-overview
description: Map an unfamiliar repository's architecture, entry points, and development commands when the user asks for onboarding or a repository overview.
---

Read the repository's agent instructions and README, then inspect manifests and a focused file listing.
Trace the main entry points far enough to explain how the core components connect.
Report in the user's language:

- The project's purpose and important directories, with file references.
- Setup, run, and test commands supported by repository evidence.
- The likely files to change for the user's stated task, if any.
- Missing setup information or assumptions that still need verification.

Distinguish documented commands from commands you actually ran. Do not install dependencies or modify the repository just to produce an overview.
