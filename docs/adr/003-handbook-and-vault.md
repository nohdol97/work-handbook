# ADR 003: 한영 지식 저장소와 vault 사본

- 상태: accepted (저장소 공개 범위는 ADR 004로 대체)
- 날짜: 2026-09-24

## 맥락

한 분야에 고정되지 않는 장기 업무 지식과 모든 Markdown의 vault 저장이 필요하다. 대화별 요약은 지식 중복과 누락을 만들고 번역 파일 존재만으로 의미 보존을 증명할 수 없다.

## 결정

이 독립 저장소 자체를 핸드북과 유지관리 하네스로 사용한다. 공개 문서는 docs/ko와 docs/en의 경로·ID 쌍이다. sources는 출처 보존 계층이며 빌드에서 제외한다. 운영 계약·ADR·스펙도 공개 빌드에서 제외한다. Markdown은 원본이고 MkDocs Material과 static-i18n이 사이트를 만든다. 기본 언어인 한국어는 사이트 루트, 영어는 /en/이며 언어 전환은 같은 주제를 유지한다.

각 출처 ID의 처리 상태와 실제 공개 비율을 분리한다. 의미·영어·개인정보 검토는 실제 검토 후 문서 해시와 묶어 남긴다. 자동 검사는 의미 자체를 판정하지 않는다.

vault는 명시적으로 요청된 단방향 Markdown 사본이다. 경로를 보존하며 충돌 시 중단하고 삭제하지 않는다. 경로와 동기화 상태는 로컬에만 둔다. private 소스 저장소를 만들고 공개 Pages 활성화는 직전 확인 후 진행한다.

## 대안과 결과

수동 HTML은 이중 유지보수가 필요해 제외했다. 단일 언어와 단순 직역은 요구를 충족하지 못한다. 양방향 vault 동기화는 충돌과 원본 권한을 복잡하게 만들어 제외했다. 직접 /ko/ 배포 경로를 만드는 사용자 정의 플러그인 대신 기본 i18n 라우팅을 사용한다.

핸드북과 하네스 제어 문서가 docs에 함께 있으므로 빌드 산출물에 제어 파일이 없는지 검사한다. vault가 오프라인이거나 수동 수정 충돌이 있으면 로컬 완료를 실패로 보고한다.

## 검증

한영 구조·출처 감사, 해시 기반 검토 만료, strict 빌드, 같은 주제 언어 링크 검사, 실제 vault 해시 대조, 원격 HEAD 비교로 확인한다.

## 공식 구성 근거

- [static-i18n 언어 구성](https://ultrabug.github.io/mkdocs-static-i18n/setup/setting-up-languages/)
- [같은 페이지 언어 전환](https://ultrabug.github.io/mkdocs-static-i18n/setup/setting-up-material/)
- [Material Mermaid](https://squidfunk.github.io/mkdocs-material/reference/diagrams/)
- [GitHub Pages workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

## 후속 결정

[ADR 004](004-public-repository-and-pages.md)가 private 소스 저장소 전제를 대체한다. 지식 구조·vault 사본·사이트 게시 범위 결정은 유지한다.
