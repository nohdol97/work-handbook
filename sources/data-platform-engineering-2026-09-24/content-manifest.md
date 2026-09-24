---
items:
- id: DPE-00-01
  knowledge: 학습 목적·개념 중심 깊이와 Chapter 1~4 복원 노트라는 출처 제약
  kind: constraint
- id: DPE-01-01
  knowledge: '1.1 OLTP vs OLAP: OLTP / OLAP / PostgreSQL이 분석 이력에 점점 불리해지는 이유'
  kind: concept
- id: DPE-01-02
  knowledge: '1.2 Row-Oriented vs Column-Oriented Storage: Row-Oriented / Column-Oriented / Compression / Column
    Pruning'
  kind: concept
- id: DPE-01-03
  knowledge: '1.3 Parquet: Row Group / Page / Encoding / Compression / Statistics / Predicate Pushdown / Pruning
    / Column Pruning'
  kind: concept
- id: DPE-01-04
  knowledge: '1.4 Object Storage: Object vs Block/File Storage / Storage / Compute Separation / Remote I/O'
  kind: concept
- id: DPE-01-05
  knowledge: '1.5 File Layout Engineering: Small File Problem / Too-Large File / Compaction / Write Amplification'
  kind: concept
- id: DPE-01-06
  knowledge: '1.6 Partitioning Fundamentals: Partition Pruning / Cardinality / Good / Bad Partition Keys / Over-Partitioning
    / Partition vs File'
  kind: concept
- id: DPE-01-07
  knowledge: '1.7 Bucketing / Sorting / Indexing: Bucketing / Sorting / Clustering / Lakehouse Indexing vs OLTP
    Index'
  kind: concept
- id: DPE-02-01
  knowledge: '2.1 Event Modeling: 주요 필드 / Event ID / Event Time / Ingestion Time / Producer Timestamp / Trace /
    Session Identifier'
  kind: concept
- id: DPE-02-02
  knowledge: '2.2 Event Contracts: 해당 절의 개념·예시·제약 전체'
  kind: concept
- id: DPE-02-03
  knowledge: '2.3 Schema Evolution: JSON vs Avro vs Protobuf / JSON / Avro / Protobuf / Schema Registry / Backward
    Compatibility / Forward Compatibility / Breaking Change'
  kind: concept
- id: DPE-02-04
  knowledge: '2.4 Delivery Semantics: At-Most-Once / At-Least-Once / Exactly-Once / Idempotency / Deduplication'
  kind: concept
- id: DPE-02-05
  knowledge: '2.5 Replay: Offset Replay / Downstream Rebuild / Backfill from Kafka / Replay Safety'
  kind: concept
- id: DPE-02-06
  knowledge: '2.6 Event → Serving + Lakehouse Dual Path: 해당 절의 개념·예시·제약 전체'
  kind: concept
- id: DPE-03-01
  knowledge: '3.1 Lakehouse Architecture: Data Plane vs Control Plane'
  kind: concept
- id: DPE-03-02
  knowledge: '3.2 Iceberg Metadata Internals: Metadata JSON / Current Snapshot / Snapshot Log / Manifest List /
    Manifest File / Data Files / Delete Files'
  kind: concept
- id: DPE-03-03
  knowledge: '3.3 Snapshot Semantics: Time Travel / Rollback / Consistent Read / Snapshot Isolation Intuition'
  kind: concept
- id: DPE-03-04
  knowledge: '3.4 Atomic Commit Model: Compare-and-Swap Intuition / Orphan Files'
  kind: concept
- id: DPE-03-05
  knowledge: '3.5 Partitioning in Iceberg: Partition Transforms / Partition Evolution / High Cardinality Design'
  kind: concept
- id: DPE-03-06
  knowledge: '3.6 Query Pruning: Scan Amplification'
  kind: concept
- id: DPE-03-07
  knowledge: '3.7 Sort Order and Clustering: 해당 절의 개념·예시·제약 전체'
  kind: concept
- id: DPE-03-08
  knowledge: '3.8 UPDATE / DELETE / MERGE: Copy-on-Write / Merge-on-Read / Position Delete / Equality Delete / UPDATE
    / MERGE'
  kind: concept
- id: DPE-03-09
  knowledge: '3.9 Maintenance: Data File Compaction / Delete File Rewrite / Manifest Rewrite / Snapshot Expiration
    / Orphan Cleanup'
  kind: concept
- id: DPE-03-10
  knowledge: '3.10 Catalogs: 해당 절의 개념·예시·제약 전체'
  kind: concept
- id: DPE-03-11
  knowledge: '3.11 Catalog vs Governance: Catalog 기본 역할 / Governance / Unity Catalog와 Iceberg Catalog'
  kind: concept
- id: DPE-04-01
  knowledge: '4.1 Spark Architecture: Driver / Executor / Cluster Manager'
  kind: concept
- id: DPE-04-02
  knowledge: '4.2 Execution Model: Job / Stage / Task / Spark Partition / DAG'
  kind: concept
- id: DPE-04-03
  knowledge: '4.3 Lazy Evaluation: Transformation / Action / Query Planning'
  kind: concept
- id: DPE-04-04
  knowledge: '4.4 Narrow vs Wide Dependencies: Narrow Dependency / Wide Dependency'
  kind: concept
- id: DPE-04-05
  knowledge: '4.5 Shuffle: 해당 절의 개념·예시·제약 전체'
  kind: concept
- id: DPE-04-06
  knowledge: '4.6 Join Strategies: Broadcast Hash Join / Sort-Merge Join / Shuffle Hash Join / Fact + Dimension
    / Large-Large Join / Semi / Anti Join / Join Cardinality / Join Explosion'
  kind: concept
- id: DPE-04-07
  knowledge: '4.7 Partition Management: repartition / coalesce / Keyed Repartitioning / Task Parallelism / Target
    Partition Size / Output File Count'
  kind: concept
- id: DPE-04-08
  knowledge: '4.8 Cache / Persist: 왜 사용하나 / unpersist / Cache가 항상 좋은 것은 아님 / Durable Iceberg Intermediate Table'
  kind: concept
- id: DPE-04-09
  knowledge: '4.9 Data Skew: Hot Key / Skewed Join / Aggregation / Null / Default Key Skew / Salting / Pre-Aggregation
    / Heavy-Key Special Path / AQE'
  kind: concept
- id: DPE-04-10
  knowledge: '4.10 Spark Performance Engineering: Executor Sizing / Spill / Straggler / Speculative Execution /
    Spark UI'
  kind: concept
- id: DPE-04-11
  knowledge: '4.11 Spark + Iceberg: Iceberg Scan Planning / Predicate Pushdown / Pruning / Spark Tasks vs Iceberg
    Files / Write Distribution / Target File Size / Sort Order / MERGE / Write Skew / Commit Behavior / Maintenance
    Debt'
  kind: concept
- id: DPE-04-12
  knowledge: '4.12 Structured Streaming: Kafka Source / Checkpoint / State / Event Time / Late Events / Watermark
    / Window / Deduplication / Output Modes / foreachBatch / Streaming → Iceberg / Streaming vs Batch Backfill'
  kind: concept
- id: DPE-04-13
  knowledge: '4.13 Spark의 역할: 해당 절의 개념·예시·제약 전체'
  kind: concept
- id: DPE-04-14
  knowledge: '4.14 Spark를 써도 dbt가 필요한가?: 해당 절의 개념·예시·제약 전체'
  kind: concept
- id: DPE-05-01
  knowledge: '5.1 Why Flink: 해당 절의 개념·예시·제약 전체'
  kind: concept
