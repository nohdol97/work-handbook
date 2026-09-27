---
id: data-platform-data-observability
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - DPE-12-01
  - DPE-12-02
  - DPE-12-03
  - DPE-12-04
  - DPE-12-05
  - DPE-12-06
  - DPE-12-07
---

# Chapter 12 — Data Observability

This Learn page covers continuous measurement of data health. The numbers and incidents are learning examples, not measurements or hands-on experience. Data quality defines expected conditions. Observability helps show the current state and locate where a problem starts.

**Reading note:** The source core below keeps the original order and form. Read the section-specific corrections, conditions, and additions in the supplement after the source material; some original statements are simplified.

<!-- SOURCE CORE START -->

## 12.1 Data Freshness

### Source Freshness

Is source data created and collected on time?

### Pipeline Freshness

Measure processing delay across Kafka → Bronze → Silver → Gold.

### Downstream Freshness

Do dashboards and BI show current data?

Freshness at each stage helps locate where delay starts.

---

## 12.2 Volume Monitoring

Detect sharp decreases or increases in row counts compared with normal levels.

Possible causes of a decrease:

- Collection failure
- Producer problem
- Filter bug

Possible causes of an increase:

- Duplicates
- Replay
- Retry storm
- Traffic spike

A missing partition is another important signal.

Rather than using only an absolute value:

- Recent averages
- The same weekday
- Seasonal patterns

Compare counts with baselines such as these.

---

## 12.3 Schema Monitoring

Watch for these changes:

- Column addition
- Column removal
- Rename
- Type change
- Nullable change

A breaking change can break downstream consumers.

Connecting schema monitoring with lineage helps find the affected consumers.

---

## 12.4 Distribution Drift

Volume can remain normal while value distributions change.

Common signals:

- Null rate drift
- Cardinality drift
- Value distribution drift
- Numeric distribution drift

Example:

```text
Usual FAILED rate = 5%
Today's FAILED rate = 45%
```

Normal volume does not prove that data is healthy.

---

## 12.5 Pipeline Health vs Data Health

Pipeline health:

- Job status
- Kafka lag
- Runtime
- CPU and memory
- Failures

Data health:

- Freshness
- Volume
- Schema
- Nulls
- Duplicates
- Distributions

The key idea:

> **Green pipeline ≠ healthy data.**

A successful job can return zero rows because its query logic is wrong.

---

## 12.6 Data SLIs / SLOs

Observability measures data state over time.

Example SLIs:

```text
Freshness = 3 minutes
NULL rate = 0.5%
Volume = 98M
```

Example SLOs:

```text
Freshness < 5 minutes
NULL rate < 1%
Volume deviation < 20%
```

Use several signals together.

---

## 12.7 Alert Design

The goal:

> **Report problems worth acting on, rather than maximizing alert count.**

### Noisy Alert

ALERT and RECOVERY repeat near the threshold.

### Actionable Alert

The alert makes it clear where to investigate.

A useful alert includes:

```text
Threshold
+
Duration
+
Severity
+
Context
```

Warning and Critical can use different levels.

Alert policies can also vary by dataset importance tier.

Avoid alert fatigue.

---

<!-- SOURCE CORE END -->

## Details to check in practice

### Freshness timestamps

Event time, collection time, processing completion time, and screen refresh time are different measurements. Define which timestamps to compare before using them in operations.

### Investigating volume and drift

An absolute threshold alone can flag a normal weekend decline. A total count can hide a missing partition.

The listed causes of decreases and increases are hypotheses. A volume change alone does not prove one. When the FAILED rate changes, check whether failures really increased or the way status is recorded changed.

Connect schema changes to [lineage](lineage-metadata.md) to help find affected consumers. If a job is late, check data health too. Find which datasets and users are affected.

### Interpreting SLIs and SLOs

Volume = 98M alone cannot show whether the deviation target is met. You need a baseline and a measurement window.

Define several signals for the dataset's business purpose. Share definitions with [quality SLOs](data-quality.md) so that measurement and response agree.

### Concrete alert context

- **Threshold:** Which condition failed?
- **Duration:** How long has it lasted?
- **Severity:** How large is the impact?
- **Context:** Which dataset, partition, stage, owner, and related run should be checked?

Define duration and context to reduce alert fatigue. Check that this does not hide important signals.

## LLM in Practice: investigate empty output from a successful job

**Situation:** The Gold job succeeded, but today's dashboard data has zero rows.

**Context to Give the LLM:** Provide sanitized row counts and freshness by stage, partition lists, recent schema and filter changes, run logs, a normal same-weekday baseline, and dataset SLOs.

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    The Gold job succeeded, but today's dashboard shows zero rows.
    Row counts, freshness by stage, and partition list: [measurements]
    Schema and filter changes and run logs: [sanitized history]
    Same-weekday baseline and SLOs: [definitions and values]
    [Task]
    Investigate this hypothetical incident before suggesting a redesign.
    Separate facts, assumptions, hypotheses, and missing evidence.
    Do not infer a root cause from correlation alone.
    [Output]
    Rank the next checks and explain what each result would support.
    [Checks]
    Compare stage query results, times, change history, and dashboard refresh.
    Do not execute operational actions before evidence supports the hypothesis.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Gold 작업은 성공했지만 오늘 대시보드는 0 rows입니다.
    단계별 row count·freshness와 partition 목록: [측정]
    schema·filter 변경과 실행 로그: [비식별 이력]
    같은 요일 기준선과 SLO: [정의와 값]
    [요청]
    재설계를 제안하기 전에 이 가상 장애를 조사하세요.
    사실·가정·가설·누락 근거를 구분하세요.
    상관관계만으로 근본 원인을 추론하지 마세요.
    [출력]
    다음 확인의 우선순위와 각 결과가 지지할 가설을 주세요.
    [검증]
    단계별 실제 query 결과·시각·변경 이력·화면 갱신을 대조하세요.
    가설을 증거로 확인하기 전에는 운영 조치를 실행하지 마세요.
    ```

**Expected Output:** Checks that separate missing source data, missing partitions, filter errors, and delayed downstream refresh.

**What the LLM Can Get Wrong:** It may treat a green job as evidence of healthy data. It may inspect only total counts and miss a missing partition.

**How to Validate:** Check actual query results and timestamps at each stage, change history, and dashboard refresh state. Confirm the LLM's hypotheses with evidence before acting.

[Data quality](data-quality.md) · [Lineage and metadata](lineage-metadata.md) · [Handbook home](../index.md)

[More practical prompts](../prompts/data-observability.md)
