---
id: data-platform-snowflake
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - DPE2-18-01
  - DPE2-18-02
  - DPE2-18-03
  - DPE2-18-04
  - DPE2-18-05
  - DPE2-18-06
  - DPE2-18-07
  - DPE2-18-08
  - DPE2-18-09
  - DPE2-18-10
  - DPE2-18-11
  - DPE2-18-12
  - DPE2-18-13
---

# Chapter 18 — Snowflake Deep Dive (Condensed)

문서 유형: Learn. 원문 18장은 한 번 요약하고 넘어간 학습 범위다. `studied`는 이 요약 개념의 학습이며 상세 구현·운영 경험이나 심화 실습 완료를 뜻하지 않는다. 예시는 실행하지 않았다. 제품 동작은 2026-09-26 공식 문서로 확인했으며 edition, cloud, region, table type, feature 상태에 따라 달라진다.

**본문 안내:** 아래 원문 구역은 원래 순서와 형태를 보존한 본문이다. 원문의 단순화된 설명에 대한 정정·적용 조건과 추가 설명은 문서 뒤 보완 구역에서 해당 절 번호와 함께 확인한다.

<!-- SOURCE CORE START -->

> 원문 학습에서는 사용자가 Snowflake를 한 번 요약한 뒤 넘어가도록 명시적으로 요청했다.

Snowflake는 다음과 같이 요약할 수 있다:

> **Storage와 compute를 분리한 관리형 클라우드 데이터 플랫폼. 역사적으로 SQL/Data Warehouse workload를 중심으로 발전했으며, 이제 data engineering, Iceberg, governance, AI로 확장했다.**

---

## 18.1 Architecture

전체 계층:

```text
Cloud Services
     ↓
Virtual Warehouses
     ↓
Storage
```

### Storage

Snowflake가 관리하는 storage 또는 Iceberg 관련 storage.

### Virtual Warehouse

Query와 DML을 실행하는 독립 compute cluster.

서로 다른 warehouse를 통해 workload를 격리한다.

### Cloud Services

담당하는 기능:

- Metadata,
- 인증,
- Query 최적화,
- 접근 제어,
- 작업 조정.

---

## 18.2 Micro-partitions

Snowflake는 table 데이터를 **micro-partitions**으로 자동 구성한다.

```text
Table
├─ Micro-partition 1
├─ Micro-partition 2
├─ Micro-partition 3
└─ ...
```

Snowflake는 값 범위 등의 metadata를 추적한다.

이 정보가 pruning을 돕는다.

---

## 18.3 Pruning

Query:

```sql
WHERE event_date = '2026-09-26'
```

Snowflake는 조건과 일치할 수 없는 micro-partition을 읽지 않을 수 있다.

개념적으로 다음과 목적이 비슷하다:

```text
Iceberg File Pruning
Parquet Row Group Pruning
```

---

## 18.4 Clustering

자주 쓰는 filter에 맞지 않게 데이터가 배치되어 있다면 clustering으로 pruning 효율을 높일 수 있다.

큰 table에서는 clustering key를 사용할 수 있다.

목적은 모든 것을 수동 partition하는 것이 아니라 query pattern에 맞게 물리 배치를 개선하는 것이다.

---

## 18.5 Streams

Stream은 table의 row-level 변경을 추적한다.

```text
Table
 ↓
Stream
 ↓
Change Data
```

증분 처리에 유용하다.

---

## 18.6 Tasks

Task는 SQL 작업을 예약하거나 trigger한다.

자주 사용하는 조합:

```text
Stream
 ↓
Task
 ↓
MERGE / SQL Transform
```

---

## 18.7 Dynamic Tables

Dynamic Table:

> **Query 결과와 원하는 freshness를 선언하면 Snowflake가 refresh를 관리한다.**

예:

```text
Raw
 ↓
Dynamic Table
 ↓
Silver
 ↓
Dynamic Table
 ↓
Gold
```

Target lag를 사용한다:

```text
TARGET_LAG = 10 minutes
```

이는 개념적으로 선언형 데이터 pipeline과 비슷하다.

---

## 18.8 Snowpipe / Snowpipe Streaming

Snowpipe:

```text
Object Storage File
 ↓
Snowpipe
 ↓
Snowflake
```

Snowpipe Streaming은 staged file에만 의존하지 않고 더 낮은 지연으로 지속적인 수집을 가능하게 한다.

