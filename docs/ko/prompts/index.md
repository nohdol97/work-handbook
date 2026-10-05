---
id: prompt-library
status: overview
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids: []
---

# 실무 프롬프트 모음

SQL·schema·설정 변경 검토, 장애 조사, 비용 분석, 배포·복구 준비에 쓸 템플릿이다. 기술 이름보다 **지금 결정해야 할 작업**으로 고른다. 반복 업무에서 근거를 정리하고 검토 누락을 찾는 용도로 선정했으며, 실제 사용 빈도나 효과를 측정한 결과는 아니다.

## 지금 필요한 작업

| 작업 | 시작할 사례 | 받을 결과 |
|---|---|---|
| SQL·모델 PR 검토 | [Join 행 폭증](spark.md#spark-01) · [Incremental 최초 실행·key](dbt.md#dbt-05) · [SCD join 경계](analytical-modeling.md#analytical-modeling-02) | 근거 위치, 반례, 최소 수정 후보 |
| Schema·계약 변경 | [CDC downstream 영향](cdc-debezium.md#cdc-debezium-03) · [이벤트 단위·의미](event-architecture.md#event-architecture-01) · [계약의 SLO·owner](governance.md#governance-06) | 깨지는 소비 조건, 미합의 항목, 배포 보류 근거 |
| 장애 초기 조사 | [데이터 최신성 지연](data-observability.md#data-observability-01) · [두 경로 결과 불일치](event-architecture.md#event-architecture-04) · [RAG 오답](ai-ready-data.md#ai-ready-data-04) | 관찰·가설, 영향 범위, 첫 확인 순서 |
| 성능·비용 검토 | [읽기 비용](foundations.md#foundations-06) · [Trino OOM](trino.md#trino-02) · [Flink backpressure](flink.md#flink-05) | 병목 근거, 한 변수 비교 계획, 채택 기준 |
| 배포·전환 준비 | [Savepoint 업그레이드](flink.md#flink-04) · [Polling→CDC](cdc-debezium.md#cdc-debezium-05) · [Embedding 갱신](ai-ready-data.md#ai-ready-data-03) | 적용 범위, 복원 조건, 진행·보류 판단 |
| 재처리·복구 확인 | [실패 task 재개](orchestration.md#orchestration-03) · [격리 데이터 재처리](data-quality.md#data-quality-03) · [소비 재개 조건](data-quality.md#data-quality-06) | 재사용 근거, 중단 조건, 복구 후 대사 |
| 평가·문서 품질 검토 | [실패를 회귀 사례로](ai-ready-data.md#ai-ready-data-02) · [버전별 평가 비교](online-evaluation.md#online-evaluation-05) · [번역 PR 대조](knowledge-workflow.md#knowledge-workflow-02) | 재발 검사, 비교 한계, 근거가 있는 수정안 |

## 사용 방법

1. 사례의 **입력 준비**를 읽고 같은 실행·기간을 가리키는 비식별 SQL·설정·로그·표본을 준비한다. 실제 자료가 없으면 가상 표본이라고 명시한다.
2. `한국어` 또는 `English` 탭에서 프롬프트를 복사하고 대괄호를 채운다. 자료에 행 번호·시각·표본 ID를 붙이고 모르는 값은 `미확인`으로 남긴다.
3. 답의 지적을 입력 근거와 대조한다. **오류 가능성**과 **기대 결과 / 검증 방법**을 기준으로 채택·보류를 판단한다. 필요한 근거가 없으면 결론보다 추가 자료 질문을 먼저 처리한다.

프롬프트는 각각 독립적으로 복사할 수 있다. 답은 검토 초안이며 실행·변경 승인이 아니다. 사용 후에는 실제로 채택한 지적, 잘못된 지적, 검토에 걸린 시간을 남겨 자기 업무에 도움이 되는지 확인한다.

## 주제별 전체 사례

100개 사례의 상세 질문과 검증 기준을 주제별로 모았다. 개념 문서의 41개 사례도 한영 탭으로 제공한다. 예시 작성은 학습 완료나 실제 운영 경험을 뜻하지 않는다.

| 주제 | 다루는 판단 |
|---|---|
| [저장·분석 기초](foundations.md) | 부하 분리·partition·pruning·읽기 비용 |
| [이벤트 아키텍처](event-architecture.md) | 계약·schema·중복·replay·시각 기준 |
| [Lakehouse / Iceberg](lakehouse-iceberg.md) | snapshot·쓰기 방식·정비·보존 |
| [Spark](spark.md) | join·메모리·출력 파일·재시도 |
| [Flink](flink.md) | window·state·checkpoint·업그레이드 |
| [CDC / Debezium](cdc-debezium.md) | snapshot 복구·삭제·schema·대사 |
| [Orchestration](orchestration.md) | 준비 조건·retry·재개·publish gate |
| [dbt](dbt.md) | 모델 PR·의존성·test·incremental·재계산 |
| [분석 모델링](analytical-modeling.md) | grain·이력 join·metric·차원 |
| [Trino](trino.md) | pushdown·메모리·skew·작업 배치 |
| [데이터 품질](data-quality.md) | 검사 배치·격리·SLO·복구 확인 |
| [데이터 관측](data-observability.md) | freshness·volume·분포·알림 |
| [계보·메타데이터](lineage-metadata.md) | catalog·정의 충돌·추적·영향 범위 |
| [거버넌스](governance.md) | 책임·접근·마스킹·보존·감사 |
| [AI-ready 데이터](ai-ready-data.md) | telemetry·회귀 사례·embedding·RAG |
| [온라인 AI 평가](online-evaluation.md) | 평가 연결·미평가·rubric·버전 비교 |
| [지식 관리](knowledge-workflow.md) | 추출·번역·통합·검토 증거 |

## 개념 문서의 업무 예시

[릴리스 평가](../data-platform/ai-evaluation.md), [플랫폼 선택](../data-platform/platform-comparison.md), [운영·복구](../data-platform/production-operations.md), [전체 구조](../data-platform/architecture.md)에서는 문맥과 함께 검토할 수 있다. 플랫폼·인프라와 AWS 사례는 각 [플랫폼·인프라 목차](../platform-infrastructure/index.md), [AWS 목차](../aws-cloud/index.md)에서 찾는다.
