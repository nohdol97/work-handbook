# AWS Cloud Basic 6~7장 매핑

- 원문: `aws_cloud_basic_ch06_ch07_source.md`, 1,416행·20,117bytes. 한국어와 영어 기술 용어. 한국어 core는 원문 그대로, 영어는 동일 구조 완역.
- 이전 자료: 압축형 1~5장 이후의 후속 자료다. 기존 1~5장 내용·ID·원문을 유지하고 현재 진도만 1~7장 완료로 갱신한다. 이전 원문의 “다음”은 당시 기록으로 표시한다.
- 영역: SQS·SNS·MSK 메시징, KMS·Secrets Manager 보안, CloudWatch·CloudTrail 관측·감사, GPU EC2·EKS GPU Node·ECR/S3·vLLM·최종 AWS 구조.
- 새 정규 문서: `aws-cloud/managed-services.md`, `aws-cloud/ai-gpu-architecture.md` 한영 2쌍. 소개·최종 요약·완료 기록은 기존 `aws-cloud/index.md`에 별도 원문 구역으로 추가한다.
- 추출: 소개·최종요약·완료 3개, 6장 번호 절 8개(6.1.1 포함)·장요약 1개, 7장 번호 절 5개 = 17개 ID. 페이지 작성 전에 추출·매핑을 확정한다.
- 중복·링크: 기존 Kafka·Kubernetes·vLLM·GPU·보안과 AWS EKS·스토리지 설명을 유지하고 링크한다. 새 원문의 반복 설명도 삭제하지 않는다.
- 범위: 기존 65쌍 + 2쌍 = 67쌍. 기존 557개 ID + 17개 = 574개.
- 읽기 분담: 통합 담당 1~13행·1337~1416행, 6장 담당 14~800행, 7장 담당 801~1336행. 독립 검토자는 전체 원문을 읽고 양언어 완성 문서를 대조한다.
- 열린 문제: AWS 계정·region·구체 버전·실제 GPU/model 사양·배포 설정은 제공되지 않았다. 원문은 실제 구축·부하·비용·장애 시험의 증거가 아니다.

## 공통 하네스 피드백

기존 원본 byte·원문 구간·번역 구조·의미·출처·문서 수·프롬프트·화면·볼트 검증을 재사용한다. 원문에서 빈 줄 없이 이어진 목록이 HTML에서 한 문단으로 합쳐지는 결함을 화면에서 발견했다. 원문 byte를 바꾸지 않고 등록된 구역의 렌더링 중간 문자열만 보정하도록 ADR 007·스펙 006·회귀 테스트를 별도 하네스 커밋으로 반영한다.

## 전문 읽기·독립 검토·공개 가능성

원문 1~1,416행을 담당자가 모두 읽고 Codex /root/chapter14가 전체를 독립 검토했다. 접근하지 못한 구간은 없다. 저장 원문은 업로드 20,117bytes와 동일하며 SHA-256은 `e81466af2bf97a9b2bdd14e34b34e7118ea07f95c62e4485cf69be1e6b3b0cc3`다. 실제 credential·계정·ARN·개인정보·내부 URL은 발견하지 않았다. `s3://model-bucket/`은 학습용 placeholder다. 가림·공백 정규화는 하지 않았다.

- 6장: Codex /root/chapters12_13 작성·한영 전문 재독, Codex /root/chapter14 독립 전문 대조. SQS/FIFO·SNS·MSK 책임·KMS 정책/rotation·Secrets envelope encryption·관측 수집 범위를 공식 자료와 확인.
- 7장: Codex /root/chapter15 작성·한영 전문 재독, Codex /root/chapter14 독립 전문 대조. GPU 요청·AMI/device plugin·확장·ECR node role/S3 workload role·model version/cache·readiness 조건을 공식 자료와 확인.
- 공통: Codex /root 최신 원문3구역·한영 목차 전체·홈/용어집/프롬프트 변경 대조, Codex /root/chapter14 독립 확인.
- 새 실무 프롬프트 1개는 비식별 업무 자료로 GPU Pod 시작 실패를 검토하는 템플릿이다. 실제 LLM 실행·효과 측정·AWS 자원 조작은 수행하지 않았다.

## 화면과 목록 검토

신규 2쌍과 AWS 목차를 한영·1280px/390px의 12개 조합에서 확인했다. 페이지 전체의 가로 넘침과 JavaScript 오류는 없었고, 프롬프트 언어 탭 및 같은 주제의 문서 언어 전환을 확인했다. 대표 본문·보완·모바일 화면을 직접 검토했다. 등록된 최신 원문에서 각 언어의 6장 33개·7장 18개·소개 5개·완료 7개, 총 63개 목록 항목이 HTML의 li 수와 일치한다. 긴 원문 도식은 코드 블록 안에서 가로 스크롤되며 원래 배치를 유지한다. 앱 브라우저 연결이 없어 임시 profile의 headless Chrome을 사용했으며 사용자 로그인 profile은 사용하지 않았다.
