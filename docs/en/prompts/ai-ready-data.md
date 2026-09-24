---
id: prompts-ai-ready-data
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# AI-ready data practical prompts

These reusable, hypothetical work examples were authored from existing study concepts. They are not records of model runs, production work, or experiments. Fill placeholders with sanitized information safe to share. Treat results as hypotheses and drafts.

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

**Situation:** It is unclear which execution owns tool-call costs and user feedback.

**Context to Give the LLM:** Trace, Observation, Session, and Execution links: [sanitized schema] / Model and agent versions, tool state, latency, tokens, cost, and scores: [fields]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Trace, Observation, Session, and Execution links: [sanitized schema]
    Model and agent versions, tool state, latency, tokens, cost, and scores: [fields]
    [Task]
    Separate requests, individual steps, and conversations to find missing links.
    Suggest the missing information needed, within collection, masking, and retention rules.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of analysis question, required link, current fields, missing evidence, and collection limits.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Trace sanitized examples from prompt to feedback and compare collection with policy.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Trace·Observation·Session·Execution 연결 정의: [비식별 schema]
    모델·agent 버전·tool 상태·latency·token·cost·score: [항목 목록]
    [요청]
    요청 묶음·개별 단계·대화 묶음을 구분해 연결 누락을 찾으세요.
    수집 허용·마스킹·보관 범위를 고려해 필요한 최소 추가 정보를 제시하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    분석 질문 / 필요한 연결 / 현재 필드 / 누락 증거 / 수집 제약 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    비식별 실행 표본에서 prompt부터 feedback까지 연결하고 정책과 대조하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of analysis question, required link, current fields, missing evidence, and collection limits.

**What the LLM Can Get Wrong:** It may confuse Sessions with Traces or default to collecting full sensitive prompts.

**How to Validate:** Trace sanitized examples from prompt to feedback and compare collection with policy.

## Turn a failure into an evaluation case {#ai-ready-data-02}

**Situation:** Draft evaluation cases to catch a fixed agent failure if it returns.

**Context to Give the LLM:** Sanitized failure trace, fix details, and expected behavior: [material] / Existing normal, hard, failure, edge, safety, and tool cases: [list]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Sanitized failure trace, fix details, and expected behavior: [material]
    Existing normal, hard, failure, edge, safety, and tool cases: [list]
    [Task]
    Define observable expected behavior in a rubric without assuming the failure cause.
    Propose a case that catches the failure and a comparison case that preserves valid behavior.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Draft input placeholders, expected behavior, failure conditions, provenance, and dataset version.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare the rubric with the original failure evidence and check it on synthetic responses.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    비식별 실패 trace·수정 내용·기대 행동: [자료]
    기존 normal·hard·failure·edge·safety·tool 사례: [목록]
    [요청]
    실패 원인을 단정하지 말고 관찰 가능한 기대 행동을 rubric으로 만드세요.
    같은 실패를 잡는 사례와 정상 행동을 보존하는 비교 사례를 제안하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    입력 placeholder / 기대 행동 / 실패 조건 / 출처 / dataset 버전 초안을 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    원래 실패의 관측 증거와 rubric을 대조하고 가상 응답으로 판정 일관성을 확인하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Draft input placeholders, expected behavior, failure conditions, provenance, and dataset version.

**What the LLM Can Get Wrong:** It may require exact wording or add only successful cases and miss the failure.

**How to Validate:** Compare the rubric with the original failure evidence and check it on synthetic responses.

## Track versions through an embedding refresh {#ai-ready-data-03}

**Situation:** Define retrieval comparisons before changing chunking and the embedding model.

**Context to Give the LLM:** Document, chunk, and embedding versions and chunking strategy: [current definitions] / Proposed changes, sample queries, retrieved results, and source owners: [sanitized material]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Document, chunk, and embedding versions and chunking strategy: [current definitions]
    Proposed changes, sample queries, retrieved results, and source owners: [sanitized material]
    [Task]
    Check document, chunk, and vector links and find missing version fields.
    Propose comparisons that distinguish model changes from chunking changes.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of change, versions to preserve, query, observed results, and unknown scope.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Check source-to-chunk links and version records, then compare results for identical queries.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    문서·chunk·embedding 버전과 chunking 전략: [현행 정의]
    변경 제안·대표 질의·검색 결과·source owner: [비식별 자료]
    [요청]
    문서·chunk·vector의 연결과 빠진 버전 필드를 찾으세요.
    모델 변경과 chunk 전략 변경을 구분할 비교 계획을 제시하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    변경 축 / 보존할 버전 / 비교 질의 / 관찰 결과 / 미확인 범위 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    원본·chunk 연결과 실제 버전 기록을 확인하고 동일 질의 결과를 비교하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of change, versions to preserve, query, observed results, and unknown scope.

