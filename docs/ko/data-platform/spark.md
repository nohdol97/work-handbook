---
id: data-platform-spark
status: studied
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids:
  - DPE-04-01
  - DPE-04-02
  - DPE-04-03
  - DPE-04-04
  - DPE-04-05
  - DPE-04-06
  - DPE-04-07
  - DPE-04-08
  - DPE-04-09
  - DPE-04-10
  - DPE-04-11
  - DPE-04-12
  - DPE-04-13
  - DPE-04-14
---

# Apache Spark

문서 유형: Learn. 제공된 학습 자료의 개념과 설계 예시를 정리했다. `studied`는 개념 학습을 뜻하며, 직접 구현하거나 운영 검증했다는 뜻이 아니다. SQL과 수치는 설명용 예시이며 실행하지 않았다.

## 4.1 Spark Architecture

Spark Application의 기본 구성:

```text
Application
   ↓
Driver
   ↓
Executors
```

### Driver

- Application 전체 관리
- Job planning
- Task scheduling
- Executor coordination

### Executor

- 실제 Task 실행
- 데이터 처리
- Cache 유지

### Cluster Manager

Spark Resource를 할당하는 시스템.

예:

- Kubernetes
- YARN
- Standalone

Spark on Kubernetes는 Kubernetes가 Driver/Executor Pod의 실행 Resource를 관리하는 형태로 이해할 수 있다.

## 4.2 Execution Model

Spark 실행 단위:

```text
Application
  ↓
Job
  ↓
Stage
  ↓
Task
```

### Job

Action이 실행되면서 생성되는 큰 작업 단위.

### Stage

Shuffle Boundary 등에 따라 나뉘는 실행 단계.

### Task

하나의 Spark Partition을 처리하는 실제 실행 단위.

### Spark Partition

Spark가 병렬 처리하는 논리적인 데이터 단위.

### DAG

Transformation 의존 관계를 그래프로 표현한다.

## 4.3 Lazy Evaluation

Spark Transformation은 호출 즉시 실행되지 않는다.

예:

```text
filter
map
join
```

을 정의해도 실제 계산은 Action이 호출될 때 시작된다.

### Transformation

새 Dataset을 정의.

### Action

실제 실행을 유발.

예:

- count
- collect
- write

---

### Query Planning

개념적으로:

```text
User Code
  ↓
Logical Plan
  ↓
Optimized Logical Plan
  ↓
Physical Plan
  ↓
Execution
```

Spark SQL/DataFrame에서는 Catalyst Optimizer가 Query Plan을 최적화한다.

`explain()`을 통해 계획을 확인할 수 있다.

## 4.4 Narrow vs Wide Dependencies

### Narrow Dependency

각 Output Partition이 소수 Input Partition에만 의존.

예:

```text
map
filter
```

데이터가 Worker 사이를 크게 이동하지 않을 수 있다.

### Wide Dependency

여러 Partition의 데이터가 재분배되어야 함.

예:

```text
groupBy
join
repartition
```

이런 재분배에는 Shuffle이 발생한다. 다만 join의 물리 계획에 따라 broadcast 등으로 shuffle 범위가 달라질 수 있다.

## 4.5 Shuffle

Shuffle은 Spark 성능에서 매우 중요한 개념이다.

```text
Worker A ─┐
Worker B ─┼→ Network Redistribution
Worker C ─┘
```

발생 가능한 비용:

- Network I/O
- Shuffle Write
- Shuffle Read
- Sort
- Serialization
- Disk Spill
- Stage Boundary

핵심:

> **대규모 Join / GroupBy가 비싼 이유는 데이터가 Worker 사이를 이동하기 때문이다.**

## 4.6 Join Strategies

### Broadcast Hash Join

큰 Fact + 작은 Dimension.

```text
Large Fact
+
Small Dimension
```

작은 Table을 모든 Executor에 Broadcast한다.

장점:
- 큰 Table Shuffle 감소

