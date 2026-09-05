# My Agent Kit

어느 컴퓨터에서든 Claude Code와 Codex에 설치해서 사용하는 개인 플러그인 저장소입니다.
공통 스킬은 한 번 작성하고, 도구별 매니페스트가 같은 파일을 참조합니다. 빌드나 심볼릭 링크가 필요하지 않습니다.

## 설치

이 변경 사항을 GitHub에 커밋·푸시한 뒤 각 컴퓨터에서 아래 명령을 실행합니다.
Git과 해당 도구가 필요하며, 비공개 저장소라면 그 컴퓨터에서 GitHub 저장소에 접근할 수 있어야 합니다.
마켓플레이스 이름은 `personal`, 플러그인 이름은 `my-agent-kit`입니다.
이미 다른 `personal` 마켓플레이스를 사용한다면 등록 전에 두 marketplace.json의 `name`을 같은 고유 이름으로 바꾸고 아래 `@personal`도 변경하세요.

### Claude Code

Claude Code 대화창에서:

```text
/plugin marketplace add woo-ming/my-agent-kit
/plugin install my-agent-kit@personal
```

설치 범위는 여러 프로젝트에서 쓸 수 있는 사용자 범위(user)를 선택합니다. 새 세션에서:

```text
/my-agent-kit:kit-help
/my-agent-kit:repo-overview
/my-agent-kit:review-changes
```

`/agents`에서 리뷰 에이전트가 로드되었는지 확인하고 `my-agent-kit:code-reviewer`에게 리뷰를 요청할 수 있습니다.

### Codex

터미널에서:

```sh
codex plugin marketplace add woo-ming/my-agent-kit
codex plugin add my-agent-kit@personal
```

새 세션에서 스킬 선택기의 `repo-overview` 또는 `review-changes`를 선택합니다.
예: `$repo-overview 이 프로젝트 구조와 실행 방법을 설명해줘`.
동명 스킬이 있다면 My Agent Kit에 속한 항목을 선택하세요. CLI의 `/plugins`에서 설치 상태를 확인합니다.
위 명령은 구성 시 설치된 Codex CLI의 `--help`로 확인했습니다.
`plugin` 명령이 없는 버전은 플러그인을 지원하는 버전으로 업데이트하세요.

## 제공 기능

| 기능 | 위치 | Claude Code | Codex |
| --- | --- | --- | --- |
| 저장소 구조·실행 방법 파악 | `skills/repo-overview/` | 스킬·슬래시 커맨드 | 스킬 |
| 변경 코드 리뷰 | `skills/review-changes/` | 스킬·슬래시 커맨드 | 스킬 |
| 사용법 안내 | `commands/kit-help.md` | 커맨드 | 미등록 |
| 리뷰 서브에이전트 | `agents/code-reviewer.md` | 네이티브 에이전트 | 미등록 |

Claude의 `agents/*.md`는 Codex 에이전트 설정으로 자동 변환되지 않습니다.
Codex에서도 같은 리뷰 절차를 쓰도록 공통 `review-changes` 스킬을 제공합니다.
Codex 전용 서브에이전트가 필요하면 해당 도구의 에이전트 설정을 별도로 추가해야 합니다.

## 구조

```text
.claude-plugin/marketplace.json       # Claude 카탈로그
.agents/plugins/marketplace.json      # Codex 카탈로그
plugins/
  my-agent-kit/
    .claude-plugin/plugin.json        # Claude 매니페스트
    .codex-plugin/plugin.json         # Codex 매니페스트
    skills/                          # 공유 원본
      repo-overview/SKILL.md
      review-changes/SKILL.md
    commands/kit-help.md              # Claude 커맨드
    agents/code-reviewer.md           # Claude 에이전트
scripts/validate.py
.github/workflows/validate.yml
```

설치 시 플러그인이 복사·캐시되므로 필요한 파일은 해당 플러그인 폴더 안에 둡니다.
컴퓨터별 절대 경로, 저장소 밖 상대 경로, 심볼릭 링크에 의존하지 마세요.

