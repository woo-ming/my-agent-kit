# 개발 환경

개인 개발 환경과 사용하는 도구를 기록한다. 새 컴퓨터에서 환경을 구성하거나 기존 설정을 확인할 때 참고한다.

- 기록일: 2026-09-05
- 도구 목록 갱신일: 2026-09-08
- 기본 환경: Apple Silicon Mac, macOS, zsh
- 저장소: [my-agent-kit](https://github.com/woo-ming/my-agent-kit)
- 재사용 스킬·커맨드·에이전트 설치 방법: [README](README.md)

아래 도구 목록은 사용하는 환경으로 지정한 항목과 이 저장소 작업 중 설정한 항목을 기준으로 한다. 모든 프로그램의 설치·로그인 상태를 검사한 목록은 아니다. 직접 확인한 버전은 별도 표에 기록한다.

## 프로그래밍 언어·런타임·버전 관리

| 도구 | 설명 | 용도 |
| --- | --- | --- |
| [Amazon Corretto 25](https://docs.aws.amazon.com/corretto/latest/corretto-25-ug/what-is-corretto-25.html) | Amazon에서 제공하는 OpenJDK 25 기반 Java 개발·실행 환경(JDK). | Java 애플리케이션 컴파일, 실행 및 IDE의 프로젝트 SDK로 사용. |
| [Kotlin](https://kotlinlang.org/) | JetBrains에서 개발한 정적 타입 프로그래밍 언어. JVM에서 실행할 수 있고 Java 코드와 상호 운용할 수 있다. | IntelliJ IDEA에서 Kotlin 애플리케이션 개발. Kotlin 버전과 JVM 대상 버전은 각 프로젝트의 빌드 설정을 따른다. |
| [nvm](https://github.com/nvm-sh/nvm) | Node.js 버전을 설치하고 프로젝트에 맞춰 전환하는 셸 기반 버전 관리자. | 프로젝트별 Node.js 버전 관리. `.nvmrc`가 있으면 `nvm use`로 해당 버전 선택. |
| [jenv](https://www.jenv.be/) | 이미 설치된 JDK를 등록하고 사용할 Java 버전을 전역·프로젝트·셸 단위로 전환하는 버전 관리자. | Corretto 등 여러 JDK를 관리하고 프로젝트별 Java 버전 선택. JDK 설치는 별도로 진행한다. |

Corretto 25는 사용하는 JDK 기준이다. 현재 터미널의 기본 Java와 IntelliJ의 프로젝트 SDK·빌드 도구 JVM이 모두 같은 버전인지는 별도로 확인한다. Node.js 기본 버전은 이 문서에서 고정하지 않으며 프로젝트 요구 사항을 따른다.

## IDE·데이터베이스

| 도구 | 설명 | 용도 |
| --- | --- | --- |
| [IntelliJ IDEA](https://www.jetbrains.com/idea/) | JetBrains의 Java·Kotlin 중심 통합 개발 환경. 코드 분석, 리팩터링, 실행 및 디버깅 기능을 제공한다. | 애플리케이션 개발, 테스트, 디버깅. |
| [DataGrip](https://www.jetbrains.com/datagrip/) | JetBrains의 데이터베이스 IDE. 데이터베이스 연결, SQL 작성, 스키마 탐색과 데이터 조회를 지원한다. | SQL 실행, 데이터 확인 및 데이터베이스 구조 관리. |

## AI·코딩 에이전트

| 도구 | 설명 | 용도 |
| --- | --- | --- |
| [ChatGPT](https://chatgpt.com/) | 대화형 AI 서비스. 질문 답변, 문서 작성, 아이디어 정리와 코드 설명 등에 활용한다. | 개발 관련 질의응답, 설계 검토와 문서 작업. |
| [Codex](https://learn.chatgpt.com/docs/build-plugins) | OpenAI의 코딩 에이전트. 저장소를 읽고 코드 수정, 명령 실행과 검증 등의 개발 작업을 수행한다. | 코드 구현·리뷰·자동화와 이 저장소의 공통 스킬 활용. |
| [Claude Code](https://code.claude.com/docs/en/overview) | Anthropic의 코딩 에이전트. 터미널 등에서 코드베이스를 탐색하고 수정·검증 작업을 수행한다. | 개발 작업과 이 저장소의 스킬·커맨드·서브에이전트 활용. |
| [Orca](https://www.onorca.dev/) | 여러 코딩 에이전트를 Git worktree별로 실행하고 터미널, 변경 diff, 브라우저를 함께 다루는 에이전트 개발 환경. | Claude Code·Codex의 작업 공간과 여러 개발 작업 관리. |

여기서 Orca는 Stably AI의 제품(`com.stablyai.orca`)이다. Docker·Linux 실행 환경인 OrbStack과는 별도 도구다.

### 이 저장소의 에이전트 확장

| 구성 요소 | 역할 | 지원 도구 |
| --- | --- | --- |
| `repo-overview` | 저장소 구조, 주요 진입점과 실행·테스트 방법 파악. | Claude Code, Codex |
| `review-changes` | 변경 코드의 버그·회귀 가능성 검토. | Claude Code, Codex |
| `kit-help` | 플러그인 사용법 안내 커맨드. | Claude Code |
| `code-reviewer` | 공통 리뷰 절차를 따르는 서브에이전트. | Claude Code |

플러그인 원본은 `plugins/my-agent-kit/`에 둔다. 각 컴퓨터의 설치본은 저장소를 푸시하는 것만으로 즉시 갱신되지 않으므로 README의 업데이트 절차를 따른다.

## 패키지·의존성·컨테이너 관리

| 도구 | 설명 | 용도 |
| --- | --- | --- |
| [Homebrew](https://brew.sh/) | macOS에서 CLI 패키지와 GUI 애플리케이션을 설치·업데이트하는 패키지 관리자. | 개발 도구 설치 및 버전 확인. 현재 환경의 기본 경로는 `/opt/homebrew`. |
| [Yarn](https://yarnpkg.com/) | JavaScript·Node.js 프로젝트의 패키지 및 의존성을 관리하는 도구. 워크스페이스를 통한 여러 패키지 관리도 지원한다. | 프로젝트 의존성 설치와 스크립트 실행. Yarn 버전과 설정은 각 프로젝트의 기준을 따른다. |
| [OrbStack](https://orbstack.dev/) | macOS에서 Docker 컨테이너와 Linux 머신을 실행·관리하는 도구. | 로컬 컨테이너, 개발용 서비스 및 Linux 환경 실행. |

## Kubernetes 관리

| 도구 | 설명 | 용도 |
| --- | --- | --- |
| [k9s](https://k9scli.io/) | 터미널 UI로 Kubernetes 클러스터의 리소스를 탐색하고 관리하는 도구. 리소스 상태와 변경 사항을 실시간으로 확인할 수 있다. | Pod·Deployment 등 리소스 조회, 컨테이너 로그 확인 및 포트 포워딩을 통한 개발·디버깅. |
| [OpenLens](https://github.com/MuhammedKalkan/OpenLens) | Lens의 오픈 소스 부분을 기반으로 한 Kubernetes 관리용 데스크톱 GUI. | Kubernetes 클러스터와 워크로드 상태를 시각적으로 확인하고 리소스 탐색·관리. |

## 브라우저·지식 관리

| 도구 | 설명 | 용도 |
| --- | --- | --- |
| [Google Chrome](https://www.google.com/chrome/) | Google의 웹 브라우저. 개발자 도구로 DOM, 콘솔, 네트워크 요청 등을 확인할 수 있다. | 웹 서비스 사용, 화면 확인과 웹 디버깅. |
| [Obsidian](https://obsidian.md/) | 로컬 Markdown 파일을 중심으로 노트를 작성하고 연결하는 지식 관리 앱. | 개발 메모, 학습 내용과 개인 지식 정리. |

## 셸·터미널 생산성

### 기본 셸

| 도구 | 설명 | 현재 구성 |
| --- | --- | --- |
| [zsh](https://www.zsh.org/) | 명령 실행, 자동 완성, 히스토리와 스크립팅을 제공하는 셸. 터미널 앱 안에서 실행된다. | 사용자 초기화 설정은 `~/.zshrc`에서 관리. |
| [Oh My Zsh](https://ohmyz.sh/) | zsh의 플러그인, 테마와 설정을 관리하는 프레임워크. | 설치 경로는 `~/.oh-my-zsh`. 내장 플러그인 `git`, `copypath` 활성화. |

### 플러그인·연동 도구

fzf와 zoxide는 독립 CLI 도구이며 zsh 초기화 설정으로 연동한다. 아래 외부 플러그인과 CLI 도구는 Homebrew로 설치했다.

| 도구 | 구분 | 설명·사용법 |
| --- | --- | --- |
| [git](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/git) | Oh My Zsh 내장 플러그인 | Git 명령의 단축 별칭 등을 제공한다. Git 자체를 설치하는 플러그인은 아니다. |
| [copypath](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/copypath) | Oh My Zsh 내장 플러그인 | `copypath`로 현재 폴더의 절대 경로를 복사한다. `copypath README.md`처럼 파일 경로도 복사할 수 있다. |
| [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) | 외부 zsh 플러그인 | 명령 입력 중 히스토리 기반 제안을 표시한다. 기본 설정에서는 커서가 줄 끝에 있을 때 오른쪽 방향키로 제안을 받아들인다. |
| [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) | 외부 zsh 플러그인 | 명령, 인자와 잘못된 명령 등을 색상으로 구분한다. 다른 플러그인·위젯 설정 뒤에 로드한다. |
| [fzf](https://github.com/junegunn/fzf) | 검색 CLI + zsh 연동 | `Ctrl+R`로 명령 기록 검색, `Ctrl+T`로 파일·디렉터리 경로 선택 및 삽입. 검색창에서는 `Enter`로 선택하고 `Esc`로 취소한다. |
| [zoxide](https://github.com/ajeetdsouza/zoxide) | 디렉터리 이동 CLI + zsh 연동 | 방문한 디렉터리를 기억한다. `z 이름일부`로 이동하고 `zi`로 fzf 기반 선택 목록을 연다. 처음에는 디렉터리 방문 기록이 필요하다. |

### 현재 `~/.zshrc` 관련 설정

전체 `.zshrc` 복사본이 아닌 개발 도구 관련 설정 발췌다. 기존 설정에 이미 있는 항목을 중복 추가하지 않는다.

```zsh
# Oh My Zsh: plugins 설정은 oh-my-zsh.sh를 불러오기 전에 둔다.
export ZSH="$HOME/.oh-my-zsh"
plugins=(git copypath)
source "$ZSH/oh-my-zsh.sh"

# nvm (Apple Silicon Mac / Homebrew)
export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"
[ -s "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm"

# fzf / zoxide: Oh My Zsh가 자동 완성을 초기화한 뒤 로드한다.
source <(fzf --zsh)
eval "$(zoxide init zsh)"

# 자동 제안
source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh

# 문법 강조: 다른 플러그인과 위젯 설정 뒤에 둔다.
source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
```

설정 변경 후 새 터미널을 열거나 `source ~/.zshrc`로 반영한다. `/opt/homebrew`는 현재 Mac의 경로이며 다른 운영체제나 Homebrew 설치 경로에서는 조정해야 한다.

### 자주 쓰는 명령

```sh
# 명령 기록 검색: Ctrl+R → 검색어 입력 → Enter
# 파일 경로 삽입: Ctrl+T → 검색어 입력 → Enter

# 처음에는 일반 cd로 프로젝트 방문
cd ~/workspace/wooming/my-agent-kit
cd ~
z my-agent          # 기억한 프로젝트로 이동
zi                 # 방문한 디렉터리 중 검색해서 선택

copypath           # 현재 폴더 경로 복사
copypath README.md # 파일의 전체 경로 복사

nvm ls             # 설치된 Node.js 버전 확인
nvm use            # 현재 프로젝트의 .nvmrc 버전 사용
node --version
java -version
brew list --versions
```

## 확인한 환경·버전

기록일에 로컬에서 확인한 값이다. 업그레이드 후에는 달라질 수 있으며, 다른 컴퓨터에 강제할 고정 버전 목록은 아니다.

| 항목 | 확인 값 |
| --- | --- |
| macOS | `26.5.1` |
| 아키텍처 | `arm64` (Apple Silicon) |
| Orca | `1.4.197` |
| nvm | `0.40.7` (Homebrew 패키지) |
| fzf | `0.74.3` |
| zoxide | `0.10.0` |
| zsh-autosuggestions | `0.7.1` |
| zsh-syntax-highlighting | `0.8.0` |

그 밖의 프로그램의 세부 버전, IntelliJ 에디션, 활성 Node.js 버전과 기본 Java 경로는 이 기록에서 확인하지 않았다. 계정, 라이선스, API 키, 데이터베이스 접속 정보는 각 컴퓨터에서 관리한다.
