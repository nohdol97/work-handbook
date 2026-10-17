---
id: data-platform-trino
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - DPE-10-01
  - DPE-10-02
  - DPE-10-03
  - DPE-10-04
  - DPE-10-05
  - DPE-10-06
  - DPE-10-07
  - DPE-10-08
---

# Chapter 10 — Trino

이 문서는 Trino를 개념적으로 학습한 기록이다. Query 성능이나 실제 운영 결과를 검증했다는 뜻이 아니다. 공식 문서는 2026-09-24에 확인했다.

**Trino**는 여러 저장소의 데이터를 SQL로 조회하는 분산 query engine이다. 여러 창고의 물품 목록을 한 창구에서 찾되, 물품을 어디서 얼마나 옮겨야 할지도 계산하는 방식에 가깝다. 아래 10.1~10.8은 connector, query 실행, pushdown, join과 memory의 관계를 설명한다.

<!-- SOURCE CORE START -->

## 10.1 Architecture

Trino는 외부 저장소의 데이터를 SQL로 조회하는 분산 엔진이다. Coordinator가 계획을 세우고 worker가 나누어 실행하므로 큰 데이터도 병렬로 읽을 수 있다.

Trino:

> **외부 데이터 저장소를 빠르게 SQL로 조회하는 분산 SQL Query Engine**

Trino 자체가 주 Storage는 아니다.

### Coordinator

- SQL 분석
- Query Plan
- Stage/Task 관리

### Worker

- 실제 Scan
- Join
- Aggregation

개념 비교:

```text
Trino Coordinator ≈ Spark Driver
Trino Worker ≈ Spark Executor
```

