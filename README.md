# Work Knowledge Handbook

## 이 프로젝트가 해결하는 문제

업무 지식을 분야와 역할이 바뀌어도 계속 확장하는 한영 핸드북이다. 학습 원문을 개념별 지식으로 통합하고 설계·운영·문제 해결에 다시 사용한다. 현재 학습 자료 1건을 반입했으며 데이터 플랫폼 기술·구조·커리큘럼 18쌍과 홈·지식 관리 방법·용어집을 합쳐 한영 21쌍이다. 자료의 Phase 1~15와 16.1은 개념 학습 범위이며, 미학습 후속 과정은 목차로 유지한다.

## 설계 원칙

- 커리큘럼은 구조, 원문은 보존할 지식을 제공한다. 자료 없이 기술 내용을 꾸며내지 않는다.
- 의미 있는 지식은 안정적인 ID와 반영표로 추적한다. 보류와 제외도 이유를 남긴다.
- 한국어와 쉬운 영어는 같은 지식을 담는다. 내용이 바뀌면 의미·영어·개인정보 검토 기록을 갱신한다.
- Git Markdown이 원본이다. HTML은 생성물이고 vault는 충돌 보호가 있는 사본이다.

## 시작하기

Python 3.12 이상과 Node.js 22 이상을 사용한다. 최초 검증은 Python 3.14, Node.js 26에서 수행했다. CI는 Python 3.12와 Node.js 22로 실행한다.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm ci --ignore-scripts
make validate
.venv/bin/mkdocs serve
```

기본 한국어는 사이트 루트, 영어는 `/en/`이다. 상단 언어 메뉴는 같은 주제로 이동한다. 자료를 넣을 때 Codex에 커리큘럼과 Markdown 경로를 제공하고 반입을 요청한다. 작업 전 [전체 운영 계약](handbook-contract.md)을 읽도록 되어 있다.

## 자료 반입

1. `sources/<batch>/source.md`에 민감 정보를 제거한 원문 전체를 보존한다. 커리큘럼이 있으면 `curriculum.md`도 둔다. 접근 불가 부분은 명시한다.
2. [입력 스키마](configs/source-model.md)에 맞춰 `content-manifest.md`, `mapping.md`, `coverage-matrix.md`를 만든다. 문서 작성 전에 모든 의미 있는 지식을 먼저 추출한다.
3. 기존 정규 주제에 유용한 지식의 합집합을 반영한다. 양쪽 언어, 메타데이터, glossary, nav, 링크와 예제를 함께 갱신한다.
4. 전체 쌍을 직접 읽어 의미·쉬운 영어·개인정보를 검토한다. `reviews/bilingual.json`에 실제 검토자, 결과, 현재 SHA-256을 기록한다. 해시만 갱신해서 검토를 대신하면 안 된다.
5. `.venv/bin/python scripts/check_handbook.py --write-reports`로 반영 보고서를 만든다. `make finalize`로 전체 검증과 vault 저장을 실행한다.
6. 검증된 지정 파일을 커밋하고 공개 원격에 push한다. 자료·커리큘럼·페이지 쌍·coverage·검증·미해결 사항을 간단히 보고한다.

## vault 설정

이 PC의 활성 Obsidian vault를 확인해 로컬 설정을 만든다. 경로는 `_workspace/vault.json`의 `vault`에, 하위 폴더는 `folder`에 넣는다. 설정은 Git에 들어가지 않는다.

```json
{"vault": "/absolute/path/to/vault", "folder": "work-handbook"}
```

```bash
make sync-vault
make finalize
```

README·운영 계약·출처·한영 문서·자체 스킬 등 first-party `.md`를 같은 경로로 복사한다. 개인 설정, private 자료, 의존성, 제삼자 문서, 생성 사이트와 symlink는 제외한다. vault를 수동 수정한 경우 자동 덮어쓰기 없이 실패한다. Git에 반영할 변경을 검토한 후 사본을 원래 동기화 상태로 복구하고 다시 실행한다. 삭제는 전파하지 않는다. Git 훅이나 상시 프로세스를 강제로 설치하지 않으며 완료 명령과 에이전트 계약이 복사를 보장한다.

## 주요 경로

| 경로 | 역할 |
|---|---|
| `docs/ko`, `docs/en` | 경로와 canonical ID가 같은 공개 문서 쌍 |
| `sources/` | 민감 정보를 제거한 원문과 지식 추적 자료. 사이트에는 미포함 |
| `sources-private/` | Git과 vault에서 제외되는 로컬 민감 자료 |
| `examples/`, `configs/`, `scripts/` | 실행 예제·설정·검증과 복사 도구 |
| `reviews/bilingual.json` | 문서 해시에 결속된 실제 검토 기록 |
| `handbook-contract.md`, `AGENTS.md` | 지식 관리·작업 계약 |
| `docs/README.md` | 비공개 운영 ADR·스펙·변경 이력 지도 |
| `_workspace/` | 개인 vault 경로와 복사 상태. Git 미추적 |
| `.agents/skills/` | 공통 하네스 스킬과 검증된 외부 스킬 |

## GitHub Pages와 안전 경계

사용자의 명시적 요청으로 소스 저장소를 public으로 전환했다. Pages source는 GitHub Actions이며 `PAGES_ENABLED=true`가 설정되어 있다. push와 PR은 테스트 및 사이트 검증을 실행하고 main push는 검증 성공 후 배포한다. 수동 workflow 실행도 지원한다. 사이트 주소는 https://nohdol97.github.io/work-handbook/ 이다. 실제 배포 성공은 workflow와 공개 HTTP 응답으로 확인한다.

저장소에 커밋한 소스·운영 문서와 이력도 GitHub에서 공개된다. 사이트에 제외된 파일이라도 저장소에서는 공개된다는 점을 구분한다. 원문은 공개 가능한 내용으로 정리한 경우에만 `sources/`에 커밋한다.

공개 산출물에는 `docs/ko`, `docs/en`만 포함한다. 내부 URL, 고객·회사 식별자, credentials, 개인정보, 독점 코드는 저장하지 않는다. 공부한 내용을 실제 업무 경험으로 표현하지 않는다.

## 검증과 문제 해결

`make validate`는 단위 테스트, 하네스 구조, 한영·출처·검토 증거, Mermaid 구문, strict 빌드와 HTML 링크·언어 전환·게시 범위를 검사한다. 의미 검토는 에이전트/사람이 수행하고 자동화는 해시가 최신인지 검사한다. 외부 링크 가용성, 실제 기술 주장, 예제 운영 적합성은 별도 증거가 필요하다.

검토 hash 오류는 실제 변경 내용을 다시 읽고 양쪽 언어의 scope를 확인한 뒤 해결한다. vault 오류는 로컬 설정, 접근 권한, 수동 편집 충돌을 확인한다. 원격 push는 branch SHA가 로컬 HEAD와 같은지 확인한다. 새로운 로컬 스킬의 자동 검색은 새 CLI 세션에서 가장 확실하다.