주의:
- Broadcast 대상이 너무 크면 Memory 문제

---

### Sort-Merge Join

두 큰 Table을 Join할 때 자주 사용되는 전략.

개념적으로:

```text
양쪽을 Join Key 기준으로 Shuffle
↓
Sort
↓
Merge
```

---

### Shuffle Hash Join

양쪽 데이터를 Partitioning 후 Hash Join.

---

### Fact + Dimension

일반적인 분석 Join Pattern.

### Large-Large Join

둘 다 크면 Shuffle 비용이 매우 커질 수 있다.

### Semi / Anti Join

존재 여부 또는 제외 조건에 사용된다.

### Join Cardinality / Join Explosion

Join Key 중복이 많으면 결과 row 수가 예상보다 크게 늘어날 수 있다.

## 4.7 Partition Management

### repartition

Partition을 다시 나눈다.

Shuffle 발생 가능.

사용:
- 병렬성 증가
- 특정 key 기준 재분배
- Output file 수 조절

### coalesce

주로 Partition 수를 줄일 때 사용.

항상 full shuffle이 필요한 것은 아니다.

---

### Keyed Repartitioning

특정 key 기준으로 같은 값이 같은 Partition으로 가도록 할 수 있다.

### Task Parallelism

Spark Partition 수가 Task 병렬성과 직접 연결된다.

### Target Partition Size / Output File Count

Partition 수는:
- Task 수
- File 수
- Memory pressure

와 연결된다.

## 4.8 Cache / Persist

Spark는 중간 결과를 Memory/Disk에 유지할 수 있다.

### 왜 사용하나

같은 데이터를 여러 번 계산하면 재계산 비용이 크다.

```text
Expensive Transform
  ↓
Cache
  ├─ Query A
  └─ Query B
```

### unpersist

더 이상 필요 없는 Cache는 해제해야 한다.

### Cache가 항상 좋은 것은 아님

- 한 번만 사용하는 데이터
- 매우 큰 Dataset
- Memory가 부족한 환경

에서는 오히려 불리할 수 있다.

### Durable Iceberg Intermediate Table

장시간 또는 Job 간 재사용해야 하는 결과라면 Cache보다 Iceberg Intermediate Table 같은 durable storage가 더 적합할 수 있다.

## 4.9 Data Skew

Data Skew는 데이터가 특정 Partition에 몰리는 현상이다.

예:

```text
team_id = A → 80%
나머지 → 20%
```

그러면 한 Task만 매우 오래 걸릴 수 있다.

### Hot Key

특정 key에 데이터가 집중.

### Skewed Join / Aggregation

Join이나 GroupBy에서 특정 key가 병목.

### Null / Default Key Skew

`NULL`, `UNKNOWN`, `0` 같은 기본값에 데이터가 몰릴 수 있다.

### Salting

Hot Key에 추가 salt를 붙여 여러 key로 분산한 뒤 나중에 합친다.

단, **원래 key ordering이 중요한 Streaming/Event 처리에는 그대로 적용하기 어렵다.**
Spark Batch의 Join/Aggregation skew 해결과 Kafka Ordering 문제는 구분해야 한다.

### Pre-Aggregation

미리 부분 집계해 Shuffle 데이터량을 줄인다.

### Heavy-Key Special Path

특정 Hot Key만 별도 처리.

### AQE

Adaptive Query Execution이 runtime statistics를 이용해 일부 skew 최적화를 할 수 있다.

## 4.10 Spark Performance Engineering

대표 병목:

- CPU
- Executor Memory
- Heap Pressure
- GC
- Disk Spill
- Network
- Shuffle
- S3 Scan
- Small Files
- Straggler

### Executor Sizing

Executor Memory/Core를 workload에 맞게 조정.

### Spill

Memory에 다 못 담은 중간 데이터를 Disk로 내림.

### Straggler

특정 Task 하나가 매우 늦게 끝나는 현상.