Coordinator/Worker와 Spark Driver/Executor의 비교는 역할 비유다. 실행 모델이 같다는 뜻은 아니다. `SQL → Query Plan → Stage → Task → Split`도 학습용 단순화이며 모든 실행 요소를 표현하지 않는다. [Trino concepts](https://trino.io/docs/current/overview/concepts.html)

Trino Catalog는 설정된 connector와 data source를 구분한다. Iceberg Catalog는 table metadata를 찾고 관리한다. Federated query의 성능은 원격 scan, 데이터 이동, source 부하를 함께 고려한다.


---

## 10.2 Connector Model

Connector는 Trino가 Iceberg나 PostgreSQL 같은 서로 다른 원천에 접근하는 통로다. 한 SQL에서 둘을 join할 수 있어도 원격 읽기와 데이터 이동 비용을 따져야 한다.

예:

- Iceberg Connector
- PostgreSQL Connector
- Hive Connector

Trino Catalog 이름 구조:

```text
catalog.schema.table
```

예:

```text
iceberg.analytics.fact_llm_call
postgres.public.users
```

Trino Catalog와 Iceberg Catalog는 의미가 다르다.

Trino Catalog:

> 어떤 Connector/Data Source를 사용할지 구분.

Federated query는 서로 다른 시스템을 한 SQL에서 join할 수 있게 한다. 다만 원천에서 읽는 양과 네트워크 이동량에 따라 느릴 수 있다.

---

## 10.3 Query Execution

Trino는 query를 stage와 task로 나눠 worker에 보낸다. Split은 읽기 작업의 작은 단위이고 exchange는 worker 사이의 데이터 이동이라서 느린 join을 볼 때 중요하다.

구조:

```text
SQL
 ↓
Query Plan
 ↓
Stage
 ↓
Task
 ↓
Split
```

### Stage

큰 실행 단계.

### Task

특정 Worker에서 실행되는 Stage 일부.

### Split

Scan의 작은 작업 단위.

### Exchange

Exchange는 join이나 집계를 위해 worker 사이에서 데이터를 다시 나누어 옮기는 과정이다.

Spark Shuffle과 비슷한 개념.

Join / GroupBy에서 Exchange가 많이 발생할 수 있다.

---

## 10.4 Pushdown

Pushdown은 filter나 집계 같은 일을 가능한 경우 원천 가까이에서 먼저 하는 방법이다. 필요한 상자만 창고에서 꺼내듯 전송량을 줄일 수 있지만 connector와 SQL 형태가 지원해야 한다.

목적:

> **가능한 연산을 데이터가 있는 쪽에서 먼저 수행해 이동/Scan을 줄인다.**

### Predicate Pushdown

`WHERE` 조건을 Source로 내려보냄.

### Projection Pushdown

필요한 Column만.

### Aggregation Pushdown

가능하면 COUNT/SUM 등을 Source에서 수행.

Iceberg에서는 Partition/File/Row Group/Column Pruning이 비슷한 목적을 수행한다.

Pushdown 지원은 connector와 query 형태에 달려 있다. SQL에 filter가 있어도 반드시 적용되는 것은 아니다. EXPLAIN과 실제 읽은 데이터량으로 확인한다.

Iceberg pruning과 원격 DB의 aggregation pushdown은 읽기와 이동량을 줄이려는 목적을 공유하지만 같은 연산은 아니다. [Trino pushdown](https://trino.io/docs/current/optimizer/pushdown.html)

원문의 “모든 Worker”는 join에 참여하는 worker를 기준으로 이해한다. Broadcast할 작은 table이 각 worker의 memory에 맞는지 확인한다. Skew가 생기면 일부 worker에 부하와 memory 사용이 집중되어 늦게 끝날 수 있다.


---

## 10.5 Join Strategies

Join 전략은 작은 쪽을 복사할지 양쪽을 key별로 재분배할지 결정한다. 두 방법 모두 데이터 크기와 key 쏠림에 영향을 받으므로 계획과 실행량을 함께 본다.

### Broadcast Join

Broadcast join은 작은 table을 join에 참여하는 worker에 복사해 큰 table의 재분배를 줄인다. 복사본이 각 worker의 memory에 맞아야 한다.

```text
Huge Fact
+
Tiny Dimension
```

### Partitioned Join

Partitioned join은 양쪽 큰 table을 join key 기준으로 재분배해 같은 key를 만나게 한다.

Exchange 비용 발생.

### Data Skew

특정 key가 특정 Worker에 몰릴 수 있다.

---

## 10.6 Memory

Trino는 join·집계·정렬 중간 결과를 memory에 둘 수 있다. 데이터가 크거나 한쪽으로 쏠리면 memory 한도에 닿아 query가 느려지거나 실패할 수 있다. Spill은 일부 데이터를 disk로 내리지만 모든 메모리 문제를 해결하지는 않는다.

주요 개념:

- Worker Memory
- Query Memory
- Spill

Spill:

```text
Memory 부족
 ↓
Disk 사용
```

Spill이 허용되는 조건에서는 일부 memory 부족을 완화할 수 있지만 disk I/O로 느려지고 모든 실패를 막지는 못한다.

Spill은 memory 압박을 줄이는 데 도움이 될 수 있지만 모든 OOM을 해결하지는 않는다. Disk I/O 때문에 query가 느려질 수 있다.

2026-09-24에 확인한 Trino 문서는 spill을 legacy 기능으로 설명하고, 적절한 task retry policy와 exchange manager를 쓰는 fault-tolerant execution 검토를 안내했다. 실제 적용은 workload·connector·설정으로 확인한다. 이번 편집에서 공식 문서를 새로 확인하거나 성능 실험을 수행한 것은 아니다. [Trino spill](https://trino.io/docs/current/admin/spill.html)

Trino/Spark 비교는 자주 맡는 역할을 설명한다. 절대적인 기능 경계나 성능 보장이 아니다.

Iceberg pruning 효과도 layout, metadata, filter, connector 구현에 따라 달라진다. [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html)


---

## 10.7 Trino vs Spark

Trino는 대화형 SQL 조회에, Spark는 큰 변환·재계산에 자주 쓰인다. 이는 흔한 역할 분담일 뿐 기능의 절대 경계가 아니므로 실제 지연·규모·운영 조건을 비교한다.

핵심:

```text
Trino
→ Interactive SQL / Query Serving

Spark
→ Large-scale Processing / Transformation
```

Trino:

- BI
- Ad-hoc Query
- 다수 사용자 동시 SQL

Spark:

- ETL
- Backfill
- Large Join
- ML Dataset
- Batch Transform

함께 사용:

```text
Spark
→ Data 생성

Trino
→ 생성된 Data 조회
```

---

## 10.8 Trino + Iceberg

Iceberg는 테이블의 현재 파일과 snapshot을 설명하고 Parquet은 파일 안의 데이터를 담는다. Trino는 metadata로 읽을 파일을 찾고 필요한 column을 조회하므로 layout과 connector 지원이 중요하다.

구조:

```text
S3
 ↓
Parquet
 +
Iceberg Metadata
 ↓
Trino
 ↓
BI / Analyst
```

Trino는 Iceberg metadata로 읽을 파일을 고르고, 지원되는 경우 Parquet의 열(column) 배치를 이용해 필요한 column만 읽는다.

역할:

```text
S3
→ 실제 File

Parquet
→ File Format

Iceberg
→ Table Metadata / Snapshot

Trino
→ SQL Query
```

---

<!-- SOURCE CORE END -->

## 이 장의 핵심

Trino query는 원천에서 읽는 양, worker 사이 이동량, memory가 함께 결정한다. Connector 지원과 실제 계획·측정값을 확인한다.

## LLM 활용: 느린 federated query 조사

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    Iceberg fact와 PostgreSQL dimension을 join한 query가 느리다. 함께 볼 자료는 익명화한 SQL, EXPLAIN, 실제 scan/output rows와 bytes, table 크기, key 분포, memory 오류, connector 설정이다.
    이 federated query를 재설계하기 전에 평가해 주세요.
    Pushdown·join distribution·exchange volume·skew·memory를 확인해 주세요.
    부족한 근거와 각 가설을 반박할 수 있는 작은 확인 작업을 나열해 주세요.
    Spill이나 broadcast가 항상 안전하다고 가정하지 말아 주세요.
    자료를 검토하되 실제 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    a query joining an Iceberg fact to a PostgreSQL dimension is slow. Use anonymized SQL, EXPLAIN, actual scan and output rows and bytes, table sizes, key distributions, memory errors, and connector settings.
    Assess this federated query before redesigning it.
    Separate observations from assumptions and hypotheses.
    Check pushdown, join distribution, exchange volume, skew, and memory.
    List missing evidence and small checks that could reject each hypothesis.
    Review the material; do not apply changes.
    ```

**핵심 사항:** 

이 검토에서는 근거별 병목 후보와 확인 순서다. LLM은 pushdown을 지원한다고 단정하거나 Spark 전환만 제안할 수 있다. 실제 query plan·runtime 통계·connector 문서를 확인하고 제한된 query 비교로 가설을 검증한다. 여기서는 해당 성능 실험을 하지 않았다.

[분석 데이터 모델링](analytical-modeling.md) · [dbt](dbt.md) · [핸드북 홈](../index.md)

[관련 실무 프롬프트 6개](../prompts/trino.md)
