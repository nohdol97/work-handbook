# ADR 001: work-handbook 초기 구조

- 날짜: 2026-09-24
- 상태: accepted

## 배경

목표는 “Build and maintain an extensible bilingual Work Knowledge Handbook with lossless source traceability and safe Markdown vault copies”이다. 공통 규칙과 실제 제품 저장소가 섞이면 하네스 개선과 제품 전달을 독립적으로 검증하기 어렵다.

## 결정

- 항상-온 규칙은 루트 `AGENTS.md`가 소유한다.
- 제품은 `project/<name>/`의 독립 저장소로 둔다.
- 프로젝트별 하네스는 `.agents/projects/<name>/`에 중앙 관리한다.
- README, docs MOC, 스킬 카탈로그, 변경 이력을 구조 검사로 동기화한다.
- 선택 capability는 `core only`다.

## 결과

하네스와 제품의 커밋·push·검증 상태를 분리해서 판단할 수 있다. 새 capability는 metaskill의 외부 스킬 및 자동 개선 경계를 통과해야 한다.