- id: DPE-05-02
  knowledge: '5.2 Flink Architecture: JobManager / TaskManager / Operator / Parallelism / Task Slot'
  kind: concept
- id: DPE-05-03
  knowledge: '5.3 DataStream Model: Source / Transformation / Sink / KeyBy'
  kind: concept
- id: DPE-05-04
  knowledge: '5.4 Event Time: 해당 절의 개념·예시·제약 전체'
  kind: concept
- id: DPE-05-05
  knowledge: '5.5 Watermark: 해당 절의 개념·예시·제약 전체'
  kind: concept
- id: DPE-05-06
  knowledge: '5.6 Window: Tumbling Window / Sliding Window / Session Window'
  kind: concept
- id: DPE-05-07
  knowledge: '5.7 State: Keyed State / ValueState / ListState / MapState / State TTL'
  kind: concept
- id: DPE-05-08
  knowledge: '5.8 Checkpoint: Distributed Snapshot / Checkpoint Barrier / Aligned Checkpoint / Unaligned Checkpoint'
  kind: concept
- id: DPE-05-09
  knowledge: '5.9 Savepoint: 해당 절의 개념·예시·제약 전체'
  kind: concept
- id: DPE-05-10
  knowledge: '5.10 Exactly-Once Processing: 해당 절의 개념·예시·제약 전체'
  kind: concept
- id: DPE-05-11
  knowledge: '5.11 Backpressure: 해당 절의 개념·예시·제약 전체'
  kind: concept
- id: DPE-05-12
  knowledge: '5.12 Flink + Kafka: Kafka Partition과 Flink Parallelism / Offset / Timestamp / Ordering / Kafka Partitioning
    vs Flink keyBy'
  kind: concept
- id: DPE-05-13
  knowledge: '5.13 Flink + Iceberg: Streaming Append / Commit Coordination / Small File Problem / Compaction / Flink
    + Spark Role Split / Update / Upsert'
  kind: concept
- id: DPE-05-14
  knowledge: '5.14 Flink vs Spark: Flink가 잘 맞는 경우 / Spark가 잘 맞는 경우'
  kind: concept
- id: DPE-06-01
  knowledge: 로그 기반 CDC와 polling SQL의 부하·삭제·순서·지연 한계, PostgreSQL WAL 경로
  kind: concept
- id: DPE-06-02
  knowledge: DB별 connector, Kafka Connect, 처리 offset, 초기 snapshot 역할
  kind: concept
- id: DPE-06-03
  knowledge: 기존 데이터와 snapshot 중·후 변경의 연결, offset 및 snapshot mode에 따른 재시작
  kind: concept
- id: DPE-06-04
  knowledge: before/after, c/u/d/r, source/transaction metadata 및 replica identity 제약
  kind: concept
- id: DPE-06-05
  knowledge: 동일 entity/key 순서, Kafka partition 순서와 cross-table transaction 경계
  kind: concept
- id: DPE-06-06
  knowledge: DELETE와 tombstone 구분, 물리·논리 삭제, history와 current state
  kind: concept
- id: DPE-06-07
  knowledge: 추가·삭제·rename·type·nullable 변경 및 전체 downstream 호환성 검증
  kind: concept
- id: DPE-06-08
  knowledge: history/current-state, INSERT/UPDATE MERGE, late sequence 방어와 replay idempotency
  kind: concept
- id: DPE-06-09
  knowledge: connector restart·stored offset·WAL replay, 중복과 offset/WAL 손실 복구
  kind: concept
- id: DPE-07-01
  knowledge: DAG/task/dependency/schedule와 Extract→Spark→dbt→quality→publish
  kind: concept
- id: DPE-07-02
  knowledge: Python/SQL/Bash/Spark/dbt operator와 orchestration/compute/query 역할
  kind: concept
- id: DPE-07-03
  knowledge: 일시·영구 실패 구분, retry idempotency, append 대비 overwrite/MERGE/replace
  kind: concept
- id: DPE-07-04
  knowledge: 장애·버그·누락·컬럼·업무 로직 변경의 full/partial backfill
  kind: concept
- id: DPE-07-05
  knowledge: 파일·DAG·데이터 준비 sensor, schedule과 dependency 차이, polling/event
  kind: concept
- id: DPE-07-06
  knowledge: process/start/end date, environment, data_interval과 명시적 과거 구간
  kind: concept
- id: DPE-07-07
  knowledge: task별 재실행, trigger rule 조건, DAG/task/time/retry/error alert
  kind: concept
- id: DPE-07-08
  knowledge: worker 대규모 compute, 큰 XCom, 복잡한 DAG 의존성, streaming 대용 오용
  kind: concept
- id: DPE-08-01
  knowledge: models/sources/tests/macros 및 staging/intermediate/marts 파일 구조
  kind: concept
- id: DPE-08-02
  knowledge: ref SQL 예시, dependency/DAG/lineage/environment relation, source와 차이
  kind: concept
- id: DPE-08-03
  knowledge: rename/type/null/date/column 정규화와 business logic 경계
  kind: concept
- id: DPE-08-04
  knowledge: staging join/aggregation 재사용과 작은 project의 생략 선택
  kind: concept
- id: DPE-08-05
  knowledge: fact/dimension/consumption mart, Gold와의 개념적 관계
  kind: concept
- id: DPE-08-06
  knowledge: append/merge/filter/late lookback/full refresh와 adapter·키 제약
  kind: concept
- id: DPE-08-07
  knowledge: not_null/unique/relationships/accepted_values/custom와 run→test→publish
  kind: concept
- id: DPE-08-08
  knowledge: current-state snapshot SCD2, type1과 비교, CDC history 중복 여부
  kind: concept
- id: DPE-08-09
  knowledge: table/column metadata, raw LLM call→daily usage lineage 및 범위
  kind: concept
- id: DPE-08-10
  knowledge: SQL definition와 engine execution, Databricks/Snowflake/Trino, Spark 공존
  kind: concept
- id: DPE-09-01
  knowledge: order/order item/LLM call grain, join 중복 집계, grain→fact→dimension→metric
  kind: concept
- id: DPE-09-02
  knowledge: event/transaction/periodic/accumulating fact 및 주문 lifecycle timestamps
  kind: concept
- id: DPE-09-03
  knowledge: customer/product/model/team dimension, natural/surrogate key와 SCD2
  kind: concept
- id: DPE-09-04
  knowledge: fact_llm_call 중심 agent/team/model/date star schema와 BI 장점
  kind: concept
- id: DPE-09-05
  knowledge: SCD1 overwrite, SCD2 customer_sk/id/region/valid_from/to와 과거 분석
  kind: concept
- id: DPE-09-06
  knowledge: OLTP normalization vs OLAP denormalization, 과도한 단일 wide table 한계
  kind: concept
- id: DPE-09-07
  knowledge: agent execution/LLM call/user event의 분리 grain, 모든 예시 필드와 conformed dimension
  kind: concept
- id: DPE-09-08
  knowledge: base/derived metric, error-rate 식, DAU/cost/error/latency semantic layer
  kind: concept
- id: DPE-10-01
  knowledge: coordinator SQL/plan/stage/task, worker scan/join/aggregation, Spark 비유 한계
  kind: concept
- id: DPE-10-02
  knowledge: Iceberg/PostgreSQL/Hive connector, catalog.schema.table 예시, federation 비용
  kind: concept
- id: DPE-10-03
  knowledge: SQL→plan→stage/task/split, worker exchange 및 join/groupby
  kind: concept
