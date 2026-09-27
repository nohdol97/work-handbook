---
id: data-platform-platform-comparison
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - DPE2-19-01
  - DPE2-19-02
  - DPE2-19-03
  - DPE2-19-04
  - DPE2-19-05
  - DPE2-19-06
  - DPE2-19-07
  - DPE2-19-08
  - DPE2-19-09
  - DPE2-19-10
  - DPE2-19-11
  - DPE2-19-12
  - DPE2-19-13
  - DPE2-19-14
  - DPE2-19-15
---

# Chapter 19 — Databricks vs Snowflake vs Open Lakehouse

문서 유형: Decision guide. 제공된 19장의 비교 개념을 정리한 학습 문서다. 실제 도입 결정·benchmark·운영 경험은 아니다. 표의 적합성은 가설이며 workload 검증이 필요하다. 제품 세부 범위는 2026-09-26 공식 문서로 확인했다.

제공된 원문의 번호·하위 제목·문단·목록·예시 순서를 보존했다. 영문은 원문 그대로이며 한국어는 같은 구조의 번역이다. 기술 용어·필드·설명용 코드 값은 원문 표기를 유지한다. 기존 추가 설명은 뒤의 보완 절에 구분했다.

**본문 안내:** 아래 원문 구역은 원래 순서와 형태를 보존한 본문이다. 원문의 단순화된 설명에 대한 정정·적용 조건과 추가 설명은 문서 뒤 보완 구역에서 해당 절 번호와 함께 확인한다.

<!-- SOURCE CORE START -->

이 장은 제품별 설명보다 비교에 초점을 맞춘다.

크게 세 가지 접근이 있다:

```text
1. Databricks-centered managed Lakehouse
2. Snowflake-centered managed Data Platform
3. Open Lakehouse assembled from open components
```

Open Lakehouse는 다음과 같이 구성할 수 있다:

```text
Object Storage
+
Iceberg
+
Spark
+
Flink
+
Trino
+
Airflow
+
dbt
+
OpenLineage
+
DataHub/OpenMetadata
+
MLflow/Langfuse
```

목표는 모든 상황에서 우세한 하나의 선택지를 선언하는 것이 아니다.

목표는 trade-off를 이해하는 것이다.

---

## 19.1 Storage Ownership

### Databricks

일반적인 모델:

```text
Cloud Object Storage
+
Delta / Iceberg
+
Unity Catalog
```

데이터는 cloud storage에 두고 Databricks가 table·governance 계층을 관리할 수 있다.

### Snowflake

전통적인 구조:

```text
Snowflake-managed storage
```

하지만 Snowflake는 Iceberg·외부 storage 상호운용 지원을 확대하고 있다.

### Open Lakehouse

가장 명확한 직접 소유 구조:

```text
Your S3 / ADLS / GCS
+
Your Iceberg Tables
```

조직이 object storage와 table metadata 아키텍처를 직접 통제한다.

이해를 위한 모델:

```text
Open Lakehouse
→ maximum direct storage ownership

Managed Platforms
→ more operational responsibilities moved to vendor
```

---

## 19.2 Iceberg Openness

Apache Iceberg는 여러 엔진 간 상호운용을 위해 설계되었다.

```text
Spark
Flink
Trino
Snowflake
Databricks
other engines
     ↓
Iceberg Table
```

Iceberg REST Catalog 사양은 여러 언어와 엔진에서 catalog에 쉽게 접근하도록 마련되었다.

현재의 Databricks는 managed Iceberg와 외부 접근을 지원한다.

Snowflake도 Iceberg와 Horizon 기반 다중 엔진 시나리오를 지원한다.

따라서 유용한 질문은 다음에서 더 나아가야 한다:

> “이 플랫폼은 Iceberg를 지원하는가?”

대신 다음을 묻는다:

> **플랫폼에서 Iceberg는 얼마나 기본적으로 통합되어 있으며, 외부 엔진이 같은 테이블에 접근해도 어느 기능까지 사용할 수 있는가?**

---

## 19.3 Compute Model

### Databricks

여러 compute 방식:

```text
Spark Runtime
Photon
SQL Warehouse
Serverless Jobs
Model Serving
```

범용 데이터 처리와 강하게 연결된다.

### Snowflake

핵심 추상화:

```text
Virtual Warehouse
```

SQL 중심의 강력한 managed compute 모델에 serverless 서비스가 결합된다.

