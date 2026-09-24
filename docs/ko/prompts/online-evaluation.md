---
id: prompts-online-evaluation
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# 온라인 AI 평가 실무 프롬프트

기존 학습 개념에서 파생해 작성한 재사용 가능한 가상 실무 예시다. 모델 호출·실제 운영·실험을 수행한 기록이 아니다. 대괄호 입력을 공개 가능한 비식별 정보로 채우고, 결과를 가설과 초안으로 검토한다.

[개념 문서](../data-platform/online-evaluation.md) · [프롬프트 모음](index.md)

| 사례 | 바로가기 |
| --- | --- |
| 01 | [평가 이벤트와 실행 연결 검토](#online-evaluation-01) |
| 02 | [미평가·평가 실패·낮은 점수 구분](#online-evaluation-02) |
| 03 | [사용자 feedback과 judge 점수 불일치 조사](#online-evaluation-03) |
| 04 | [자동 평가 규칙의 검증 범위 정리](#online-evaluation-04) |
| 05 | [agent 버전별 온라인 신호 비교](#online-evaluation-05) |
| 06 | [실환경에서 새로 나타난 평가 사례 정리](#online-evaluation-06) |

## 평가 이벤트와 실행 연결 검토 {#online-evaluation-01}

**상황:** 점수만 저장된 이벤트로는 어떤 agent 실행을 평가했는지 알 수 없다.

**LLM에 제공할 맥락:** trace_id·execution_id·model·prompt·agent 버전: [이벤트 정의] / score·feedback·평가 정의·evaluator 버전·시각·상태: [필드 목록]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    trace_id·execution_id·model·prompt·agent 버전: [이벤트 정의]
    score·feedback·평가 정의·evaluator 버전·시각·상태: [필드 목록]
    [요청]
    평가 대상 실행과 평가 조건을 복원하는 데 빠진 항목을 찾으세요.
    사용자 feedback·rule·judge 이벤트의 출처를 구분하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    필드 / 연결 목적 / 현재 증거 / 누락 시 오해 / 확인 방법 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    가상 이벤트를 원본 실행과 연결하고 버전·평가 정의가 일치하는지 확인하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    trace_id, execution_id, model, prompt, and agent versions: [event definition]
    Score, feedback, evaluator definition/version, time, and state: [field list]
    [Task]
    Find missing fields needed to recover the execution and evaluation conditions.
    Distinguish user feedback, rule, and judge event sources.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of field, link purpose, current evidence, risk when absent, and check.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Link synthetic events to executions and check version and evaluation-definition agreement.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 필드 / 연결 목적 / 현재 증거 / 누락 시 오해 / 확인 방법 표를 주세요.

**LLM 오류 가능성:** score만으로 평가의 의미를 추정하거나 모든 이벤트를 같은 척도로 취급할 수 있다.

**검증 방법:** 가상 이벤트를 원본 실행과 연결하고 버전·평가 정의가 일치하는지 확인하세요.

## 미평가·평가 실패·낮은 점수 구분 {#online-evaluation-02}

**상황:** 응답은 끝났지만 비동기 평가 일부가 아직 끝나지 않았다.

**LLM에 제공할 맥락:** 요청·응답·평가 시각과 score 상태: [비식별 이벤트] / 평가 실패·대기·완료 기준과 evaluator 버전: [정의]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    요청·응답·평가 시각과 score 상태: [비식별 이벤트]
    평가 실패·대기·완료 기준과 evaluator 버전: [정의]
    [요청]
    미평가·평가 실패·낮은 점수·정상 점수를 별도 집계하세요.
    관측 마감 시각 때문에 아직 점수가 없는 사례를 표시하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    상태별 건수·분모와 추가 확인할 평가 실행 목록을 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    원본 이벤트 상태와 평가 시각을 대조하고 같은 마감 시각으로 다시 집계하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Request, response, and evaluation times and score states: [sanitized events]
    Evaluation failure, pending, and completion rules and evaluator versions: [definitions]
    [Task]
    Count unscored, evaluator-failed, low-score, and normal-score cases separately.
    Mark cases that have no score yet because of the observation cutoff.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give counts and denominators by state and a list of evaluations to inspect.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare event states and evaluation times and recount using one cutoff.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 상태별 건수·분모와 추가 확인할 평가 실행 목록을 주세요.

**LLM 오류 가능성:** 누락 점수를 성공이나 0점으로 치환해 품질을 왜곡할 수 있다.

**검증 방법:** 원본 이벤트 상태와 평가 시각을 대조하고 같은 마감 시각으로 다시 집계하세요.

## 사용자 feedback과 judge 점수 불일치 조사 {#online-evaluation-03}

**상황:** 사용자는 thumbs-down을 줬는데 judge 점수는 높다.

**LLM에 제공할 맥락:** 비식별 응답·feedback·judge 근거·평가 정의: [표본] / trace의 질문·tool 상태·권한·evaluator 버전: [허용 요약]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    비식별 응답·feedback·judge 근거·평가 정의: [표본]
    trace의 질문·tool 상태·권한·evaluator 버전: [허용 요약]
    [요청]
    사람의 평가 이유와 judge가 측정한 항목을 분리하세요.
    어느 한쪽을 정답으로 고정하지 말고 불일치 유형과 누락 증거를 찾으세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    사례 / feedback 이유 / judge 기준 / 불일치 가설 / 사람 검토 질문 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    원본 질문·응답·rubric을 사람이 함께 검토하고 판단 불가 사례를 남기세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Sanitized response, feedback, judge rationale, and evaluation definition: [samples]
    Trace question, tool state, permissions, and evaluator version: [permitted summary]
    [Task]
    Separate the user's reason from the dimensions measured by the judge.
    Find disagreement types and missing evidence without making either signal absolute truth.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of case, feedback reason, judge criterion, disagreement hypothesis, and human-review question.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Have a person compare the question, answer, and rubric and mark unresolved cases.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 사례 / feedback 이유 / judge 기준 / 불일치 가설 / 사람 검토 질문 표를 주세요.

**LLM 오류 가능성:** 높은 judge 점수로 불만을 무시하거나 feedback 한 건을 전체 품질로 일반화할 수 있다.

**검증 방법:** 원본 질문·응답·rubric을 사람이 함께 검토하고 판단 불가 사례를 남기세요.

## 자동 평가 규칙의 검증 범위 정리 {#online-evaluation-04}

**상황:** citation·SQL·형식·금지 정보 검사를 하나의 성공 점수로 묶으려 한다.

**LLM에 제공할 맥락:** 응답 유형·형식·citation 요구·금지 정보 정책: [정의] / 현재 rule·judge 기준·격리 검증 가능 범위: [목록]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    응답 유형·형식·citation 요구·금지 정보 정책: [정의]
    현재 rule·judge 기준·격리 검증 가능 범위: [목록]
    [요청]
    citation 존재와 내용 정확성, SQL 실행 가능성과 의도 적합성을 구분하세요.
    규칙별 통과가 보장하지 못하는 범위와 사람 검토 항목을 적으세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    검사 / 입력 / 통과 조건 / 놓칠 오류 / 추가 검증 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    가상 반례로 규칙을 점검하고 SQL 실행 검증은 별도 격리 환경 계획으로 남기세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Response types, format, citation needs, and prohibited-information policy: [definitions]
    Current rules, judge criteria, and available isolated checks: [list]
    [Task]
    Separate citation presence from accuracy and SQL execution from task correctness.
    State what each passing rule does not prove and what needs human review.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of check, input, pass condition, missed errors, and further validation.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Review rules against synthetic counterexamples; plan SQL execution only in a separate isolated environment.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 검사 / 입력 / 통과 조건 / 놓칠 오류 / 추가 검증 표를 주세요.

**LLM 오류 가능성:** citation이 있으면 정확하거나 SQL이 실행되면 정답이라고 결론낼 수 있다.

**검증 방법:** 가상 반례로 규칙을 점검하고 SQL 실행 검증은 별도 격리 환경 계획으로 남기세요.

## agent 버전별 온라인 신호 비교 {#online-evaluation-05}

**상황:** 두 agent 버전의 점수가 다르지만 들어온 질문과 도구 상태도 다르다.

**LLM에 제공할 맥락:** 버전별 점수·feedback·미평가 수·관측 기간: [비식별 집계] / 질문 유형·긴 context·권한·tool 장애·평가 버전: [구성]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    버전별 점수·feedback·미평가 수·관측 기간: [비식별 집계]
    질문 유형·긴 context·권한·tool 장애·평가 버전: [구성]
    [요청]
    traffic 구성과 평가 조건 차이를 먼저 표시하세요.
    비교 가능한 구간과 고정 입력의 offline 확인이 필요한 질문을 나누세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    버전 / 관측 신호 / 조건 차이 / 비교 한계 / 후속 확인 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    같은 정의·기간의 원본 집계를 대조하고 traffic 차이가 남는 범위를 표시하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Scores, feedback, unscored counts, and windows by version: [sanitized aggregates]
    Question types, long context, permissions, tool failures, and evaluator versions: [mix]
    [Task]
    Mark differences in traffic and evaluation conditions first.
    Separate comparable scopes from questions that need fixed-input offline checks.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of version, observed signal, condition differences, comparison limits, and next checks.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare source aggregates with matched definitions and windows and mark remaining traffic differences.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 버전 / 관측 신호 / 조건 차이 / 비교 한계 / 후속 확인 표를 주세요.

**LLM 오류 가능성:** 평균 점수 차이를 버전 변경의 인과 효과로 단정할 수 있다.

**검증 방법:** 같은 정의·기간의 원본 집계를 대조하고 traffic 차이가 남는 범위를 표시하세요.

## 실환경에서 새로 나타난 평가 사례 정리 {#online-evaluation-06}

**상황:** offline 사례에 없던 질문·긴 context·tool 장애 신호가 온라인에서 보인다.

**LLM에 제공할 맥락:** 비식별 trace·error type·feedback·rule 또는 judge 결과: [표본] / 기존 평가 사례 범위·권한 조건·데이터 변경: [비교 자료]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    비식별 trace·error type·feedback·rule 또는 judge 결과: [표본]
    기존 평가 사례 범위·권한 조건·데이터 변경: [비교 자료]
    [요청]
    새 질문·tool 장애·긴 context·권한·데이터 변화 증상을 분류하세요.
    실패로 확인된 사례와 평가 신호만 있는 사례를 나누어 후속 검토를 제시하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    증상 / trace 근거 / 기존 coverage / 추가 사례 후보 / 확인 질문 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    원본을 허용 범위에서 검토하고 비식별화된 후보만 기존 사례와 대조하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Sanitized traces, error types, feedback, and rule or judge results: [samples]
    Existing evaluation coverage, permission conditions, and data changes: [comparison material]
    [Task]
    Classify symptoms for new questions, tool failures, long context, permissions, and data changes.
    Separate confirmed failures from evaluation signals and propose follow-up review.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of symptom, trace evidence, existing coverage, candidate case, and review question.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Review sources within permitted access and compare only sanitized candidates with existing cases.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 증상 / trace 근거 / 기존 coverage / 추가 사례 후보 / 확인 질문 표를 주세요.

**LLM 오류 가능성:** 낮은 점수만으로 새 오류를 확정하거나 민감한 실제 대화를 평가 자료에 복사할 수 있다.

**검증 방법:** 원본을 허용 범위에서 검토하고 비식별화된 후보만 기존 사례와 대조하세요.
