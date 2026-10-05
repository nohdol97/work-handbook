# AI Model Fine-Tuning / QLoRA Basic 매핑

- 원문: `ai_model_qlora_training_basic.md`, 1,998행·30,285bytes, SHA-256 `82c1e31a3618723b29bd30e2ecbeef3e96d123dfcb301acbc35b8b554a5f9fb4`. 한국어 core 그대로 보존하고 영어는 같은 구조로 번역한다.
- 영역: 신규 `ai-model-development`의 1~10장과 소개·최종 요약. 기존 AI evaluation·AI-ready data·GPU·vLLM·AWS S3·개발자 플랫폼은 유지하고 관련 링크로 연결한다.
- 페이지: 장마다 정규 한영 1쌍, 소개·요약 목차 1쌍. 기존 67쌍 + 11쌍 = 78쌍. 번호 절 61개 + 소개 1개 + 요약 9개 = 71개 ID; 기존 574개 + 71개 = 645개.
- 추출·원문 읽기: root가 1~8행·1835~1998행, chapters12_13이 9~626행, chapter14가 627~1367행, chapter15가 1368~1834행을 전문 읽고 페이지 작성 전에 ID·매핑을 확정했다. 접근하지 못한 구간은 없다.
- 원문의 제목·번호·순서·표·코드·공백을 유지한다. 반복되는 원문 요약도 삭제하지 않는다. 원문의 코드·JSON·YAML·S3 경로는 실행하지 않는다.
- 사전 privacy 검토: 실제 자격증명·개인정보·계정·내부 URL 발견 없음. S3 bucket명, dataset-v12/v13, run/eval ID, abc123 등은 학습용 예시다.
- 주요 보완: 1.2 LoRA 행렬 차원 오류, adapter/base revision·tokenizer 호환, 4bit 저장과 연산 dtype, artifact 파일 조건, quantized merge 지원, golden 반복 선택 누수, 학습 전략 분류축, metadata와 bitwise 재현 차이. 모두 원문 밖에 공식 근거와 절 번호를 붙인다.
- 열린 범위: 실제 base model revision·GPU·라이브러리·학습 데이터·metric 결과·배포 환경이 없다. 원문은 실행·성능·재현성 보장의 증거가 아니다.

## 장별 정규 문서

| 장 | 문서 | 지식 ID |
|---|---|---|
| 1 | `ai-model-development/qlora-artifacts.md` | AIMFT-01-01~08 |
| 2 | `ai-model-development/adapter-compatibility.md` | AIMFT-02-01~04 |
| 3 | `ai-model-development/training-datasets.md` | AIMFT-03-01~07 |
| 4 | `ai-model-development/qlora-training.md` | AIMFT-04-01~14 |
| 5 | `ai-model-development/evaluation-promotion.md` | AIMFT-05-01~06 |
| 6 | `ai-model-development/model-retraining.md` | AIMFT-06-01~03 |
| 7 | `ai-model-development/artifact-lineage.md` | AIMFT-07-01~04 |
| 8 | `ai-model-development/model-developer.md` | AIMFT-08-01~08 |
| 9 | `ai-model-development/model-platform-collaboration.md` | AIMFT-09-01~03 |
| 10 | `ai-model-development/training-platform-architecture.md` | AIMFT-10-01~04 |

소개·최종 요약: `ai-model-development/index.md`, AIMFT-00-01~10.

## 전문 검토와 적용 조건

- Ch1~3: Codex /root/chapters12_13 작성·전문 읽기, Codex /root/chapter14 독립 검토.
- Ch4~7: Codex /root/chapter14 작성·전문 읽기, Codex /root/chapters12_13 독립 검토.
- Ch8~10: Codex /root/chapter15 작성·전문 읽기, Codex /root/chapter14 독립 검토.
- 소개·최종 요약: Codex /root 작성, Codex /root/chapter14 양언어 전체 독립 검토. 기존 67쌍에서 QLoRA 11쌍과 별도 실전 영어 5쌍을 더해 전체 83쌍이다.
- PEFT/QLoRA/TRL/Transformers/PyTorch·scikit-learn·vLLM·S3·MLflow의 공식 근거를 각 보완에 연결했다. 1.2의 LoRA 차원 오류, 5.2의 가상 수치가 5.4 gate를 통과하지 못하는 점, golden 재사용과 독립 평가, 메타데이터와 실제 재현의 차이를 명시했다.
- LLM 실습은 dataset 누수 검토·training 설정 검토·플랫폼 artifact 전달 검토 3개다. 작성한 작업 템플릿이며 실제 모델 호출·학습·AWS 자원 생성·성능 시험은 수행하지 않았다.
- 사용자 후속 요청에 따라 이 자료를 포함한 영어 본문 전체를 먼저 집계하고 중급 한영 어휘·숙어/관용 표현/연어·구동사·업무/면접 문장 학습을 추가했다. 원문 source core는 변경하지 않는다.

## 공통 하네스 피드백

기존 원문 목록 렌더링 보정과 원문·번역·privacy·vault 검증을 재사용했다. 실전 영어의 반복 반영은 사용자가 명시적으로 요청한 지속 작업으로 스펙 008·ADR 008·반입 skill과 최신성 검사에 기록한다. 원문 보존과 별도 편집 학습 자료의 책임을 구분한다.

## 화면 검토

QLoRA의 목차·artifact·학습·평가·플랫폼과 영어 학습의 다섯 페이지를 한영·1280px/390px 총40조합에서 확인했다. 본문 가로 넘침·JavaScript 오류가 없고, 실습 탭과 같은 주제 언어 전환이 정상이다. 영어114항목의 HTML 순서도 실제 집계 순서와 일치한다. 모바일 첫 화면에서 표현·예문이 먼저 보이도록 상세 집계 기준을 영어 학습 안내에 모았다. 이 마지막 편집 이후 영어 화면 20조합을 다시 확인했고 정렬·가로 넘침·언어 전환에 문제가 없었다. 임시 headless Chrome을 사용했으며 사용자 로그인 profile에는 접근하지 않았다.
