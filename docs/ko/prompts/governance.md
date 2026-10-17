---
id: prompts-governance
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# 데이터 거버넌스 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

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

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    schema 변경과 KPI 문의가 같은 창구로 몰려 책임을 나눈다.
    Technical owner와 Business owner의 책임을 구분하세요.
    품질 장애·의미 변경·schema 변경별 협의 대상을 제시하세요.
    데이터셋 / 책임 / 담당 역할 / 미지정 범위 / 확인 질문 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Schema changes and KPI questions go to one team, so clarify responsibility.
    Separate technical-owner and business-owner responsibilities.
    Name roles to consult for quality incidents, meaning changes, and schema changes.
    Give a table of dataset, responsibility, role, unassigned scope, and questions.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 실제 역할 합의와 미지정 책임. 승인된 정책과 검토 중인 제안을 분리해 제공한다. 업무 의미의 최종 판단을 pipeline 담당자에게 임의 배정할 수 있다. 기술 담당자가 업무 의미의 최종 결정권자라고 임의 지정하지 않는다.

## 분류를 접근·마스킹 정책에 연결 {#governance-02}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    새 schema의 민감 필드에 어떤 검토가 필요한지 정리하려고 해.
    중요도 등급과 PII 같은 데이터 성격을 별도로 평가하세요.
    column 접근 제한과 값 마스킹을 구분해 정책 연결을 검토하세요.
    column / 분류 근거 / 접근 대상 / 마스킹 / 보관 질문 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Identify the policy review needed for sensitive fields in a new schema.
    Assess importance levels separately from data types such as PII.
    Review policy links while separating column access from value masking.
    Give a table of column, classification evidence, access roles, masking, and retention questions.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 승인된 분류 체계와 역할별 사용 목적. 승인된 정책과 검토 중인 제안을 분리해 제공한다. PII를 모든 등급의 최상위 값으로 놓거나 마스킹을 암호화로 취급할 수 있다. 필드 이름만으로 민감도나 허용 역할을 확정하지 않는다.

## 접근 경로별 정책 검증 계획 {#governance-03}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    catalog에는 정책이 보이지만 여러 엔진에서 같은 제어가 적용되는지 모른다.
    표시된 정책과 실제 조회 경로의 강제 적용을 구분하세요.
    각 경로에 허용·거부·마스킹 기대 결과를 정하고 미확인 지원을 표시하세요.
    역할 × 경로 검증 표와 필요한 공식 문서·설정 증거를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Policies appear in the catalog, but enforcement across engines is unknown.
    Separate displayed policies from enforcement on real query paths.
    State allow, deny, and masking expectations for each path and mark unknown support.
    Give a role-by-path check matrix and required official-doc and configuration evidence.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 실제 API·엔진·storage 접근 경로 목록. 승인된 정책과 검토 중인 제안을 분리해 제공한다. 한 엔진의 성공을 모든 storage·API 경로의 보호로 일반화할 수 있다. 한 경로의 성공을 전체 경로의 정책 적용 증거로 쓰지 않는다.

## 보관 요구와 snapshot 정책 구분 {#governance-04}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    저장 비용을 줄이려는데 원본·snapshot·backup의 보관 요구가 다르다.
    데이터 보관 요구와 snapshot 보존 기간을 분리하세요.
    보관 계층 선택과 정리 위험을 검토하되 삭제 작업은 실행하지 마세요.
    대상 / 승인 요구 / 현재 보관 / 참조·쓰기 위험 / 확인 질문 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Storage cost needs review, but source, snapshot, and backup retention needs differ.
    Separate data retention requirements from snapshot retention periods.
    Review storage-tier choices and cleanup risks without executing deletion.
    Give a table of scope, approved need, current retention, reference/write risks, and questions.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 정책 owner가 확인한 원본·snapshot·backup 보존 요구. 승인된 정책과 검토 중인 제안을 분리해 제공한다. 가상 14일을 법적 기본값으로 쓰거나 활성 파일을 orphan으로 오인할 수 있다. 보관 계층 변경과 물리 삭제 완료를 같은 결과로 취급하지 않는다.

## 감사 기록으로 접근·변경 흐름 정리 {#governance-05}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    정책 변경 뒤 어떤 역할이 어떤 데이터에 접근했는지 검토 중이야.
    접근 감사와 변경 감사를 구분해 시간순으로 연결하세요.
    누가 무엇을 했는지와 데이터가 정상인지를 서로 다른 질문으로 다루세요.
    시각 / 역할 / 대상 / 행위 / 정책 상태 / 확인되지 않은 구간 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review which roles accessed which data after a policy change.
    Separate access and change audits and connect them by time.
    Treat who did what and whether data was healthy as separate questions.
    Give a table of time, role, target, action, policy state, and unverified scope.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 감사 수집 범위와 정책 변경 시점. 승인된 정책과 검토 중인 제안을 분리해 제공한다. 로그 누락을 접근 없음으로 해석하거나 원본 query의 민감 값을 노출할 수 있다. 로그 공백을 접근 없음이나 정책 준수의 증거로 쓰지 않는다.

## producer와 consumer의 데이터 계약 검토 {#governance-06}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    schema는 합의했지만 단위·품질·최신성·owner가 빠져 해석이 다르다.
    타입뿐 아니라 의미·단위·필수·유일·범위 조건을 검토하세요.
    품질·최신성·소유권·버전의 빠진 약속을 질문으로 남기세요.
    계약 항목 / 현재 정의 / 모호함 / 가상 위반 예 / 합의 대상 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    A schema is agreed, but units, quality, freshness, and ownership are missing.
    Review meanings, units, required values, uniqueness, and ranges as well as types.
    List questions for missing quality, freshness, ownership, and version agreements.
    Give a table of contract item, definition, ambiguity, synthetic violation, and parties to consult.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: producer·consumer가 합의한 의미·SLO·변경 책임. 승인된 정책과 검토 중인 제안을 분리해 제공한다. integer가 밀리초를 보장한다고 보거나 제안 SLO를 승인된 약속으로 바꿀 수 있다. 제안 목표와 승인된 계약을 구분한 상태로 검토를 마친다.
