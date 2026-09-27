---
id: data-platform-online-evaluation
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - DPE-16-01
  - DPE2-16-01
---

# Chapter 16 — AI Evaluation Data Platform

첫 원문에서는 Phase 16의 16.1만 학습했고, 추가 원문으로 이 내용을 보강했다. 이 페이지는 16.1의 개념 학습 기록이며 운영 시스템을 구현했다는 주장이 아니다. 16.2–16.12는 [AI 평가 데이터 플랫폼](ai-evaluation.md)에서 이어진다.


본문은 최신 통합본 16.1을 같은 구조로 번역했다. 기존 자료의 Langfuse 설명과 평가 적용 조건은 본문 뒤 보완 설명에서 구분한다.

**본문 안내:** 아래 원문 구역은 원래 순서와 형태를 보존한 본문이다. 원문의 단순화된 설명에 대한 정정·적용 조건과 추가 설명은 문서 뒤 보완 구역에서 해당 절 번호와 함께 확인한다.

<!-- SOURCE CORE START -->

## 16.1 Online Evaluation Events

Online Evaluation은 다음을 뜻한다:

> **실제 Production에서 일어난 AI 실행을 평가하고 해당 Trace에 평가 데이터를 연결하는 것.**

기본 흐름:

```text
User Request
   ↓
Agent
   ↓
LLM / Tool
   ↓
Response
   ↓
Evaluation
```

가능한 평가 이벤트:

```text
thumbs_up / thumbs_down
rating
user_feedback
llm_judge_score
rule_based_score
error_type
```

점수만으로는 충분하지 않다.

부족한 예:

```text
score = 0.4
```

더 나은 예:

```text
trace_id
execution_id
agent_version
prompt_version
model_version
score
feedback
```

이 정보를 연결하면 다음 질문에 답할 수 있다:

```text
이 응답의 품질이 낮았던 이유는 무엇인가?
어떤 Prompt를 사용했는가?
어떤 Model이 생성했는가?
어떤 Tool을 호출했는가?
어떤 Agent 릴리스에서 생성했는가?
```

### User Feedback

가장 단순한 Online Evaluation은 다음과 같다:

```text
Response
  ↓
👍 / 👎
```

더 상세하게 다음 정보를 남길 수도 있다:

```text
rating = 1~5
reason = inaccurate
comment = "wrong tool was selected"
```

### Automatic Evaluation

Production 응답을 자동으로 평가할 수도 있다.

```text
Response
 ↓
LLM Judge
 ↓
Score
```

또는:

```text
Response
 ↓
Rule Check
 ↓
Pass / Fail
```

검사할 수 있는 항목:

- 생성된 SQL을 실행할 수 있는가?
- 필요한 Citation이 있는가?
- 출력에 금지된 정보가 포함됐는가?
- 응답이 예상 Schema를 따르는가?
- Agent가 올바르거나 허용된 Tool을 호출했는가?

핵심:

> **Online Evaluation은 실제 Production 조건에서 AI가 어떻게 동작하는지 보여 준다.**

Offline Test에서 놓칠 수 있는 것:

- 새로운 사용자 행동,
- 변화하는 데이터,
- Tool 장애,
- 긴 Context,
- 권한,
- Production에서만 발생하는 Edge Case.

---

<!-- SOURCE CORE END -->

## 보완 설명: 16.1 Langfuse 연결과 평가 조건

### 기존 자료의 Langfuse 연결

개념:

```text
Langfuse Trace
 ├─ Prompt
 ├─ LLM Call
 ├─ Tool Call
 ├─ Response
 └─ Score / Feedback
```

활용:

- 낮은 Score Trace 검색
- Thumbs-down 사례 분석
- 특정 Agent Version 비교
- Production Failure → Eval Dataset 추가

Online Evaluation의 목적:

> **실제 사용자 환경의 품질을 지속 관찰**

Offline Test에서 드러나지 않는:

- 새로운 사용자 질문
- Tool 장애
- 긴 Context
- 실제 Permission
- Production Data 변화

를 관찰할 수 있다.

---


**Tool 평가 조건:** 예상 schema 준수와 tool 권한 준수는 별도 검사다. 선택한 tool이 적절한지와 그 사용이 허용됐는지를 각각 확인한다. 점수만으로 근본 원인을 증명할 수는 없다.

Online 평가는 실제 traffic에 평가를 붙이고, offline 평가는 고정한 입력으로 변경을 비교한다. 사람의 feedback, 규칙, LLM judge는 서로 다른 신호이며 점수 하나를 절대적인 정답으로 취급하지 않는다. [Langfuse evaluation concepts](https://langfuse.com/docs/evaluation/core-concepts).

평가 실행은 응답 직후뿐 아니라 비동기로 끝날 수 있다. 평가 정의와 evaluator 버전, 평가 시각, 실패·미평가 상태도 구분하면 점수 누락을 성공으로 오해하지 않을 수 있다. 이는 원문의 trace 연결 원칙을 확장한 설계 권고이며 여기서 구현·측정한 결과는 아니다. SQL 실행 가능성 확인은 별도 격리 환경에서 수행하고, citation 존재 여부와 내용의 정확성을 구분한다.

## LLM in Practice: 낮은 점수 조사

- **상황:** 새 agent 버전에서 낮은 점수 사례가 늘었다.
- **제공 맥락:** 비식별 trace, tool 상태, 평가 규칙·버전, 평가 실패 수, 배포 전후 표본과 traffic 구성.
- **예시 prompt:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    낮은 점수 trace와 평가 기록: [비식별 표본]
    tool 상태·평가 규칙·버전·평가 실패 수: [자료]
    전후 표본·traffic 구성: [비교 구간]
    [요청]
    retrieval·generation·tool·permission 증상별로 관측 실패를 묶으세요.
    미평가 요청을 성공 요청과 구분하세요.
    [출력]
    각 가설의 누락 근거와 다음 확인을 나열하세요.
    증상에 해당 trace와 평가 근거를 연결하세요.
    [검증]
    tool을 실행하거나 점수만으로 근본 원인을 추론하지 마세요.
    원본 trace·평가를 대조하고 안전한 재현 계획을 적으세요.
    judge 오류와 agent 오류를 구분하고 실행했다고 주장하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Low-score traces and evaluation records: [sanitized samples]
    Tool state, evaluation rules, versions, and evaluator failure counts: [material]
    Before/after samples and traffic mix: [comparison windows]
    [Task]
    Group observed failures by retrieval, generation, tool, and permission symptoms.
    Keep unscored requests separate from successful requests.
    [Output]
    List missing evidence and the next checks for each hypothesis.
    Link symptoms to the related traces and evaluation evidence.
    [Checks]
    Do not execute tools or infer a root cause from the score alone.
    Compare original traces and evaluations and draft a safe reproduction plan.
    Separate judge errors from agent errors; do not claim checks were run.
    ```

- **기대 결과:** 근거가 연결된 증상 분류와 추가 확인 목록.
- **오류 가능성:** judge 오류를 agent 오류로 보거나 미평가 요청을 정상으로 셀 수 있다.
- **검증:** 원본 trace와 평가 결과를 사람이 대조하고, 안전한 환경에서 실패 조건을 재현한다. 실행 검증은 아직 하지 않았다.

[AI-ready 데이터](ai-ready-data.md) · [학습 범위와 남은 과정](curriculum.md)

[더 많은 실무 프롬프트](../prompts/online-evaluation.md)
