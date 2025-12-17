[Mission]
Initialize the "afterSessions" repository as my personal tech conference/seminar note system.

[Goal]
- 이 레포를 컨퍼런스/세미나/강의 이후 정리용 표준 템플릿 레포로 초기 세팅한다.
- 최소한의 디렉터리 구조, 템플릿 파일, 기본 README 를 만들어서 바로 쓸 수 있게 해라.

[Context]
- 현재 열려 있는 프로젝트가 "afterSessions" 레포라고 가정해라.
- 나는 컨퍼런스/세미나를 다녀온 뒤:
  - raw/: 원본 스크랩(웹에서 긁은 소개/agenda, 현장 메모)
  - events/: 정리된 노트 (LLM + 내가 편집)
  - reports/: 사내 보고용, 블로그용 최종 아티클
  - templates/: LLM이 사용할 마크다운 템플릿
  - scripts/: CLI 스크립트
  - meta/: 네이밍 규칙, 태그 정의
  로 관리하고 싶다.

[Scope]
- 생성/수정 **허용** 경로:
  - README.md, SUMMARY.md
  - raw/, events/, reports/, templates/, scripts/, meta/
- 다음은 **절대 수정·삭제하지 말 것**:
  - .git/, .gitignore, .github/, .env, 기타 상위 디렉터리
- 신규 패키지 설치, git push, rm -rf 등 파괴적인 터미널 명령은 실행하지 말고, 필요하면 텍스트로만 제안해라.

[Deliverables]
아래 작업들을 Plan 모드에서 먼저 계획 보여준 뒤, 내가 승인하면 실행해라.

1) 디렉터리 구조 생성
- 최상위에 다음 디렉터리를 만든다:
  - raw/
  - events/
  - reports/
    - reports/company/
    - reports/blog/
  - templates/
  - scripts/
  - meta/
- 연도별 폴더 기본 골격:
  - events/2025/.gitkeep
  - raw/2025/.gitkeep

2) README.md 작성/수정
- 한국어 + 영어 간단 소개를 포함해라:
  - 한 줄 요약(ko): "테크 컨퍼런스·세미나·강의 이후 인사이트와 액션 아이템을 정리하는 레포지토리입니다."
  - One-line summary(en): "Notes & reflections after tech conferences, meetups, and courses."
- 포함할 섹션:
  - What is afterSessions
  - Folder structure (raw / events / reports / templates / scripts / meta 간단 설명)
  - Basic workflow
    - Step 1: raw/에 행사 소개/agenda/현장 메모 저장
    - Step 2: templates 기반으로 events/에 정리본 작성(LLM + 수동)
    - Step 3: 여러 이벤트를 묶어 reports/ 아래에 사내 보고서·블로그 초안 생성

3) SUMMARY.md 생성
- 전체 이벤트 인덱스를 적을 표 헤더만 만들어라 (내용은 나중에 채울 것).
- 예시 테이블 헤더:
  - Date | Title | Type | Organizer | Tags | Path

4) meta/conventions.md 생성
- 이 레포에서 사용할 **네이밍 규칙**을 명시해라:
  - 이벤트 폴더 이름: `YYYY-MM-DD_slug` (예: `2025-12-17_claude-code-meetup`)
  - events/ 구조:
    - events/YYYY/YYYY-MM-DD_slug/
      - meta.yaml
      - 01_overview.md
      - 02_session-notes.md
      - 03_reflection.md
      - 04_actions.md
  - raw/ 구조:
    - raw/YYYY/YYYY-MM-DD_slug/
      - agenda.txt
      - my_notes.md
      - etc/
- 각 파일 역할을 bullet로 짧게 설명해라.

5) meta/tags.yaml 생성
- YAML 형식으로 태그 예시와 카테고리 정의를 적어라.
- 예시 구조:
  - categories: [tech, domain, career, networking]
  - examples:
    - tech: [RAG, LLM, MLOps, infra]
    - domain: [healthcare, insurance, finance]
    - career: [leadership, communication]
    - networking: [community, meetup]
- 실제 값은 위 정도 예시로 채워라. 나중에 내가 수정할 것이다.

6) templates/event-notes-template.md 생성
- 하나의 행사에 대해 쓸 기본 마크다운 템플릿을 만들어라.
- 구조 예시:
  - Front-matter 형식(또는 맨 위 블럭)으로:
    - title:
    - date:
    - place:
    - organizer:
    - type: (conference | meetup | course | etc)
    - tags: []
    - url:
  - 섹션 헤더:
    - # 1. Overview
      - 왜 갔는지 / 기대했던 점 / 실제로 얻은 것 요약
    - # 2. Sessions
      - 세션별로 `## 세션명` + bullet 요약
    - # 3. Key Takeaways
      - 기술/도메인 인사이트 bullet
    - # 4. For My Work
      - 현재 내가 하는 프로젝트/업무와의 연결점
    - # 5. Action Items
      - Follow-up 할 일 TODO 체크리스트

7) templates/company-report-template.md 생성
- 분기별/월별 사내 공유용 요약 템플릿을 만들어라.
- 섹션 예:
  - Title, Period, 작성자
  - 1. 이번 기간에 참여한 행사 목록
  - 2. 주요 기술 인사이트
  - 3. 우리 팀/프로덕트에 주는 시사점
  - 4. 향후 액션 아이템

8) templates/blog-post-template.md 생성
- 블로그용 글 템플릿을 만들어라.
- 섹션 예:
  - Title, Date
  - Intro (왜 이 행사에 갔는지, 누구에게 도움이 되는 글인지)
  - 행사/강의 요약
  - 인사이트 & 배운 점
  - 현재/미래 프로젝트에 어떻게 적용할 것인지
  - 마무리(링크, 참고자료 등)

9) scripts/after_sessions_new.py 스켈레톤 생성
- 아직 완벽 구현 말고, 최소 스켈레톤만 작성해라.
- 요구사항:
  - Python 스크립트
  - argparse로 다음 인자 받기:
    - --date (YYYY-MM-DD)
    - --slug (예: claude-code-meetup)
    - --title (optional)
    - --tags (optional, comma-separated)
  - 실행 시:
    - raw/YYYY/YYYY-MM-DD_slug/ 와 events/YYYY/YYYY-MM-DD_slug/ 디렉터리 생성
    - events 쪽에 meta.yaml, 01~04 md 파일을 템플릿 내용으로 채워서 생성
    - raw 쪽에 agenda.txt, my_notes.md 빈 파일 생성
  - 실제 동작이 문제 없이 돌아가도록 코드 작성해라.
- 패키지는 표준 라이브러리만 사용해라.

[Safety]
- 반드시 Plan 모드로 먼저 전체 변경 사항 요약(어떤 파일을 만들고, 각 파일에 어떤 내용이 들어갈지)을 보여준 후, 내가 승인하면 실행해라.
- 터미널 명령은 디렉터리 생성 등 최소한만 사용하고, 파괴적인 명령(rm, mv -rf 등)은 절대 실행하지 마라.
- 기존 파일이 이미 있을 경우, 내용을 덮어쓰기 전에 항상 백업 파일(.bak) 생성 방안을 제안해라.
