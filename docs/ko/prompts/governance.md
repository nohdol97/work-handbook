---
id: prompts-governance
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# 데이터 거버넌스 실무 프롬프트

기존 학습 개념에서 파생해 작성한 재사용 가능한 가상 실무 예시다. 모델 호출·실제 운영·실험을 수행한 기록이 아니다. 대괄호 입력을 공개 가능한 비식별 정보로 채우고, 결과를 가설과 초안으로 검토한다.

[개념 문서](../data-platform/governance.md) · [프롬프트 모음](index.md)

| 사례 | 바로가기 |
| --- | --- |
| 01 | [소유권과 변경 책임 정리](#governance-01) |
| 02 | [분류를 접근·마스킹 정책에 연결](#governance-02) |
| 03 | [접근 경로별 정책 검증 계획](#governance-03) |
| 04 | [보관 요구와 snapshot 정책 구분](#governance-04) |
| 05 | [감사 기록으로 접근·변경 흐름 정리](#governance-05) |
| 06 | [producer와 consumer의 데이터 계약 검토](#governance-06) |

## 소유권과 변경 책임 정리 {#governance-01}

**상황:** schema 변경과 KPI 문의가 같은 창구로 몰려 책임을 나눈다.

**LLM에 제공할 맥락:** 데이터셋·pipeline·schema·SLO·KPI 정의: [비식별 목록] / 현재 기술·업무 담당 역할과 미지정 항목: [역할 목록]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    데이터셋·pipeline·schema·SLO·KPI 정의: [비식별 목록]
    현재 기술·업무 담당 역할과 미지정 항목: [역할 목록]
    [요청]
    Technical owner와 Business owner의 책임을 구분하세요.
    품질 장애·의미 변경·schema 변경별 협의 대상을 제시하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    데이터셋 / 책임 / 담당 역할 / 미지정 범위 / 확인 질문 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    실제 역할 합의와 catalog owner 정보를 대조하고 미지정 책임을 확인하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Datasets, pipelines, schemas, SLOs, and KPI definitions: [sanitized list]
    Current technical and business roles and unassigned items: [role list]
    [Task]
    Separate technical-owner and business-owner responsibilities.
    Name roles to consult for quality incidents, meaning changes, and schema changes.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of dataset, responsibility, role, unassigned scope, and questions.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare agreed roles with catalog owners and confirm unassigned responsibilities.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 데이터셋 / 책임 / 담당 역할 / 미지정 범위 / 확인 질문 표를 주세요.

**LLM 오류 가능성:** 업무 의미의 최종 판단을 pipeline 담당자에게 임의 배정할 수 있다.

**검증 방법:** 실제 역할 합의와 catalog owner 정보를 대조하고 미지정 책임을 확인하세요.

## 분류를 접근·마스킹 정책에 연결 {#governance-02}

**상황:** 새 schema의 민감 필드에 어떤 검토가 필요한지 정리한다.

**LLM에 제공할 맥락:** 필드명·의미·가상 값 유형·기존 분류 체계: [정의] / 역할별 사용 목적·접근·마스킹·보관 규칙: [승인된 정책]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    필드명·의미·가상 값 유형·기존 분류 체계: [정의]
    역할별 사용 목적·접근·마스킹·보관 규칙: [승인된 정책]
    [요청]
    중요도 등급과 PII 같은 데이터 성격을 별도로 평가하세요.
    column 접근 제한과 값 마스킹을 구분해 정책 연결을 검토하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    column / 분류 근거 / 접근 대상 / 마스킹 / 보관 질문 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    정책 담당자에게 분류·역할별 기대 결과를 확인하고 가상 값으로 검토하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Field names, meanings, synthetic value types, and classification scheme: [definitions]
    Role purposes, access, masking, and retention rules: [approved policy]
    [Task]
    Assess importance levels separately from data types such as PII.
    Review policy links while separating column access from value masking.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of column, classification evidence, access roles, masking, and retention questions.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Confirm classifications and expected role results with policy owners using synthetic values.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** column / 분류 근거 / 접근 대상 / 마스킹 / 보관 질문 표를 주세요.

**LLM 오류 가능성:** PII를 모든 등급의 최상위 값으로 놓거나 마스킹을 암호화로 취급할 수 있다.

**검증 방법:** 정책 담당자에게 분류·역할별 기대 결과를 확인하고 가상 값으로 검토하세요.

## 접근 경로별 정책 검증 계획 {#governance-03}

**상황:** catalog에는 정책이 보이지만 여러 엔진에서 같은 제어가 적용되는지 모른다.

**LLM에 제공할 맥락:** 역할·row/column 정책·마스킹 기대 결과: [정의] / 엔진·runtime·API·storage 경로와 지원 근거: [목록]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    역할·row/column 정책·마스킹 기대 결과: [정의]
    엔진·runtime·API·storage 경로와 지원 근거: [목록]
    [요청]
    표시된 정책과 실제 조회 경로의 강제 적용을 구분하세요.
    각 경로에 허용·거부·마스킹 기대 결과를 정하고 미확인 지원을 표시하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    역할 × 경로 검증 표와 필요한 공식 문서·설정 증거를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    설치된 버전의 문서·설정과 격리된 가상 데이터 조회 결과로 확인하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Roles, row/column policies, and expected masking results: [definitions]
    Engines, runtimes, APIs, storage paths, and support evidence: [list]
    [Task]
    Separate displayed policies from enforcement on real query paths.
    State allow, deny, and masking expectations for each path and mark unknown support.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a role-by-path check matrix and required official-doc and configuration evidence.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Check installed-version docs, configuration, and isolated queries against synthetic data.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 역할 × 경로 검증 표와 필요한 공식 문서·설정 증거를 주세요.

**LLM 오류 가능성:** 한 엔진의 성공을 모든 storage·API 경로의 보호로 일반화할 수 있다.

**검증 방법:** 설치된 버전의 문서·설정과 격리된 가상 데이터 조회 결과로 확인하세요.

## 보관 요구와 snapshot 정책 구분 {#governance-04}

**상황:** 저장 비용을 줄이려는데 원본·snapshot·backup의 보관 요구가 다르다.

**LLM에 제공할 맥락:** 데이터 유형·분석 가치·민감도·승인된 보관 요구: [목록] / snapshot 참조·backup·활성 쓰기·Hot/Cold/Archive 구성: [현황]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    데이터 유형·분석 가치·민감도·승인된 보관 요구: [목록]
    snapshot 참조·backup·활성 쓰기·Hot/Cold/Archive 구성: [현황]
    [요청]
    데이터 보관 요구와 snapshot 보존 기간을 분리하세요.
    보관 계층 선택과 정리 위험을 검토하되 삭제 작업은 실행하지 마세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    대상 / 승인 요구 / 현재 보관 / 참조·쓰기 위험 / 확인 질문 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    정책 owner가 요구를 확인하고 snapshot 참조·backup·실행 상태를 대조하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Data types, analytical value, sensitivity, and approved retention needs: [list]
    Snapshot references, backups, active writes, and Hot/Cold/Archive setup: [state]
    [Task]
    Separate data retention requirements from snapshot retention periods.
    Review storage-tier choices and cleanup risks without executing deletion.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of scope, approved need, current retention, reference/write risks, and questions.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Have policy owners confirm requirements and compare snapshot, backup, and run state.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 대상 / 승인 요구 / 현재 보관 / 참조·쓰기 위험 / 확인 질문 표를 주세요.

**LLM 오류 가능성:** 가상 14일을 법적 기본값으로 쓰거나 활성 파일을 orphan으로 오인할 수 있다.

**검증 방법:** 정책 owner가 요구를 확인하고 snapshot 참조·backup·실행 상태를 대조하세요.

## 감사 기록으로 접근·변경 흐름 정리 {#governance-05}

**상황:** 정책 변경 뒤 어떤 역할이 어떤 데이터에 접근했는지 검토한다.

**LLM에 제공할 맥락:** 익명 역할·dataset·시각·action·query 유형: [비식별 감사 요약] / schema·정책·owner·보관 변경과 수집 공백: [이력]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    익명 역할·dataset·시각·action·query 유형: [비식별 감사 요약]
    schema·정책·owner·보관 변경과 수집 공백: [이력]
    [요청]
    접근 감사와 변경 감사를 구분해 시간순으로 연결하세요.
    누가 무엇을 했는지와 데이터가 정상인지를 서로 다른 질문으로 다루세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    시각 / 역할 / 대상 / 행위 / 정책 상태 / 확인되지 않은 구간 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    감사 수집 범위와 정책 변경 기록을 대조하고 식별값 없이 결과를 검토하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Anonymous roles, datasets, times, actions, and query types: [sanitized audit summary]
    Schema, policy, owner, and retention changes and logging gaps: [history]
    [Task]
    Separate access and change audits and connect them by time.
    Treat who did what and whether data was healthy as separate questions.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of time, role, target, action, policy state, and unverified scope.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare audit coverage and policy-change records and review results without identifiers.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 시각 / 역할 / 대상 / 행위 / 정책 상태 / 확인되지 않은 구간 표를 주세요.

**LLM 오류 가능성:** 로그 누락을 접근 없음으로 해석하거나 원본 query의 민감 값을 노출할 수 있다.

**검증 방법:** 감사 수집 범위와 정책 변경 기록을 대조하고 식별값 없이 결과를 검토하세요.

## producer와 consumer의 데이터 계약 검토 {#governance-06}

**상황:** schema는 합의했지만 단위·품질·최신성·owner가 빠져 해석이 다르다.

**LLM에 제공할 맥락:** event_id·latency_ms·상태 필드 정의: [계약 초안] / producer·consumer 요구·SLO·owner·version: [합의와 미합의]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    event_id·latency_ms·상태 필드 정의: [계약 초안]
    producer·consumer 요구·SLO·owner·version: [합의와 미합의]
    [요청]
    타입뿐 아니라 의미·단위·필수·유일·범위 조건을 검토하세요.
    품질·최신성·소유권·버전의 빠진 약속을 질문으로 남기세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    계약 항목 / 현재 정의 / 모호함 / 가상 위반 예 / 합의 대상 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    양측 담당자의 요구와 정상·위반 가상 이벤트로 계약 해석을 확인하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    event_id, latency_ms, and status definitions: [draft contract]
    Producer and consumer needs, SLO, owner, and version: [agreed and open items]
    [Task]
    Review meanings, units, required values, uniqueness, and ranges as well as types.
    List questions for missing quality, freshness, ownership, and version agreements.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of contract item, definition, ambiguity, synthetic violation, and parties to consult.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Check interpretation with both owners' requirements and valid and invalid synthetic events.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 계약 항목 / 현재 정의 / 모호함 / 가상 위반 예 / 합의 대상 표를 주세요.

**LLM 오류 가능성:** integer가 밀리초를 보장한다고 보거나 제안 SLO를 승인된 약속으로 바꿀 수 있다.

**검증 방법:** 양측 담당자의 요구와 정상·위반 가상 이벤트로 계약 해석을 확인하세요.
