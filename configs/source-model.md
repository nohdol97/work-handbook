# 자료 추적 스키마

자료별로 `sources/<batch>/`에 다음 파일을 만든다. 아래는 예시 스키마이며 실제 반입 자료가 아니다. 지식 ID는 원문 batch가 달라도 충돌하지 않게 유지한다. 공개 페이지 front matter의 `knowledge_ids`에는 반영된 ID를 넣는다.

## 원문과 매핑

`source.md`에는 민감 정보를 제거한 원문과 원문 범위, 읽기 완료 여부, 접근하지 못한 부분을 기록한다. 대화 URL에만 의존하지 않는다. `curriculum.md`는 제공된 경우에만 만든다.

`mapping.md`에는 Source, Source language, Curriculum, Primary domain, Topics discovered, Existing canonical pages, New pages required, Potential duplicates, Cross-links, Open questions, Expected bilingual page pairs를 기록한다.

사용자가 기존 자료의 통합본을 다시 제공하면 최신 지정 파일과 이전 파일을 먼저 비교한다. 새 지식이 없고 기존 ID로 전부 대응할 수 있으면 같은 batch의 `complete-source-YYYY-MM-DD.md`처럼 별도 원문으로 보존하고 mapping에 새 파일·hash·기존 ID 대응을 기록한다. 이전 원문은 삭제하지 않으며 같은 지식을 새 ID로 중복 집계하지 않는다. `*source*.md`에 기록된 업로드 byte·hash·공백 복원 metadata는 모두 무결성 검사 대상이다.

## 원문 형태 대응

학습 본문을 임의 요약·병합하지 않는다. 원래 언어는 지정 구간을 그대로 두고 반대 언어는 동일 구조로 번역한다. `reviews/source-preservation.json`의 `spans`에 다음과 같이 등록한다.

```json
{
  "spans": [{
    "page": "data-platform/topic.md",
    "source": "sources/batch/source.md",
    "start": "# Chapter 6 — Topic",
    "end": "# Chapter 7 — Next topic",
    "verbatim_language": "ko"
  }]
}
```

기본 구간은 시작 제목 다음 줄부터 끝 제목 직전까지다. 시작 제목도 포함하려면 `include_start: true`, 파일 끝까지면 `end: null`을 쓴다. 양언어 페이지에 `<!-- SOURCE CORE START -->`와 `<!-- SOURCE CORE END -->`를 넣는다. 같은 페이지의 다른 원문 구역은 `marker`에 `SOURCE APPENDIX` 같은 별도 이름을 등록한다. `verbatim_language`는 `ko` 또는 `en`이다. 보완·정정·추가 그림·실무 예시는 경계 밖에 두고 원래 절 번호와 연결한다.

검사기의 원문 동일성·구조 signature 통과는 의미 동등성과 가독성의 증거가 아니다. 전문 대조 및 화면 확인을 별도로 수행한다.

## content-manifest.md

```yaml
---
items:
  - id: EXAMPLE-001
    knowledge: 보존해야 할 구체적인 지식
    kind: constraint
---
```

front matter 아래에 개념·예시·제약의 구체적인 내용과 원문 위치를 기록한다. kind는 concept, example, constraint, failure, misconception, question 등 의미를 드러내는 이름이다. 원문을 읽기 전에 빈 목록으로 완료를 주장하지 않는다.

## coverage-matrix.md

```yaml
---
items:
  - id: EXAMPLE-001
    state: Included
    destination: engineering/example/topic.md
    ko: Synced
    en: Synced
    reason: 양쪽 문서에 제약과 예시를 보존함
  - id: EXAMPLE-002
    state: Deferred
    destination: null
    ko: Pending
    en: Pending
    reason: 버전별 근거를 아직 확인하지 못함
---
```

모든 ID가 manifest에 있어야 하며 모든 manifest ID가 matrix에 있어야 한다. `Included`와 `Merged`는 존재하는 같은 상대 경로와 양쪽 `knowledge_ids`가 필요하다. `Deferred`와 `Excluded`는 구체적 이유가 필요하고 공개를 주장하면 안 된다. Merged는 여러 출처 ID를 하나의 정규 페이지에 통합할 때 사용한다.

## coverage-report.md

검사기의 `--write-reports`로 생성한다. 추적 완료 비율, 실제 공개 비율, 보류·제외 개수, 한영 반영 상태를 구분한다. 0건을 100% 지식 보존으로 표현하지 않는다.

## 실제 검토 기록

`reviews/bilingual.json`의 `pages`에서 상대 경로를 key로 사용한다. 각 값에 `ko_sha256`, `en_sha256`, `semantic`, `simple_english`, `privacy`, `reviewer`를 넣는다. 세 결과 필드는 실제 통과 시에만 `pass`다. 범위와 검토 근거를 `notes`에 남긴다. 해시는 해당 파일 bytes의 SHA-256이며 문서 변경 후 다시 검토한다.

## 문서 유형

Learn, Reference, How-to, Runbook, Decision, Architecture, Methodology 중 독자 목적에 맞게 선택한다. 각 템플릿의 후보 섹션은 `handbook-contract.md`에 있다. 빈 섹션은 만들지 않는다. LLM 시나리오에는 상황·제공 맥락·구체적인 prompt·기대 결과·오류 가능성·현실 검증을 모두 넣는다.
