---
id: data-platform-dbt
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - DPE-08-01
  - DPE-08-02
  - DPE-08-03
  - DPE-08-04
  - DPE-08-05
  - DPE-08-06
  - DPE-08-07
  - DPE-08-08
  - DPE-08-09
  - DPE-08-10
---

# Chapter 8 — dbt

이 문서는 dbt의 역할과 모델 계층을 개념적으로 학습한 기록이다. 프로젝트 실행·성능 측정·운영 경험을 주장하지 않는다. 공식 문서는 2026-09-24에 확인했다.

본문은 제공된 원문의 번호·문단·목록·예시·순서를 그대로 보존했다. 원문의 단순화된 설명에 필요한 조건과 기존 추가 설명은 뒤의 **적용 시 보완할 점**에서 구분한다.

**본문 안내:** 아래 원문 구역은 원래 순서와 형태를 보존한 본문이다. 원문의 단순화된 설명에 대한 정정·적용 조건과 추가 설명은 문서 뒤 보완 구역에서 해당 절 번호와 함께 확인한다.

<!-- SOURCE CORE START -->
## 8.1 Project Structure

dbt:

> **SQL 기반 Transformation을 체계적으로 관리하는 도구**

핵심 구성:

### Models

SQL Transformation 단위.

### Sources

dbt 밖에서 만들어진 원본 Table.

### Tests

데이터 품질 규칙.

### Macros

반복 SQL Logic 재사용.

일반 구조:

```text
models/
  staging/
  intermediate/
  marts/

tests/
macros/
```

---

## 8.2 ref()

`ref()`:

> **다른 dbt Model을 참조하며 Dependency를 선언**

예:

```sql
SELECT *
FROM {{ ref('stg_orders') }}
```

효과:

- 실행 순서 계산
- DAG 생성
- Lineage 생성
- 환경별 Relation 처리

`source()`:

```text
dbt 외부 원본
```

`ref()`:

```text
다른 dbt model
```

---

## 8.3 Staging Models

Staging:

> **원본을 깨끗하게 정리하는 첫 변환 계층**

주요 역할:

- Rename
- Type normalization
- Basic null handling
- 날짜 형식 통일
- 필요한 Column 선택

복잡한 Business Logic은 많이 넣지 않는다.

---

## 8.4 Intermediate Models

Intermediate:

> **Staging Data를 Join/Aggregation해 재사용 가능한 Business Logic을 만드는 계층**

예:

```text
stg_orders
+
stg_customers
 ↓
int_orders_with_customer
```

여러 Mart가 이를 재사용할 수 있다.

작은 Project는 Intermediate를 생략할 수도 있다.

---

## 8.5 Marts

Mart:

> **최종 분석/소비 목적에 맞게 만든 Data Layer**

### Fact

사건/측정값.

### Dimension

Fact 설명 속성.

### Consumption Table

Dashboard/Report가 바로 사용할 수 있도록 미리 집계한 Table.

Lakehouse의 Gold Layer와 개념적으로 많이 겹친다.

```text
Staging
→ Intermediate
→ Mart

≈

Bronze/Silver
→ Gold
```

---

## 8.6 Incremental Models

매번 전체 Table을 다시 계산하지 않고 변경분만 처리.

### Append

새 데이터 추가만.

### Merge

INSERT + UPDATE.

### Incremental Filter

예:

```sql
WHERE event_time > last_processed_time
```

Late Arrival을 고려해 최근 며칠을 다시 읽고 MERGE할 수도 있다.

### Full Refresh

Logic 변경 등 필요 시 전체 재생성.

---

## 8.7 dbt Tests

대표 Test:

- not_null
- unique
- relationships
- accepted_values
- custom test

Pipeline 예:

```text
dbt run
 ↓
dbt test
 ↓
Pass
 ↓
Publish
```

dbt Test는 Data Quality 전체가 아니라 기본적인 Model/Table 규칙 검증에 특히 적합하다.

---

## 8.8 Snapshots

dbt Snapshot:

> **현재 Table을 비교해 변경 이력을 보존**

주로 SCD Type 2와 연결.

### Type 1

기존 값 overwrite.

### Type 2

과거 row 유지 + 새 version row 생성.

CDC History가 이미 충분히 있다면 별도의 Snapshot이 반드시 필요한 것은 아니다.

---

## 8.9 Documentation / Lineage

Table/Column 설명을 Metadata로 관리할 수 있다.

`source()`와 `ref()` 관계를 이용해 dbt Model Lineage를 생성한다.

예:

```text
raw.llm_calls
 ↓
stg_llm_calls
 ↓
int_llm_calls
 ↓
fact_llm_call
 ↓
mart_daily_usage
```

dbt Lineage는 전체 Data Platform Lineage의 일부다.

---

## 8.10 dbt + Databricks / Snowflake / Trino

dbt는 Compute Engine이 아니다.

```text
dbt
 ↓ SQL 생성/관리
Databricks / Snowflake / Trino
 ↓
실제 Compute
```

역할:

```text
dbt
→ Transformation Definition

Engine
→ Query / Compute Execution
```

