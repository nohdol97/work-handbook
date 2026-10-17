# work-handbook 운영 규칙 요약

> source-hash: `ca073a4a8ff7`
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

## 핸드북 운영

이 루트가 업무 지식 저장소다. 모든 자료 반입 전에 `handbook-contract.md`를 읽는다. 공개 문서는 한영 쌍으로 작성하며 영어 페이지는 한국어 문서 규칙의 예외다. 출처별 ID, 누락 없는 반영표, 실제 의미·영어·개인정보 검토를 유지한다. `make validate`와 vault를 포함한 `make finalize`를 완료한다. 공개 Pages 활성화 직전에 확인을 받는다.

## 학습 원문의 형태 보존

최신 지정 자료의 목차·순서와 핵심 기술 지식을 유지하고 원본 증거와 ID를 추적한다. `preserve-study-source` 스킬로 문서를 작성·개정할 때는 선택된 등록 구역만 사용자 상시 지시·작업 범위 증거와 `editable` 모드로 전환하고, 원본을 남긴 채 어려운 문장 자체를 쉽게 고친다. 선택하지 않은 구역은 기존 보존을 유지하며 사용자가 원문 그대로를 명시하면 예외로 둔다. 쉬운 표현, 첫 용어 풀이, 적절한 비유와 예시, 개념의 필요성과 사용 시점, 기술 연결, 장별 짧은 정리를 적용한다. [스펙 010](docs/specs/010-requested-source-rewrite.md)을 따르고 등록 검사·원본 대비 양언어 전문·화면·vault를 검증한다. ID coverage만으로 누락이나 가독성을 판단하지 않는다.