Skew 등이 원인이 될 수 있다.

### Speculative Execution

유난히 느린 Task를 다른 Executor에서 중복 실행해 먼저 끝나는 결과를 사용할 수 있다.

### Spark UI

어느 Stage/Task가 병목인지 진단하는 데 중요하다.

## 4.11 Spark + Iceberg

Spark는 Iceberg 데이터를 Batch 처리하는 주요 Compute Engine 중 하나다.

```text
Iceberg
  ↓
Spark
  ↓
Transform
  ↓
Iceberg
```

### Iceberg Scan Planning

Iceberg Metadata를 이용해 읽어야 할 File을 결정한다.

### Predicate Pushdown / Pruning

불필요한 File/Row Group을 읽지 않는다.

### Spark Tasks vs Iceberg Files

하나의 File이 반드시 하나의 Task와 1:1은 아니지만 File Layout이 Task 병렬성과 Scan 효율에 영향을 준다.

### Write Distribution

데이터를 적절히 분산해서 File을 생성해야 한다.

### Target File Size

너무 작은 File을 만들지 않도록 관리한다.

### Sort Order

Query Pattern에 맞춰 Layout을 최적화할 수 있다.

### MERGE

CDC Current-State Table 구성 등에 사용 가능.

### Write Skew

특정 Partition/Key에 Write가 몰릴 수 있다.

### Commit Behavior

Spark Task가 File을 만들고 Iceberg Commit을 통해 새 Snapshot을 Table에 반영한다.

### Maintenance Debt

Streaming Write, MERGE, 작은 File 등이 쌓이면 Compaction 등 Maintenance가 필요해진다.

## 4.12 Structured Streaming

Spark Structured Streaming은 Streaming 데이터를 Table처럼 다루는 모델을 제공한다.

주로 **Micro-batch** 방식으로 이해할 수 있다.

```text
Kafka
 ↓
Micro Batch
 ↓
Spark
 ↓
Sink
```

### Kafka Source

Kafka Topic을 Streaming Source로 사용.

### Checkpoint

처리 상태와 offset 등의 복구 정보 저장.

### State

Streaming Aggregation / Deduplication 등에 필요한 상태 유지.

### Event Time

실제 Event 발생 시간.

### Late Events

늦게 도착한 Event.

### Watermark

Event-time 진행을 나타내며 지원되는 연산에서 late event 처리와 state 정리에 쓰는 기준.

### Window

시간 구간 단위 집계.

### Deduplication

중복 Event 제거.

### Output Modes

Aggregation 결과를 어떤 방식으로 출력할지 결정.

### foreachBatch

각 Micro Batch를 Batch Logic으로 처리할 수 있다.

### Streaming → Iceberg

실시간에 가깝게 Iceberg에 적재 가능.

주의:

```text
자주 쓰기
→ 작은 File
→ Compaction 필요
```

### Streaming vs Batch Backfill

실시간 처리는 Streaming, 과거 대규모 재처리는 Batch Spark가 자연스럽다.

## 4.13 Spark의 역할

질문:

> Spark 역할이 무엇인가?

핵심:

> **Spark는 대규모 분산 데이터 처리 엔진이다.**

주요 활용:

- 대규모 ETL
- Join
- Aggregation
- Backfill
- Lakehouse Transform
- ML Dataset 생성
- Batch Processing
- Structured Streaming

Spark는 Storage가 아니다.

```text
Iceberg / S3
→ Storage/Table

Spark
→ Compute
```

## 4.14 Spark를 써도 dbt가 필요한가?

역할이 다르다.

```text
Spark
→ 대규모 데이터 처리 엔진

dbt
→ SQL Transformation 관리 계층
```

함께 사용할 수 있다.

예:

```text
Raw
 ↓
Spark
 ↓
Silver
 ↓
dbt
 ↓
Gold / Mart
```

반대로 단순 SQL Transformation이면 Spark 없이 dbt + Trino/Warehouse만으로 처리할 수도 있다.

