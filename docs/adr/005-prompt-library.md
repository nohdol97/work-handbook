# ADR 005: Markdown 기반 실무 프롬프트 모음과 언어 탭

- 상태: accepted
- 날짜: 2026-09-24

## 맥락

사용자가 긴 한 줄 prompt의 가독성 개선과 많은 실무 예시, 한영 전환을 요청했다. 기존 기술 문서에 모든 사례를 늘어놓으면 개념 학습과 예시 탐색이 모두 어려워진다.

## 결정

`docs/ko/prompts`와 `docs/en/prompts`에 주제별 파생 예시를 Markdown 원본으로 저장한다. 기존 개념 페이지의 예시는 유지하고 관련 모음을 연결한다. 새 예시는 기존 지식의 적용 예시로 표시하며 `overview` 상태로 두고 실제 실행 경험이나 새로 학습한 원문으로 취급하지 않는다.

각 prompt는 PyMdown Tabbed와 Material의 `content.tabs.link`로 한국어·영어를 선택한다. 문서 언어 선택은 기존 i18n을 유지한다. 전용 `.prompt` code block만 줄바꿈하도록 CSS를 적용하며 copy 기능은 기존 Material 기능을 사용한다. 사용자 정의 JavaScript나 별도 번역 서비스는 추가하지 않는다.

## 대안과 결과

- 모든 예시를 기술 문서에 삽입하는 방법은 본문 길이가 크게 늘어 제외했다.
- 영어 prompt만 유지하고 문서 전체만 번역하는 방법은 요청을 충족하지 못한다.
- 별도 앱·JSON 원본은 Markdown/vault 이중 관리와 구현 비용이 커 제외했다.

장점은 한 페이지에서 언어를 바꾸고 복사할 수 있고, Markdown 사본에도 양쪽 prompt가 남는다는 점이다. 두 언어 페이지 각각에 양쪽 prompt를 담으므로 변경 시 일치 검토가 필요하다. 탭 상태는 Material이 관리하며 native radio/label 구조를 사용한다.

## 검증

[스펙 005](../specs/005-practical-prompts.md)의 출력 HTML·구문 회귀, 375px/1280px 브라우저 줄바꿈·전환·복사, 한영 의미 검토, 전체 빌드와 vault hash로 확인한다.

## 공식 근거

- [Material content tabs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/)
- [Material code blocks](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/)
- [PyMdown SuperFences](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/)
