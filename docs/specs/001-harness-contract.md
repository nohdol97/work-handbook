# 스펙 001: work-handbook 기본 계약

- 상태: active
- 날짜: 2026-09-24
- 관련 ADR: 001, 002

## 문제

Build and maintain an extensible bilingual Work Knowledge Handbook with lossless source traceability and safe Markdown vault copies

## 목표

1. 공통 규칙과 제품 저장소의 소유권을 분리한다.
2. 동작 변경을 SDD와 TDD로 검증한다.
3. 외부 스킬과 원격 전달 상태를 재현 가능하게 기록한다.
4. 독립 작업은 안전한 범위에서 병렬 실행하고 공유 변경은 직렬화한다.

## 비목표

- 하네스 생성만으로 공개 배포나 자격 증명 변경을 승인하지 않는다.
- 관찰된 필요가 없는 프로젝트 전용 자산을 미리 만들지 않는다.

## 요구사항

### R1. 구조

루트 계약, README, docs MOC, core skills, registry, integrity checker가 존재해야 한다.

### R2. 개발

동작 변경은 스펙, 실패 테스트, 최소 구현, fresh verification을 따라야 한다.

### R3. 전달

현재 작업의 검증된 프로젝트 커밋은 local-only가 아니면 upstream으로 push하고 remote ref를 확인해야 한다.

### R4. 병렬 실행

비자명한 작업에서 독립적이고 의미 있는 작업 단위가 둘 이상이면 사용 가능한 동시성 범위에서 병렬 실행해야 한다. 구체적이고 범위가 겹치지 않는 하위 작업은 보조 에이전트를 사용할 수 있을 때 위임한다. 같은 파일·외부 상태를 변경하거나, 미결정 공통 판단 또는 순서가 있는 검증에 의존하는 작업은 직렬화하며, 주 에이전트가 통합과 최종 검증을 책임진다.

## 완료 기준

1. `python3 scripts/check_harness.py`가 성공한다.
2. 모든 shared skill이 한국어 카탈로그에 정확히 한 번 연결된다.
3. 외부 installed skill마다 lock entry와 license가 존재한다.
4. `AGENTS.md`가 병렬 실행의 firing condition, 위임 조건, 직렬화 경계와 주 에이전트 책임을 명시한다.
