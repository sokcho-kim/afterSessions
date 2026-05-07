# Android Offline APK Scaffold

이 폴더는 `정환님 취업형 AI EXPO 가이드`를 오프라인 WebView 앱으로 감싼 최소 안드로이드 프로젝트입니다.

## 현재 상태
- 로컬 HTML 자산을 `file:///android_asset/guide/index.html`로 로드
- 네트워크 없이도 열리는 오프라인 앱 구조
- Android Studio / SDK가 있으면 바로 빌드 가능한 형태

## 필요한 것
- Android Studio
- Android SDK Platform 34
- Gradle sync

## 빌드
1. Android Studio에서 `C:\Jimin\afterSessions\android` 열기
2. Sync 완료
3. `Build > Build APK(s)` 실행

## 자산 위치
- `app/src/main/assets/guide/`
  - `index.html`
  - `layout.webp`

현재 환경에는 Android SDK/Gradle이 없어서 여기서 직접 APK 빌드는 못 했습니다.