- id: DPE-10-04
  knowledge: predicate/projection/aggregation pushdown와 Iceberg pruning, 지원 범위
  kind: concept
- id: DPE-10-05
  knowledge: broadcast tiny dimension vs partitioned large join, exchange와 skew
  kind: concept
- id: DPE-10-06
  knowledge: worker/query memory, spill disk 비용 및 legacy·비보장 제약
  kind: concept
- id: DPE-10-07
  knowledge: interactive BI/ad hoc/concurrent SQL vs ETL/backfill/large join/ML/batch 역할
  kind: concept
- id: DPE-10-08
  knowledge: S3/Parquet/Iceberg metadata/Trino/BI 역할과 selective file/column scan
  kind: concept
- id: DPE-11-01
  knowledge: 'Quality Dimensions: ### Completeness 필수 데이터가 빠지지 않았는가. ### Uniqueness 중복되면 안 되는 값이 중복되지 않았는가. ###
    Validity 허용된 형식/범위인가. ### Consistency 다른 데이터와 모순되지 않는가. ### Freshness 제시간에 들어왔는가. ### Accuracy 실제 세계의 값과 맞는가.
    ### Volume 데이터 양이 정상 범위인가. AI 예: ```text fact_llm_call Completeness → model_id NULL? Uniqueness → llm_call_id
    중복? Validity → negative latency? Consistency → model_id가 dim_model에 존재? Freshness → 최근 Event 5분 이내? Accuracy
    → billing과 cost 일치? Volume → 호출량 급증/급감? ```'
  kind: concept
- id: DPE-11-02
  knowledge: 'Validation Layers: ### Ingestion Validation - Schema - Format - Required Field - Parsing ### Silver
    Validation - Dedup - Relationships - Business Rules - Valid Values ### Gold Validation - KPI - Freshness - Aggregate
    Consistency - Expected Volume 핵심: ```text 초기 → 형식 중간 → 데이터 논리 최종 → 비즈니스 결과 ```'
  kind: concept
- id: DPE-11-03
  knowledge: 'Quarantine Patterns: Invalid Data를 버리지 않고 별도 보관. ```text Incoming ↓ Validation ↙ ↘ Valid Invalid ↓
    ↓ Silver Quarantine ``` Quarantine에: - Raw payload - Error type - Error message - Received time 등을 저장. 문제 수정
    후 Reprocessing. Quarantine이 쌓이기만 하면 안 되며 Volume/Error Reason Monitoring도 필요하다.'
  kind: concept
- id: DPE-11-04
  knowledge: 'dbt Tests: Data Quality 관점의 dbt Test: - not_null - unique - relationships - accepted_values 강점: -
    Model/Table 수준 정적 검증 부족할 수 있는 영역: - Volume anomaly - Distribution drift - Freshness anomaly'
  kind: concept
- id: DPE-11-05
  knowledge: 'Soda / Great Expectations / Deequ: 공통: > **Data Quality Rule 자동 검사 도구** ### Soda Rule/check 중심. ###
    Great Expectations Expectation 기반 검증. ### Deequ Spark 환경 대규모 Data Quality 검사에 친화적. 세 도구는 기능이 많이 겹치며 이 세션에서는
    각각의 구현보다 범주를 이해하는 것이 목표였다.'
  kind: concept
- id: DPE-11-06
  knowledge: 'Data Quality SLOs: SLI: > 실제 측정값. SLO: > 목표 수준. 예: ```text Freshness < 5 min Completeness > 99.9%
    Duplicate Rate < 0.01% ``` Dataset마다 SLO가 달라야 한다. 실시간 Dashboard와 월간 Report는 필요한 Freshness가 다르다.'
  kind: concept
- id: DPE-11-07
  knowledge: 'Incident Handling: 흐름: ```text Detect ↓ Contain ↓ Fix ↓ Reprocess ↓ Verify ``` ### Detect SLO 위반 감지.
    ### Contain 잘못된 Data의 Downstream 전파 차단. ### Fix Root Cause 수정. ### Reprocess Backfill / Replay. ### Verify Quality
    Check 후 재개. 중요: > **서비스가 살아 있어도 데이터가 틀리면 Data Incident다.**'
  kind: concept
- id: DPE-12-01
  knowledge: 'Data Freshness: ### Source Freshness 원본 데이터가 제시간에 생성/수집되는가. ### Pipeline Freshness Kafka → Bronze
    → Silver → Gold 처리 지연. ### Downstream Freshness Dashboard/BI가 최신 데이터를 보여주는가. 단계별 Freshness를 보면 어느 구간부터 지연됐는지
    찾을 수 있다.'
  kind: concept
- id: DPE-12-02
  knowledge: 'Volume Monitoring: 평소 대비 데이터 건수 급감/급증 탐지. 급감 원인 예: - 수집 장애 - Producer 문제 - Filter Bug 급증 원인 예: - Duplicate
    - Replay - Retry Storm - Traffic Spike Missing Partition도 중요한 Signal. 단순 절대값이 아니라: - 최근 평균 - 같은 요일 - Seasonal
    pattern 등과 비교할 수 있다.'
  kind: concept
- id: DPE-12-03
  knowledge: 'Schema Monitoring: 감시: - Column 추가 - 삭제 - Rename - Type 변경 - Nullable 변경 Breaking Change는 Downstream
    Consumer를 깨뜨릴 수 있다. Schema Monitoring + Lineage를 연결하면 영향 범위를 찾을 수 있다.'
  kind: concept
- id: DPE-12-04
  knowledge: 'Distribution Drift: Volume은 정상인데 값 분포가 달라질 수 있다. 대표 Signal: - Null Rate Drift - Cardinality Drift
    - Value Distribution Drift - Numeric Distribution Drift 예: ```text 평소 FAILED = 5% 오늘 FAILED = 45% ``` Volume은
    정상이어도 Data Health는 이상할 수 있다.'
  kind: concept
- id: DPE-12-05
  knowledge: 'Pipeline Health vs Data Health: Pipeline Health: - Job Status - Kafka Lag - Runtime - CPU/Memory -
    Failure Data Health: - Freshness - Volume - Schema - Null - Duplicate - Distribution 중요 문장: > **Green Pipeline
    ≠ Healthy Data** Job이 성공해도 Query Logic이 잘못돼 결과가 0 rows일 수 있다.'
  kind: concept
- id: DPE-12-06
  knowledge: 'Data SLIs / SLOs: Observability 관점에서 Data State를 지속 측정한다. SLI 예: ```text Freshness = 3분 NULL Rate
    = 0.5% Volume = 98M ``` SLO 예: ```text Freshness < 5분 NULL Rate < 1% Volume Deviation < 20% ``` 여러 Signal을 동시에
    본다.'
  kind: concept
- id: DPE-12-07
  knowledge: 'Alert Design: 목표: > **이상을 최대한 많이 알리는 것이 아니라 실제 대응할 가치가 있는 Alert를 만드는 것** ### Noisy Alert Threshold
    근처에서 ALERT/RECOVERY가 반복. ### Actionable Alert 알림만 보고도 어디를 조사할지 알 수 있음. 좋은 Alert: ```text Threshold + Duration
    + Severity + Context ``` Warning / Critical을 나눌 수 있다. Dataset 중요도 Tier별 Alert 정책도 가능. Alert Fatigue를 방지해야 한다.'
  kind: concept
- id: DPE-13-01
  knowledge: 'Metadata Types: Metadata: > **데이터를 설명하는 데이터** ### Technical Metadata - Table - Column - Type - Schema
    - Partition - File Format 질문: > 구조가 어떻게 생겼는가? ### Operational Metadata - Last Updated - Job Status - Freshness
    - Row Count - Processing Time 질문: > 지금 정상적으로 운영되는가? ### Business Metadata - Description - Owner - KPI Definition
    - Business Term - Classification 질문: > 이 데이터는 업무적으로 무엇을 의미하는가?'
  kind: concept
- id: DPE-13-01A
  knowledge: 'Business Metadata vs Semantic Layer: 세션 중 보충 질문: > Business Metadata는 Semantic Layer와 유사해 보인다. 답:
    > **겹치는 부분은 많지만 동일하지 않다.** Business Metadata: > 데이터의 의미를 설명. 예: ```text Revenue → VAT 제외 → Refund 제외 → Owner:
    Finance ``` Semantic Layer: > 의미를 실제 계산 가능한 Metric/Dimension 정의로 제공. 예: ```text Revenue = SUM(order_amount)
    - SUM(refund) - SUM(vat) ``` 관계: ```text Business Metadata → "Revenue가 무엇인가?" Semantic Layer → "Revenue를 어떻게
    계산하는가?" BI / Dashboard / AI → 동일 정의 사용 ``` Semantic Layer는 Business Metadata의 **실행 가능한 분석 정의**를 구체화한 계층으로 이해하면
    좋다.'
  kind: concept
