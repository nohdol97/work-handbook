# 자료 추적 스키마

자료별로 `sources/<batch>/`에 다음 파일을 만든다. 아래는 예시 스키마이며 실제 반입 자료가 아니다. 지식 ID는 원문 batch가 달라도 충돌하지 않게 유지한다. 공개 페이지 front matter의 `knowledge_ids`에는 반영된 ID를 넣는다.

## 원문과 매핑

`source.md`에는 민감 정보를 제거한 원문과 원문 범위, 읽기 완료 여부, 접근하지 못한 부분을 기록한다. 대화 URL에만 의존하지 않는다. `curriculum.md`는 제공된 경우에만 만든다.

`mapping.md`에는 Source, Source language, Curriculum, Primary domain, Topics discovered, Existing canonical pages, New pages required, Potential duplicates, Cross-links, Open questions, Expected bilingual page pairs를 기록한다.

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
