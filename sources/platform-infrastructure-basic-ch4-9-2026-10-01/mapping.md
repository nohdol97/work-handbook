# 플랫폼·인프라·AI 서빙 4~9장 매핑

- 원문: `platform_infra_ai_serving_basic_ch4_ch9.md`, 전체 3,865행·49,215 bytes. `source.md` 경계 뒤에 byte 그대로 저장한다.
- 원래 언어: 한국어와 표준 영어 기술 용어. 한국어 core는 그대로, 영어는 같은 구조의 완전 번역이다.
- 영역: Redis/PostgreSQL/Kafka 운영, vLLM/LiteLLM AI 서빙, GPU 메모리·스케줄링·장애 조사.
- 이전 자료: 1~3장은 그대로 유지한다. 이전 진도 ID PIS-00-01/PIS-04-01은 당시 범위라는 설명을 유지하고 현재 진도는 새 자료로 갱신한다.
- 정규 목적지: `platform-infrastructure/redis.md`, `postgresql.md`, `kafka.md`, `vllm.md`, `litellm.md`, `gpu-infrastructure.md` 한영6쌍. 기존 index에서 소개·연결 구조·후속 진도를 다룬다.
- 중복과 링크: 데이터 플랫폼의 Kafka/CDC/운영 문서는 데이터 처리 관점으로 유지한다. 이번 운영·서빙 본문은 원문 순서로 보존하고 같은 언어의 기존 주제와 연결한다. KV Cache와 GPU 메모리의 반복 설명도 원문에서 제거하지 않는다.
- 상태: 1~9장은 Basic 개념 학습, 10~15장은 not-started. 학습용 설정·수치·명령을 실제 실행 결과로 표현하지 않는다.
- 민감도·검토: 장별 전체 읽기·개인정보·한영 대응 검토를 수행한다. GPU/모델명·용량·계산은 source 주장과 공식 확인 조건을 구분한다. 확인할 수 없는 모델 세부사항은 미확인으로 명시한다.
- 예상 문서: 기존47쌍 + 신규6쌍 = 53쌍. 기존304개 지식 ID를 유지한다.

## 읽기 분담과 경계

통합 담당은 서두1~10행 및 연결·진도3797~3865행, 데이터 서비스 담당은4~5장11~1333행, gateway/event 담당은6장1334~1740행 및8장2640~3116행, serving/GPU 담당은7장1741~2639행 및9장3117~3796행을 담당한다. 최신 업로드의 모든 줄을 분담하며 각 담당은 페이지 작성 전에 상세 개념·예시·숫자·조건을 추출한다.

## 실제 읽기·개인정보 검토 결과

네 담당이 배정된 전체 구간을 읽었고 접근하지 못한 줄은 없다. Alice/user1001/sessionabc123/payment-123 및 `<API_KEY>`는 설명용 값·placeholder이며 실제 credential·내부 URL·직접 식별정보를 발견하지 않았다. GPU 두 서버·세 replica·30명 등은 원문에서 제시한 질문과 수치이며 실제 환경 확인이나 측정 결과로 확대하지 않는다. 첫 파일과 달리 끝 공백도 정규화하지 않아 모든 업로드 byte를 그대로 복원한다.

## 주요 정정·적용 조건

- Redis lock/dedup의 원자성과 실패창, AOF/fsync 및 Sentinel/Cluster의 조건을 본문 밖에 구분한다.
- PostgreSQL WAL·pool mode·VACUUM·EXPLAIN ANALYZE의 실행 효과, sync commit·PITR·work_mem 조건을 구분한다.
- Kafka acks=all/current ISR·minISR·ELR·Strimzi 자원, LiteLLM 외부 provider 경로·budget/shared state/cache 조건을 보완한다.
- GLM 모델별 parameter/checkpoint 차이, FP4 이론 용량과 실제 artifact, 1M의 단위와 KV overhead를 분리한다. 16GPU 중4GPU spare는8GPU node 장애 시12GPU serving 전체복구를 보장하지 않는다. GPU utilization 한 지표로 병목을 확정하지 않는다.

명령·부하시험·failover·복구·GPU 모델 실행은 수행하지 않았다. 기존304개 ID와 신규58개 ID의 출처 추적을 유지하고 개념 학습과 실행 검증을 구분한다.