---

## 18.9 Iceberg Tables

Snowflake는 Apache Iceberg table과 다중 엔진 상호운용을 지원한다.

```text
Snowflake
 ↓
Iceberg Table
 ↓
Object Storage
```

Snowflake와 Horizon은 Iceberg catalog workflow에 참여할 수 있다.

Spark와 Trino 같은 외부 엔진도 열린 Iceberg workflow에 참여할 수 있다.

---

## 18.10 Governance — Horizon Catalog

Unity Catalog와 개념적으로 대응하는 관계:

```text
Databricks
→ Unity Catalog

Snowflake
→ Horizon Catalog
```

Horizon이 제공하는 영역:

- Discovery,
- Metadata,
- Lineage,
- Classification,
- Masking,
- Row access,
- Governance,
- Iceberg 가시성,
- Semantic/business 맥락.

---

## 18.11 Cortex / AI

Snowflake는 AI 기능을 점차 통합하고 있다:

```text
Cortex AI
Search
Analyst
Agents
AI interfaces
```

제품의 전체 방향은 다른 업계 흐름과 비슷하다:

> 거버넌스가 적용된 기업 데이터 가까이에서 AI를 사용하도록 한다.

---

## 18.12 Cost Model

Compute 단위:

```text
Virtual Warehouse
```

과금은 credit 기반이다.

비용 항목:

```text
Warehouse Compute
Serverless Compute
Cloud Services
Storage
```

최적화:

```text
Auto Suspend
Right-size Warehouse
Reduce Scan
Efficient Queries
Use incremental refresh where possible
```

---

## 18.13 Snowflake Mental Model

기억할 구조:

```text
Storage
→ Snowflake-managed / Iceberg

Compute
→ Virtual Warehouse

Layout
→ Micro-partitions

Performance
→ Pruning + Clustering

Pipeline
→ Dynamic Tables
→ Streams + Tasks

Ingestion
→ Snowpipe

Governance
→ Horizon Catalog

AI
→ Cortex / Search / Agents

Billing
→ Credits
```

발전 과정:

```text
Databricks
→ Spark / Data Engineering / AI
→ expanded into SQL Warehouse

Snowflake
→ Cloud Data Warehouse / SQL
→ expanded into Data Engineering / Iceberg / AI
```

현재 두 플랫폼은 상당한 기능 영역이 겹친다.

---

<!-- SOURCE CORE END -->

## 운영 검토와 공식 문서 보완

다음은 원문과 구분한 기존 보완 설명이다. 제품의 지원 조건과 주의사항은 2026-09-26 검토 범위를 유지한다. 이번 편집에서 새 버전을 시험하거나 공식 문서를 재확인한 것은 아니다.

### Architecture

Snowflake는 storage와 compute를 분리한 관리형 클라우드 데이터 플랫폼이다. SQL/Data Warehouse에서 출발해 data engineering, Iceberg, governance, AI로 확장했다.

```mermaid
flowchart TD
    C[Cloud Services: metadata, auth, optimization, coordination]
    C --> W1[Virtual Warehouse: BI]
    C --> W2[Virtual Warehouse: transformation]
    W1 --> S[Storage: native tables or Iceberg]
    W2 --> S
```