- id: DPE-13-02
  knowledge: 'Dataset Lineage: Dataset Lineage: > **Source → Job → Target 관계** 예: ```text raw_user_events ↓ Spark
    Job ↓ silver_user_events ↓ dbt ↓ mart_daily_users ``` ### Upstream 나를 만드는 쪽. ### Downstream 나를 사용하는 쪽. 활용: -
    Root Cause - Impact Analysis - Data Trust'
  kind: concept
- id: DPE-13-03
  knowledge: 'OpenLineage: OpenLineage: > **서로 다른 Data Tool이 Lineage 정보를 공통 형식으로 표현하는 표준** 핵심 Entity: ### Job 어떤
    작업인가. ### Run 특정 Job의 실행 1회. ### Dataset Input / Output Data. 예: ```text bronze.orders ↓ Job: transform_orders
    ↓ silver.orders ``` OpenLineage는 UI 자체라기보다 **Lineage Event Standard**다.'
  kind: concept
- id: DPE-13-04
  knowledge: 'Column-Level Lineage: Table-Level보다 더 세밀한 Column 관계. 예: ```text raw_orders.amount ────┐ ├→ silver_orders.net_amount
    raw_orders.discount ──┘ ``` 활용: - KPI Root Cause - Schema Change Impact - Sensitive Data Tracking'
  kind: concept
- id: DPE-13-05
  knowledge: 'Impact Analysis: Lineage를 이용해 변경/장애 영향 확인. ### Upstream Analysis 문제 원인을 거슬러 올라감. ### Downstream Impact
    Analysis 변경이 어디까지 영향을 주는지 확인. 예: ```text raw_orders.amount type 변경 ↓ stg_orders ↓ fact_sales ↓ mart_daily_sales
    ↓ Dashboard ```'
  kind: concept
- id: DPE-13-06
  knowledge: 'Marquez: Marquez: > **OpenLineage Event를 저장하고 조회/시각화하는 Lineage System** 관계: ```text OpenLineage →
    표준 Marquez → 수집/저장/UI/API ``` Marquez는 Catalog 전체보다 Lineage/Run 관계에 초점이 강하다.'
  kind: concept
- id: DPE-13-07
  knowledge: 'Catalog Integration: Catalog에 여러 정보를 통합. ```text Iceberg → Technical Metadata dbt → Model / Documentation
    / Dependencies Airflow → Pipeline / Runs OpenLineage → Lineage Quality Tool → Data Quality ``` Catalog에서 볼 수
    있는 정보: - Description - Owner - Freshness - Quality - Upstream / Downstream - Classification - Access Policy
    현대 Catalog는 단순 Table 목록이 아니라: ```text Discovery + Metadata + Lineage + Governance ``` 로 발전한다.'
  kind: concept
- id: DPE-14-01
  knowledge: 'Dataset Ownership: Dataset마다 책임 주체를 명확히 한다. ### Technical Owner - Pipeline - Schema - Quality - SLO
    ### Business Owner - 의미 - KPI - 업무 정의 Owner가 없으면 문제/변경 대응이 어려워진다.'
  kind: concept
- id: DPE-14-02
  knowledge: 'Classification: 데이터 중요도/민감도 분류. 예: - Public - Internal - Confidential - PII - Sensitive Column-level
    Classification도 중요하다. 예: ```text email → PII team_id → Internal ``` Classification은 Access / Masking / Retention
    Policy와 연결된다.'
  kind: concept
- id: DPE-14-03
  knowledge: 'Retention Policies: Retention: > **얼마나 오래 보관할 것인가** 기준: - 비용 - 법/규제 - 민감도 - 분석 가치 예: ```text Debug
    Log → 14일 User Event → 1년 Aggregated Metrics → 장기 보관 ``` Hot / Cold / Archive Tier로 나눌 수도 있다. Iceberg Snapshot
    Expiration도 Retention과 연결된다.'
  kind: concept
- id: DPE-14-04
  knowledge: 'Deletion Policies: Deletion: > **언제, 어디서, 어떤 방식으로 실제 제거할 것인가** 원본만 삭제해서 끝나지 않을 수 있다. ```text PostgreSQL
    ↓ Kafka ↓ Bronze ↓ Silver ↓ Gold ↓ Backup ``` 모든 Copy/Derived Data를 고려해야 한다. ### Logical Delete 삭제 표시. ### Physical
    Delete 실제 제거. Iceberg에서는 현재 Snapshot에서 안 보인다고 물리적으로 완전히 삭제된 것은 아닐 수 있다. 과거 Snapshot/File cleanup까지 고려해야 한다.'
  kind: concept
- id: DPE-14-05
  knowledge: 'Masking: 민감한 실제 값을 가려서 보여준다. ### Static Masking 가린 값 자체를 별도 저장. ### Dynamic Masking 조회 User/Role에
    따라 다르게 표시. Classification과 연결: ```text PII ↓ Masking Policy ``` AI Prompt/Response에도 PII Masking이 필요할 수 있다.
    Masking과 Encryption은 다르다.'
  kind: concept
- id: DPE-14-06
  knowledge: 'Row / Column Access: ### Row-Level Access 사용자/팀별로 볼 수 있는 row 제한. ### Column-Level Access 민감 column
    자체 조회 제한. Masking과 차이: ```text Column Access → Column을 못 봄 Masking → Column은 보이지만 값이 가려짐 ``` ### RBAC Role 단위
    권한 관리.'
  kind: concept
- id: DPE-14-07
  knowledge: 'Auditability: 누가 언제 어떤 데이터에 접근/변경했는지 기록. Access Audit: ```text user dataset time action query ```
    Change Audit: - Schema 변경 - Policy 변경 - Owner 변경 - Retention 변경 Observability와 차이: ```text Observability → 시스템/데이터가
    정상인가? Audit → 누가 무엇을 했는가? ```'
  kind: concept
- id: DPE-14-08
  knowledge: 'Data Contracts: Producer와 Consumer 사이 데이터 약속. 포함 가능: - Schema - Semantics - Quality - SLO - Ownership
    - Version 예: ```text event_id → required + unique latency_ms → integer → millisecond → >= 0 Freshness → < 5
    min Owner → AI Platform Team ``` Schema Contract보다 넓은 개념이다.'
  kind: concept
- id: DPE-14-09
  knowledge: '14.9 Governance Platforms: Databricks Unity Catalog / AWS Lake Formation / Snowflake Horizon Catalog'
  kind: concept
- id: DPE-15-01
  knowledge: What Makes Data AI-Ready
  kind: concept
- id: DPE-15-02
  knowledge: AI Telemetry Model
  kind: concept
- id: DPE-15-02A
  knowledge: Langfuse as AI Telemetry / Evaluation Layer
  kind: concept
- id: DPE-15-03
  knowledge: Dataset Versioning
  kind: concept
- id: DPE-15-04
  knowledge: Reproducibility
  kind: concept
- id: DPE-15-05
  knowledge: Evaluation Dataset Construction
  kind: concept
- id: DPE-15-06
  knowledge: Embedding Data
  kind: concept
- id: DPE-15-07
  knowledge: Retrieval Metadata
  kind: concept
- id: DPE-15-08
  knowledge: Provenance
  kind: concept
- id: DPE-15-09
  knowledge: Feature / Label Freshness
  kind: concept
- id: DPE-16-01
  knowledge: Online Evaluation Events
  kind: concept
- id: DPE-17-01
  knowledge: 전체 기술 역할 맵
  kind: concept
- id: DPE-17-02
  knowledge: Storage / Table / Compute / Query / Transformation 구분
  kind: concept
- id: DPE-17-03
  knowledge: Data Quality vs Data Observability
  kind: concept
- id: DPE-17-04
  knowledge: Metadata / Catalog / Semantic Layer 차이
  kind: concept
- id: DPE-17-05
  knowledge: AI Observability vs General Data Platform
  kind: concept
- id: DPE-18-01
  knowledge: Phase 1~15 학습 완료 범위
  kind: progress
- id: DPE-18-02
  knowledge: Phase 16은 16.1만 완료; 16.2~16.11 후속 과정
  kind: curriculum
- id: DPE-18-03
  knowledge: 미학습 Phase 17 Databricks Deep Dive의 전체 목차
  kind: curriculum
- id: DPE-18-04
  knowledge: 미학습 Phase 18 Snowflake Deep Dive의 전체 목차
  kind: curriculum
- id: DPE-18-05
  knowledge: 미학습 Phase 19 제품 및 Open Lakehouse 비교 기준
  kind: curriculum
- id: DPE-18-06
  knowledge: 미학습 Phase 20 운영 엔지니어링 목차
  kind: curriculum
- id: DPE-18-07
  knowledge: 미학습 Phase 21 최종 프로젝트 목표 구조와 검증 질문
  kind: curriculum
- id: DPE-19-01
  knowledge: 최종 mental model의 데이터 경로와 횡단 관심사·역할 구분
  kind: concept
---

# 추출한 지식과 원문 위치

문서 작성 전에 4개 담당 영역에서 추출·매핑했다. ID는 원문의 의미 구간을 묶는 단위이며, 세부 지식 수와 동일하지 않다. 원문 행 번호는 `source.md`의 ORIGINAL SOURCE START 경계 다음부터 시작한다.

## DPE-00-01

- 원문 위치: `문서 목적 / 학습 방식 / 주의`.
- 범위: 학습 목적·개념 중심 깊이와 Chapter 1~4 복원 노트라는 출처 제약.
- 목적지: `data-platform/curriculum.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-01-01

