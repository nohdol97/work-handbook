# 공통 스킬 카탈로그

각 섹션은 실제 공유 스킬 하나와 정확히 연결된다. 세부 판단은 링크된 영어 원본을 따른다.

## preserve-study-source

- 원본: [preserve-study-source/SKILL.md](preserve-study-source/SKILL.md)
- 역할·트리거: 제공된 학습 Markdown의 반입·복원·한영 번역, 번호 누락·절 병합·원문 재작성 문제 수정.
- 보존 기준: 최신 지정 원문을 원래 언어로 그대로 유지하고 반대 언어는 같은 구조로 번역한다. 보완·정정·그림·실무 예시는 원문 밖에 구분한다.
- 완료 기준: 원문 구간 동일성 검사, 양언어 전문 검토, 영어 빈도 후보 확인·학습 어휘/표현 갱신·예문 검토, 화면·빌드·vault 검증. ID coverage를 원문 형태나 가독성의 증거로 대신하지 않는다.
- 사용하지 않을 때: 새로운 글 작성이나 사용자가 명시적으로 요청한 별도 요약문.

## adr

- 원본: [adr/SKILL.md](adr/SKILL.md)
- 역할·트리거: Record, supersede, and review durable architecture decisions with context, alternatives, consequences, and document-map synchronization. Use when work changes architecture, ownership, data flow, security boundaries, deployment, repository layout, or a long-lived workflow rule. Do not use for routine implementation details or unsettled proposals. Re-run: ADR, architecture decision, 구조 결정, 결정 기록.
- 사용하지 않을 때: 원본 description의 경계와 루트 라우팅을 따른다.
- 완료 기준: 원본 절차의 검증과 루트 4필드 증거를 모두 충족한다.

## metaskill

- 원본: [metaskill/SKILL.md](metaskill/SKILL.md)
- 역할·트리거: Create, bootstrap, audit, improve, consolidate, or retire personal development harnesses and their independent project repositories; select and pin external skills; maintain README, ADR, SDD, TDD, validation, automatic improvement, and verified push contracts. Use for 새 하네스, 하네스 만들어, 하네스 개선, project scaffold or carry-in, external skill selection, and reusable harness feedback discovered during work. Not for ordinary product implementation after routing is established. Re-run: metaskill, harness, scaffold, evolve, 하네스, 프로젝트 반입.
- 사용하지 않을 때: 원본 description의 경계와 루트 라우팅을 따른다.
- 완료 기준: 원본 절차의 검증과 루트 4필드 증거를 모두 충족한다.

## spec-driven-development

- 원본: [spec-driven-development/SKILL.md](spec-driven-development/SKILL.md)
- 역할·트리거: Define or revise an executable behavior contract before implementing a feature, bug fix, refactor, gate, hook, or workflow change. Use when behavior or authority changes and reviewers need stable numbered requirements and acceptance criteria. Do not use for wording-only or behavior-invariant metadata edits. Re-run: SDD, spec first, write a spec, 스펙부터, 요구사항 정리.
- 사용하지 않을 때: 원본 description의 경계와 루트 라우팅을 따른다.
- 완료 기준: 원본 절차의 검증과 루트 4필드 증거를 모두 충족한다.

## test-driven-development

- 원본: [test-driven-development/SKILL.md](test-driven-development/SKILL.md)
- 역할·트리거: Implement features, fixes, refactors, gates, hooks, and scripts through a practical red-green-refactor loop tied to an accepted specification. Use before production behavior changes. Allows documented structural verification only for generated files, documentation-only work, or cases where deterministic tests are genuinely impractical. Re-run: TDD, test first, failing test, red green refactor, 테스트부터.
- 사용하지 않을 때: 원본 description의 경계와 루트 라우팅을 따른다.
- 완료 기준: 원본 절차의 검증과 루트 4필드 증거를 모두 충족한다.

## verification-before-completion

- 원본: [verification-before-completion/SKILL.md](verification-before-completion/SKILL.md)
- 역할·트리거: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
- 사용하지 않을 때: 원본 description의 경계와 루트 라우팅을 따른다.
- 완료 기준: 원본 절차의 검증과 루트 4필드 증거를 모두 충족한다.