## 기능 추가

공통 기능은 `plugins/my-agent-kit/skills/<skill-name>/SKILL.md`로 추가합니다.
폴더명과 `name`은 같은 소문자 영문·숫자·하이픈 이름을 사용합니다.

```markdown
---
name: summarize-tests
description: Summarize test failures and likely causes when the user asks to analyze test output.
---

Read the supplied test output and relevant test files.
Separate confirmed causes from hypotheses and suggest the smallest useful next check.
Respond in the user's language.
```

참고 자료·스크립트는 해당 스킬의 `references/`, `scripts/`, `assets/`에 넣고 SKILL.md에서 참조합니다.
새 스킬은 매니페스트에 개별 등록할 필요가 없습니다.

Claude 전용 커맨드는 `commands/<name>.md`에 `description` 프런트매터와 지침을 작성합니다.
같은 이름의 스킬과 커맨드를 동시에 만들지 마세요.
Claude 에이전트는 `agents/<name>.md`에 `name`, `description`, 필요한 `tools`와 역할 지침을 작성합니다.
예제처럼 공통 스킬을 참조하면 작업 절차를 한 곳에서 관리할 수 있습니다.

별도 설치할 기능 묶음은 `plugins/<new-plugin>/`에 두 매니페스트와 스킬을 만들고 두 카탈로그에 추가합니다.
Claude의 `source`는 `./plugins/<new-plugin>`, Codex의 `source`는
`{"source":"local","path":"./plugins/<new-plugin>"}`입니다.
Codex 항목의 `policy`, `category`는 기존 항목을 참고하세요.

## 로컬 개발·검증

Python 3.10 이상에서:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
```

Windows는 `.venv/bin/python` 대신 `.venv\Scripts\python.exe`를 사용합니다.
두 카탈로그 일치, 경로, 버전, 스킬 메타데이터와 이름 충돌을 검사하며 GitHub Actions에서도 실행합니다.
이 검증이 도구의 실제 로딩·모델 동작을 대신 검증하지는 않습니다.

푸시 전 Claude에서 임시 로드하려면 저장소 루트에서:

```sh
claude --plugin-dir ./plugins/my-agent-kit
```

Codex에서 로컬 저장소로 설치하려면:

```sh
codex plugin marketplace add .
codex plugin add my-agent-kit@personal
```

같은 이름의 Git 마켓플레이스와 로컬 마켓플레이스를 동시에 등록하지 마세요.
새 세션에서 두 스킬을 실행하고 Claude에서는 커맨드와 `/agents`도 확인합니다.

## 업데이트

1. 내용을 수정하고 두 `plugin.json`의 `version`을 같은 `x.y.z` 버전으로 올립니다.
2. 검증 후 커밋·푸시합니다.
3. 각 컴퓨터에서 마켓플레이스와 설치본을 갱신합니다.

Claude Code 대화창:

```text
/plugin marketplace update personal
/plugin update my-agent-kit@personal
```

Codex 터미널(Git으로 등록한 경우):

```sh
codex plugin marketplace upgrade personal
codex plugin add my-agent-kit@personal
```

로컬 경로로 등록했다면 해당 clone에서 `git pull`한 뒤 플러그인을 다시 추가합니다.
업데이트 후 새 세션을 시작하세요. 푸시만으로 다른 컴퓨터의 설치본이 즉시 갱신되지는 않습니다.

## 참고

- [Claude Code 플러그인 규격](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code 마켓플레이스](https://code.claude.com/docs/en/plugin-marketplaces)
- [Codex 플러그인 제작](https://learn.chatgpt.com/docs/build-plugins)
- [Codex 플러그인 사용](https://learn.chatgpt.com/docs/plugins)

자격 증명과 개인별 설정은 각 컴퓨터에서 관리하고 이 저장소에 커밋하지 않습니다.
