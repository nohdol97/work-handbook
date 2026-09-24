# 자료 매핑

- **Source:** `data_platform_engineering_study_source-3.md` 업로드 전체. 공개 가능한 원문을 `source.md`에 보존했고, 행 끝 공백 제거 위치를 source.md 주석 ledger에 남기고 복원한 bytes를 업로드와 대조했다. 개인 upload 경로는 저장하지 않는다.
- **Source language:** 한국어와 표준 영어 기술 용어.
- **Curriculum:** 원문 Chapter 18에서 `curriculum.md`로 추출. Phase 1~15 및 16.1 완료, 16.2~16.11과 Phase 17~21 미학습.
- **Primary domain:** Data Platform Engineering.
- **Topics discovered:** 기초 저장 구조, 이벤트, Lakehouse/Iceberg, Spark/Flink, CDC, orchestration, dbt, 분석 모델, Trino, 품질, 관측, 계보, governance, AI-ready data, 온라인 평가, 전체 구조.
- **Existing canonical pages:** 홈·지식 관리 방법·용어집. 기존 기술 문서 중복 없음.
- **New pages required:** 아래 18개 한영 쌍. 원문 세션/날짜가 아니라 재사용 가능한 기술 주제로 구성.
- **Potential duplicates:** Chapter 17과 Final Mental Model의 반복 구조·역할은 architecture에 통합. dbt tests, SLO, catalog 등의 관점 차이는 각 주제에 유지하고 상호 링크.
- **Cross-links:** architecture와 curriculum에서 모든 기술 주제로 연결. 각 언어는 같은 언어 트리에 머물고 용어집이 정규 주제로 연결.
- **Open questions:** 원본 대화와 Chapter 1~4 복원 전 자료 없음; 구체적인 제품 버전·운영 환경·실행 결과 없음; Langfuse→Iceberg 연동과 Phase 17~21 구현 미학습. 공식 문서 대조는 개념의 조건을 보완하며 실제 실행 증거를 대신하지 않음.
- **Expected bilingual page pairs:** 새 18쌍, 기존 3쌍, 합계 21쌍.

## 추출 및 읽기 증거

원문 1~44행은 목적·목차, 45~2622행은 foundations 담당, 2623~4017행은 processing 담당, 4018~4996행은 governance 담당, 4997행 이후는 통합 담당이 전체 읽었다. 원문에 접근하지 못한 본문은 없다. 각 담당자는 문서 작성 전에 지식 ID와 목적지를 추출했다. 각 ID의 세부 범위와 행은 content-manifest.md에 기록한다.

원문 개인정보 검토에서 실제 고객·회사 식별자, credentials, 내부 URL, 개인정보를 발견하지 않았다. 제품명·generic 테이블 및 필드·가상의 숫자와 사례는 유지한다. 학습 내용과 실제 경험을 구분한다.

## 정규 문서 매핑

| 목적지 | 지식 구간 수 |
|---|---:|
| `data-platform/ai-ready-data.md` | 10 |
| `data-platform/analytical-modeling.md` | 8 |
| `data-platform/architecture.md` | 6 |
| `data-platform/cdc-debezium.md` | 9 |
| `data-platform/curriculum.md` | 8 |
| `data-platform/data-observability.md` | 7 |
| `data-platform/data-quality.md` | 7 |
| `data-platform/dbt.md` | 10 |
| `data-platform/event-architecture.md` | 6 |
| `data-platform/flink.md` | 14 |
| `data-platform/foundations.md` | 7 |
| `data-platform/governance.md` | 9 |
| `data-platform/lakehouse-iceberg.md` | 11 |
| `data-platform/lineage-metadata.md` | 8 |
| `data-platform/online-evaluation.md` | 1 |
| `data-platform/orchestration.md` | 8 |
| `data-platform/spark.md` | 14 |
| `data-platform/trino.md` | 8 |

## 검증 범위

기술별 공식 문서 근거와 보완은 각 정규 페이지에 기록한다. SQL·코드·서비스 연동은 실행하지 않았으며 `tested_with`를 만들지 않는다. 전체 한영 의미·쉬운 영어·개인정보 검토는 `reviews/bilingual.json`, 구조·사이트·mirror 결과는 완료 검증으로 확인한다.

## 원문 포맷 정규화

Git 공백 검사를 위해 원문 6개 행의 Markdown hard-break용 끝 공백 2개씩을 제거했다. `source.md` 머리말의 `whitespace_restoration`은 원문 기준 행 번호와 제거 문자열을 담는다. 경계 뒤 본문에서 해당 공백을 복원하면 업로드 88,486 bytes 및 기록한 SHA-256과 정확히 일치한다. 의미 있는 본문은 제거하지 않았다.
