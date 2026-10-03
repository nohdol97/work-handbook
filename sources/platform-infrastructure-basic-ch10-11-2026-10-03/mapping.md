# 플랫폼·인프라·AI 서빙 10~11장 매핑

- 원문: `platform_infra_ai_serving_basic_ch10_ch11.md`, 2,624행·30,821 bytes. `source.md` 경계 뒤에 전체 byte를 보존한다.
- 원래 언어: 한국어와 영어 기술 용어. 한국어 core 원문 보존, 영어 동일 구조 완역.
- 영역: 플랫폼 보안, Kubernetes 권한·네트워크·컨테이너·공급망·tenant 격리, CI/CD·Helm·GitOps·Argo CD·모델 교체·GPU 용량.
- 정규 목적지: `platform-infrastructure/platform-security.md`, `platform-infrastructure/cicd-gitops.md` 한영2쌍. 소개·장간 연결·진도는 기존 `platform-infrastructure/index.md`에 새 source span으로 추가한다.
- 중복 경계: 기존 Kubernetes·LiteLLM·vLLM·GPU 문서를 유지하고 링크한다. 새 원문에서 반복되는 설명도 삭제하지 않는다. 과거 진도 source core는 당시 기록이라는 안내 아래 보존하고 현재 요약은 1~11장 완료·12장 다음으로 갱신한다.
- 추출 순서: 장 담당이 번호별 개념·예시·조건을 `_workspace` 추출 기록에 작성한 뒤 페이지를 쓴다. 10장8절, 11장8절과 GPU 보충, 소개·연결·진도3항목을 출처 ID로 추적한다.
- 읽기 분담: 통합 담당은1~10행과2538행~끝, 보안 담당은11~1355행, GitOps 담당은1356~2537행. 독립 검토자는 전체 원문과 완성된 한영 페이지를 대조한다.
- 범위: 기존53쌍 + 신규2쌍 = 55쌍. 기존362개 지식 ID와 기존 원문 구간을 유지한다. 12~15장은 not-started이며 학습 본문을 만들지 않는다.

## 전체 읽기·공개 가능성 검토

배정된 모든 줄을 읽었고 독립 검토자가 원문 1~2624행 전체를 재확인했다. 접근하지 못한 구간은 없다. `password123`은 원문이 나쁜 예로 명시한 더미이며, `DB_PASSWORD`·`API_KEY`·`JWT_SECRET`는 이름, `registry.example.com`과 `repoURL: ...`는 예시다. 실제 자격증명·내부 주소·직접 식별정보를 발견하지 않았다. 원문을 수정하거나 공백을 정규화하지 않았다.

## 별도로 구분한 적용 조건

- ClusterRole 정의와 binding에 따른 유효 범위, Secret의 encoding/encryption·회전·Pod 경유 접근, NetworkPolicy의 plugin/양방향/가산 조건을 구분한다.
- mTLS 신원 확인과 인가, container 수준 보안 설정, image 서명 검증과 namespace 격리의 한계를 구분한다.
- Helm 3 release 기록과 Argo CD의 template 렌더링·Application 이력, 자동 sync/selfHeal/prune, auto-sync Application rollback 제약과 Health의 한계를 구분한다.
- 4+4=8 및12+4=16 GPU·모델명·1M context는 가정 예시다. rollout 전략별 추가 용량과 기존/신규 모델 동시 운영·장애 여유를 구분한다.

현재 제품 문서의 적용 조건은 각 장의 보완 구역에서 공식 근거와 확인일을 제공한다. 실제 클러스터·Helm·Argo CD·모델 배포, 보안 침투 시험, 부하·장애·복구 실험은 수행하지 않았다.

## 공통 하네스 피드백

기존 source byte 무결성, 원문 구간·번역 구조, 전체 문서 수, 한영 프롬프트, 검토 hash 검증을 그대로 적용한다. 이번 반입에서 추가 공통 동작 변경이 필요한 결함은 현재 확인되지 않았다. 과거 진도 원문은 보존하고 현재 진도 안내를 분리하는 기존 원문 보존 계약을 재사용한다.
