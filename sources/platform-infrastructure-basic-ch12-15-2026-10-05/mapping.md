# 플랫폼·인프라·AI 서빙 12~15장 매핑

- 원문: `platform_infra_ai_serving_basic_ch12_ch15.md`, 4,047행·48,741 bytes. source.md 경계 뒤 전체 byte 보존.
- 언어: 한국어 원문과 영어 기술 용어. 한국어 본문 그대로, 영어 동일 구조 완역.
- 영역: Terraform/IaC·state·환경·운영, multi-tenancy·quota·비용, IDP·self-service·governance, 최종 AI platform 구조·장애 대응.
- 정규 목적지: `platform-infrastructure/terraform-iac.md`, `multitenancy-cost.md`, `developer-platform.md`, `architecture.md` 한영 4쌍. 소개는 기존 index.md의 별도 원문 구역.
- 추출: 소개 1개, 12장 10절, 13장 10절, 14장 24절, 15장 87절과 최종 구조·mental model·목표·완료 4개, 총 136개 ID. 원문의 상위 15.4~15.10 제목도 변경 없이 architecture 본문에 보존.
- 기존 정규 문서: 1~11장·AWS·데이터 플랫폼 본문 유지. 반복 개념도 새 원문에서 삭제하지 않고 관련 문서로 연결한다. 과거 원문 진도는 당시 기록으로 남기고 현재 요약만 1~15장 완료로 갱신한다.
- 신규 페이지 작성 전 추출·매핑 확정. 기존 61쌍 + 4쌍 = 65쌍.
- 읽기 분담: 통합 담당 1~8행과 기존 현황, 장 담당 각각 9~848행, 849~1588행, 1589~4047행. 각 담당은 배정된 전체 원문과 양언어 완성 문서를 대조한다.
- 열린 문제: 실제 Terraform/provider/Kubernetes/serving 버전·구성·성능·배포 환경은 제공되지 않았다. 실행 가능한 예제라고 보증하지 않는다.

## 공통 하네스 피드백

기존 원문 byte·구조·한영 의미 검토·문서 수·링크·vault 검증을 재사용한다. 이번 원문 13.6의 LLM Quota 제목을 실무 프롬프트로 오인하는 기존 검사기 결함을 재현했다. 실습 제목만 판별하도록 스펙·회귀 테스트와 함께 별도 하네스 커밋으로 수정한다.

## 전문 읽기·번역·개인정보 검토

담당자들이 전체 1~4,047행을 읽었고 새 장 4쌍을 서로 독립 검토했다. 접근하지 못한 부분은 없다. 원본 SHA-256은 `72cf7231f3c4cf8477775ed27921e9e034ad4c282ab436778362f27d2d4f995d`다. `llm.company.com`, team-a/b, 모델명, image tag와 GPU·token 수는 원문에서 제시한 가상 구성 예다. 실제 자격증명·개인정보·내부 운영 주소를 발견하지 않았다. 따라서 가림이나 공백 정규화 없이 원본을 보존한다.

- 12~13장: Codex /root/chapters12_13 작성·전체 재독, Codex /root/chapter14 전체 독립 대조.
- 14장: Codex /root/chapter14 작성·전체 재독, Codex /root/chapters12_13 전체 독립 대조. 최종 프롬프트 표식 수정은 작성자가 내용 보존과 실제 Markdown 렌더를 재확인.
- 15장: Codex /root/chapter15 작성·전체 재독, Codex /root/chapters12_13 전체 독립 대조. 87절·마지막 4부·상위 제목의 중복 번호도 유지.
- 공통 문서: Codex /root 전체 내용 및 변경 대조, 홈·용어집·학습 현황 변경은 Codex /root/chapters12_13도 확인.

공식 최신 자료는 각 장의 별도 보완에서 출처와 확인일을 제공한다. Kubernetes·Terraform·LiteLLM의 실제 배포, provider/API 호출, GPU 측정, 비용 계산 및 장애 실험은 수행하지 않았다.

## 화면 검토

로컬 빌드의 신규 4쌍을 1280px·390px에서 열어 페이지 너비를 확인했다(16개 조합, 수평 페이지 넘침 없음). 14·15장 본문 시작과 보완 구역의 한영 desktop/mobile 스크린샷을 생성하고 대표 화면을 직접 확인했다. 긴 text 도식은 코드 영역 안에서 가로 스크롤되며 원문 배치를 유지한다. 15장의 실제 언어 링크를 따라 같은 주제의 영어 페이지로 이동했다. 브라우저 JavaScript 오류는 없었다. 앱 브라우저 연결이 없어 별도 임시 profile의 headless Chrome을 사용했고 사용자 로그인 profile은 사용하지 않았다.
