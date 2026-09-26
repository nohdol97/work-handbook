---
id: handbook-glossary
status: overview
last_updated: 2026-09-26
last_reviewed: 2026-09-26
knowledge_ids: []
---

# 용어집

| 용어 | 의미 |
|---|---|
| Canonical knowledge | 여러 자료의 유용한 지식을 통합한 기준 지식. |
| Canonical page ID | 경로가 바뀌어도 유지하는 페이지 식별자. 한영 쌍은 같은 ID를 쓴다. |
| Content manifest | 의미 있는 원문 지식과 안정적인 ID의 목록. |
| Coverage matrix | 각 ID가 포함·통합·보류·제외된 위치와 이유를 추적하는 표. |
| Semantic audit | 두 언어에 같은 개념, 예시, 제약과 경고가 있는지 검토하는 과정. |
| Source of truth | 변경과 판단의 기준이 되는 원본. 이 핸드북에서는 Git의 Markdown이다. |

## 데이터 플랫폼 용어

| 용어 | 의미 | 정규 주제 |
|---|---|---|
| OLTP | 서비스의 작은 범위 트랜잭션을 처리하는 workload. | [foundations](../data-platform/foundations.md) |
| OLAP | 대량 이력을 scan·집계·join하는 분석 workload. | [foundations](../data-platform/foundations.md) |
| Column pruning | 질의에 필요한 column만 읽는 최적화. | [foundations](../data-platform/foundations.md) |
| Partition / pruning | 데이터를 나누는 규칙 / 조건에 맞지 않는 구간을 읽지 않는 최적화. | [foundations](../data-platform/foundations.md) |
| Cardinality | 서로 다른 값의 수. | [foundations](../data-platform/foundations.md) |
| Compaction | 작은 파일을 적절한 크기로 합치는 유지보수. | [foundations](../data-platform/foundations.md) |
| Schema | 데이터 필드와 타입 등 구조의 정의. | [event-architecture](../data-platform/event-architecture.md) |
| Idempotency | 같은 작업을 반복해도 의도한 결과가 중복되지 않는 성질. | [event-architecture](../data-platform/event-architecture.md) |
| Consumer lag | 소비자가 아직 처리하지 못한 로그 위치 차이 등 뒤처짐의 지표. | [event-architecture](../data-platform/event-architecture.md) |
| Snapshot | 테이블이나 처리 상태를 특정 시점의 일관된 상태로 표현한 것. 종류별 범위는 다르다. | [lakehouse-iceberg](../data-platform/lakehouse-iceberg.md) |
| Shuffle | 키별 연산 등을 위해 처리 노드 사이에 데이터를 재분배하는 과정. | [spark](../data-platform/spark.md) |
| Data skew | 일부 키나 task에 데이터·작업이 편중된 상태. | [spark](../data-platform/spark.md) |
| Watermark | 이벤트 시간 진행을 추정해 지연 데이터와 상태 처리에 사용하는 기준. | [flink](../data-platform/flink.md) |
| Checkpoint / savepoint | 장애 복구용 상태 snapshot / 계획된 운영 변경 등에 쓰는 상태 snapshot. | [flink](../data-platform/flink.md) |
| Backpressure | 하류 처리 속도가 부족해 상류 처리에 압력이 전달되는 현상. | [flink](../data-platform/flink.md) |
| CDC | INSERT·UPDATE·DELETE 같은 원본 변경을 캡처하는 방식. | [cdc-debezium](../data-platform/cdc-debezium.md) |
| WAL | DB 변경을 복구와 복제 등에 활용하도록 기록하는 write-ahead log. | [cdc-debezium](../data-platform/cdc-debezium.md) |
| Tombstone | Kafka compacted topic에서 key 삭제를 표시하는 null-value record. | [cdc-debezium](../data-platform/cdc-debezium.md) |
| Orchestration / DAG | 작업 의존성과 실행 관리 / 방향이 있고 순환이 없는 작업 그래프. | [orchestration](../data-platform/orchestration.md) |
| Backfill | 지정한 과거 범위의 데이터를 채우거나 재계산하는 작업. | [orchestration](../data-platform/orchestration.md) |
| Grain | 테이블의 한 row가 나타내는 단위. | [analytical-modeling](../data-platform/analytical-modeling.md) |
| Fact / dimension | 측정 대상 이벤트·수치 / 이를 설명하는 속성. | [analytical-modeling](../data-platform/analytical-modeling.md) |
| SCD Type 2 | 유효 기간 등을 가진 새 row로 속성 변경 이력을 보존하는 모델. | [analytical-modeling](../data-platform/analytical-modeling.md) |
| Semantic layer | metric·dimension의 의미와 계산을 재사용하게 정의하는 계층. | [analytical-modeling](../data-platform/analytical-modeling.md) |
| Predicate pushdown | 필터 조건의 처리를 데이터 원본 쪽으로 전달하는 최적화. | [trino](../data-platform/trino.md) |
| Data quality | 정확성·완전성·유효성 등 데이터 요구 규칙의 충족 여부. | [data-quality](../data-platform/data-quality.md) |
| Quarantine | 유효하지 않은 데이터를 정상 경로에서 분리해 추적·복구하는 방식. | [data-quality](../data-platform/data-quality.md) |
| SLI / SLO | 관찰하는 서비스 수준 지표 / 그 지표에 대한 목표. | [data-observability](../data-platform/data-observability.md) |
| Freshness | 데이터가 업무에 필요한 만큼 최신인지 나타내는 특성. | [data-observability](../data-platform/data-observability.md) |
| Observability | 관찰 신호로 시스템·데이터 상태와 변화를 이해하는 능력. | [data-observability](../data-platform/data-observability.md) |
| Lineage | 데이터의 생성·이동·변환 관계. | [lineage-metadata](../data-platform/lineage-metadata.md) |
| Metadata / catalog | 데이터를 설명하는 정보 / 그 정보를 찾고 탐색하는 시스템. | [lineage-metadata](../data-platform/lineage-metadata.md) |
| Data contract | schema뿐 아니라 의미·품질·최신성·owner 등을 합의한 계약. | [governance](../data-platform/governance.md) |
| RBAC | 역할을 기준으로 권한을 부여하는 접근 통제. | [governance](../data-platform/governance.md) |
| Retention | 데이터와 파생 사본의 보존 기간·조건. | [governance](../data-platform/governance.md) |
| Trace / observation / session | 실행 흐름 / 개별 단계 / 관련 실행의 묶음. | [ai-ready-data](../data-platform/ai-ready-data.md) |
| Provenance | 데이터·AI 결과의 출처와 생성 맥락을 추적하는 정보. | [ai-ready-data](../data-platform/ai-ready-data.md) |
| Reproducibility | 과거 실험 조건을 다시 구성하는 능력. 동일 LLM 문장 생성의 보장은 아니다. | [ai-ready-data](../data-platform/ai-ready-data.md) |
| Regression dataset | 과거 실패가 재발하는지 확인하는 평가 사례 모음. | [ai-ready-data](../data-platform/ai-ready-data.md) |
| Online evaluation | 실제 AI 실행에 feedback·규칙·judge 등의 평가 신호를 연결하는 과정. | [online-evaluation](../data-platform/online-evaluation.md) |

