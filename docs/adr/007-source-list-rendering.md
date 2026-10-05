# ADR 007: 원문 byte를 유지하는 목록 렌더링 보정

- 상태: accepted
- 날짜: 2026-10-05
- 관련 결정: [ADR 006](006-source-preserving-study-pages.md)

## 맥락

AWS 7장의 `대표 용도:` 바로 다음 bullet과 소개의 blockquote 목록, 완료 상태의 목록은 원문에 구분 빈 줄이 없다. 원문을 그대로 보존해도 Python Markdown은 이 형식을 일부 문단 안의 문자로 표시해 화면에서 목록이 합쳐진다. 원문 보존 검사만으로 HTML 가독성을 증명할 수 없다는 실제 사례다.

## 결정

Git·source·vault의 Markdown byte는 그대로 유지한다. MkDocs `on_page_markdown` hook에서 등록된 원문 페이지와 START/END marker 구간만 대상으로 일반 문장 뒤의 최상위 bullet·숫자/마침표 목록과 blockquote 목록 앞에 표시용 구분 행을 추가한다. 이 문자열만 Markdown 변환기에 전달하며 파일에 저장하지 않는다.

Fenced code와 그 안의 가짜 marker를 건너뛰고, 기존 정상 목록·nested/indented 내용·원문 밖·미등록 구역은 바꾸지 않는다. 기존 원문·양언어 의미·구조 검사, 사이트/화면 검증과 vault byte 검증의 책임은 유지한다. 새 권한·배포 대상·저장 형식은 추가하지 않는다.

## 대안과 결과

- 원문에 빈 줄을 삽입: 원래 언어 byte 보존 계약을 깨므로 제외한다.
- 모든 페이지에 전역 Markdown 문법 확장 적용: 원문 밖 기존 페이지까지 해석이 달라져 이번 문제보다 범위가 넓다.
- HTML/CSS로 literal hyphen을 목록처럼 꾸미기: 의미 있는 `ul/ol/li` 구조와 접근성을 복구하지 못한다.

원문 파일과 렌더링 중간 문자열이 달라지는 대신, 한정된 입력 형태를 실제 목록으로 읽을 수 있다. 이 hook은 CommonMark 전체를 구현하지 않는다. 숫자 목록은 현재 변환기가 지원하는 마침표 형식이며, 새로운 문법 사례가 나타나면 별도 재현·검토가 필요하다.

## 검증

[스펙 006 R7–R8](../specs/006-source-preservation.md)의 실제 hook·사이트 Markdown 변환 회귀에서 기존 화면 증상을 먼저 실패시킨 뒤 확인한다. 원본 byte·미등록/원문 밖 구역·fence·nested/indented 내용·정상 목록·한영 적용·멱등성을 검사한다. 독립 검토에서 발견한 tight list의 lazy continuation, indented/inline backtick 오인도 실제 변환 회귀로 보호한다. 전체 strict 빌드와 한영 desktop/mobile 화면은 통합 단계에서 확인한다.

## 공식 근거

- [MkDocs hooks](https://www.mkdocs.org/user-guide/configuration/#hooks)
- [MkDocs on_page_markdown](https://www.mkdocs.org/dev-guide/plugins/#on_page_markdown)
