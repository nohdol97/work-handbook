# 하네스 변경 이력

| 날짜 | 변경 | 대상 | 검증 |
|---|---|---|---|
| 2026-09-24 | work-handbook 초기 생성과 의존성 기반 병렬 실행 계약 수립 | 루트 계약, 병렬 작업 ADR, 문서, core skills, 선택 capability `core only` | 생성기, 병렬 정책 회귀와 구조 검사 |
| 2026-09-24 | 한영 지식 보존 계약, 3개 페이지 쌍, 출처·검토·사이트 검증, vault 복사와 CI/Pages 준비 | 전체 계약·스펙·ADR·테스트·빌드 | 단위 테스트·strict 빌드·vault hash 검증 |
| 2026-09-24 | 공통 검사기의 의존성 README 오탐 수정 반입 | scripts/check_harness.py | 팩토리 회귀와 자체 검사 통과 |
| 2026-09-24 | 사용자 요청으로 저장소 public 전환 및 Pages workflow 활성화 | README·지식 계약·ADR 003/004·문서 지도·GitHub 설정 | 공개 전 이력 검토·API 상태·전체 검증·배포와 HTTP 확인 |
| 2026-09-24 | 자료 반입 중 재현한 npm 사용자 캐시 EPERM의 작업 폴더 캐시 우회 방법 문서화 | README 문제 해결; 실행·권한 계약 변경 없음 | 실패 재현 후 `npm ci --ignore-scripts --cache _workspace/npm-cache` 설치 성공, Mermaid 24개 구문 통과 |
| 2026-09-24 | 프롬프트를 한영 탭·다중행·모바일 줄바꿈으로 개선하고 새 실무 예시 100개 추가 | Markdown 모음·표시 설정·prompt 감사·스펙 005·ADR 005·지식 계약 | 탭 렌더링/한 줄 회귀 red→green, 전체 검증·브라우저·vault 검증 |
| 2026-09-24 | 페이지·anchor 증가 시 링크 검사가 같은 HTML을 반복 파싱하던 비용을 제거 | check_site·파싱 횟수 회귀·스펙 004 R8 | 3파일 fixture 파싱 6회 실패→3회 통과, 누락 링크·fragment 회귀 유지, 전체 검증 53개·사이트 오류 0건 |