- 원문 위치: 원문 47–151행, `1.1 OLTP vs OLAP`.
- 범위: OLTP; OLAP; PostgreSQL이 분석 이력에 점점 불리해지는 이유.
- 목적지: `data-platform/foundations.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-01-02

- 원문 위치: 원문 152–245행, `1.2 Row-Oriented vs Column-Oriented Storage`.
- 범위: Row-Oriented; Column-Oriented; Compression; Column Pruning.
- 목적지: `data-platform/foundations.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-01-03

- 원문 위치: 원문 246–377행, `1.3 Parquet`.
- 범위: Row Group; Page; Encoding / Compression; Statistics; Predicate Pushdown / Pruning; Column Pruning.
- 목적지: `data-platform/foundations.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-01-04

- 원문 위치: 원문 378–448행, `1.4 Object Storage`.
- 범위: Object vs Block/File Storage; Storage / Compute Separation; Remote I/O.
- 목적지: `data-platform/foundations.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-01-05

- 원문 위치: 원문 449–519행, `1.5 File Layout Engineering`.
- 범위: Small File Problem; Too-Large File; Compaction; Write Amplification.
- 목적지: `data-platform/foundations.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-01-06

- 원문 위치: 원문 520–614행, `1.6 Partitioning Fundamentals`.
- 범위: Partition Pruning; Cardinality; Good / Bad Partition Keys; Over-Partitioning; Partition vs File.
- 목적지: `data-platform/foundations.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-01-07

- 원문 위치: 원문 615–666행, `1.7 Bucketing / Sorting / Indexing`.
- 범위: Bucketing; Sorting; Clustering; Lakehouse Indexing vs OLTP Index.
- 목적지: `data-platform/foundations.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-02-01

- 원문 위치: 원문 672–736행, `2.1 Event Modeling`.
- 범위: 주요 필드; Event ID; Event Time; Ingestion Time; Producer Timestamp; Trace / Session Identifier.
- 목적지: `data-platform/event-architecture.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-02-02

- 원문 위치: 원문 737–773행, `2.2 Event Contracts`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/event-architecture.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-02-03

- 원문 위치: 원문 774–852행, `2.3 Schema Evolution`.
- 범위: JSON vs Avro vs Protobuf; JSON; Avro; Protobuf; Schema Registry; Backward Compatibility; Forward Compatibility; Breaking Change.
- 목적지: `data-platform/event-architecture.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-02-04

- 원문 위치: 원문 853–921행, `2.4 Delivery Semantics`.
- 범위: At-Most-Once; At-Least-Once; Exactly-Once; Idempotency; Deduplication.
- 목적지: `data-platform/event-architecture.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-02-05

- 원문 위치: 원문 922–972행, `2.5 Replay`.
- 범위: Offset Replay; Downstream Rebuild; Backfill from Kafka; Replay Safety.
- 목적지: `data-platform/event-architecture.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-02-06

- 원문 위치: 원문 973–1000행, `2.6 Event → Serving + Lakehouse Dual Path`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/event-architecture.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-03-01

- 원문 위치: 원문 1003–1052행, `3.1 Lakehouse Architecture`.
- 범위: Data Plane vs Control Plane.
- 목적지: `data-platform/lakehouse-iceberg.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-03-02

- 원문 위치: 원문 1053–1140행, `3.2 Iceberg Metadata Internals`.
- 범위: Metadata JSON; Current Snapshot; Snapshot Log; Manifest List / Manifest File; Data Files; Delete Files.
- 목적지: `data-platform/lakehouse-iceberg.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-03-03

- 원문 위치: 원문 1141–1180행, `3.3 Snapshot Semantics`.
- 범위: Time Travel; Rollback; Consistent Read; Snapshot Isolation Intuition.
- 목적지: `data-platform/lakehouse-iceberg.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-03-04

- 원문 위치: 원문 1181–1223행, `3.4 Atomic Commit Model`.
- 범위: Compare-and-Swap Intuition; Orphan Files.
- 목적지: `data-platform/lakehouse-iceberg.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-03-05

- 원문 위치: 원문 1224–1278행, `3.5 Partitioning in Iceberg`.
- 범위: Partition Transforms; Partition Evolution; High Cardinality Design.
- 목적지: `data-platform/lakehouse-iceberg.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-03-06