### Open Lakehouse

Compute를 명시적으로 조합할 수 있다:

```text
Spark
→ Batch / ETL

Flink
→ Streaming

Trino
→ Interactive SQL

vLLM
→ AI Serving
```

유연성이 높지만 통합 부담도 커진다.

---

## 19.4 Batch

### Databricks

Spark 기반의 발전 경로 덕분에 매우 잘 맞는다.

자연스럽게 적용할 수 있는 작업:

- ETL
- Backfill
- 대규모 join
- ML 데이터셋 생성
- Lakehouse 변환

### Snowflake

SQL 기반 변환과 Dynamic Tables에 강점이 있다.

변환이 주로 SQL과 warehouse 중심일 때 잘 맞는다.

### Open Lakehouse

선택 폭이 가장 넓다.

사용할 수 있는 도구:

```text
Spark
Trino
dbt
other engines
```

다만 조직이 이들을 운영해야 한다.

---

## 19.5 Streaming

### Databricks

다음을 통해 강점을 갖는다:

```text
Spark Structured Streaming
Lakeflow Pipelines
Lakeflow Connect
```

Streaming이 Lakehouse workflow와 통합될 때 잘 맞는다.

### Snowflake

다음을 통해 streaming 수집과 증분 갱신을 지원한다:

```text
Snowpipe Streaming
Streams
Dynamic Tables
```

### Open Lakehouse

복잡한 stateful·event-time workload에 Flink를 사용할 수 있다.

다음 요구가 있을 때 특히 잘 맞는다:

- 매우 낮은 latency
- 큰 state
- 복잡한 event time
- 세밀한 streaming 제어

대가로 운영 복잡성이 늘어난다.

---

## 19.6 SQL / BI

### Snowflake

SQL·Data Warehouse는 전통적으로 제품의 중심이다.

```text
BI / Analyst
 ↓
Virtual Warehouse
 ↓
Snowflake Data
```

### Databricks

SQL Warehouse와 Photon은 BI·interactive SQL을 주요 workload로 다룬다.

### Open Lakehouse

일반적인 구조:

```text
Iceberg
 ↓
Trino
 ↓
BI
```

매우 개방적이지만 SQL 서비스 운영은 사용자 책임이다.

---

## 19.7 Governance

### Databricks

```text
Unity Catalog
```

결합하는 영역:

- 접근 제어
- Lineage
- 분류
- 감사
- Data·AI governance

### Snowflake

```text
Horizon Catalog
```

유사한 governance 영역을 결합한다.

### Open Lakehouse

다음을 조립해야 할 수 있다:

```text
Catalog
+
IAM
+
OpenLineage
+
DataHub/OpenMetadata
+
Policy Engine
+
Audit
```

Open 접근은 선택권을 주지만 플랫폼 작업을 늘린다.

---

## 19.8 Lineage

Managed 플랫폼은 자체 실행 시스템을 관찰할 수 있다는 이점이 있다.

예:

```text
Databricks Job
→ Table
→ Dashboard
```

위 흐름은 플랫폼 내부에서 자동 수집할 수 있는 경우가 많다.

Open Lakehouse의 lineage는 다음을 아우를 수 있다:

```text
Kafka
Flink
Spark
dbt
Trino
BI
```

더 유연하지만 표준화와 통합이 필요하다.

이 지점에서 OpenLineage가 유용해진다.

---

## 19.9 AI Ecosystem

### Databricks

통합 AI 방향:

```text
Lakehouse
+
MLflow
+
AI Search
+
Model Serving
+
Agents
+
Unity Catalog
```

AI workload가 데이터 엔지니어링 자산에 밀접하게 접근해야 할 때 자연스럽다.

### Snowflake

통합 방향:

```text
Snowflake Data
+
Cortex
+
Search / Analyst
+
Agents
+
Horizon
```

기업 데이터가 이미 Snowflake에 있을 때 자연스럽다.

### Open Lakehouse

조합 가능한 AI stack:

```text
Iceberg
+
Vector DB
+
vLLM
+
LiteLLM
+
Langfuse
+
MLflow
+
Agent Framework
```

유연성과 이식성은 가장 높지만 통합 부담도 가장 크다.

---

## 19.10 Portability

### Open Lakehouse

다음을 기반으로 할 때 개념적으로 가장 높은 이식성을 갖는다:

```text
Parquet
Iceberg
OpenLineage
Open APIs
```

