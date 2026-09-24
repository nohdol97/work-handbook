# ADR 004: 공개 저장소와 GitHub Pages 활성화

- 상태: accepted
- 날짜: 2026-09-24
- 부분 대체: [ADR 003](003-handbook-and-vault.md)의 private 소스 저장소 전제

## 맥락

GitHub Pages 활성화 요청은 현재 요금제에서 private 저장소를 지원하지 않아 HTTP 422로 실패했다. 사용자는 이후 이 저장소 자체를 public으로 변경하도록 명시적으로 요청했다.

## 결정

`nohdol97/work-handbook`을 public으로 전환한다. GitHub Pages는 workflow 방식으로 활성화하고 `PAGES_ENABLED=true`를 설정한다. main push는 기존 검증을 통과한 뒤 사이트를 배포한다. 이 대상의 통상적인 문서 업데이트와 배포는 기존 승인 범위다.

사이트 주소: https://nohdol97.github.io/work-handbook/

## 대안

private 저장소를 유지하려면 지원 요금제로 변경하거나 별도 공개 HTML 저장소와 배포 연결을 마련해야 한다. 사용자가 현재 저장소의 공개 전환을 선택했으므로 이 대안들은 적용하지 않는다.

## 결과와 공개 경계

사이트에는 한영 핸드북만 게시한다. 그러나 저장소의 모든 추적 파일, 원문, 운영 계약, 검토 기록과 Git 이력은 GitHub에서 공개된다. `sources/`도 공개 가능한 자료만 커밋해야 한다. `_workspace/`, `sources-private/` 등 ignore된 로컬 자료는 커밋하지 않는다. vault 경로와 상태는 로컬에 남는다.

## 검증

공개 전 기존 한 개 커밋의 파일 목록과 민감정보 패턴을 확인했다. 저장소 API의 PUBLIC 응답, Pages workflow 설정, 실제 배포 실행 결과 및 인증 없는 HTTP 응답으로 공개 상태를 검증한다. 패턴 검사는 임의의 모든 민감정보를 판정하는 도구가 아니며 자료 반입 시 내용 검토가 계속 필요하다.