- 원문 위치: 원문 1279–1308행, `3.6 Query Pruning`.
- 범위: Scan Amplification.
- 목적지: `data-platform/lakehouse-iceberg.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-03-07

- 원문 위치: 원문 1309–1332행, `3.7 Sort Order and Clustering`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/lakehouse-iceberg.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-03-08

- 원문 위치: 원문 1333–1393행, `3.8 UPDATE / DELETE / MERGE`.
- 범위: Copy-on-Write; Merge-on-Read; Position Delete; Equality Delete; UPDATE; MERGE.
- 목적지: `data-platform/lakehouse-iceberg.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-03-09

- 원문 위치: 원문 1394–1423행, `3.9 Maintenance`.
- 범위: Data File Compaction; Delete File Rewrite; Manifest Rewrite; Snapshot Expiration; Orphan Cleanup.
- 목적지: `data-platform/lakehouse-iceberg.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-03-10

- 원문 위치: 원문 1424–1444행, `3.10 Catalogs`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/lakehouse-iceberg.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-03-11

- 원문 위치: 원문 1445–1492행, `3.11 Catalog vs Governance`.
- 범위: Catalog 기본 역할; Governance; Unity Catalog와 Iceberg Catalog.
- 목적지: `data-platform/lakehouse-iceberg.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-01

- 원문 위치: 원문 1495–1533행, `4.1 Spark Architecture`.
- 범위: Driver; Executor; Cluster Manager.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-02

- 원문 위치: 원문 1534–1569행, `4.2 Execution Model`.
- 범위: Job; Stage; Task; Spark Partition; DAG.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-03

- 원문 위치: 원문 1570–1621행, `4.3 Lazy Evaluation`.
- 범위: Transformation; Action; Query Planning.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-04

- 원문 위치: 원문 1622–1652행, `4.4 Narrow vs Wide Dependencies`.
- 범위: Narrow Dependency; Wide Dependency.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-05

- 원문 위치: 원문 1653–1678행, `4.5 Shuffle`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-06

- 원문 위치: 원문 1679–1740행, `4.6 Join Strategies`.
- 범위: Broadcast Hash Join; Sort-Merge Join; Shuffle Hash Join; Fact + Dimension; Large-Large Join; Semi / Anti Join; Join Cardinality / Join Explosion.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-07

- 원문 위치: 원문 1741–1780행, `4.7 Partition Management`.
- 범위: repartition; coalesce; Keyed Repartitioning; Task Parallelism; Target Partition Size / Output File Count.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-08

- 원문 위치: 원문 1781–1814행, `4.8 Cache / Persist`.
- 범위: 왜 사용하나; unpersist; Cache가 항상 좋은 것은 아님; Durable Iceberg Intermediate Table.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-09

- 원문 위치: 원문 1815–1860행, `4.9 Data Skew`.
- 범위: Hot Key; Skewed Join / Aggregation; Null / Default Key Skew; Salting; Pre-Aggregation; Heavy-Key Special Path; AQE.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-10

- 원문 위치: 원문 1861–1899행, `4.10 Spark Performance Engineering`.
- 범위: Executor Sizing; Spill; Straggler; Speculative Execution; Spark UI.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-11

- 원문 위치: 원문 1900–1955행, `4.11 Spark + Iceberg`.
- 범위: Iceberg Scan Planning; Predicate Pushdown / Pruning; Spark Tasks vs Iceberg Files; Write Distribution; Target File Size; Sort Order; MERGE; Write Skew; Commit Behavior; Maintenance Debt.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-12

- 원문 위치: 원문 1956–2029행, `4.12 Structured Streaming`.
- 범위: Kafka Source; Checkpoint; State; Event Time; Late Events; Watermark; Window; Deduplication; Output Modes; foreachBatch; Streaming → Iceberg; Streaming vs Batch Backfill.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-13

- 원문 위치: 원문 2030–2062행, `4.13 Spark의 역할`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-04-14

- 원문 위치: 원문 2063–2094행, `4.14 Spark를 써도 dbt가 필요한가?`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/spark.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-01

- 원문 위치: 원문 2097–2130행, `5.1 Why Flink`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-02

- 원문 위치: 원문 2131–2164행, `5.2 Flink Architecture`.
- 범위: JobManager; TaskManager; Operator; Parallelism; Task Slot.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-03

- 원문 위치: 원문 2165–2210행, `5.3 DataStream Model`.
- 범위: Source; Transformation; Sink; KeyBy.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-04

- 원문 위치: 원문 2211–2228행, `5.4 Event Time`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-05

- 원문 위치: 원문 2229–2269행, `5.5 Watermark`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-06

- 원문 위치: 원문 2270–2306행, `5.6 Window`.
- 범위: Tumbling Window; Sliding Window; Session Window.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-07

- 원문 위치: 원문 2307–2343행, `5.7 State`.
- 범위: Keyed State; ValueState; ListState; MapState; State TTL.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-08

- 원문 위치: 원문 2344–2381행, `5.8 Checkpoint`.
- 범위: Distributed Snapshot; Checkpoint Barrier; Aligned Checkpoint; Unaligned Checkpoint.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-09

- 원문 위치: 원문 2382–2412행, `5.9 Savepoint`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-10

- 원문 위치: 원문 2413–2444행, `5.10 Exactly-Once Processing`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-11

- 원문 위치: 원문 2445–2489행, `5.11 Backpressure`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-12

- 원문 위치: 원문 2490–2538행, `5.12 Flink + Kafka`.
- 범위: Kafka Partition과 Flink Parallelism; Offset; Timestamp; Ordering; Kafka Partitioning vs Flink keyBy.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-13

- 원문 위치: 원문 2539–2586행, `5.13 Flink + Iceberg`.
- 범위: Streaming Append; Commit Coordination; Small File Problem; Compaction; Flink + Spark Role Split; Update / Upsert.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-05-14

- 원문 위치: 원문 2587–2622행, `5.14 Flink vs Spark`.
- 범위: Flink가 잘 맞는 경우; Spark가 잘 맞는 경우.
- 목적지: `data-platform/flink.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-06-01

- 원문 위치: 원문 2625–2670행, `6.1 CDC Fundamentals`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/cdc-debezium.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-06-02

- 원문 위치: 원문 2671–2695행, `6.2 Debezium Architecture`.
- 범위: Debezium Connector; Kafka Connect; Offset; Snapshot.
- 목적지: `data-platform/cdc-debezium.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-06-03

- 원문 위치: 원문 2696–2727행, `6.3 Initial Snapshot`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/cdc-debezium.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-06-04

- 원문 위치: 원문 2728–2780행, `6.4 CDC Event Structure`.
- 범위: INSERT; UPDATE; DELETE.
- 목적지: `data-platform/cdc-debezium.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-06-05

- 원문 위치: 원문 2781–2801행, `6.5 Ordering`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/cdc-debezium.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-06-06

- 원문 위치: 원문 2802–2837행, `6.6 Deletes`.
- 범위: DELETE Event; Tombstone; Physical Delete; Logical Delete; History vs Current State.
- 목적지: `data-platform/cdc-debezium.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-06-07

- 원문 위치: 원문 2838–2888행, `6.7 Schema Changes`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/cdc-debezium.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-06-08

- 원문 위치: 원문 2889–2942행, `6.8 CDC → Iceberg`.
- 범위: History Table; Current-State Table; MERGE / Upsert; Late Change; Idempotency.
- 목적지: `data-platform/cdc-debezium.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-06-09

- 원문 위치: 원문 2943–2980행, `6.9 CDC Failure Recovery`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/cdc-debezium.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-07-01

- 원문 위치: 원문 2983–3024행, `7.1 DAG Fundamentals`.
- 범위: DAG; Task; Dependency; Schedule.
- 목적지: `data-platform/orchestration.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-07-02

