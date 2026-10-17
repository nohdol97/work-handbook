---
id: prompts-ai-ready-data
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# AI-ready 데이터 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

[개념 문서](../data-platform/ai-ready-data.md) · [프롬프트 모음](index.md)

| 사례 | 바로가기 |
| --- | --- |
| 01 | [AI 실행 telemetry의 연결 누락 찾기](#ai-ready-data-01) |
| 02 | [실패를 평가 데이터 사례로 바꾸기](#ai-ready-data-02) |
| 03 | [embedding 갱신의 버전 추적](#ai-ready-data-03) |
| 04 | [RAG 검색 실패와 생성 실패 구분](#ai-ready-data-04) |
| 05 | [사용 금지 source의 파생 영향 추적](#ai-ready-data-05) |
| 06 | [늦게 확정되는 label과 오래된 입력 구분](#ai-ready-data-06) |

## AI 실행 telemetry의 연결 누락 찾기 {#ai-ready-data-01}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    도구 호출 비용과 사용자 피드백이 어느 실행에 속하는지 불명확하다.
    요청 묶음·개별 단계·대화 묶음을 구분해 연결 누락을 찾으세요.
    수집 허용·마스킹·보관 범위를 고려해 필요한 최소 추가 정보를 제시하세요.
    분석 질문 / 필요한 연결 / 현재 필드 / 누락 증거 / 수집 제약 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    It is unclear which execution owns tool-call costs and user feedback.
    Separate requests, individual steps, and conversations to find missing links.
    Suggest the missing information needed, within collection, masking, and retention rules.
    Give a table of analysis question, required link, current fields, missing evidence, and collection limits.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: Trace·Observation·Execution 식별자의 실제 연결 규칙. Session과 Trace를 혼동하거나 민감한 prompt 전체 수집을 기본으로 제안할 수 있다. 허용된 표본이 실행·단계·feedback까지 연결되는지 확인한다. 분석 편의를 이유로 전체 prompt 수집을 기본값으로 추가하지 않는다.

## 실패를 평가 데이터 사례로 바꾸기 {#ai-ready-data-02}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    수정된 agent 오류가 다시 발생하지 않도록 평가 사례 초안을 만든다.
    실패 원인을 단정하지 말고 관찰 가능한 기대 행동을 rubric으로 만드세요.
    같은 실패를 잡는 사례와 정상 행동을 보존하는 비교 사례를 제안하세요.
    입력 placeholder / 기대 행동 / 실패 조건 / 출처 / dataset 버전 초안을 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Draft evaluation cases to catch a fixed agent failure if it returns.
    Define observable expected behavior in a rubric without assuming the failure cause.
    Propose a case that catches the failure and a comparison case that preserves valid behavior.
    Draft input placeholders, expected behavior, failure conditions, provenance, and dataset version.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 확인된 실패 증거와 수정 뒤 기대 행동. 정확한 문장 일치만 요구하거나 성공 사례만 늘려 실패 조건을 놓칠 수 있다. 특정 문장 일치 대신 관찰 가능한 실패 재발 조건으로 채점한다.

## embedding 갱신의 버전 추적 {#ai-ready-data-03}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    chunk 전략과 embedding model을 바꾸기 전에 재검색 비교 범위를 정한다.
    문서·chunk·vector의 연결과 빠진 버전 필드를 찾으세요.
    모델 변경과 chunk 전략 변경을 구분할 비교 계획을 제시하세요.
    변경 축 / 보존할 버전 / 비교 질의 / 관찰 결과 / 미확인 범위 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Define retrieval comparisons before changing chunking and the embedding model.
    Check document, chunk, and vector links and find missing version fields.
    Propose comparisons that distinguish model changes from chunking changes.
    Give a table of change, versions to preserve, query, observed results, and unknown scope.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 문서·chunk·embedding의 버전 대응과 변경 축. vector 공간이 같다고 가정하거나 검색 변화 원인을 모델 하나로 단정할 수 있다. chunk 전략과 모델을 동시에 바꾼 결과에서 한 원인을 확정하지 않는다.

## RAG 검색 실패와 생성 실패 구분 {#ai-ready-data-04}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    답이 틀렸을 때 필요한 문서를 못 찾았는지 찾고도 잘못 답했는지 분류한다.
    필요 문서가 권한 내에서 검색되고 모델에 전달됐는지 확인하세요.
    검색 누락·오래된 근거·생성 해석 오류를 각각 가설로 구분하세요.
    질문 / 검색 근거 / 응답 주장 / 실패 구간 후보 / 다음 확인 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Classify whether a wrong answer came from missing evidence or misuse of retrieved evidence.
    Check whether required, authorized evidence was retrieved and sent to the model.
    Separate missing retrieval, stale evidence, and answer-interpretation hypotheses.
    Give a table of question, retrieved evidence, response claim, possible failure stage, and next check.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 실제로 모델에 전달된 허용 chunk와 기대 근거. 정답 문서가 있어도 권한 없이 제공해야 한다고 보거나 높은 score를 정답으로 볼 수 있다. 높은 검색 score를 근거 충족이나 정답의 증거로 대신하지 않는다.

## 사용 금지 source의 파생 영향 추적 {#ai-ready-data-05}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    문서를 더 이상 사용할 수 없어 관련 chunk·vector·응답 범위를 조사한다.
    원본부터 응답까지 provenance 경로와 알려진 파생 범위를 정리하세요.
    추적 가능성과 실제 사용 중단·삭제 완료를 구분하세요.
    대상 / 원본 연결 증거 / 영향 후보 / 확인 담당 / 미확인 사본 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    A source may no longer be used, so investigate related chunks, vectors, and responses.
    Map provenance from source to response and list known derived scope.
    Separate traceability from proof that use has stopped or deletion is complete.
    Give a table of target, source-link evidence, possible impact, owner, and unknown copies.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 사용 중단 대상 source 버전과 파생 연결의 수집 범위. lineage 경로만으로 모든 응답을 찾았다고 주장하거나 삭제를 실행할 수 있다. lineage가 이어진다는 사실과 실제 사용 중단 완료를 따로 기록한다.

## 늦게 확정되는 label과 오래된 입력 구분 {#ai-ready-data-06}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    평가에 최신 입력과 아직 확정되지 않은 결과 label이 섞였다.
    입력 freshness와 label 확정 지연을 서로 다른 문제로 분리하세요.
    미확정 label을 확정 정답으로 사용하는 사례와 오래된 입력을 찾으세요.
    사례 구간 / 입력 나이 / label 상태 / 평가 포함 조건 / 보류 이유 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Evaluation mixes current inputs with outcome labels that are not yet final.
    Separate input freshness from delay in label finalization.
    Find cases using pending labels as final truth and cases with stale inputs.
    Give a table of case window, input age, label state, inclusion criteria, and hold reason.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 결과 관찰창과 label 확정 시각. 아직 발생하지 않은 결과를 음성 label로 확정하거나 최신성 기준을 임의로 만들 수 있다. 아직 관찰창이 끝나지 않은 결과를 음성 정답으로 확정하지 않는다.
