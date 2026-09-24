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

# dbt로 SQL 변환 관리하기

이 문서는 dbt의 역할과 모델 계층을 개념적으로 학습한 기록이다. 프로젝트 실행·성능 측정·운영 경험을 주장하지 않는다. 공식 문서는 2026-09-24에 확인했다.

## 프로젝트와 실행 역할

dbt는 SQL 기반 transformation을 체계적으로 정의·관리한다. Model은 SQL 변환 단위, source는 dbt 밖에서 만들어진 원본 table, test는 데이터 품질 규칙, macro는 반복 SQL logic을 재사용하는 기능이다.

```text
models/
  staging/
  intermediate/
  marts/
tests/
macros/
```

dbt 자체는 분산 compute engine이 아니다. dbt가 SQL과 의존성을 관리하면 Databricks, Snowflake, Trino 같은 연결된 engine이 query/compute를 수행한다. 지원 기능은 adapter와 engine 조합마다 다르다. Spark와 dbt는 함께 사용할 수 있다. Spark는 계산을 수행하고 dbt는 SQL 변환 정의를 관리하는 식이다.

## ref와 source

다른 dbt model을 참조할 때 `ref()`를 사용한다. 다음은 dbt template SQL 예시이며 standalone SQL로 실행하는 문장이 아니다.

```sql
SELECT *
FROM {{ ref('stg_orders') }}
```

`ref()`는 relation을 참조하면서 dependency를 선언한다. 실행 순서, DAG, lineage, 환경별 relation 해석에 쓰인다. `source()`는 dbt 외부의 원본을 나타낸다는 점이 다르다. [dbt ref](https://docs.getdbt.com/reference/dbt-jinja-functions/ref)

## Staging, intermediate, mart

| 계층 | 역할 | 예시·경계 |
| --- | --- | --- |
| Staging | 원본을 정리하는 첫 계층 | Rename, type normalization, 기본 null 처리, 날짜 형식 통일, 필요한 column 선택. 복잡한 business logic은 최소화한다. |
| Intermediate | 재사용 가능한 join·aggregation·business logic | `stg_orders + stg_customers → int_orders_with_customer`. 여러 mart가 재사용할 수 있고 작은 프로젝트에서는 생략할 수 있다. |
| Mart | 최종 분석·소비 목적 | 사건·측정값인 fact, 설명 속성인 dimension, dashboard/report용 사전 집계 consumption table. |

`Staging → Intermediate → Mart`는 lakehouse의 Bronze/Silver에서 Gold로 가는 정제 흐름과 개념적으로 겹친다. 하지만 계층 이름이 일대일 대응하는 표준은 아니다. 원본의 형태와 품질 책임에 따라 경계를 정한다. Fact와 dimension은 [분석 데이터 모델링](analytical-modeling.md)에서 설명한다.

## Incremental 모델

Incremental은 매번 전체 table 대신 선택한 새 데이터나 변경분을 처리한다.

- Append는 새 행을 추가한다.
- Merge는 key를 기준으로 INSERT와 UPDATE를 수행하는 방식이다.
- Incremental filter는 처리할 입력 범위를 정한다.
- Full refresh는 logic 변경 등으로 전체 결과를 다시 만들어야 할 때 사용한다.

원문의 간단한 filter는 다음과 같다. 이 식은 누락 위험을 생각하기 위한 의사 SQL이며 그대로 배포할 설정이 아니다.

```sql
WHERE event_time > last_processed_time
```

이벤트 시간이 오래된 late arrival은 이 조건에서 빠질 수 있다. 최근 며칠을 다시 읽는 lookback과 MERGE를 조합할 수 있다. Lookback 밖의 지연은 별도 backfill 대상으로 남는다. 데이터 grain에 맞는 `unique_key`를 정의하고 null·중복 여부를 검증한다. Key 설정이 그 자체로 uniqueness 검증을 실행하는 것은 아니다. Incremental SQL은 최초 전체 실행과 이후 incremental 실행 모두에서 유효해야 한다. Strategy 지원과 update 방식은 adapter·engine에 따라 다르다. [dbt incremental models](https://docs.getdbt.com/docs/build/incremental-models)

## Tests와 공개 조건

대표 test는 다음과 같다.

| Test | 확인하는 규칙 |
| --- | --- |
| `not_null` | 필수 값이 비어 있지 않음 |
| `unique` | 지정 key가 중복되지 않음 |
| `relationships` | 참조 key가 대상에 존재함 |
| `accepted_values` | 값이 허용 집합에 속함 |
| Custom test | 업무별 규칙 |

개념적인 품질 gate는 `dbt run → dbt test → pass → publish`다. Test 실패가 실제로 publish를 막도록 orchestration 조건을 연결해야 한다. dbt test는 model/table 규칙에 특히 유용하지만 데이터 품질 전체를 보장하지 않는다. 예를 들어 의미상 잘못된 값이 모든 기본 test를 통과할 수 있다. [dbt data tests](https://docs.getdbt.com/docs/build/data-tests)

## Snapshot과 SCD

dbt snapshot은 시간에 따라 source table의 상태를 비교해 변경 이력을 보존하며 SCD Type 2와 연결된다. Type 1은 기존 값을 덮어쓰고, Type 2는 과거 행을 남기며 새 version 행을 만든다. 이미 충분한 CDC history가 있다면 별도 snapshot이 반드시 필요한 것은 아니다.

Snapshot은 관측 시점 사이에 일어난 모든 중간 변경을 CDC처럼 자동 보존하지 않는다. 실행 간격과 변경 감지 기준을 설계해야 한다. [dbt snapshots](https://docs.getdbt.com/docs/build/snapshots)

## Documentation과 lineage

Table·column 설명은 metadata로 관리한다. `source()`와 `ref()` 관계로 dbt 모델 lineage를 만든다. 예를 들어 다음 의존성을 추적할 수 있다.

```text
raw.llm_calls
  → stg_llm_calls
  → int_llm_calls
  → fact_llm_call
  → mart_daily_usage
```

dbt lineage는 전체 플랫폼 lineage의 일부다. 수집 서비스, dbt 외부 job, BI 소비까지 자동으로 모두 추적한다고 가정하지 않는다.

## LLM 활용: incremental 누락 검토

상황: daily usage model에서 늦게 도착한 LLM call이 빠진다. 제공할 맥락은 model SQL, grain·key, adapter/engine 버전, event/ingestion time, late arrival 범위, 재실행 결과다.

```text
Review this incremental model before rewriting it.
Separate observations, assumptions, and missing evidence.
Check late arrivals, key uniqueness, null keys, first-run SQL, and rerun safety.
Propose small tests and explain what a lookback window cannot recover.
```

기대 결과는 누락 조건과 검증 가능한 수정 후보다. LLM은 `event_time` 최대값을 안전한 watermark로 단정하거나 모든 adapter에 MERGE를 적용할 수 있다. 공식 adapter 문서, 실제 compiled SQL, 늦은 행·중복 key를 넣은 제한된 실행으로 검증한다. 여기서는 실행하지 않았다.

[오케스트레이션](orchestration.md) · [분석 데이터 모델링](analytical-modeling.md) · [Trino](trino.md) · [핸드북 홈](../index.md)