Compute engine을 더 쉽게 교체할 수 있다.

### Managed Platforms

현재의 Databricks와 Snowflake는 특히 Iceberg 주변에서 과거보다 더 개방적인 인터페이스를 지원한다.

하지만 플랫폼 고유 기능은 여전히 의존성을 만들 수 있다.

예:

```text
managed workflow definitions
vendor-specific governance policies
serverless execution behavior
AI services
proprietary optimization
```

테이블 데이터는 이식할 수 있어도 **운영 시스템**은 완전히 이식하지 못할 수 있다.

---

## 19.11 Operational Complexity

### Open Lakehouse

직접 운영해야 할 수 있는 구성요소:

```text
Kafka
Flink
Spark
Trino
Airflow
Catalog
Lineage
MLflow
Observability
Security Integration
```

통제권을 얻는 대신 역량 있는 플랫폼 팀이 필요하다.

### Databricks / Snowflake

줄일 수 있는 작업:

- 설치
- 확장
- 업그레이드
- 호환성 관리
- 구성요소 간 인증
- 모니터링 일부
- Governance 통합 일부

가치는 한 엔진이 더 우수한가보다 다음에 있는 경우가 많다:

> **통합과 운영 작업을 줄이는 것.**

---

## 19.12 Vendor Lock-in

Lock-in은 단순히 다음 질문만으로 판단할 수 없다:

```text
"Is the table format open?"
```

Lock-in은 여러 계층에서 발생할 수 있다:

```text
Data Format
Catalog
Pipeline Definitions
Orchestration
Security Policies
ML Registry
AI Evaluation
Serving
Operational Knowledge
```

예:

```text
Iceberg Table
→ portable

But

vendor-specific pipeline + governance + AI stack
→ less portable
```

따라서 계층별로 생각한다.

---

## 19.13 Total Cost

다음만 비교하지 않는다:

```text
$/compute-hour
```

총비용에 포함되는 항목:

```text
Compute
Storage
Network
Licenses
Platform Engineering Labor
Operations
Upgrades
Incident Response
Security Integration
Governance
Developer Productivity
```

Open Lakehouse는 직접 소프트웨어 비용이 낮아도 인력·운영 비용이 높을 수 있다.

Managed 플랫폼은 서비스 비용이 높아도 엔지니어링 부담을 줄일 수 있다.

적절한 비교 기준은 표시 가격이 아니라 **TCO**다.

---

## 19.14 Simplified Comparison Table

| 영역 | Databricks | Snowflake | Open Lakehouse |
|---|---|---|---|
| 역사적 중심 | Spark/Data/AI | SQL/DWH | 개방형 데이터 아키텍처 |
| 저장소 | Object storage + Delta/Iceberg | Managed + Iceberg 선택지 | Object storage |
| Batch | 매우 강함 | 강함 | Spark 사용 시 매우 강함 |
| Streaming | 강함 | 강점이 커지고 있음 | Flink 사용 시 가장 높은 유연성 |
| Interactive SQL | SQL Warehouse | 핵심 강점 | Trino |
| Governance | Unity Catalog | Horizon Catalog | 도구 조립 |
| ML/AI | 매우 높은 통합 수준 | 통합 수준이 높아지고 있음 | 자유로운 조합 |
| Iceberg | 강한 지원 | 강한 지원 | 기본 설계로 선택 |
| 이식성 | 기능에 따라 중간~높음 | 기능에 따라 중간~높음 | 가장 높음 |
| 운영 부담 | 낮음~중간 | 낮음~중간 | 높음 |
| 공급자 의존성 | 중간~높음 | 중간~높음 | 낮음~중간 |
| 플랫폼 엔지니어링 자유도 | 중간 | 중간 | 가장 높음 |

---

## 19.15 Practical Decision Heuristics

다음이 중심이라면 Databricks 중심 접근을 선택한다:

```text
large-scale ETL
Spark expertise
ML/AI workloads
Lakehouse architecture
data engineering + AI integration
```

위 항목이 중심인 경우다.

다음이 중심이라면 Snowflake 중심 접근을 선택한다:

```text
SQL analytics
enterprise warehouse
BI
managed simplicity
warehouse-centric organization
```

위 항목이 중심인 경우다.

다음이 중요하다면 Open Lakehouse를 선택한다:

```text
multi-engine flexibility
deep infrastructure control
open standards
portability
custom platform capability
```

