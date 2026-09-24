# work-handbook 운영 규칙 요약

> source-hash: `{{SOURCE_HASH}}`
> 영어 원본 `AGENTS.md`가 판단 기준이며, 원본이 바뀌면 이 요약과 해시를 같은 커밋에서 갱신한다.

## 목표

Build and maintain an extensible bilingual Work Knowledge Handbook with lossless source traceability and safe Markdown vault copies

## 핵심 규칙

- 프로젝트 작업 전 `REGISTRY.md`와 중앙 프로젝트 하네스를 읽는다.
- 동작 변경은 스펙 → 실패 테스트 → 최소 구현 → 전체 검증 순서로 진행한다.
- 구조·보안·배포·소유권 결정은 ADR로 남긴다.
- 독립적이고 의미 있는 작업 단위가 둘 이상이면 사용 가능한 동시성 범위에서 병렬 실행하고, 충돌 가능성이 있는 변경은 직렬화한다.
- 현재 작업에서 관찰된 재사용 가능한 공통 개선은 자동 반영하지만, 추측성 확장·삭제·시크릿·공개 배포는 별도 승인을 요구한다.
- 외부 스킬은 검토된 고정 SHA와 라이선스가 있는 후보만 자동 설치한다.
- 하위 프로젝트는 독립 저장소이며 검증된 현재 작업 커밋을 기본 push한 뒤 원격 SHA를 확인한다.

## 선택 capability

core only
