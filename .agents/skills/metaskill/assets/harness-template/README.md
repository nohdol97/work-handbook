# work-handbook

> Build and maintain an extensible bilingual Work Knowledge Handbook with lossless source traceability and safe Markdown vault copies

## 이 프로젝트가 해결하는 문제

이 저장소는 제품 코드가 아니라 개인 개발 하네스다. 공통 규칙과 스킬, 문서, 검증을 한곳에서 관리하고 실제 제품은 `project/<name>/`의 독립 저장소로 유지한다.

## 설계 원칙

| 원칙 | 방식 |
|---|---|
| 목표 우선 | 하네스 목표와 비목표를 스펙에 고정한다. |
| SDD + TDD | 동작 계약과 실패 테스트가 구현을 이끈다. |
| 결정 보존 | 구조적 선택은 ADR로 기록한다. |
| 의존성 기반 병렬 실행 | 독립적인 조사·검증·구현을 동시 실행하고 공유 변경은 직렬화한다. |
| 안전한 자동 개선 | 현재 작업의 공통 증거에 한해 하네스를 개선한다. |
| 재현 가능한 외부 스킬 | 고정 SHA, 라이선스, 감사 기록을 lock에 남긴다. |
| 저장소 전달 | 검증된 프로젝트 작업을 push하고 원격 ref를 확인한다. |

## 시작하기

1. 이 루트에서 Codex 또는 Claude Code를 연다.
2. `REGISTRY.md`에 프로젝트를 등록하거나 “새 프로젝트 만들어줘”라고 요청한다.
3. 다음 명령으로 하네스를 확인한다.

```bash
python3 scripts/check_harness.py
```

선택 capability: core only

## 병렬 작업

비자명한 작업은 먼저 의존 관계와 공유 변경 표면을 확인한다. 독립적이고 의미 있는 작업 단위가 둘 이상이면 사용 가능한 동시성 범위에서 조사, 검색, 테스트와 겹치지 않는 구현을 함께 진행한다. 구체적이고 범위가 분리된 하위 작업은 보조 에이전트를 사용할 수 있을 때 위임한다.

같은 파일이나 외부 상태를 변경하는 작업, 아직 결정되지 않은 공통 판단을 전제로 하는 작업, 올바른 검증을 위해 실행 순서가 필요한 작업은 직렬화한다. 주 에이전트는 최종 통합, 충돌 해소, 권한 판단과 전체 검증을 책임진다.

## 주요 경로

| 경로 | 역할 |
|---|---|
| `AGENTS.md` | 항상 적용되는 운영 계약 |
| `AGENTS.ko.md` | 사용자를 위한 한국어 요약 |
| `REGISTRY.md` | 이 PC의 프로젝트 라우팅 정보, git 미추적 |
| `.agents/skills/` | 공통 스킬 원본 |
| `.agents/projects/` | 프로젝트별 중앙 하네스, git 미추적 |
| `docs/README.md` | ADR·스펙·제안서 지도 |
| `skills.lock.json` | 외부 스킬 출처와 고정 리비전 |
| `project/` | 독립 제품 저장소, 루트에서 git 미추적 |

## 자동 개선 경계

현재 작업에서 재현된 공통 누락·반복·우회만 가장 작은 기존 자산에 반영한다. 삭제, 통합, 프로젝트 전용 스킬, 시크릿 접근, 공개 배포는 자동 개선 범위가 아니다.

## 프로젝트 전달

새 프로젝트는 local-only 요청이 아니면 검증 후 private GitHub 저장소 생성과 첫 push까지 진행한다. 기존 프로젝트도 현재 작업의 커밋만 포함된 경우 upstream으로 push하고 원격 branch SHA를 확인한다.

## 검증과 문제 해결

`python3 scripts/check_harness.py`가 실패하면 먼저 출력된 파일과 문서 지도를 수정한다. 외부 스킬이 pending이면 네트워크를 복구한 뒤 metaskill의 외부 스킬 설치 절차를 다시 실행한다. GitHub 인증이 샌드박스에서만 실패하면 macOS Keychain 접근으로 같은 read-only 상태를 다시 확인한다.

## 참고

- [운영 규칙 요약](AGENTS.ko.md)
- [문서 지도](docs/README.md)
- [스킬 카탈로그](.agents/skills/README.ko.md)