위 항목이 전략적으로 중요하고 조직이 운영 부담을 감당할 수 있는 경우다.

Hybrid 구성도 자연스럽다.

예:

```text
Kafka/Flink
   ↓
Iceberg
   ↓
Databricks + Trino
```

또는:

```text
Iceberg
├─ Snowflake
├─ Spark
└─ Trino
```

목표는 아키텍처의 순수성을 지키는 것이 아니다.

목표:

> **실제 workload와 조직 제약을 만족하는 데 필요한 최소한의 구성요소를 사용하는 것.**

---

<!-- SOURCE CORE END -->

## 적용 시 보완할 점

원문의 강점·순위 표현은 학습용 비교이며 benchmark 결과가 아니다. 아래는 기존 문서의 조건부 해석·확인 항목이다. 지원 범위·가격·성능을 새로 확인했다는 뜻이 아니며 공식 문서 확인일은 2026-09-26을 유지한다.

### 19.1 Storage Ownership

“파일이 내 bucket에 있다”와 “수명주기·catalog·권한·commit을 내가 통제한다”는 다르다. Open은 직접 통제를, managed는 공급자에 넘기는 운영 책임을 늘리는 방향이다. 실제 계정·보관·삭제·외부 접근 경계는 계약과 설정을 확인한다. [Databricks](databricks.md), [Snowflake](snowflake.md).

### 19.2 Iceberg Openness

