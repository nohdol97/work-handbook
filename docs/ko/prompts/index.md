---
id: prompt-library
status: overview
last_updated: 2026-09-26
last_reviewed: 2026-09-26
knowledge_ids: []
---

# 실무 프롬프트 모음

설계 검토·SQL 리뷰·장애 조사·데이터 검증·문서화에 바로 맞춰 쓸 수 있는 **새 예시 100개**다. 개념 문서의 예시 23개를 합치면 총 123개이며, 모두 한영 탭과 여러 줄 형식으로 읽을 수 있다. 아래에서 주제를 고르면 각 페이지의 상황별 목차로 이동할 수 있다.

## 사용 방법

1. 현재 상황과 맞는 예시를 선택한다.
2. `한국어` 또는 `English` 탭을 선택한다. 같은 이름의 탭은 다른 예시와 함께 전환된다.
3. 복사 버튼으로 prompt를 복사하고 `[입력 항목]`을 비식별 자료로 바꾼다. 문서 본문의 설명 언어는 상단 언어 메뉴로 바꾼다.
4. LLM의 답을 관찰·가설·추가 확인으로 나누어 읽고 각 예시의 검증 방법을 수행한다.

이 예시는 기존 핸드북의 학습 개념을 적용해 새로 작성했다. 실제 업무 빈도·모델 성능을 측정하거나 production 작업을 실행한 기록이 아니다. 프롬프트 작성 자체로 원문 학습 상태가 달라지지는 않는다. 현재 완료 범위는 [학습 현황](../data-platform/curriculum.md)에서 확인한다.

## 주제별로 찾기

| 주제 | 사용 상황 | 새 예시 |
|---|---|---:|
| [저장·분석 기초](foundations.md) | 파일 배치·partition·scan 비용 | 6 |
| [이벤트 아키텍처](event-architecture.md) | 계약·schema·중복·전달 | 6 |
| [Lakehouse / Iceberg](lakehouse-iceberg.md) | snapshot·commit·유지보수 | 6 |
| [Spark](spark.md) | 실행 계획·shuffle·skew | 6 |
| [Flink](flink.md) | watermark·state·checkpoint | 6 |
| [CDC / Debezium](cdc-debezium.md) | 변경 순서·snapshot·삭제·복구 | 6 |
| [Orchestration](orchestration.md) | 의존성·retry·backfill | 6 |
| [dbt](dbt.md) | 모델·증분 처리·테스트·이력 | 6 |
| [분석 모델링](analytical-modeling.md) | grain·join·차원·metric | 6 |
| [Trino](trino.md) | 질의 계획·pushdown·메모리 | 6 |
| [데이터 품질](data-quality.md) | 규칙·격리·SLO·재처리 | 6 |
| [데이터 관측](data-observability.md) | freshness·volume·drift·alert | 6 |
| [계보·메타데이터](lineage-metadata.md) | 영향 분석·catalog·업무 의미 | 6 |
| [거버넌스](governance.md) | owner·권한·마스킹·보존·감사 | 6 |
| [AI-ready 데이터](ai-ready-data.md) | trace·버전·retrieval·재현성 | 6 |
| [온라인 AI 평가](online-evaluation.md) | feedback·score·trace 연결 | 6 |
| [지식 관리](knowledge-workflow.md) | 추출·번역 대조·통합·검토 | 4 |

## 좋은 입력의 기준

증상과 기대 동작, 제품·connector 버전, 실제 설정, 비교 기간, 비식별 sample, 관찰한 로그·metric, 바꿀 수 없는 조건을 함께 제공한다. 아직 모르는 값은 모른다고 적는다. 예시는 운영계 변경을 자동 승인하는 명령이 아니며, 제안된 조치는 담당자가 실제 권한과 복구 절차를 확인한 뒤 수행한다.

[데이터 플랫폼 전체 구조](../data-platform/architecture.md) · [학습 범위](../data-platform/curriculum.md) · [지식 관리 방법](../methodologies/knowledge-workflow.md)

## 후속 학습 주제의 예시

새 자료를 반영한 [AI 평가](../data-platform/ai-evaluation.md), [Databricks](../data-platform/databricks.md), [Snowflake](../data-platform/snowflake.md), [플랫폼 비교](../data-platform/platform-comparison.md), [운영·복구](../data-platform/production-operations.md), [전체 구조](../data-platform/architecture.md)에도 각각 한영 예시가 있다.
