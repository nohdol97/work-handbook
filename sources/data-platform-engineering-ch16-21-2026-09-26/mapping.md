# 후속 자료 매핑

- **Source:** 사용자 업로드 `data_platform_engineering_source_ch16_21_final.md` 전체 5,480행, 72,467 bytes. `source.md`와 공백 복원 ledger로 원문을 보존한다.
- **Source language:** 영어. 한국어 정규 문서와 쉬운 영어 정규 문서를 함께 작성한다.
- **Curriculum:** Phase 16~21 완료 내용. Phase 1~21의 완료는 개념 중심 학습이며 구현·운영·장애 실험 완료를 뜻하지 않는다. Snowflake Chapter 18은 condensed 범위다.
- **Primary domain:** Data Platform Engineering / AI evaluation / managed platforms / production operations / architecture.
- **Topics discovered:** 평가 데이터셋·사람 feedback·judge·버전·experiment·비용/품질/지연, Databricks, Snowflake, 플랫폼 비교, 복구·backfill·SLO·capacity·비용, 전체 구조와 구성 요소 축소.
- **Existing canonical pages:** `online-evaluation.md`의 16.1과 `architecture.md`의 역할·데이터 경로에 중복 개념을 통합한다. `curriculum.md`는 이전 진행 상태를 새 자료로 갱신한다. 기존 DPE ID 151개와 의미는 보존한다.
- **New pages required:** `ai-evaluation.md`, `databricks.md`, `snowflake.md`, `platform-comparison.md`, `production-operations.md`의 한영 5쌍. 세션 번호를 페이지 경로로 사용하지 않는다.
- **Potential duplicates:** 16.1과 기존 온라인 평가, Chapter21 및 최종 mental model의 기존 아키텍처 역할은 의미의 합집합으로 병합한다. 제품 설명·장애 절차는 정규 주제를 링크하고 architecture에는 역할·선택·실패 경계를 남긴다.
- **Cross-links:** 같은 언어 내 전체 구조·curriculum·새 5개 주제·기존 관련 주제·용어집을 연결한다.
- **Open questions:** 실제 제품 버전·cloud/region/edition·workload·성능·요금·원문 대화는 제공되지 않았다. 최신 공식 문서는 적용 조건을 보완하는 근거이며 실서비스 실행 증거가 아니다.
- **Expected bilingual page pairs:** 기존 39쌍 + 새 5쌍 = 44쌍. 이번 자료의 115개 ID와 기존 151개를 별도 batch로 추적한다.

## 읽기와 추출 책임

평가 담당은 Chapter16 전체(50~1268행), 제품 담당은 Chapter17~19 전체(1269~3341행)와 마지막 공식 근거 메모, 운영 담당은 Chapter20 전체(3342~4130행)를 읽었다. 통합 담당은 도입·완료 현황(1~49행), Chapter21부터 끝까지(4131~5480행)를 읽었다. 전체 파일을 팀이 분담해 읽었으며 접근하지 못한 본문은 없다. 각 담당자는 페이지 작성 전에 지식 ID·원문 행·세부 범위·목적지를 추출했다.

## 공개 및 보존 경계

입력은 공개 제품명, 가상 모델/버전/필드/수치와 개념 예시다. 영역별 전체 읽기와 민감값 패턴 검사를 완료했으며 게시를 막는 실제 민감정보를 발견하지 않았다. 실제 환경 식별자·credentials·개인정보를 게시하지 않는다. 원문 3348행 끝의 Markdown 공백 2개만 ledger에 기록하여 제거했다. 이를 복원하면 업로드 byte/hash와 일치한다. 이전 source batch는 당시 학습 이력으로 보존하고 현재 상태는 정규 curriculum에서 갱신한다.

## 정규 목적지

| 정규 문서 | 신규 자료 ID 수 |
|---|---:|
| `data-platform/ai-evaluation.md` | 11 |
| `data-platform/architecture.md` | 37 |
| `data-platform/curriculum.md` | 4 |
| `data-platform/databricks.md` | 12 |
| `data-platform/online-evaluation.md` | 1 |
| `data-platform/platform-comparison.md` | 15 |
| `data-platform/production-operations.md` | 22 |
| `data-platform/snowflake.md` | 13 |