Spark와 dbt는 경쟁 관계가 아니라 함께 사용할 수 있다.

---

<!-- SOURCE CORE END -->

## 적용 시 보완할 점

### 원문 8.6·8.7의 설명 범위

Incremental은 선택한 새 데이터나 변경분을 처리한다. MERGE는 key를 기준으로 INSERT와 UPDATE를 수행하는 방식이다.

| Test | 확인하는 규칙 |
| --- | --- |
| `not_null` | 필수 값이 비어 있지 않음 |
| `unique` | 지정 key가 중복되지 않음 |
| `relationships` | 참조 key가 대상에 존재함 |
| `accepted_values` | 값이 허용 집합에 속함 |
| Custom test | 업무별 규칙 |

### Relation과 모델 계층

`ref()` 예시는 dbt template SQL이며 standalone SQL로 실행하는 문장이 아니다. `ref()`는 relation을 참조하면서 dependency를 선언한다. [dbt ref](https://docs.getdbt.com/reference/dbt-jinja-functions/ref)

Staging/Intermediate/Mart와 Bronze/Silver/Gold는 일대일 대응하는 표준이 아니다. 원본 형태와 품질 책임에 따라 경계를 정한다. Fact와 dimension은 [분석 데이터 모델링](analytical-modeling.md)에서 설명한다.

### Incremental 처리의 경계

`event_time > last_processed_time`은 누락 위험을 생각하기 위한 의사 SQL이다. 이벤트 시간이 오래된 late arrival은 이 조건에서 빠질 수 있다. Lookback과 MERGE를 조합해도 lookback 밖의 지연은 별도 backfill 대상으로 남는다.

- 데이터 grain에 맞는 `unique_key`를 정의하고 null·중복 여부를 검증한다. Key 설정 자체가 uniqueness 검증을 실행하지는 않는다.
- Incremental SQL은 최초 전체 실행과 이후 incremental 실행 모두에서 유효해야 한다.
- Strategy 지원과 update 방식은 adapter·engine에 따라 다르다.

[dbt incremental models](https://docs.getdbt.com/docs/build/incremental-models)

### 품질 gate, snapshot, lineage

Test 실패가 실제로 publish를 막도록 orchestration 조건을 연결해야 한다. 의미상 잘못된 값이 모든 기본 test를 통과할 수도 있다. [dbt data tests](https://docs.getdbt.com/docs/build/data-tests)

Snapshot은 관측 시점 사이의 모든 중간 변경을 CDC처럼 자동 보존하지 않는다. 실행 간격과 변경 감지 기준을 설계해야 한다. [dbt snapshots](https://docs.getdbt.com/docs/build/snapshots)

dbt lineage가 수집 서비스, dbt 외부 job, BI 소비까지 자동으로 모두 추적한다고 가정하지 않는다. 연결 engine에서 쓸 수 있는 기능도 adapter와 engine 조합마다 다르다.

## LLM 활용: incremental 누락 검토

상황: daily usage model에서 늦게 도착한 LLM call이 빠진다. 제공할 맥락은 model SQL, grain·key, adapter/engine 버전, event/ingestion time, late arrival 범위, 재실행 결과다.

=== "한국어"

    ```text {.prompt}
    [맥락]
    Model SQL·grain·key·adapter/engine 버전: [맥락]
    Event/ingestion time·지연 범위·재실행 결과: [가상 샘플]

    [요청]
    이 incremental model을 다시 작성하기 전에 검토해 주세요.
    관찰·가정·부족한 근거를 구분해 주세요.
    Late arrival·key uniqueness·null key·최초 실행 SQL·재실행 안전성을 확인해 주세요.
    작은 테스트를 제안하고 lookback window가 복구할 수 없는 것을 설명해 주세요.

    [출력]
    누락 조건과 검증 가능한 수정 후보를 주세요.

    [검증]
    공식 adapter 문서·compiled SQL·가상 지연 및 중복 행으로 검증해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Model SQL, grain, keys, and adapter and engine versions: [context]
    Event and ingestion times, lateness, and rerun results: [synthetic samples]

    [Task]
    Review this incremental model before rewriting it.
    Separate observations, assumptions, and missing evidence.
    Check late arrivals, key uniqueness, null keys, first-run SQL, and rerun safety.
    Propose small tests and explain what a lookback window cannot recover.

    [Output]
    Return missed-data conditions and testable change candidates.

    [Checks]
    Validate with official adapter documentation, compiled SQL, and synthetic late and duplicate rows.
    ```

기대 결과는 누락 조건과 검증 가능한 수정 후보다. LLM은 `event_time` 최대값을 안전한 watermark로 단정하거나 모든 adapter에 MERGE를 적용할 수 있다. 공식 adapter 문서, 실제 compiled SQL, 늦은 행·중복 key를 넣은 제한된 실행으로 검증한다. 여기서는 실행하지 않았다.

[오케스트레이션](orchestration.md) · [분석 데이터 모델링](analytical-modeling.md) · [Trino](trino.md) · [핸드북 홈](../index.md)

[관련 실무 프롬프트 6개](../prompts/dbt.md)