- 원문 위치: 원문 3025–3056행, `7.2 Operators / Tasks`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/orchestration.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-07-03

- 원문 위치: 원문 3057–3096행, `7.3 Retries`.
- 범위: Transient Failure; Permanent Failure; Idempotency.
- 목적지: `data-platform/orchestration.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-07-04

- 원문 위치: 원문 3097–3122행, `7.4 Backfills`.
- 범위: Full Backfill; Partial / Partition Backfill.
- 목적지: `data-platform/orchestration.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-07-05

- 원문 위치: 원문 3123–3146행, `7.5 Sensors / Event Dependencies`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/orchestration.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-07-06

- 원문 위치: 원문 3147–3176행, `7.6 Parameterization`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/orchestration.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-07-07

- 원문 위치: 원문 3177–3204행, `7.7 Failure Handling`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/orchestration.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-07-08

- 원문 위치: 원문 3205–3234행, `7.8 Orchestrator Anti-Patterns`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/orchestration.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-08-01

- 원문 위치: 원문 3237–3274행, `8.1 Project Structure`.
- 범위: Models; Sources; Tests; Macros.
- 목적지: `data-platform/dbt.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-08-02

- 원문 위치: 원문 3275–3308행, `8.2 ref()`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/dbt.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-08-03

- 원문 위치: 원문 3309–3326행, `8.3 Staging Models`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/dbt.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-08-04

- 원문 위치: 원문 3327–3348행, `8.4 Intermediate Models`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/dbt.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-08-05

- 원문 위치: 원문 3349–3381행, `8.5 Marts`.
- 범위: Fact; Dimension; Consumption Table.
- 목적지: `data-platform/dbt.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-08-06

- 원문 위치: 원문 3382–3409행, `8.6 Incremental Models`.
- 범위: Append; Merge; Incremental Filter; Full Refresh.
- 목적지: `data-platform/dbt.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-08-07

- 원문 위치: 원문 3410–3435행, `8.7 dbt Tests`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/dbt.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-08-08

- 원문 위치: 원문 3436–3455행, `8.8 Snapshots`.
- 범위: Type 1; Type 2.
- 목적지: `data-platform/dbt.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-08-09

- 원문 위치: 원문 3456–3479행, `8.9 Documentation / Lineage`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/dbt.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-08-10

- 원문 위치: 원문 3480–3505행, `8.10 dbt + Databricks / Snowflake / Trino`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/dbt.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-09-01

- 원문 위치: 원문 3508–3539행, `9.1 Grain`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/analytical-modeling.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-09-02

- 원문 위치: 원문 3540–3572행, `9.2 Fact Tables`.
- 범위: Event Fact; Transaction Fact; Periodic Snapshot Fact; Accumulating Snapshot Fact.
- 목적지: `data-platform/analytical-modeling.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-09-03

- 원문 위치: 원문 3573–3599행, `9.3 Dimension Tables`.
- 범위: Natural Key; Surrogate Key.
- 목적지: `data-platform/analytical-modeling.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-09-04

- 원문 위치: 원문 3600–3619행, `9.4 Star Schema`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/analytical-modeling.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-09-05

- 원문 위치: 원문 3620–3643행, `9.5 SCD`.
- 범위: Type 1; Type 2.
- 목적지: `data-platform/analytical-modeling.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-09-06

- 원문 위치: 원문 3644–3663행, `9.6 Denormalization`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/analytical-modeling.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-09-07

- 원문 위치: 원문 3664–3731행, `9.7 AI Platform Modeling`.
- 범위: fact_agent_execution; fact_llm_call; fact_user_event; dim_agent; dim_model; dim_team.
- 목적지: `data-platform/analytical-modeling.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-09-08

- 원문 위치: 원문 3732–3773행, `9.8 Metrics Modeling`.
- 범위: Base Metric; Derived Metric; Semantic Layer.
- 목적지: `data-platform/analytical-modeling.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-10-01

- 원문 위치: 원문 3776–3804행, `10.1 Architecture`.
- 범위: Coordinator; Worker.
- 목적지: `data-platform/trino.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-10-02

- 원문 위치: 원문 3805–3837행, `10.2 Connector Model`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/trino.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-10-03

- 원문 위치: 원문 3838–3875행, `10.3 Query Execution`.
- 범위: Stage; Task; Split; Exchange.
- 목적지: `data-platform/trino.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-10-04

- 원문 위치: 원문 3876–3897행, `10.4 Pushdown`.
- 범위: Predicate Pushdown; Projection Pushdown; Aggregation Pushdown.
- 목적지: `data-platform/trino.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-10-05

- 원문 위치: 원문 3898–3921행, `10.5 Join Strategies`.
- 범위: Broadcast Join; Partitioned Join; Data Skew.
- 목적지: `data-platform/trino.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-10-06

- 원문 위치: 원문 3922–3943행, `10.6 Memory`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/trino.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-10-07

- 원문 위치: 원문 3944–3981행, `10.7 Trino vs Spark`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/trino.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-10-08

- 원문 위치: 원문 3982–4017행, `10.8 Trino + Iceberg`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/trino.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-11-01

- 원문 위치: 원문 4020–4078행, `11.1 Quality Dimensions`.
- 범위: Completeness; Uniqueness; Validity; Consistency; Freshness; Accuracy; Volume.
- 목적지: `data-platform/data-quality.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-11-02

- 원문 위치: 원문 4079–4116행, `11.2 Validation Layers`.
- 범위: Ingestion Validation; Silver Validation; Gold Validation.
- 목적지: `data-platform/data-quality.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-11-03

- 원문 위치: 원문 4117–4145행, `11.3 Quarantine Patterns`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/data-quality.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-11-04

- 원문 위치: 원문 4146–4164행, `11.4 dbt Tests`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/data-quality.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-11-05

- 원문 위치: 원문 4165–4186행, `11.5 Soda / Great Expectations / Deequ`.
- 범위: Soda; Great Expectations; Deequ.
- 목적지: `data-platform/data-quality.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-11-06

- 원문 위치: 원문 4187–4210행, `11.6 Data Quality SLOs`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/data-quality.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-11-07

- 원문 위치: 원문 4211–4252행, `11.7 Incident Handling`.
- 범위: Detect; Contain; Fix; Reprocess; Verify.
- 목적지: `data-platform/data-quality.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-12-01

- 원문 위치: 원문 4255–4272행, `12.1 Data Freshness`.
- 범위: Source Freshness; Pipeline Freshness; Downstream Freshness.
- 목적지: `data-platform/data-observability.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-12-02

- 원문 위치: 원문 4273–4301행, `12.2 Volume Monitoring`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/data-observability.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-12-03

- 원문 위치: 원문 4302–4317행, `12.3 Schema Monitoring`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/data-observability.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-12-04

- 원문 위치: 원문 4318–4339행, `12.4 Distribution Drift`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/data-observability.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-12-05

- 원문 위치: 원문 4340–4366행, `12.5 Pipeline Health vs Data Health`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/data-observability.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-12-06

- 원문 위치: 원문 4367–4390행, `12.6 Data SLIs / SLOs`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/data-observability.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-12-07

