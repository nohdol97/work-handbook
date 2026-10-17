---
id: prompts-online-evaluation
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Online AI evaluation practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

[Concept guide](../data-platform/ai-evaluation.md#161-online-evaluation-events) · [Prompt library](index.md)

| Case | Jump to example |
| --- | --- |
| 01 | [Review links between evaluation events and executions](#online-evaluation-01) |
| 02 | [Separate unscored, failed, and low-score evaluations](#online-evaluation-02) |
| 03 | [Investigate disagreement between feedback and judge scores](#online-evaluation-03) |
| 04 | [Define what automatic evaluation rules prove](#online-evaluation-04) |
| 05 | [Compare online signals across agent versions](#online-evaluation-05) |
| 06 | [Organize evaluation cases first seen in live use](#online-evaluation-06) |

## Review links between evaluation events and executions {#online-evaluation-01}

**Prompt:**

=== "English"

    ```text {.prompt}
    A score-only event does not show which agent execution it evaluates.
    Find missing fields needed to recover the execution and evaluation conditions.
    Distinguish user feedback, rule, and judge event sources.
    Give a table of field, link purpose, current evidence, risk when absent, and check.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    점수만 저장된 이벤트로는 어떤 agent 실행을 평가했는지 알 수 없다.
    평가 대상 실행과 평가 조건을 복원하는 데 빠진 항목을 찾으세요.
    사용자 feedback·rule·judge 이벤트의 출처를 구분하세요.
    필드 / 연결 목적 / 현재 증거 / 누락 시 오해 / 확인 방법 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: evaluated execution IDs and evaluator definitions/versions. Link scores to evaluation definitions, versions, and pending states for the same samples. It may infer meaning from a score alone or treat all events as one scale. Do not combine different rubrics merely because their score numbers match.

## Separate unscored, failed, and low-score evaluations {#online-evaluation-02}

**Prompt:**

=== "English"

    ```text {.prompt}
    Responses are complete, but some asynchronous evaluations are unfinished.
    Count unscored, evaluator-failed, low-score, and normal-score cases separately.
    Mark cases that have no score yet because of the observation cutoff.
    Give counts and denominators by state and a list of evaluations to inspect.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    응답은 끝났지만 비동기 평가 일부가 아직 끝나지 않았다.
    미평가·평가 실패·낮은 점수·정상 점수를 별도 집계하세요.
    관측 마감 시각 때문에 아직 점수가 없는 사례를 표시하세요.
    상태별 건수·분모와 추가 확인할 평가 실행 목록을 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: the observation cutoff and pending/failed/completed evaluation states. Link scores to evaluation definitions, versions, and pending states for the same samples. It may distort quality by treating missing scores as success or zero. Reject aggregates that replace unscored cases with success or zero.

## Investigate disagreement between feedback and judge scores {#online-evaluation-03}

**Prompt:**

=== "English"

    ```text {.prompt}
    A user gives thumbs-down while the judge score is high.
    Separate the user's reason from the dimensions measured by the judge.
    Find disagreement types and missing evidence without making either signal absolute truth.
    Give a table of case, feedback reason, judge criterion, disagreement hypothesis, and human-review question.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    사용자는 thumbs-down을 줬는데 judge 점수는 높다.
    사람의 평가 이유와 judge가 측정한 항목을 분리하세요.
    어느 한쪽을 정답으로 고정하지 말고 불일치 유형과 누락 증거를 찾으세요.
    사례 / feedback 이유 / judge 기준 / 불일치 가설 / 사람 검토 질문 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: reasons for human feedback and the rubric used by the judge. Link scores to evaluation definitions, versions, and pending states for the same samples. It may dismiss complaints because of judge scores or generalize one response to all quality. Do not treat either users or judges as automatically correct.

## Define what automatic evaluation rules prove {#online-evaluation-04}

**Prompt:**

=== "English"

    ```text {.prompt}
    Citation, SQL, format, and prohibited-information checks may become one success score.
    Separate citation presence from accuracy and SQL execution from task correctness.
    State what each passing rule does not prove and what needs human review.
    Give a table of check, input, pass condition, missed errors, and further validation.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    citation·SQL·형식·금지 정보 검사를 하나의 성공 점수로 묶으려 한다.
    citation 존재와 내용 정확성, SQL 실행 가능성과 의도 적합성을 구분하세요.
    규칙별 통과가 보장하지 못하는 범위와 사람 검토 항목을 적으세요.
    검사 / 입력 / 통과 조건 / 놓칠 오류 / 추가 검증 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: each check's purpose and the scope of checks actually run. Link scores to evaluation definitions, versions, and pending states for the same samples. It may assume a citation is accurate or executable SQL is correct. Citation presence and executable SQL must not substitute for task correctness.

## Compare online signals across agent versions {#online-evaluation-05}

**Prompt:**

=== "English"

    ```text {.prompt}
    Agent versions have different scores, but questions and tool states also differ.
    Mark differences in traffic and evaluation conditions first.
    Separate comparable scopes from questions that need fixed-input offline checks.
    Give a table of version, observed signal, condition differences, comparison limits, and next checks.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    두 agent 버전의 점수가 다르지만 들어온 질문과 도구 상태도 다르다.
    traffic 구성과 평가 조건 차이를 먼저 표시하세요.
    비교 가능한 구간과 고정 입력의 offline 확인이 필요한 질문을 나누세요.
    버전 / 관측 신호 / 조건 차이 / 비교 한계 / 후속 확인 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: comparability of traffic mix and evaluator versions across agent versions. Link scores to evaluation definitions, versions, and pending states for the same samples. It may treat average score differences as the causal effect of a version change. Do not call a mean score difference the causal effect of a version improvement.

## Organize evaluation cases first seen in live use {#online-evaluation-06}

**Prompt:**

=== "English"

    ```text {.prompt}
    Online signals show questions, long context, and tool failures absent from offline cases.
    Classify symptoms for new questions, tool failures, long context, permissions, and data changes.
    Separate confirmed failures from evaluation signals and propose follow-up review.
    Give a table of symptom, trace evidence, existing coverage, candidate case, and review question.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    offline 사례에 없던 질문·긴 context·tool 장애 신호가 온라인에서 보인다.
    새 질문·tool 장애·긴 context·권한·데이터 변화 증상을 분류하세요.
    실패로 확인된 사례와 평가 신호만 있는 사례를 나누어 후속 검토를 제시하세요.
    증상 / trace 근거 / 기존 coverage / 추가 사례 후보 / 확인 질문 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: traces of confirmed failures and existing evaluation coverage. Link scores to evaluation definitions, versions, and pending states for the same samples. It may treat a low score as a confirmed new bug or copy sensitive conversations into evaluation data. Keep low-score-only cases separate from demonstrated failures.
