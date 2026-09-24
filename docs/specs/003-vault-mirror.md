# 스펙 003: Markdown vault 복사

- 상태: active
- 날짜: 2026-09-24
- 관련 ADR: [003: handbook와 vault](../adr/003-handbook-and-vault.md)

## 문제

Git 저장소에서 관리하는 Markdown을 vault에서도 읽고 싶다. 단순 덮어쓰기는 vault 편집을 잃게 하고 잘못된 경로는 저장소나 다른 파일을 바꿀 수 있다.

## 목표

Git의 Markdown 원본을 지정한 vault 하위 폴더에 안전하게 복사한다. 상태 기록으로 외부 편집을 감지한다.

## 비목표

- 양방향 병합, 삭제 전파, 백그라운드 감시, 공개 배포
- 개인정보 탐지 또는 민감한 원본의 자동 분류

## 요구사항

### R1. 명시한 대상과 복사 범위

`--root`, `--vault`, `--folder`를 받는다. 기본 root는 스크립트가 속한 저장소이며 folder는 `work-handbook`이다. 폴더 이름은 단일 안전한 경로 요소여야 한다. `.agents`를 포함한 자체 Markdown을 상대 경로 그대로 복사한다. Git ignore 여부는 복사 범위를 바꾸지 않는다. `.git`, `.venv`, `venv`, `node_modules`, `site`, `_workspace`, `project`, `third_party`, `sources-private`, `private`, `.private`, `.obsidian` 디렉터리와 모든 심볼릭 링크는 제외한다. vault는 Git의 대체 원본이 아니다.

### R2. 충돌과 기존 파일 보호

이전 복사본과 다른 vault 파일은 자동 덮어쓰지 않는다. 관리 이력이 없는 같은 파일은 채택할 수 있지만 내용이 다르면 실패한다. 모든 충돌을 쓰기 전에 검사한다. 원본에서 사라진 파일은 vault에서 삭제하지 않는다.

### R3. 경로 및 상태 보호

저장소와 vault 대상이 서로 포함되는 경우 실패한다. 대상 내부의 심볼릭 링크, 대상 자체의 심볼릭 링크, 잘못된 상태 파일은 실패한다. `_workspace/vault-state.json`에 파일 hash와 절대 대상 식별자를 기록한다. 기존 상태와 다른 vault를 사용하려 하면 실패한다. 파일과 상태는 같은 디렉터리의 임시 파일에서 atomic replace로 저장한다. 상태는 ignore되어야 한다.

### R4. 검증 모드와 출력

`--check`는 파일과 디렉터리를 쓰지 않는다. 복사가 필요한 상태면 CLI는 비정상 종료한다. 이미 동기화되었으면 성공한다. CLI는 개수와 일반 오류만 출력하며 사용자 경로를 출력하지 않는다. Python 함수 `run_sync(root, vault, folder='work-handbook', check=False)`는 개수 사전을 반환한다.

### R5. 로컬 vault 설정

CLI에서 `--vault`를 생략하면 원본 저장소의 `_workspace/vault.json`에서 `vault`와 선택적인 `folder`를 읽는다. 설정이 없거나 잘못되면 일반 오류로 실패한다. 명시적 `--vault`가 있으면 로컬 설정을 읽지 않는다. 명시적 `--folder`는 설정값보다 우선한다. 설정의 상대 vault 경로는 원본 저장소를 기준으로 해석한다. 설정은 ignore되어야 하며 경로를 출력하지 않는다.

## 완료 기준

- `python3 -m unittest discover -s tests -p 'test_sync_vault.py' -v`: 최초 복사, 업데이트, 충돌 시 전체 사전 차단, 같은 파일 채택, 삭제 미전파, 제외 범위, symlink 차단, 중첩 경로 차단, 상태 대상 불일치, 검증 모드, 로컬 설정 로드·누락·오류·명시적 값 우선 처리가 통과한다.
- 테스트는 임시 디렉터리만 사용한다. 실제 외부 vault 쓰기는 이 검증에 포함되지 않는다.

## 운영 한계

동시에 실행하거나 실행 중 vault를 편집하지 않는다. 여러 파일의 전체 트랜잭션을 보장하지 않으며 디스크 오류 시 일부 파일만 복사되었을 수 있다. 각 파일의 atomic replace와 사전 충돌 검사를 보장한다. vault가 다른 장치에 동기화되는지는 검사하지 않는다. `private`/`.private` 밖의 민감한 Markdown은 복사 전 사용자가 분류해야 한다.
