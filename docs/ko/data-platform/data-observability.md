---
id: data-platform-data-observability
status: studied
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids:
  - DPE-12-01
  - DPE-12-02
  - DPE-12-03
  - DPE-12-04
  - DPE-12-05
  - DPE-12-06
  - DPE-12-07
---

# 데이터 관측성

이 Learn 문서는 데이터 상태를 지속적으로 측정하는 개념을 다룬다. 아래 수치와 장애는 학습용 예시이며 실측이나 실무 경험이 아니다. 데이터 품질이 기대 조건을 정의한다면, 관측성은 데이터가 지금 어떤 상태인지 확인하고 이상 구간을 찾도록 돕는다.

## 최신성을 단계별로 나누기

| 단계 | 질문 | 확인 범위 |
| --- | --- | --- |
| Source freshness | 원본이 제시간에 생성·수집되는가 | 원본 생성과 수집 |
| Pipeline freshness | 처리 지연은 어느 구간에서 커지는가 | Kafka → Bronze → Silver → Gold |
| Downstream freshness | 사용자가 최신 데이터를 보는가 | Dashboard와 BI |

단계별 시각을 비교하면 지연이 시작된 구간을 찾기 쉽다. 운영에 적용할 때는 이벤트 시각, 수집 시각, 처리 완료 시각, 화면 갱신 시각을 구별해야 한다. 이들은 같은 측정값이 아니다.

## 데이터 양의 변화

평소보다 적거나 많은 건수, 누락된 partition은 조사 신호다.

| 변화 | 가능한 원인 |
| --- | --- |
| 급감 | 수집 장애, producer 문제, filter bug |
| 급증 | duplicate, replay, retry storm, 실제 traffic spike |
| Partition 누락 | 해당 범위가 생성되거나 처리되지 않았을 가능성 |

최근 평균, 같은 요일, 계절적 패턴과 비교한다. 절대 임계값만 보면 정상적인 주말 감소를 장애로 알리거나 특정 partition 누락을 전체 합계 속에서 놓칠 수 있다. 위 원인들은 가설이며 건수 변화만으로 확정하지 않는다.

## 스키마와 분포 감시

스키마 감시 대상은 column 추가·삭제·rename, type 변경, nullable 변경이다. Breaking change는 downstream consumer를 깨뜨릴 수 있다. [Lineage](lineage-metadata.md)를 연결하면 영향을 받을 소비자를 찾는 데 도움이 된다.

Volume이 정상이어도 값의 분포는 달라질 수 있다. Null rate drift, cardinality drift, 범주 값의 분포 변화, 수치 분포 변화를 본다.

```text
평소 FAILED 비율 = 5%
오늘 FAILED 비율 = 45%
전체 row 수 = 평소 범위
```

이 예시는 건수만으로 data health를 판단할 수 없음을 보여 준다. 실패율의 실제 증가인지 status 기록 방식의 변경인지 추가 증거로 구분해야 한다.

## Pipeline health와 data health

| Pipeline health | Data health |
| --- | --- |
| Job status | Freshness |
| Kafka lag | Volume |
| Runtime | Schema |
| CPU와 memory | NULL과 duplicate |
| 실행 failure | Distribution |

**Green pipeline ≠ healthy data.** Job이 성공했어도 query logic 오류로 결과가 0 rows일 수 있다. 반대로 job 지연을 발견했어도 어느 데이터와 사용자가 영향을 받는지는 데이터 상태와 함께 확인해야 한다.

## SLI와 SLO

관측성은 데이터 상태를 계속 측정한다. 아래는 대응하는 측정값과 목표의 가상 예다.

| SLI 측정값 | SLO 목표 예시 |
| --- | --- |
| Freshness = 3분 | Freshness < 5분 |
| NULL rate = 0.5% | NULL rate < 1% |
| Volume = 98M rows | 기준선 대비 volume deviation < 20% |

98M이라는 값만으로 편차 목표의 충족 여부를 판단할 수 없다. 기준선과 측정 기간이 필요하다. 여러 신호를 함께 보고 데이터셋의 업무 목적에 맞게 정의한다. [품질 SLO](data-quality.md)와 같은 정의를 공유해야 측정과 대응이 어긋나지 않는다.

## 대응할 수 있는 알림

목표는 알림 수를 늘리는 것이 아니라 대응할 가치가 있는 이상을 전달하는 것이다. 임계값 근처에서 ALERT와 RECOVERY가 반복되면 noisy alert가 된다. 어디부터 조사해야 하는지 알 수 있어야 actionable alert다.

알림에 다음을 포함한다.

- **Threshold:** 어떤 조건을 위반했는가.
- **Duration:** 얼마나 지속됐는가.
- **Severity:** 영향이 얼마나 큰가. Warning과 Critical을 구분할 수 있다.
- **Context:** 어떤 dataset과 partition, 단계, owner, 관련 실행을 확인해야 하는가.

데이터셋 중요도 tier별로 정책을 달리할 수 있다. 지속 시간과 문맥을 정의해 alert fatigue를 줄이되 중요한 신호가 가려지지 않는지 확인한다.

## LLM in Practice: 성공한 작업의 빈 결과 조사

**상황:** Gold 작업은 성공했는데 대시보드의 오늘 데이터가 0 rows다.

**LLM에 제공할 맥락:** 단계별 row count와 freshness, partition 목록, 최근 schema 및 filter 변경, 실행 로그, 평소 같은 요일의 기준선, 데이터셋 SLO를 익명화해 제공한다.

**예시 프롬프트:**

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

**기대 결과:** 원본 미도착, partition 누락, filter 오류, downstream 갱신 지연 등을 구별하는 조사 순서다.

**틀릴 수 있는 부분:** Green job을 정상 데이터의 증거로 취급하거나 전체 건수만 보고 누락된 partition을 놓칠 수 있다.

**검증 방법:** 각 단계의 실제 쿼리 결과와 시각, 변경 이력, 대시보드 갱신 상태를 확인한다. LLM의 가설을 증거로 확인한 뒤 조치한다.

[데이터 품질](data-quality.md) · [Lineage와 metadata](lineage-metadata.md) · [핸드북 홈](../index.md)

[더 많은 실무 프롬프트](../prompts/data-observability.md)
