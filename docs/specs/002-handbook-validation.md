# 스펙 002: 핸드북 검증

- 상태: active
- 날짜: 2026-09-24
- 관련 ADR: 001-handbook-architecture.md

## 문제와 목표

파일 쌍이 존재하는 것만으로 지식 보존이나 번역 동등성이 보장되지 않는다. 공개 문서 구조, 원본 추적, 검토 증거를 자동 검사하고 검증 한계를 명시한다.

## 비목표

자동 번역, 의미의 자동 판정, 외부 링크의 가용성 검사, 원본 공개, Mermaid 문법 분석은 이 검사기의 역할이 아니다.

## 요구사항

### R1. 언어 쌍과 메타데이터

`docs/ko`와 `docs/en`의 Markdown 상대 경로가 정확히 같아야 한다. 각 페이지에는 영문 소문자/숫자/하이픈 canonical ID, 허용된 status, 유효한 날짜 메타데이터가 필요하다. ID는 언어 쌍에서 같고 다른 쌍과 중복되지 않는다. `knowledge_ids` 목록은 언어 쌍에서 같아야 한다. 빈 제목은 거부한다.

### R2. 링크와 탐색

로컬 링크는 저장소 밖을 가리키면 안 된다. 페이지 링크는 같은 언어 트리 안의 실제 파일과 유효한 제목 앵커로 연결되어야 한다. 예제 파일은 저장소 내부를 허용한다. MkDocs의 언어 상대 nav가 모든 공개 페이지를 포함하고 존재하는 페이지를 가리켜야 한다.

### R3. 지식 보존

각 sources 하위 묶음에는 source, manifest, matrix, report, mapping Markdown이 필요하다. curriculum은 선택이다. Manifest의 `items`는 id/knowledge/kind를 가진다. Matrix의 `items`는 id/state/destination/reason/ko/en을 가진다. ID는 전체 원본에서 고유하며 manifest와 matrix 항목 집합이 일치해야 한다. Included/Merged는 존재하는 양언어 페이지와 해당 페이지의 knowledge_ids, 양언어 Synced 상태가 필요하다. Deferred/Excluded는 구체적 사유가 필요하며 공개 완료로 표시할 수 없다.

### R4. 보고서

`--write-reports`는 추적된 항목 수와 실제 공개된 항목 수를 구분해 coverage-report를 생성한다. 원본이 비어 있으면 백분율을 N/A로 표시한다. 기본 audit은 읽기 전용이며 보고서가 현재 manifest와 matrix로 생성한 정확한 내용과 다르면 실패한다. Bilingual synchronization은 양언어 Synced 항목 수를 공개 항목 수로 나눈 값이며 공개 항목이 없으면 N/A이다. 이 수치는 실제 의미 동등성을 자동 판정하지 않는다.

### R5. 검토 증거

`reviews/bilingual.json`의 pages는 언어 상대 경로로 구성된다. 각 항목은 최신 ko_sha256/en_sha256과 semantic/simple_english/privacy의 pass, 비어 있지 않은 reviewer를 요구한다. 파일 변경 시 재검토해야 한다. 해시는 검토 이후 변경 여부만 확인한다. 실제 의미 동등성, 쉬운 영어, 개인정보는 사람 또는 에이전트가 원문을 읽고 검토해야 한다.

### R6. 실행 계약

`audit(root)`는 오류 문자열 목록을 반환한다. CLI의 기본 root는 스크립트가 속한 저장소이며 `--root`를 지원한다. 오류가 있으면 종료 코드 1을 반환한다. 손상된 YAML/JSON과 비정상 자료형은 성공으로 처리하지 않는다.

### R7. 기록된 원문 복원 무결성

원문 정규화 기록의 `ORIGINAL SOURCE START`, `원본 bytes`, `whitespace_restoration` 중 하나가 있으면 정확히 하나씩의 경계·byte 수/SHA-256 기록·JSON ledger를 요구한다. 본문의 지정 행 끝에 ledger의 공백을 복원한 UTF-8 bytes가 기록된 크기와 hash 모두에 맞아야 한다. 행 번호는 중복 없는 유효한 정수이며 복원 문자열은 비어 있지 않은 space/tab만 허용한다. 오류는 읽기 전용 audit에서 실패하며 본문·ledger를 자동 수정하지 않는다. 이 메타데이터가 없는 기존 일반 source 파일은 기존 추적 규칙을 유지한다. 이는 기록된 업로드와의 byte 동일성만 검사하며 개인정보·의미 검토를 대신하지 않는다.

인수 기준은 한글·CRLF·끝 공백 복원 통과, 같은 길이 본문 변조 검출, 손상·중복·범위 밖 ledger 거부, 불완전 기록 거부, 기존 일반 source fixture 통과다.

## 완료 기준

`python -m unittest discover -s tests -p test_handbook.py -v`로 올바른 최소 저장소 통과와 각 규칙 위반의 실패를 확인한다. MkDocs 빌드, Mermaid, 브라우저 언어 전환 검증은 별도 통합 검증이다.

## 미검증 범위

임의 문장의 사실 여부나 의미 동등성은 이 검사기가 증명하지 않는다. 검토 기록은 검토자의 판단을 보존하며 자동 내용 검토를 대체하지 않는다.
