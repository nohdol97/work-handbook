---
id: prompts-ai-ready-data
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# AI-ready data practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

[Concept guide](../data-platform/ai-ready-data.md) · [Prompt library](index.md)

| Case | Jump to example |
| --- | --- |
| 01 | [Find missing links in AI telemetry](#ai-ready-data-01) |
| 02 | [Turn a failure into an evaluation case](#ai-ready-data-02) |
| 03 | [Track versions through an embedding refresh](#ai-ready-data-03) |
| 04 | [Separate RAG retrieval failures from answer failures](#ai-ready-data-04) |
| 05 | [Trace effects of a source that can no longer be used](#ai-ready-data-05) |
| 06 | [Separate delayed labels from stale inputs](#ai-ready-data-06) |

## Find missing links in AI telemetry {#ai-ready-data-01}

**Prompt:**

=== "English"

    ```text {.prompt}
    It is unclear which execution owns tool-call costs and user feedback.
    Separate requests, individual steps, and conversations to find missing links.
    Suggest the missing information needed, within collection, masking, and retention rules.
    Give a table of analysis question, required link, current fields, missing evidence, and collection limits.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    도구 호출 비용과 사용자 피드백이 어느 실행에 속하는지 불명확하다.
    요청 묶음·개별 단계·대화 묶음을 구분해 연결 누락을 찾으세요.
    수집 허용·마스킹·보관 범위를 고려해 필요한 최소 추가 정보를 제시하세요.
    분석 질문 / 필요한 연결 / 현재 필드 / 누락 증거 / 수집 제약 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: actual linking rules for Trace, Observation, and Execution identifiers. It may confuse Sessions with Traces or default to collecting full sensitive prompts. Check that permitted samples link executions, steps, and feedback. Do not default to collecting full prompts for analytical convenience.

## Turn a failure into an evaluation case {#ai-ready-data-02}

**Prompt:**

=== "English"

    ```text {.prompt}
    Draft evaluation cases to catch a fixed agent failure if it returns.
    Define observable expected behavior in a rubric without assuming the failure cause.
    Propose a case that catches the failure and a comparison case that preserves valid behavior.
    Draft input placeholders, expected behavior, failure conditions, provenance, and dataset version.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    수정된 agent 오류가 다시 발생하지 않도록 평가 사례 초안을 만든다.
    실패 원인을 단정하지 말고 관찰 가능한 기대 행동을 rubric으로 만드세요.
    같은 실패를 잡는 사례와 정상 행동을 보존하는 비교 사례를 제안하세요.
    입력 placeholder / 기대 행동 / 실패 조건 / 출처 / dataset 버전 초안을 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: confirmed failure evidence and expected behavior after the fix. It may require exact wording or add only successful cases and miss the failure. Score observable recurrence of the failure rather than exact wording.

## Track versions through an embedding refresh {#ai-ready-data-03}

**Prompt:**

=== "English"

    ```text {.prompt}
    Define retrieval comparisons before changing chunking and the embedding model.
    Check document, chunk, and vector links and find missing version fields.
    Propose comparisons that distinguish model changes from chunking changes.
    Give a table of change, versions to preserve, query, observed results, and unknown scope.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    chunk 전략과 embedding model을 바꾸기 전에 재검색 비교 범위를 정한다.
    문서·chunk·vector의 연결과 빠진 버전 필드를 찾으세요.
    모델 변경과 chunk 전략 변경을 구분할 비교 계획을 제시하세요.
    변경 축 / 보존할 버전 / 비교 질의 / 관찰 결과 / 미확인 범위 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: version mapping across documents, chunks, and embeddings and the changed dimensions. It may assume vector spaces are unchanged or blame every retrieval change on the model. Do not isolate one cause when chunking and the model changed together.

## Separate RAG retrieval failures from answer failures {#ai-ready-data-04}

**Prompt:**

=== "English"

    ```text {.prompt}
    Classify whether a wrong answer came from missing evidence or misuse of retrieved evidence.
    Check whether required, authorized evidence was retrieved and sent to the model.
    Separate missing retrieval, stale evidence, and answer-interpretation hypotheses.
    Give a table of question, retrieved evidence, response claim, possible failure stage, and next check.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    답이 틀렸을 때 필요한 문서를 못 찾았는지 찾고도 잘못 답했는지 분류한다.
    필요 문서가 권한 내에서 검색되고 모델에 전달됐는지 확인하세요.
    검색 누락·오래된 근거·생성 해석 오류를 각각 가설로 구분하세요.
    질문 / 검색 근거 / 응답 주장 / 실패 구간 후보 / 다음 확인 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: authorized chunks actually sent to the model and expected evidence. It may demand an unauthorized document or treat a high retrieval score as a correct answer. Do not treat high retrieval scores as sufficient evidence or proof of correctness.

## Trace effects of a source that can no longer be used {#ai-ready-data-05}

**Prompt:**

=== "English"

    ```text {.prompt}
    A source may no longer be used, so investigate related chunks, vectors, and responses.
    Map provenance from source to response and list known derived scope.
    Separate traceability from proof that use has stopped or deletion is complete.
    Give a table of target, source-link evidence, possible impact, owner, and unknown copies.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    문서를 더 이상 사용할 수 없어 관련 chunk·vector·응답 범위를 조사한다.
    원본부터 응답까지 provenance 경로와 알려진 파생 범위를 정리하세요.
    추적 가능성과 실제 사용 중단·삭제 완료를 구분하세요.
    대상 / 원본 연결 증거 / 영향 후보 / 확인 담당 / 미확인 사본 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: prohibited source versions and collection scope for derived links. It may claim all responses are found from lineage alone or try to delete data. Record traceability separately from verified cessation of use.

## Separate delayed labels from stale inputs {#ai-ready-data-06}

**Prompt:**

=== "English"

    ```text {.prompt}
    Evaluation mixes current inputs with outcome labels that are not yet final.
    Separate input freshness from delay in label finalization.
    Find cases using pending labels as final truth and cases with stale inputs.
    Give a table of case window, input age, label state, inclusion criteria, and hold reason.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    평가에 최신 입력과 아직 확정되지 않은 결과 label이 섞였다.
    입력 freshness와 label 확정 지연을 서로 다른 문제로 분리하세요.
    미확정 label을 확정 정답으로 사용하는 사례와 오래된 입력을 찾으세요.
    사례 구간 / 입력 나이 / label 상태 / 평가 포함 조건 / 보류 이유 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: the outcome observation window and label finalization times. It may mark an outcome as negative before its window closes or invent freshness limits. Do not label an outcome as negative before its observation window closes.
