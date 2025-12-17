# afterSessions

> **테크 컨퍼런스·세미나·강의 이후 인사이트와 액션 아이템을 정리하는 레포지토리입니다.**
> *Notes & reflections after tech conferences, meetups, and courses.*

## What is afterSessions
개발자로서 참석한 다양한 컨퍼런스, 밋업, 세미나, 강의 등의 내용을 기록하고 내 것으로 만들기 위한 공간입니다. 단순히 정보를 나열하는 것을 넘어, **인사이트(Insights)**와 **액션 아이템(Action Items)**을 도출하여 실무와 커리어에 적용하는 것을 목표로 합니다.

## Folder Structure

- **`raw/`**: 행사 현장에서 수집한 원본 자료(스크랩, Agenda, 날 것의 메모 등)를 보관합니다.
- **`events/`**: `raw` 데이터를 바탕으로 정리된 구조화된 노트가 저장됩니다. (Overview, Session Notes, Reflections, Actions)
- **`reports/`**: 여러 이벤트를 종합하여 작성한 사내 공유 보고서(`company/`)나 블로그 포스팅 초안(`blog/`)이 저장됩니다.
- **`templates/`**: 노트 및 보고서 작성을 위한 마크다운 템플릿입니다.
- **`scripts/`**: 반복 작업을 자동화하기 위한 스크립트 모음입니다.
- **`meta/`**: 이 레포지토리의 규칙(Conventions)과 태그(Tags) 정의를 담고 있습니다.

## Basic Workflow

1. **Step 1: Preparation**  
   행사 참석 전후로 `scripts/after_sessions_new.py` 스크립트를 실행하여 기본 폴더와 템플릿을 생성합니다.
   ```bash
   python scripts/after_sessions_new.py --date 2025-12-17 --slug my-conference --tags tech
   ```

2. **Step 2: Collect (Raw)**  
   `raw/YYYY/Date_Slug/` 폴더에 발표자료, 사진, 빠르게 휘갈겨 쓴 메모 등을 저장합니다.

3. **Step 3: Organize (Events)**  
   `events/YYYY/Date_Slug/` 폴더의 템플릿 파일들을 채워넣으며 내용을 정리합니다. LLM을 활용해 요약하거나, 직접 회고를 작성합니다.

4. **Step 4: synthesize (Reports)**  
   필요한 경우 `reports/` 폴더에서 분기별 리포트나 블로그 글을 작성하여 지식을 2차 가공합니다.
