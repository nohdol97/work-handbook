---
id: data-platform-dbt
status: studied
last_updated: 2026-09-24
last_reviewed: 2026-09-24
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

# Managing SQL transformations with dbt

This page records conceptual study of dbt and model layers. It does not claim project execution, performance testing, or production experience. Official documentation was checked on 2026-09-24.

## Project structure and execution

dbt defines and manages SQL transformations. A model is a SQL transformation unit. A source is an input table created outside dbt. A test defines a data quality rule. A macro reuses SQL logic.

```text
models/
  staging/
  intermediate/
  marts/
tests/
macros/
```

dbt is not a distributed compute engine. It manages SQL and dependencies. A connected engine such as Databricks, Snowflake, or Trino executes the queries. Features depend on the adapter and engine. Spark and dbt can work together: Spark executes compute while dbt manages SQL transformation definitions.

## ref and source

Use `ref()` to refer to another dbt model. This is dbt template SQL, not a standalone SQL statement.

```sql
SELECT *
FROM {{ ref('stg_orders') }}
```

`ref()` resolves a relation and declares a dependency. It supports execution order, the DAG, lineage, and relation names for each environment. `source()` refers to source data created outside dbt. [dbt ref](https://docs.getdbt.com/reference/dbt-jinja-functions/ref)

## Staging, intermediate, and marts

| Layer | Purpose | Examples and limits |
| --- | --- | --- |
| Staging | First cleanup of source data | Rename columns, normalize types, handle basic nulls, standardize dates, and select columns. Keep complex business logic small. |
| Intermediate | Reusable joins, aggregations, and business logic | `stg_orders + stg_customers → int_orders_with_customer`. Several marts can reuse it. Small projects may skip this layer. |
| Mart | Final analysis and consumption | Facts store events or measurements. Dimensions describe them. Consumption tables pre-aggregate data for dashboards or reports. |

`Staging → Intermediate → Mart` has some overlap with the lakehouse flow from Bronze/Silver to Gold. These names are not a standard one-to-one mapping. Set boundaries based on input data and quality responsibilities. See [analytical data modeling](analytical-modeling.md) for facts and dimensions.

## Incremental models

An incremental model processes selected new or changed rows instead of rebuilding the whole table each time.

- Append adds new rows.
- Merge inserts and updates rows based on a key.
- An incremental filter chooses the input range.
- A full refresh rebuilds the result when needed, such as after a logic change.

The source uses this simple filter. It is pseudo-SQL for discussing missed data, not a deployment configuration.

```sql
WHERE event_time > last_processed_time
```

A late arrival with an old event time can be missed. One option is to read recent days again and merge the result. Events outside that lookback still need a separate backfill. Define a `unique_key` that matches the grain. Check nulls and duplicates. Setting a key does not itself run a uniqueness test. SQL must be valid on the first full run and later incremental runs. Strategy support and update behavior depend on the adapter and engine. [dbt incremental models](https://docs.getdbt.com/docs/build/incremental-models)

## Tests and publication gates

| Test | Rule |
| --- | --- |
| `not_null` | Required values are present |
| `unique` | The selected key has no duplicates |
| `relationships` | Reference keys exist in the target |
| `accepted_values` | Values belong to an allowed set |
| Custom test | A business-specific rule |

A conceptual quality gate is `dbt run → dbt test → pass → publish`. Configure orchestration so a failed test really blocks publication. dbt tests work well for model and table rules. They do not cover all data quality concerns. A value can pass basic tests and still be wrong in meaning. [dbt data tests](https://docs.getdbt.com/docs/build/data-tests)

## Snapshots and SCD

dbt snapshots compare source table states over time and preserve change history. They implement the SCD Type 2 idea. Type 1 overwrites the old value. Type 2 keeps the old row and adds a new version. A separate snapshot may be unnecessary when adequate CDC history already exists.

A snapshot does not automatically capture every intermediate change between observations as CDC can. Design the run interval and change detection rule. [dbt snapshots](https://docs.getdbt.com/docs/build/snapshots)

## Documentation and lineage

Manage table and column descriptions as metadata. `source()` and `ref()` relationships create model lineage. For example:

```text
raw.llm_calls
  → stg_llm_calls
  → int_llm_calls
  → fact_llm_call
  → mart_daily_usage
```

dbt lineage covers part of the platform. Do not assume it automatically tracks ingestion services, external jobs, and all BI use.

## LLM in Practice: review missed incremental data

Situation: a daily usage model misses late LLM calls. Give the LLM the model SQL, grain, key, adapter and engine versions, event and ingestion times, observed lateness, and rerun results.

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

Expected output is a list of missed-data conditions and testable fixes. The LLM may treat the maximum `event_time` as a safe watermark or assume every adapter supports MERGE. Check official adapter documentation, actual compiled SQL, and a small run with late rows and duplicate keys. No such run was performed here.

[Orchestration](orchestration.md) · [Analytical modeling](analytical-modeling.md) · [Trino](trino.md) · [Handbook home](../index.md)

[Six related practical prompts](../prompts/dbt.md)