Virtual Warehouse는 query/DML을 실행하는 독립 compute cluster다. 서로 다른 warehouse로 workload를 격리할 수 있다. Cloud Services는 metadata, authentication, query optimization, access control, coordination을 맡는다. Storage는 Snowflake 관리형 저장 또는 Iceberg 구성으로 구분한다. [공식 아키텍처](https://docs.snowflake.com/en/user-guide/intro-key-concepts).

### Micro-partitions

Snowflake native table 데이터는 자동으로 micro-partitions에 배치된다. `Table → Micro-partition 1, 2, 3 …`이며 값 범위 등의 metadata가 pruning을 돕는다. 이 설명을 외부 Iceberg 파일의 물리 구조에 그대로 적용하지 않는다.

### Pruning

설명용 필터 `WHERE event_date = '2026-09-26'`가 있으면 일치할 수 없는 micro-partition을 읽지 않을 수 있다. [Iceberg file pruning](lakehouse-iceberg.md), Parquet row group pruning과 “불필요한 읽기 제거”라는 목적은 비슷하지만 metadata와 실행 방식은 다르다. 효과는 실제 query profile의 scan으로 확인한다.

### Clustering

빈번한 filter에 맞지 않는 물리 배치에서는 clustering이 pruning을 도울 수 있다. 큰 테이블은 clustering key를 검토할 수 있다. 모든 테이블을 수동 partition하라는 뜻이 아니다. 쿼리 패턴에 맞는 값 분포를 만드는 것이 목적이며 유지 비용도 비교한다. [Micro-partitions와 clustering](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions).

### Streams

Stream은 source table의 row 변화 정보를 증분 처리에 제공한다. Kafka 같은 독립 event log로 보면 안 된다. Stream 자체는 데이터 복사본 대신 source object의 offset을 보관하고 table history를 통해 변경을 계산한다. 단순 SELECT는 offset을 진행시키지 않는다. 변경을 소비하는 DML transaction의 commit이 기준이다. 보존 범위를 벗어난 stale stream을 감시한다. [Streams](https://docs.snowflake.com/en/user-guide/streams-intro).

### Tasks

Task는 SQL 작업을 스케줄하거나 트리거한다. 대표 흐름은 `Table → Stream → Task → MERGE / SQL transform`이다. 무엇이 변경됐는지는 Stream, 언제 처리할지는 Task, 결과를 어떻게 만들지는 SQL의 역할이다. [Tasks](https://docs.snowflake.com/en/user-guide/tasks-intro).

### Dynamic Tables

Dynamic Table은 결과 쿼리와 원하는 신선도를 선언하고 Snowflake가 refresh를 관리한다. `Raw → Dynamic Table(Silver) → Dynamic Table(Gold)`처럼 데이터셋 의존성을 표현한다.

설명용 설정은 `TARGET_LAG = '10 minutes'`다. **10분마다 실행하라는 스케줄도, 지연을 반드시 10분 이하로 보장하는 계약도 아니다.** 신선도 목표이며 실제 지연은 warehouse, 데이터 양, 쿼리 복잡도, 의존성 깊이의 영향을 받는다. 실제 lag와 refresh history를 확인한다. 모든 SQL이 incremental refresh에 적합하다고 가정하지 않는다. [Target lag](https://docs.snowflake.com/en/user-guide/dynamic-tables/target-lag).

### Snowpipe / Snowpipe Streaming

Snowpipe는 `Object storage file → Snowpipe → Snowflake`처럼 staged file을 수집한다. Snowpipe Streaming은 파일 staging에만 의존하지 않고 지속적으로 낮은 지연의 데이터를 수집하는 방식이다. 수집 지연, 처리 지연, 최종 mart 신선도는 별도로 측정한다. 스트리밍 수집이 [Flink](flink.md)의 복잡한 event-time/state 처리와 같은 기능을 뜻하지 않는다. [Snowpipe](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro), [Snowpipe Streaming](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-overview).

### Iceberg Tables

`Snowflake → Iceberg table → Object storage`로 표 형식, compute, storage를 구분한다. Snowflake-managed catalog와 external catalog 구성을 구별하고 누가 metadata commit과 maintenance를 책임지는지 정한다. Spark/Trino 같은 외부 엔진의 읽기·쓰기·인증·table feature 지원을 각각 확인한다. [Iceberg tables](https://docs.snowflake.com/en/user-guide/tables-iceberg).

Horizon의 Iceberg REST endpoint는 다중 엔진 접근에 참여할 수 있다. 이것이 모든 Snowflake 기능이나 모든 외부 엔진 조합에서 동일한 동작을 보장하지는 않는다. [Horizon을 통한 외부 엔진 접근](https://docs.snowflake.com/en/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).

### Governance: Horizon Catalog

Databricks Unity Catalog와 Snowflake Horizon Catalog는 “통합 거버넌스”라는 개념 영역에서 비교할 수 있다. Horizon은 discovery, metadata, lineage, classification, masking, row access, governance, Iceberg visibility, semantic/business context를 다룬다. 기능 이름 대응을 정책·권한·외부 엔진의 완전한 동등성으로 해석하지 않는다. [Horizon Catalog](https://docs.snowflake.com/en/user-guide/snowflake-horizon).

### Cortex / AI

Cortex AI, Search, Analyst, Agents, AI 인터페이스는 관리되는 기업 데이터 가까이에서 AI를 쓰려는 기능 영역이다. 검색, 구조화 데이터 분석, agent 도구 사용을 구분한다. 모델·리전·권한·데이터 접근 범위는 실제 기능 문서에서 확인한다. [Snowflake AI와 ML](https://docs.snowflake.com/en/guides-overview-ai-features).

### 비용 모델

Compute 사용은 credit 기반으로 과금하며 Virtual Warehouse, serverless compute, Cloud Services와 storage를 함께 계산한다. credit을 고정 CPU 개수나 모든 기능에 동일한 금액으로 해석하지 않는다.

Auto Suspend, 적절한 warehouse 크기, scan 감소, 효율적인 query, 가능한 incremental refresh가 검토 대상이다. 크기를 줄이는 것만으로 총비용이 낮아진다고 가정하지 않는다. 실행시간·대기·신선도와 함께 실제 사용량으로 비교한다. [Snowflake 비용](https://docs.snowflake.com/en/user-guide/cost-understanding-overall).

### 멘탈모델

| 책임 | 기억할 기능 |
|---|---|
| Storage | Native managed storage / Iceberg 구성 |
| Compute | Virtual Warehouse |
| Native layout | Micro-partitions |
| Performance | Pruning + Clustering |
| Pipeline | Dynamic Tables 또는 Streams + Tasks |
| Ingestion | Snowpipe / Snowpipe Streaming |
| Governance | Horizon Catalog |
| AI | Cortex / Search / Analyst / Agents |
| Billing | Credits와 storage 등 전체 항목 |

Databricks는 Spark/data engineering/AI에서 SQL로, Snowflake는 SQL/warehouse에서 engineering/Iceberg/AI로 확장했다. 현재 겹치는 영역이 많으므로 역사적 이미지보다 workload를 기준으로 고른다. [플랫폼 비교](platform-comparison.md), [Databricks](databricks.md), [분석 모델링](analytical-modeling.md)을 함께 본다.

## LLM in Practice

### Dynamic Table 신선도 검토

**상황:** 가상의 mart가 목표보다 오래된 데이터를 보여준다.

**LLM에 제공할 맥락:** 비식별 의존성 DAG, target lag, refresh history, 실제 지연, warehouse 사용률·queue, 변경량, SQL과 refresh mode를 제공한다.

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    의존성: [Raw-Silver-Gold DAG와 SQL]
    설정: [target lag, warehouse, refresh mode]
    관찰: [refresh history, actual lag, queue, 변경량]
    [요청]
    target lag를 실행 주기나 보장으로 취급하지 말라.
    수집 지연과 refresh 지연을 분리해 원인 가설을 세워라.
    증설 전에 현재 설계와 증거를 평가하라.
    [출력]
    관찰, 가정, 미확인 항목, 가설별 반증 지표를 표로 작성하라.
    작은 실험과 중단·복구 조건을 제시하라.
    [검증]
    공식 기능 조건과 실제 refresh 기록을 대조하라.
    실험 전후 신선도, 비용, 결과 정확성을 비교하고 사람의 실행 승인을 요구하라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Dependencies: [Raw-Silver-Gold DAG and SQL]
    Settings: [target lag, warehouse, refresh mode]
    Observations: [refresh history, actual lag, queue, change volume]
    [Task]
    Do not treat target lag as an interval or guarantee.
    Separate ingestion delay from refresh delay and form hypotheses.
    Assess the current design and evidence before resizing.
    [Output]
    Table observations, assumptions, unknowns, and evidence that could reject each hypothesis.
    Propose small experiments with stop and recovery conditions.
    [Checks]
    Compare official requirements with actual refresh records.
    Compare freshness, cost, and correctness before and after the experiment; require human approval to run it.
    ```

**기대 출력:** 지연 구간별 가설, 확인 쿼리의 목적, 작은 실험, 비용·정확성·신선도 판단 기준.

**LLM이 틀릴 수 있는 점:** target lag를 실행 주기나 보장으로 착각하고 증거 없이 warehouse 증설을 권할 수 있다.

**검증 방법:** 공식 target lag 정의와 refresh mode 조건을 확인한다. refresh history와 query profile로 가설을 반박하고 제한된 실험 전후의 actual lag·비용·결과 일치를 비교한다. 실행 승인은 사람이 한다.
