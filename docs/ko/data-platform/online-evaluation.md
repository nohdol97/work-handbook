---
id: data-platform-online-evaluation
status: studied
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids:
  - DPE-16-01
---

# 온라인 AI 평가 이벤트

원문에서 Phase 16은 16.1만 학습했다. 이 페이지는 해당 범위의 개념 학습 기록이며 운영 시스템을 구현했다는 주장이 아니다.

## 16.1 Online Evaluation Events

Online Evaluation:

> **실제 Production에서 발생한 AI 실행에 평가 데이터를 붙이는 것**

흐름:

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

Evaluation Event 예:

- thumbs_up / thumbs_down
- rating
- user_feedback
- LLM judge score
- rule-based score
- error type

중요:

```text
score = 0.4
```

만 저장하면 부족하다.

Trace와 연결해야 한다.

함께 연결:

- trace_id
- execution_id
- model_version
- prompt_version
- agent_version
- score
- feedback

---

### User Feedback

Production Online Evaluation의 가장 단순한 형태.

```text
Response
 ↓
👍 / 👎
```

---

### Automatic Evaluation

Response 직후:

```text
LLM Judge
Rule Check
```

등으로 평가 가능.

예:

- SQL 실행 가능?
- Citation 존재?
- 금지 정보 포함?
- Output Format 준수?

---

### Langfuse 연결

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

## 평가 데이터의 한계

Online 평가는 실제 traffic에 평가를 붙이고, offline 평가는 고정한 입력으로 변경을 비교한다. 사람의 feedback, 규칙, LLM judge는 서로 다른 신호이며 점수 하나를 절대적인 정답으로 취급하지 않는다. [Langfuse evaluation concepts](https://langfuse.com/docs/evaluation/core-concepts).

평가 실행은 응답 직후뿐 아니라 비동기로 끝날 수 있다. 평가 정의와 evaluator 버전, 평가 시각, 실패·미평가 상태도 구분하면 점수 누락을 성공으로 오해하지 않을 수 있다. 이는 원문의 trace 연결 원칙을 확장한 설계 권고이며 여기서 구현·측정한 결과는 아니다. SQL 실행 가능성 확인은 별도 격리 환경에서 수행하고, citation 존재 여부와 내용의 정확성을 구분한다.

## LLM in Practice: 낮은 점수 조사

- **상황:** 새 agent 버전에서 낮은 점수 사례가 늘었다.
- **제공 맥락:** 비식별 trace, tool 상태, 평가 규칙·버전, 평가 실패 수, 배포 전후 표본과 traffic 구성.
- **예시 prompt:**

```text
Inspect these low-score traces and evaluation records.
Group observed failures by retrieval, generation, tool, and permission symptoms.
Keep unscored requests separate from successful requests.
List missing evidence and the next checks for each hypothesis.
Do not execute tools or infer a root cause from the score alone.
```

- **기대 결과:** 근거가 연결된 증상 분류와 추가 확인 목록.
- **오류 가능성:** judge 오류를 agent 오류로 보거나 미평가 요청을 정상으로 셀 수 있다.
- **검증:** 원본 trace와 평가 결과를 사람이 대조하고, 안전한 환경에서 실패 조건을 재현한다. 실행 검증은 아직 하지 않았다.

[AI-ready 데이터](ai-ready-data.md) · [학습 범위와 남은 과정](curriculum.md)