## 적용 시 보완할 점

논리적 join이라고 양쪽 입력이 반드시 shuffle되지는 않는다. Broadcast나 기존 partition 배치가 물리 계획을 바꿀 수 있다. `explain()`과 Spark UI에서 실제 계획, shuffle bytes, task별 시간·spill·GC·입력 크기를 확인한다. AQE는 runtime statistics로 지원되는 계획만 바꾸며 모든 skew를 해결하지 않는다. Join 결과 폭증은 key 중복과 grain부터 확인한다. Semi join은 존재하는 행, anti join은 일치하지 않는 행을 선택한다. [Spark 성능 가이드](https://spark.apache.org/docs/latest/sql-performance-tuning.html)

Speculation은 느린 task를 다시 실행할 뿐 원래 skew를 없애지 않는다. Cache와 durable table은 보존 수명이 다르다. `repartition`은 보통 shuffle을 만들며, partition을 지나치게 줄이면 병렬성도 줄어든다. Spark→dbt 경로는 예시이지 반드시 지켜야 하는 계층 경계가 아니다.

Iceberg 목표 파일 크기는 보장되는 출력 크기가 아니다. 하나의 파일은 task와 Iceberg partition 경계를 넘지 못하며, 압축된 파일 크기와 Spark 메모리 내 크기도 다르다. [Iceberg Spark 쓰기](https://iceberg.apache.org/docs/latest/spark-writes/)

Watermark는 단순한 대기 타이머가 아니라 event-time 진행 및 state 정리 기준이다. Output mode는 append/update/complete 등 연산·sink 조합에 제약이 있다. `foreachBatch`의 기본 write 보장은 at-least-once다. `batchId` 등을 활용한 멱등 sink와 재시도 검증 없이 end-to-end exactly-once를 주장하지 않는다. [Spark Structured Streaming](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html)

## 연결해서 읽기

[Iceberg](lakehouse-iceberg.md), [Flink](flink.md), [이벤트 의미](event-architecture.md).

## LLM 실전: 느린 Stage 진단

- 상황: 가상의 join stage에서 task 하나만 오래 걸린다.
- 제공할 맥락: 물리 계획, task별 입력·shuffle·spill·GC·시간, key 빈도, executor 자원을 제공한다.
- 기대 결과: 원인별 근거와 반증 조건, 작은 실험 계획이다.
- 오류 가능성: 느린 task를 무조건 skew라 하거나 broadcast를 무조건 권할 수 있다.
- 검증 방법: Spark UI와 계획을 대조하고 같은 입력으로 한 설정씩 바꿔 측정한다.

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    계획과 분포: [physical plan·key 빈도·executor 자원]
    Task 지표: [입력·shuffle·spill·GC·실행 시간]

    [요청]
    재설계 제안 전에 느린 stage를 진단해 줘.
    Skew·메모리 압박·느린 I/O 가설을 근거에 따라 순위로 정리해 줘.

    [출력]
    근거와 가정을 구분하고 누락된 측정 및 반증 조건을 작성해 줘.

    [검증]
    가설마다 동일 입력으로 한 조건만 바꾸는 통제된 실험을 제안해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Plan and distribution: [physical plan, key counts, executor resources]
    Task metrics: [input, shuffle, spill, GC, duration]

    [Task]
    Diagnose the slow stage before proposing a redesign.
    Rank skew, memory-pressure, and slow-I/O hypotheses by evidence.

    [Output]
    Separate evidence from assumptions; request missing metrics and falsification checks.

    [Checks]
    Propose one controlled test per hypothesis, changing one condition on the same input.
    ```

[이 주제의 실무 프롬프트 6개 더 보기](../prompts/spark.md)

LLM 출력은 작업 가설이다. 공식 문서와 실제 설정·로그·측정으로 검증한다. 외부 문서 확인일: 2026-09-24. 구현 버전을 시험했다는 의미는 아니다.
