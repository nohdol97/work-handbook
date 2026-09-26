# 문서 지도

## ADR

| ADR | 상태 | 결정 |
|---|---|---|
| [001](adr/001-initial-harness.md) | accepted | work-handbook의 목표와 기본 구조 |
| [002](adr/002-dependency-aware-parallel-work.md) | accepted | 독립 작업은 병렬 실행하고 공유 변경은 직렬화 |
| [003](adr/003-handbook-and-vault.md) | accepted | 한영 정규 지식과 vault 사본 |
| [004](adr/004-public-repository-and-pages.md) | accepted | 사용자 승인에 따른 public 소스 저장소와 Pages 활성화 |
| [005](adr/005-prompt-library.md) | accepted | 주제별 Markdown 실무 프롬프트와 한영 탭 |

## 스펙

| 스펙 | 상태 | 범위 |
|---|---|---|
| [001](specs/001-harness-contract.md) | active | 생성된 하네스의 기본 동작과 완료 기준 |
| [002](specs/002-handbook-validation.md) | active | 한영·출처·원문 복원·검토 증거 검증 |
| [003](specs/003-vault-mirror.md) | active | 충돌 보호 Markdown vault 사본 |
| [004](specs/004-build-and-delivery.md) | active | 사이트 빌드·검증·전달 |
| [005](specs/005-practical-prompts.md) | active | 프롬프트 줄바꿈·언어 전환·실무 예시 100개 |

## 제안서

아직 제안서가 없다. 외부 도구나 패턴을 평가할 때 `proposals/YYYY-MM-DD-title.md`를 만들고 이 표에 추가한다.

## 변경 이력

- [하네스 변경 이력](harness-changelog.md)
