---
id: handbook-home
status: overview
last_updated: 2026-10-03
last_reviewed: 2026-10-03
knowledge_ids: []
---

# Work Knowledge Handbook

업무에서 배우고 검증한 지식을 오래 쓰기 위한 핸드북이다. 개념 이해, 설계, 운영, 문제 해결, 프로젝트 진행과 LLM 활용에 필요한 지식을 정리한다.

## 현재 범위

데이터 플랫폼 1~21장 통합본과 플랫폼·인프라 1~11장 자료에서 데이터 플랫폼의 저장·이벤트·처리·분석·품질·관측·거버넌스·AI 평가와 managed 플랫폼·운영·최종 구조를 정리했다. 데이터 플랫폼 기술·구조·커리큘럼 22쌍, 플랫폼·인프라 12쌍, 실무 프롬프트 모음 18쌍, 홈·지식 관리 방법·용어집을 합쳐 한영 55쌍이다.

데이터 플랫폼 후속 자료로 Phase 1~21의 개념 학습 완료 범위를 통합했다. 첫 자료의 Chapter 1~4는 복원된 노트이고 Snowflake는 요약 범위라는 한계를 유지한다. 학습 내용을 실제 구축·운영·장애 실험 경험으로 표현하지 않는다.

새로 추가한 주제: [AI 평가 플랫폼](data-platform/ai-evaluation.md) · [Databricks](data-platform/databricks.md) · [Snowflake](data-platform/snowflake.md) · [플랫폼 비교](data-platform/platform-comparison.md) · [운영·복구](data-platform/production-operations.md). [전체 구조](data-platform/architecture.md)에는 일관성·복구·확장·비용·규모별 축소와 open/managed 대안을 통합했다.

[플랫폼·인프라 기초](platform-infrastructure/index.md) 영역도 추가했다. [Linux·컨테이너](platform-infrastructure/linux-containers.md), [Kubernetes 핵심](platform-infrastructure/kubernetes-core.md), [Kubernetes 운영](platform-infrastructure/kubernetes-operations.md)의 Chapter 1~3은 Basic 개념 학습 범위다. 이어 [Redis](platform-infrastructure/redis.md)·[PostgreSQL](platform-infrastructure/postgresql.md)·[Kafka 운영](platform-infrastructure/kafka.md)·[vLLM](platform-infrastructure/vllm.md)·[LiteLLM](platform-infrastructure/litellm.md)·[GPU 인프라](platform-infrastructure/gpu-infrastructure.md)의 4~9장을 추가했다. 10~11장 [플랫폼 보안](platform-infrastructure/platform-security.md)과 [CI/CD·Helm·Argo CD·GitOps](platform-infrastructure/cicd-gitops.md)도 추가했다. 12~15장은 미학습 후속 목차이며 다음은 Terraform & Infrastructure as Code다.

소프트웨어, 데이터, AI, 플랫폼, 인프라, 아키텍처, 운영 등 실제 자료가 들어온 분야부터 확장한다. 새로운 역할이나 기술을 기존 분류에 억지로 끼워 넣지 않는다.

## 바로 쓸 수 있는 실무 예시

[실무 프롬프트 모음](prompts/index.md)에서 주제별 새 예시 100개를 찾을 수 있다. 개념 문서의 34개를 합친 총 134개 예시를 모두 한국어·English 탭으로 선택하고 복사할 수 있다. 입력 자료·요청·출력·검증을 여러 줄로 구분했다. 예시는 실제 운영 결과가 아니라 학습 개념을 적용한 작성 템플릿이다.

## 원문과 보완 설명

학습 본문은 공유된 MD의 제목·번호·순서·문단·목록·예시를 유지한다. 원래 언어는 원문 그대로, 반대 언어는 같은 구조의 번역이다. 추가 설명과 정정·적용 조건은 본문 뒤 보완 영역에 구분했다. 원문에 단순화된 설명이 있으면 해당 절의 보완 조건도 함께 읽는다.

## 읽는 방법

[데이터 플랫폼 전체 구조](data-platform/architecture.md)에서 각 도구의 역할을 파악하고, [학습 범위와 완료 현황](data-platform/curriculum.md)에서 필요한 주제로 이동한다. [지식 관리 방법](methodologies/knowledge-workflow.md)은 자료가 핸드북이 되는 과정을, [용어집](glossary/index.md)은 핵심 용어와 정규 주제 위치를 설명한다.

모든 공개 페이지에는 같은 지식을 담은 영어 페이지가 있다. 상단 언어 선택기로 같은 주제의 언어를 바꿀 수 있다.
