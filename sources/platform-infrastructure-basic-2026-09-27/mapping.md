# 플랫폼·인프라 기초 자료 매핑

- **Source:** `platform_infra_ai_serving_basic_ch1_ch3.md` 업로드 전체 4,132행, 55,197 bytes. `source.md`에 내용·행 순서와 공백 복원 ledger를 보존한다.
- **Source language:** 한국어와 표준 영어 기술 용어. 정규 한국어와 쉬운 영어로 같은 지식을 제공한다.
- **Curriculum:** Chapter 1 Linux/networking/containers, 2 Kubernetes core, 3 Kubernetes production operations까지 Basic 개념 학습 완료. 4~15장은 후속 목차이며 AI serving 실습 완료를 주장하지 않는다.
- **Primary domain:** Platform / Infrastructure / Linux / Containers / Kubernetes.
- **Topics discovered:** Process·resource·FD·network·signal·namespace·cgroup·OCI·container storage, 선언형 API·workloads·network/storage·scheduling/probes, HA·etcd·CNI/CSI/DNS·scaling·reliability·node/upgrade/troubleshooting.
- **Existing canonical pages:** 데이터 플랫폼의 orchestration·연산·운영과는 관점이 다르다. 기존 자료 266개 ID와 문서를 유지하고, 이번 runtime/cluster 기초는 별도 정규 영역으로 연결한다.
- **New pages required:** `platform-infrastructure/index.md`, `linux-containers.md`, `kubernetes-core.md`, `kubernetes-operations.md`의 한영 4쌍.
- **Potential duplicates:** 원문 각 절의 핵심 정리와 장별 마지막 정리는 해당 정규 절/페이지의 설명·검토 질문에 합집합으로 보존한다. Linux request/limit·Kubernetes resource·node pressure는 각 계층 맥락과 상호 링크를 유지한다.
- **Cross-links:** 같은 언어의 영역 index·세 기술 페이지·홈·glossary·prompt index를 연결한다. 데이터 처리 역할은 기존 data-platform architecture를 참조한다.
- **Open questions:** 실제 Linux 배포판/kernel/cgroup·runtime·Kubernetes/CNI/CSI/cloud 버전, 실행 기록, 장애 실험, 회사 환경이 없다. 제품 문서 확인은 적용 조건을 보완하며 명령 실행 성공이나 운영 경험을 뜻하지 않는다.
- **Expected bilingual page pairs:** 기존 44쌍 + 새 4쌍 = 48쌍. 새 source ID 38개와 기존 266개를 별도 batch로 유지한다.

## 읽기·선추출 범위

통합 담당은 1~8행과 4112~4132행, Linux 담당은 9~1628행, core 담당은 1629~2890행, operations 담당은 2891~4111행 전체를 읽었다. 각 담당자는 작성 전에 지식 ID·행 범위·세부 예시·목적지를 추출했다. 팀 분담 전체 읽기이며 접근하지 못한 본문은 없다.

## 공개·보존 경계

명령의 `example.com`, `server:8080`, `backend`, `my-api` 등은 가상 설명용 주소이며 개인 환경으로 해석하지 않는다. `DB_PASSWORD`, `API_KEY`, `TOKEN`은 설정 키 이름이며 실제 비밀값이 아니다. 전체 읽기와 패턴 검사를 완료했고 공개를 막는 실제 민감정보를 발견하지 않았다. 원문 3·4행의 끝 공백 2개씩만 정규화했고 복원한 byte/hash는 업로드와 일치한다.

## 목적지별 추출

| 정규 문서 | 신규 ID |
|---|---:|
| platform-infrastructure/index.md | 2 |
| platform-infrastructure/linux-containers.md | 12 |
| platform-infrastructure/kubernetes-core.md | 14 |
| platform-infrastructure/kubernetes-operations.md | 10 |

## 재공유 원문과 형태 복원

2026-09-27에 다시 제공된 동명 파일은 55,197 bytes, SHA-256 `9c5236418f74d28e84794d8a98e66742afbb000835354e2039a2212a953ae536`으로 기존 업로드와 같다. 원문 1~3장 본문은 한국어로 그대로 복원하고 영어는 같은 단락·목록·제목·코드 구조로 번역한다. 기존 보완 설명·Mermaid·프롬프트는 원문 구역 밖에 유지한다. 4~15장은 후속 목차 상태를 유지한다.