- 원문 위치: 원문 4391–4424행, `12.7 Alert Design`.
- 범위: Noisy Alert; Actionable Alert.
- 목적지: `data-platform/data-observability.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-13-01

- 원문 위치: 원문 4427–4471행, `13.1 Metadata Types`.
- 범위: Technical Metadata; Operational Metadata; Business Metadata.
- 목적지: `data-platform/lineage-metadata.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-13-01A

- 원문 위치: 원문 4472–4525행, `13.1A Business Metadata vs Semantic Layer`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/lineage-metadata.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-13-02

- 원문 위치: 원문 4526–4561행, `13.2 Dataset Lineage`.
- 범위: Upstream; Downstream.
- 목적지: `data-platform/lineage-metadata.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-13-03

- 원문 위치: 원문 4562–4595행, `13.3 OpenLineage`.
- 범위: Job; Run; Dataset.
- 목적지: `data-platform/lineage-metadata.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-13-04

- 원문 위치: 원문 4596–4615행, `13.4 Column-Level Lineage`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/lineage-metadata.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-13-05

- 원문 위치: 원문 4616–4643행, `13.5 Impact Analysis`.
- 범위: Upstream Analysis; Downstream Impact Analysis.
- 목적지: `data-platform/lineage-metadata.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-13-06

- 원문 위치: 원문 4644–4663행, `13.6 Marquez`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/lineage-metadata.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-13-07

- 원문 위치: 원문 4664–4710행, `13.7 Catalog Integration`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/lineage-metadata.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-14-01

- 원문 위치: 원문 4713–4733행, `14.1 Dataset Ownership`.
- 범위: Technical Owner; Business Owner.
- 목적지: `data-platform/governance.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-14-02

- 원문 위치: 원문 4734–4758행, `14.2 Classification`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/governance.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-14-03

- 원문 위치: 원문 4759–4785행, `14.3 Retention Policies`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/governance.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-14-04

- 원문 위치: 원문 4786–4823행, `14.4 Deletion Policies`.
- 범위: Logical Delete; Physical Delete.
- 목적지: `data-platform/governance.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-14-05

- 원문 위치: 원문 4824–4849행, `14.5 Masking`.
- 범위: Static Masking; Dynamic Masking.
- 목적지: `data-platform/governance.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-14-06

- 원문 위치: 원문 4850–4875행, `14.6 Row / Column Access`.
- 범위: Row-Level Access; Column-Level Access; RBAC.
- 목적지: `data-platform/governance.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-14-07

- 원문 위치: 원문 4876–4908행, `14.7 Auditability`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/governance.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-14-08

- 원문 위치: 원문 4909–4943행, `14.8 Data Contracts`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/governance.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-14-09

- 원문 위치: 원문 4944–4996행, `14.9 Governance Platforms`.
- 범위: Databricks Unity Catalog; AWS Lake Formation; Snowflake Horizon Catalog.
- 목적지: `data-platform/governance.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-15-01

- 원문 위치: 원문 4999–5030행, `15.1 What Makes Data AI-Ready`.
- 범위: Trustworthy; Fresh; Versioned; Discoverable; Governed.
- 목적지: `data-platform/ai-ready-data.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-15-02

- 원문 위치: 원문 5031–5105행, `15.2 AI Telemetry Model`.
- 범위: Prompt / Response; Model; Agent; Tool Call; Latency; Token / Cost; Feedback; Trace / Execution / Session ID.
- 목적지: `data-platform/ai-ready-data.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-15-02A

- 원문 위치: 원문 5106–5180행, `15.2A Langfuse as AI Telemetry / Evaluation Layer`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/ai-ready-data.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-15-03

- 원문 위치: 원문 5181–5219행, `15.3 Dataset Versioning`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/ai-ready-data.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-15-04

- 원문 위치: 원문 5220–5259행, `15.4 Reproducibility`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/ai-ready-data.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-15-05

- 원문 위치: 원문 5260–5312행, `15.5 Evaluation Dataset Construction`.
- 범위: Regression Dataset.
- 목적지: `data-platform/ai-ready-data.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-15-06

- 원문 위치: 원문 5313–5359행, `15.6 Embedding Data`.
- 범위: Document; Chunk; Embedding.
- 목적지: `data-platform/ai-ready-data.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-15-07

- 원문 위치: 원문 5360–5396행, `15.7 Retrieval Metadata`.
- 범위: Access Metadata.
- 목적지: `data-platform/ai-ready-data.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-15-08

- 원문 위치: 원문 5397–5437행, `15.8 Provenance`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/ai-ready-data.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-15-09

- 원문 위치: 원문 5438–5493행, `15.9 Feature / Label Freshness`.
- 범위: Feature; Label.
- 목적지: `data-platform/ai-ready-data.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-16-01

- 원문 위치: 원문 5496–5614행, `16.1 Online Evaluation Events`.
- 범위: User Feedback; Automatic Evaluation; Langfuse 연결.
- 목적지: `data-platform/online-evaluation.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-17-01

- 원문 위치: 원문 5617–5675행, `17.1 전체 기술 역할 맵`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/architecture.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-17-02

- 원문 위치: 원문 5676–5707행, `17.2 Storage / Table / Compute / Query / Transformation 구분`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/architecture.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-17-03

- 원문 위치: 원문 5708–5741행, `17.3 Data Quality vs Data Observability`.
- 범위: Data Quality; Data Observability.
- 목적지: `data-platform/architecture.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-17-04

- 원문 위치: 원문 5742–5769행, `17.4 Metadata / Catalog / Semantic Layer 차이`.
- 범위: Metadata; Catalog; Business Metadata; Semantic Layer; Lineage; Governance.
- 목적지: `data-platform/architecture.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-17-05

- 원문 위치: 원문 5770–5808행, `17.5 AI Observability vs General Data Platform`.
- 범위: 절 전체의 설명, 예시, 비교와 주의 사항.
- 목적지: `data-platform/architecture.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-18-01

- 원문 위치: `Chapter 18 / 완료`.
- 범위: Phase 1~15 학습 완료 범위.
- 목적지: `data-platform/curriculum.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-18-02

- 원문 위치: `Chapter 18 / 진행 중`.
- 범위: Phase 16은 16.1만 완료; 16.2~16.11 후속 과정.
- 목적지: `data-platform/curriculum.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-18-03

- 원문 위치: `Chapter 18 / Phase 17`.
- 범위: 미학습 Phase 17 Databricks Deep Dive의 전체 목차.
- 목적지: `data-platform/curriculum.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-18-04

- 원문 위치: `Chapter 18 / Phase 18`.
- 범위: 미학습 Phase 18 Snowflake Deep Dive의 전체 목차.
- 목적지: `data-platform/curriculum.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-18-05

- 원문 위치: `Chapter 18 / Phase 19`.
- 범위: 미학습 Phase 19 제품 및 Open Lakehouse 비교 기준.
- 목적지: `data-platform/curriculum.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-18-06

- 원문 위치: `Chapter 18 / Phase 20`.
- 범위: 미학습 Phase 20 운영 엔지니어링 목차.
- 목적지: `data-platform/curriculum.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-18-07

- 원문 위치: `Chapter 18 / Phase 21`.
- 범위: 미학습 Phase 21 최종 프로젝트 목표 구조와 검증 질문.
- 목적지: `data-platform/curriculum.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.

## DPE-19-01

- 원문 위치: `Final Mental Model`.
- 범위: 최종 mental model의 데이터 경로와 횡단 관심사·역할 구분.
- 목적지: `data-platform/architecture.md`.
- 이 ID는 위 절 안의 예시·숫자·질문·실패 조건·제약을 포함한다. 원문 보존본과 양쪽 문서를 함께 검토한다.