[지식 관리 방법](../methodologies/knowledge-workflow.md) · [홈](../index.md)

## 평가·managed 플랫폼·복구

| 용어 | 의미 | 정규 주제 |
|---|---|---|
| Rubric | 평가 항목별 점수·판정 기준표. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| Groundedness | 응답이 제공된 근거에 기반하는 정도. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| Inter-rater agreement | 같은 사례를 평가한 사람들의 판정 일치도. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| Bundle version | Agent·prompt·tool·model·retrieval 구성 조합의 버전. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| TTFT | Time to first token. 요청부터 첫 출력 token까지 걸린 시간. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| Cost per success | 전체 비용을 성공 실행 수로 나눈 값. 성공 정의와 측정 범위도 명시한다. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| DBU | Databricks 사용량 단위. 실제 요금은 compute 유형·계약 등과 함께 확인한다. | [databricks](../data-platform/databricks.md) |
| Photon | Databricks의 벡터화된 query execution engine. | [databricks](../data-platform/databricks.md) |
| UniForm | Delta table에 Iceberg reader용 metadata를 제공한다. Writer 동등성을 뜻하지 않는다. | [databricks](../data-platform/databricks.md) |
| Micro-partition | Snowflake가 자동 관리하며 pruning용 metadata를 가진 columnar 저장 단위. | [snowflake](../data-platform/snowflake.md) |
| Dynamic Table | 선언한 query 결과를 target lag 목표에 맞춰 갱신하는 Snowflake 객체. | [snowflake](../data-platform/snowflake.md) |
| RTO | Recovery time objective. 복구에 허용하는 목표 시간. | [production-operations](../data-platform/production-operations.md) |
| RPO | Recovery point objective. 시간으로 표현한 허용 데이터 손실 범위. | [production-operations](../data-platform/production-operations.md) |