Spark, Flink, Trino, Snowflake, Databricks 같은 여러 엔진을 Iceberg table에 연결할 수 있다. REST Catalog 명세는 언어·엔진을 넘는 catalog 연결 규약이다. [Apache Iceberg REST 명세](https://iceberg.apache.org/rest-catalog-spec/).

질문은 “Iceberg 지원?”에서 **“어떤 포맷 버전·native 기능·외부 reader/writer·정책이 유지되는가?”**로 바뀐다. managed Iceberg, Delta의 Iceberg 읽기 호환, external catalog 등록은 서로 다른 구성이다. catalog credential과 object storage 직접 접근도 구분한다. [Databricks 외부 접근](https://docs.databricks.com/aws/en/external-access), [Snowflake Iceberg](https://docs.snowflake.com/en/user-guide/tables-iceberg).

### 19.3 Compute Model

Compute 종류를 늘리기 전에 workload isolation, latency, throughput, 팀 역량을 정한다.

### 19.4 Batch

Databricks는 Spark 기반 ETL, backfill, 큰 join, ML dataset 생성, Lakehouse 변환의 자연스러운 후보다. Snowflake는 SQL 변환과 Dynamic Tables를 중심으로 warehouse 데이터 처리를 묶는다. Open은 Spark, Trino, dbt 등 선택이 넓지만 운영해야 한다. “강하다”는 표현을 측정 결과로 보지 말고 실제 데이터 크기·skew·재처리로 검증한다.

### 19.5 Streaming

Databricks는 Structured Streaming, Lakeflow Pipelines, Connect와 Lakehouse의 결합을 제공한다. Snowflake는 Snowpipe Streaming 수집, Streams 변경 추적, Dynamic Tables 갱신을 연결한다. 이는 모두 같은 stateful streaming engine이라는 뜻이 아니다.

Open에서 Flink는 낮은 지연, 큰 state, 복잡한 event time, 세밀한 제어가 필요할 때 후보가 된다. 그만큼 checkpoint, state, scaling, recovery 운영 책임이 생긴다. 수집 신선도와 event-time 정확성을 따로 비교한다. [Flink](flink.md), [Spark](spark.md).

### 19.6 SQL / BI

Snowflake는 `BI/Analyst → Virtual Warehouse → Data`가 중심이었다. Databricks의 SQL Warehouse + Photon도 interactive SQL/BI를 다룬다. Open은 `Iceberg → Trino → BI`를 구성할 수 있고 SQL 서비스 운영은 조직 책임이다. 동시성, queue, p95 query latency, connector와 semantic definition을 같은 조건에서 비교한다.

### 19.7 Governance

Databricks의 Unity Catalog와 Snowflake의 Horizon Catalog는 access, lineage, classification, audit, Data/AI governance의 통합 영역이다. Open은 Catalog + IAM + OpenLineage + DataHub/OpenMetadata + Policy Engine + Audit를 조합할 수 있다. 도구 선택 폭은 넓지만 정책의 실제 강제 지점과 인증 통합은 플랫폼 작업이다.

어느 쪽이든 제품이 있다는 사실로 보안을 검증하지 않는다. query, file path, external engine, AI retrieval 각각에서 허용/거부 동작을 확인한다. 특히 Databricks AI Search의 row/column 권한 제한은 [관련 경계](databricks.md)에서 확인한다.

### 19.8 Lineage

Managed 플랫폼은 내부 실행을 관찰하므로 `Job → Table → Dashboard` 계보를 자동 수집하기 유리할 수 있다. Open의 `Kafka → Flink → Spark → dbt → Trino → BI` 전체 계보는 표준화와 connector 통합이 필요하다. [OpenLineage](lineage-metadata.md)는 이 연결을 돕는다. 내부 자동 수집을 외부 도구·모든 열·모든 동적 SQL의 완전한 계보라고 보지 않는다.

### 19.9 AI Ecosystem

자유도는 통합·운영 부담과 함께 증가한다. 모델 교체뿐 아니라 prompt/agent/retrieval/evaluation version을 옮길 수 있는지도 확인한다. [AI-ready data](ai-ready-data.md), [Online evaluation](ai-evaluation.md#161-online-evaluation-events).

### 19.10 Portability

Parquet, Iceberg, OpenLineage, open API는 엔진 교체를 쉽게 할 수 있다. 관리형 플랫폼도 특히 Iceberg 주변에서 열린 인터페이스를 제공한다. 하지만 managed workflow definition, vendor-specific governance policy, serverless execution behavior, AI service, proprietary optimization은 별도 의존성이다.

**데이터가 이식 가능해도 운영 시스템 전체가 이식 가능한 것은 아니다.** 파일 읽기 테스트와 workflow·권한·장애 복구·평가 이력의 이관 테스트를 구분한다.

### 19.11 Operational Complexity

Open에서는 Kafka, Flink, Spark, Trino, Airflow, Catalog, Lineage, MLflow, Observability, Security Integration을 운영할 수 있어야 한다. 강한 플랫폼 팀이 필요하다.

Managed는 설치, 확장, 업그레이드, 호환성 관리, 구성요소 사이 인증, 관측과 거버넌스 통합의 일부를 줄인다. 장애 대응, 데이터 정확성, 비용 관리까지 사라지는 것은 아니다. 가치는 엔진 하나의 우열보다 통합·운영 업무 감소인 경우가 많다.

### 19.12 Vendor Lock-in

Lock-in을 table format 하나로 판단하지 않는다. **Data Format → Catalog → Pipeline Definitions → Orchestration → Security Policies → ML Registry → AI Evaluation → Serving → Operational Knowledge**를 각각 살핀다.

예를 들어 Iceberg table은 옮길 수 있어도 vendor pipeline·governance·AI stack은 다시 구현해야 할 수 있다. 각 계층에 export 형식, 대체 대상, 변경 비용, 검증 방법을 적는다. Open도 특정 엔진 동작과 팀의 운영 지식에 의존할 수 있다.

### 19.13 Total Cost

TCO는 Compute + Storage + Network + Licenses + Platform Engineering Labor + Operations + Upgrades + Incident Response + Security Integration + Governance + Developer Productivity를 포함한다. compute-hour 단가만 비교하지 않는다.

Open은 직접 소프트웨어 비용이 낮아도 사람·운영 비용이 커질 수 있다. Managed는 서비스 요금이 높아도 엔지니어링 부담을 줄일 수 있다. 동일한 workload, SLO, 복구 수준, 보존 기간, 인력 시간으로 비교한다. 이 문서는 단가나 절감률을 가정하지 않는다.

### 19.14 비교표

아래는 원문의 방향성을 보존한 **조건부 설계 가설**이며 benchmark 순위가 아니다.

| 영역 | Databricks | Snowflake | Open Lakehouse |
|---|---|---|---|
| 역사적 중심 | Spark / Data / AI | SQL / DWH | 열린 데이터 구조 |
| Storage | Object + Delta/Iceberg | Managed + Iceberg 옵션 | 직접 object storage |
| Batch | Spark 중심 대규모 처리 | SQL 중심 처리 | Spark 등 선택 |
| Streaming | Lakehouse 연계 | 수집·증분 갱신 | Flink 등 세밀한 제어 |
| Interactive SQL | SQL Warehouse | Virtual Warehouse | Trino 등 |
| Governance | Unity Catalog | Horizon Catalog | 도구·정책 통합 |
| ML/AI | 통합 스택 | 데이터 중심 AI 통합 | 직접 조합 |
| Iceberg | 타입·기능별 확인 | 타입·catalog별 확인 | 기본 설계로 선택 가능 |
| Portability | 사용 기능에 의존 | 사용 기능에 의존 | 열린 표준 중심이면 높일 수 있음 |
| Ops burden | 일부 운영 위임 | 일부 운영 위임 | 직접 운영 범위 큼 |
| Vendor dependency | 플랫폼 기능에서 증가 가능 | 플랫폼 기능에서 증가 가능 | 낮출 수 있으나 사라지지 않음 |
| Engineering freedom | 관리형 경계 안의 선택 | 관리형 경계 안의 선택 | 직접 통제 범위 큼 |

### 19.15 실무 선택 기준

- 대규모 ETL, Spark 역량, ML/AI, Lakehouse, 데이터 엔지니어링과 AI 통합이 중심이면 Databricks를 검토한다.
- SQL analytics, enterprise warehouse, BI, 관리 편의, warehouse 중심 조직이면 Snowflake를 검토한다.
- 다중 엔진, 인프라 통제, open standards, portability, 자체 platform 역량이 전략적이고 운영 부담을 감당할 수 있으면 Open을 검토한다.

혼합도 자연스럽다. 예시는 `Kafka/Flink → Iceberg → Databricks + Trino`, 또는 하나의 Iceberg 기반을 Snowflake·Spark·Trino가 사용하는 구조다. 실제 catalog·writer·권한 호환성은 별도 검증한다. 목표는 순수한 아키텍처가 아니라 **실제 workload와 조직 제약을 만족하는 최소 구성요소**다.

## LLM in Practice

### 세 가지 플랫폼의 의사결정 근거 작성

**상황:** 가상의 팀이 managed와 open의 선택 기준을 정한다.

**LLM에 제공할 맥락:** workload·SLO·보존·복구 요구, 인력·운영역량, 비용 자료, 필수 외부 엔진·정책, migration 제약을 비식별 형태로 제공한다.

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    입력: [workload, SLO, 보존·복구 요구]
    제약: [인력, 운영역량, 예산자료, 필수 엔진·정책, 이관 조건]
    [요청]
    현재 문제와 필요한 책임부터 평가하라.
    Databricks, Snowflake, Open Lakehouse, 최소 hybrid를 비교하라.
    storage, table format, catalog, pipeline, security, AI, 운영 지식의 이식성을 나눠라.
    [출력]
    관찰·가정·미확인을 구분한 요구별 표와 대안별 trade-off를 작성하라.
    동일 조건 TCO 항목, 최소 PoC, 실패·철회 기준을 제시하라.
    [검증]
    단가·지원 기능·benchmark를 만들지 말라.
    공식 문서와 실제 읽기·쓰기·거부 테스트, 측정할 비용·인력시간을 지정하라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Inputs: [workloads, SLOs, retention and recovery needs]
    Constraints: [staff, operating skills, budget evidence, required engines/policies, migration conditions]
    [Task]
    Assess the current problems and required responsibilities first.
    Compare Databricks, Snowflake, Open Lakehouse, and a minimal hybrid.
    Separate portability of storage, table format, catalog, pipelines, security, AI, and operating knowledge.
    [Output]
    Give a requirement table that separates observations, assumptions, and unknowns, plus trade-offs by option.
    List comparable TCO items, minimal proofs of concept, failure criteria, and exit criteria.
    [Checks]
    Do not invent prices, supported features, or benchmarks.
    Specify official docs, real read/write/denied-access tests, and cost/staff-time measurements.
    ```

**기대 출력:** 요구별 적합성·불확실성표, 계층별 lock-in, 같은 조건의 TCO 측정계획, 최소 PoC와 철회 조건.

**LLM이 틀릴 수 있는 점:** 특정 제품을 무조건 우승자로 정하거나 공개 포맷만으로 완전한 이식성을 주장할 수 있다.

**검증 방법:** 공식 지원표와 실제 reader/writer·권한 테스트를 확인한다. 동일 데이터·SLO·복구수준에서 비용과 인력시간을 측정한다. 이해관계자가 가중치·trade-off·미확인 항목을 검토한다.
