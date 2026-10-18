# 공통 스킬 카탈로그

각 섹션은 실제 공유 스킬 하나와 정확히 연결된다. 세부 판단은 링크된 영어 원본을 따른다.

## handbook-interactive-slides

- 원본: [handbook-interactive-slides/SKILL.md](handbook-interactive-slides/SKILL.md)
- 역할·트리거: 공개 한영 Handbook 문서에서 원문 추적 인터랙티브 HTML 슬라이드를 생성·갱신하고 공통 렌더러·검토된 설명 설계를 확장한다. 정적 원문이 기본값이며 퀴즈·채점·암기 카드는 제외한다.
- 경계: MkDocs 탐색의 공개 문서만 대상으로 삼고 원본 Markdown과 vault 사본은 수정하지 않는다. 원문에 없는 계산·수치·실제 운영 결과를 만들지 않으며 단순화 모델의 한계를 화면에 표시한다.
- 읽기 방식: 기본 학습 모드는 같은 절의 정의·관계·예제·한계를 이어 읽는 페이지로 제공하고 문서 세로 스크롤을 허용한다. 발표 모드는 한 화면에 맞춰 의미 단위로 분할한다. 두 모드 모두 가로 넘침·내부 스크롤·잘림·읽기 어려운 축소를 금지하며 모드·언어 전환의 읽던 위치를 유지한다.
- 완료 기준: 전체 변환 보고서의 실패·미대응 구역 0, 모든 학습 절의 본문 보존·배치 감사, 한영·원문 왕복 링크·오프라인 브라우저 조작·전체 사이트 및 vault 검증. 자동 줄 단위 커버리지나 접근성 트리는 의미 검토·실제 화면 읽기 프로그램·사용자 이해도 검증을 대신하지 않는다.

## preserve-study-source

- 원본: [preserve-study-source/SKILL.md](preserve-study-source/SKILL.md)
- 역할·트리거: 제공된 학습 Markdown의 반입·복원·한영 번역·명시적으로 요청된 본문 개정, 번호 누락·절 병합 수정.
- 보존 기준: 최신 지정 원문의 목차·순서·핵심 지식을 유지한다. 스킬로 문서를 작성·개정하면 선택된 등록 구역에 사용자 상시 지시와 작업 범위의 증거·`editable` 모드를 기록하고 원본 자료를 남긴 채 공개 본문의 문장을 직접 고친다. 선택하지 않은 구역은 기존 byte 보존을 유지한다. 사용자가 원문 그대로를 명시하면 해당 구역은 예외로 보존한다.
- 새로 쓰거나 개정하는 설명은 개념·작동 원리·왜/언제 쓰는지·실무 문제·결과 판단을 자연스럽게 연결한다. 핵심 개념에는 일상 비유를 적극적으로 쓰고 실제 기술 의미·한계를 바로 연결한다. 필요한 보완과 정정은 대응 원문 절에 녹이고 별도 보완 절은 기본으로 만들지 않는다. 원래 제목·번호·예제 형태는 유지하고 새 설명·도식·목록은 필요한 곳에 추가할 수 있다. AI 예시는 조사·개발·설계·디버깅·검증에서 실제로 도움을 줄 때만 둔다. 짧은 상황·복사 가능한 자연스러운 요청·핵심 사항을 우선하며 맥락/요청/출력/검증 표지나 획일적 구조를 강제하지 않는다. 목표·필요한 맥락·중요 제약을 남기고 운영 안전·데이터 보호·필수 승인은 보존한다. [스펙 005](../../docs/specs/005-practical-prompts.md)·[009](../../docs/specs/009-beginner-friendly-writing.md)·[010](../../docs/specs/010-requested-source-rewrite.md)·[011](../../docs/specs/011-integrated-study-pages.md)과 [ADR 011](../../docs/adr/011-accessible-writing-and-source-boundaries.md)·[012](../../docs/adr/012-scoped-source-rewrite.md)·[013](../../docs/adr/013-integrated-study-explanations.md)를 따른다.
- 명시적 예외: 사용자가 원문 사이 추가를 요청하면 요청 증거·marker·한영 hash를 span의 `inline_additions`에 등록한다. 검증된 추가 블록만 비교에서 제외하며 원문 자체의 보존과 전문 검토는 유지한다. 미등록·누락·중복·중첩·변조 블록은 실패한다. [ADR 009](../../docs/adr/009-explicit-inline-additions.md)을 따른다.
- 완료 기준: 모드별 등록·구조 검사, 원본과 양언어 전문 대조, 영어 빈도 후보 확인·학습 어휘/표현 갱신·예문 검토, 화면·빌드·vault 검증. ID coverage를 의미 보존이나 가독성의 증거로 대신하지 않는다.
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
