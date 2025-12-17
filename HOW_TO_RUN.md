# afterSessions 실행 가이드

이 프로젝트는 컨퍼런스, 세미나, 강의 등에서 얻은 지식을 체계적으로 기록하고 관리하기 위한 도구입니다. 아래 순서에 따라 사용하세요.

## 0. 사전 준비 (Prerequisites)
- **Python 3.x**가 설치되어 있어야 합니다.
- 별도의 외부 라이브러리 설치는 필요하지 않습니다 (표준 라이브러리만 사용).

## 1. 새로운 이벤트 생성 (Preparation)
행사 내용을 URL로 자동 수집하거나, 수동으로 생성할 수 있습니다.

### 방법 A: URL 스크래핑 (추천)
Playwright를 통해 브라우저로 접속하여 내용과 스크린샷을 수집합니다.

```bash
# 기본 사용법
python scripts/scrape_event.py --url [행사URL] --date YYYY-MM-DD --slug [행사명_슬러그]

# 예시
python scripts/scrape_event.py --url "https://example.com" --date 2025-12-17 --slug tech-news
```
**실행 결과:**
- `raw` 폴더에 `screenshot.png`, `content.txt`, `original.html` 등이 생성됩니다.

### 방법 B: 수동 생성
스크래핑 없이 빈 폴더만 생성합니다.

```bash
# 기본 사용법
python scripts/after_sessions_new.py --date YYYY-MM-DD --slug [행사명_슬러그]

# 예시 (제목과 태그 포함)
python scripts/after_sessions_new.py --date 2025-12-17 --slug claude-meetup --title "Claude Code Meetup" --tags tech,ai
```

**실행 결과:**
- `raw/2025/2025-12-17_claude-meetup/` 생성 (빈 노트, Agenda 파일)
- `events/2025/2025-12-17_claude-meetup/` 생성 (템플릿 파일들)

## 2. 자료 수집 (Raw Data)
생성된 `raw/` 폴더에 행사 자료를 모읍니다.
- **`raw/.../agenda.txt`**: 행사 일정표나 세션 목차를 붙여넣으세요.
- **`raw/.../my_notes.md`**: 현장에서 빠르게 작성한 메모를 적으세요.
- **`raw/.../sources/`**: (선택) 세션별 스크립트나 상세 텍스트 파일이 있다면 여기에 `.txt` 파일로 저장하세요.
- **`raw/.../links.md`**: (선택) 관련 링크나 참고 자료 URL을 적으세요.

## 3. 내용 정리 및 요약 (Summarize)
수집한 `raw` 데이터를 바탕으로 `events` 폴더의 정리된 노트로 변환/병합합니다.

```bash
# 요약 스크립트 실행
python scripts/after_sessions_summarize.py --date YYYY-MM-DD --slug [행사명_슬러그]

# 예시
python scripts/after_sessions_summarize.py --date 2025-12-17 --slug claude-meetup
```

**실행 결과:**
- `events/.../01_overview.md`: Agenda와 내 메모가 합쳐집니다.
- `events/.../02_session-notes.md`: `sources/` 폴더의 내용이 병합됩니다.
- `events/.../03_reflection.md`: 링크 자료가 추가됩니다.

> **참고**: 이미 파일이 존재하고 Raw 데이터가 변경되지 않았다면 스킵됩니다. 강제로 다시 덮어쓰려면 `--force` 옵션을 붙이세요.

## 4. 최종 편집 (Finalize)
`events/` 폴더의 마크다운 파일들을 열어 최종적으로 내용을 다듬습니다.
- **`03_reflection.md`**: 이번 행사에서 느낀 점과 회고를 작성합니다.
- **`04_actions.md`**: 실무에 적용할 액션 아이템을 체크리스트로 관리합니다.

## (Optional) 리포트 작성
여러 행사의 내용을 모아 사내 공유용이나 블로그용 글을 쓸 때는 `reports/` 폴더를 활용하세요.
- `templates/` 폴더의 `company-report-template.md` 등을 복사해서 사용하면 편리합니다.