**What the LLM Can Get Wrong:** It may assume vector spaces are unchanged or blame every retrieval change on the model.

**How to Validate:** Check source-to-chunk links and version records, then compare results for identical queries.

## Separate RAG retrieval failures from answer failures {#ai-ready-data-04}

**Situation:** Classify whether a wrong answer came from missing evidence or misuse of retrieved evidence.

**Context to Give the LLM:** Question, expected evidence, retrieved chunks, scores, and document versions: [sanitized samples] / Model input, response, access_level, and permission-filter results: [permitted summary]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Question, expected evidence, retrieved chunks, scores, and document versions: [sanitized samples]
    Model input, response, access_level, and permission-filter results: [permitted summary]
    [Task]
    Check whether required, authorized evidence was retrieved and sent to the model.
    Separate missing retrieval, stale evidence, and answer-interpretation hypotheses.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of question, retrieved evidence, response claim, possible failure stage, and next check.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Check permissions and actual model input first, then compare claims with the chunks.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    질문·기대 근거·검색 chunk·score·document 버전: [비식별 표본]
    모델 입력·응답·access_level·권한 필터 결과: [허용된 요약]
    [요청]
    필요 문서가 권한 내에서 검색되고 모델에 전달됐는지 확인하세요.
    검색 누락·오래된 근거·생성 해석 오류를 각각 가설로 구분하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    질문 / 검색 근거 / 응답 주장 / 실패 구간 후보 / 다음 확인 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    권한과 실제 모델 입력을 먼저 확인하고 응답 주장을 해당 chunk와 대조하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of question, retrieved evidence, response claim, possible failure stage, and next check.

**What the LLM Can Get Wrong:** It may demand an unauthorized document or treat a high retrieval score as a correct answer.

**How to Validate:** Check permissions and actual model input first, then compare claims with the chunks.

## Trace effects of a source that can no longer be used {#ai-ready-data-05}

**Situation:** A source may no longer be used, so investigate related chunks, vectors, and responses.

**Context to Give the LLM:** Source document, version, chunk, embedding, and retrieval links: [sanitized metadata] / Model and response links, retention/use policy, and missing paths: [record]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Source document, version, chunk, embedding, and retrieval links: [sanitized metadata]
    Model and response links, retention/use policy, and missing paths: [record]
    [Task]
    Map provenance from source to response and list known derived scope.
    Separate traceability from proof that use has stopped or deletion is complete.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of target, source-link evidence, possible impact, owner, and unknown copies.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Review scope using actual references, retrieval records, and policy owners; do not delete data.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    원본 문서·버전·chunk·embedding·retrieval 연결: [비식별 metadata]
    model·response 연결·보관 및 사용 정책·누락 경로: [기록]
    [요청]
    원본부터 응답까지 provenance 경로와 알려진 파생 범위를 정리하세요.
    추적 가능성과 실제 사용 중단·삭제 완료를 구분하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    대상 / 원본 연결 증거 / 영향 후보 / 확인 담당 / 미확인 사본 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    실제 참조·검색 기록·정책 담당자 확인으로 범위를 검토하고 삭제는 실행하지 마세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of target, source-link evidence, possible impact, owner, and unknown copies.

**What the LLM Can Get Wrong:** It may claim all responses are found from lineage alone or try to delete data.

**How to Validate:** Review scope using actual references, retrieval records, and policy owners; do not delete data.

## Separate delayed labels from stale inputs {#ai-ready-data-06}

**Situation:** Evaluation mixes current inputs with outcome labels that are not yet final.

**Context to Give the LLM:** Feature cutoff, input refresh, and prediction times: [sanitized time definitions] / Outcome window, label finalization time, and pending state: [rules and counts]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Feature cutoff, input refresh, and prediction times: [sanitized time definitions]
    Outcome window, label finalization time, and pending state: [rules and counts]
    [Task]
    Separate input freshness from delay in label finalization.
    Find cases using pending labels as final truth and cases with stale inputs.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of case window, input age, label state, inclusion criteria, and hold reason.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare times with business finalization rules and count pending cases separately.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    feature 기준 시각·입력 갱신·예측 시각: [비식별 시각 정의]
    결과 관찰 기간·label 확정 시각·미확정 상태: [규칙과 집계]
    [요청]
    입력 freshness와 label 확정 지연을 서로 다른 문제로 분리하세요.
    미확정 label을 확정 정답으로 사용하는 사례와 오래된 입력을 찾으세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    사례 구간 / 입력 나이 / label 상태 / 평가 포함 조건 / 보류 이유 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    업무상 결과 확정 규칙과 각 시각을 대조하고 미확정 사례를 따로 집계하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of case window, input age, label state, inclusion criteria, and hold reason.

**What the LLM Can Get Wrong:** It may mark an outcome as negative before its window closes or invent freshness limits.

**How to Validate:** Compare times with business finalization rules and count pending cases separately.
