---
id: prompts-online-evaluation
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# 온라인 AI 평가 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

[개념 문서](../data-platform/ai-evaluation.md#161-online-evaluation-events) · [프롬프트 모음](index.md)

| 사례 | 바로가기 |
| --- | --- |
| 01 | [평가 이벤트와 실행 연결 검토](#online-evaluation-01) |
| 02 | [미평가·평가 실패·낮은 점수 구분](#online-evaluation-02) |
| 03 | [사용자 feedback과 judge 점수 불일치 조사](#online-evaluation-03) |
| 04 | [자동 평가 규칙의 검증 범위 정리](#online-evaluation-04) |
| 05 | [agent 버전별 온라인 신호 비교](#online-evaluation-05) |
| 06 | [실환경에서 새로 나타난 평가 사례 정리](#online-evaluation-06) |

## 평가 이벤트와 실행 연결 검토 {#online-evaluation-01}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    점수만 저장된 이벤트로는 어떤 agent 실행을 평가했는지 알 수 없다.
    평가 대상 실행과 평가 조건을 복원하는 데 빠진 항목을 찾으세요.
    사용자 feedback·rule·judge 이벤트의 출처를 구분하세요.
    필드 / 연결 목적 / 현재 증거 / 누락 시 오해 / 확인 방법 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    A score-only event does not show which agent execution it evaluates.
    Find missing fields needed to recover the execution and evaluation conditions.
    Distinguish user feedback, rule, and judge event sources.
    Give a table of field, link purpose, current evidence, risk when absent, and check.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 평가 대상 실행 ID와 evaluator 정의·버전. 점수뿐 아니라 평가 정의·버전·대기 상태를 같은 표본에 연결한다. score만으로 평가의 의미를 추정하거나 모든 이벤트를 같은 척도로 취급할 수 있다. 점수 숫자가 같다는 이유로 다른 rubric 결과를 합치지 않는다.

## 미평가·평가 실패·낮은 점수 구분 {#online-evaluation-02}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    응답은 끝났지만 비동기 평가 일부가 아직 끝나지 않았다.
    미평가·평가 실패·낮은 점수·정상 점수를 별도 집계하세요.
    관측 마감 시각 때문에 아직 점수가 없는 사례를 표시하세요.
    상태별 건수·분모와 추가 확인할 평가 실행 목록을 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Responses are complete, but some asynchronous evaluations are unfinished.
    Count unscored, evaluator-failed, low-score, and normal-score cases separately.
    Mark cases that have no score yet because of the observation cutoff.
    Give counts and denominators by state and a list of evaluations to inspect.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 관측 마감 시각과 평가 대기·실패·완료 상태 정의. 점수뿐 아니라 평가 정의·버전·대기 상태를 같은 표본에 연결한다. 누락 점수를 성공이나 0점으로 치환해 품질을 왜곡할 수 있다. 미평가를 성공 또는 0점으로 대체한 집계는 거부한다.

## 사용자 feedback과 judge 점수 불일치 조사 {#online-evaluation-03}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    사용자는 thumbs-down을 줬는데 judge 점수는 높다.
    사람의 평가 이유와 judge가 측정한 항목을 분리하세요.
    어느 한쪽을 정답으로 고정하지 말고 불일치 유형과 누락 증거를 찾으세요.
    사례 / feedback 이유 / judge 기준 / 불일치 가설 / 사람 검토 질문 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    A user gives thumbs-down while the judge score is high.
    Separate the user's reason from the dimensions measured by the judge.
    Find disagreement types and missing evidence without making either signal absolute truth.
    Give a table of case, feedback reason, judge criterion, disagreement hypothesis, and human-review question.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 사람 feedback의 이유와 judge가 적용한 rubric. 점수뿐 아니라 평가 정의·버전·대기 상태를 같은 표본에 연결한다. 높은 judge 점수로 불만을 무시하거나 feedback 한 건을 전체 품질로 일반화할 수 있다. 사용자나 judge 어느 한쪽을 자동 정답으로 채택하지 않는다.

## 자동 평가 규칙의 검증 범위 정리 {#online-evaluation-04}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    citation·SQL·형식·금지 정보 검사를 하나의 성공 점수로 묶으려 한다.
    citation 존재와 내용 정확성, SQL 실행 가능성과 의도 적합성을 구분하세요.
    규칙별 통과가 보장하지 못하는 범위와 사람 검토 항목을 적으세요.
    검사 / 입력 / 통과 조건 / 놓칠 오류 / 추가 검증 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Citation, SQL, format, and prohibited-information checks may become one success score.
    Separate citation presence from accuracy and SQL execution from task correctness.
    State what each passing rule does not prove and what needs human review.
    Give a table of check, input, pass condition, missed errors, and further validation.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 검사별 목적과 실제 실행한 검증 범위. 점수뿐 아니라 평가 정의·버전·대기 상태를 같은 표본에 연결한다. citation이 있으면 정확하거나 SQL이 실행되면 정답이라고 결론낼 수 있다. citation 존재·SQL 실행 가능성이 의도 적합성을 대신하지 않아야 한다.

## agent 버전별 온라인 신호 비교 {#online-evaluation-05}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    두 agent 버전의 점수가 다르지만 들어온 질문과 도구 상태도 다르다.
    traffic 구성과 평가 조건 차이를 먼저 표시하세요.
    비교 가능한 구간과 고정 입력의 offline 확인이 필요한 질문을 나누세요.
    버전 / 관측 신호 / 조건 차이 / 비교 한계 / 후속 확인 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Agent versions have different scores, but questions and tool states also differ.
    Mark differences in traffic and evaluation conditions first.
    Separate comparable scopes from questions that need fixed-input offline checks.
    Give a table of version, observed signal, condition differences, comparison limits, and next checks.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 버전별 traffic 구성과 evaluator 버전의 비교 가능성. 점수뿐 아니라 평가 정의·버전·대기 상태를 같은 표본에 연결한다. 평균 점수 차이를 버전 변경의 인과 효과로 단정할 수 있다. 평균 점수 차이를 곧바로 버전 개선의 인과 효과로 표현하지 않는다.

## 실환경에서 새로 나타난 평가 사례 정리 {#online-evaluation-06}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    offline 사례에 없던 질문·긴 context·tool 장애 신호가 온라인에서 보인다.
    새 질문·tool 장애·긴 context·권한·데이터 변화 증상을 분류하세요.
    실패로 확인된 사례와 평가 신호만 있는 사례를 나누어 후속 검토를 제시하세요.
    증상 / trace 근거 / 기존 coverage / 추가 사례 후보 / 확인 질문 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Online signals show questions, long context, and tool failures absent from offline cases.
    Classify symptoms for new questions, tool failures, long context, permissions, and data changes.
    Separate confirmed failures from evaluation signals and propose follow-up review.
    Give a table of symptom, trace evidence, existing coverage, candidate case, and review question.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 실패로 확인된 trace와 기존 평가 coverage. 점수뿐 아니라 평가 정의·버전·대기 상태를 같은 표본에 연결한다. 낮은 점수만으로 새 오류를 확정하거나 민감한 실제 대화를 평가 자료에 복사할 수 있다. 낮은 점수뿐인 사례와 실제 실패가 입증된 사례를 따로 남긴다.
