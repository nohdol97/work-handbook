---
items:
- id: PIS2-00-01
  knowledge: Chapter4~9 Basic 핵심 개념·중간 실무 질문 및 이전1~3장과의 학습 경계
  kind: scope
  source_lines: 1–10
  destination: platform-infrastructure/index.md
- id: PIS2-04-01
  knowledge: RAM 기반 key-value 접근, String/Hash/List/Set/Sorted Set 차이, session TTL 30분과 만료, 영구 계정·상품은 PostgreSQL/세션·캐시는
    Redis 역할 예시. RAM 비용·용량 제한.
  kind: 개념·운영·예시·조건
  source_lines: 13–109
  destination: platform-infrastructure/redis.md
- id: PIS2-04-02
  knowledge: Cache hit/miss 흐름, 3 Pod 공유 세션과 요청별 Pod 변경, 분당 100회 counter, 분산 lock과 payment-123 중복 방지 개념, 트래픽보다 반복
    읽기·병목 우선. 수십~수백/수백~수천/수천~수만+ req/s는 절대 기준 아님. 5,000 req/s·95% hit에서 DB 약250 req/s. invalidation·TTL·장애·메모리·hot
    key·불일치 비용, Index/Query/Pool 선행.
  kind: 개념·운영·예시·조건
  source_lines: 110–308
  destination: platform-infrastructure/redis.md
- id: PIS2-04-03
  knowledge: RDB 10:00 snapshot dump.rdb의 작은 파일·빠른 복구·백업과 마지막 이후 손실, AOF SET/INCR/DEL 재생과 파일·Disk I/O 부담. 캐시 유실
    시 PostgreSQL 재조회·재생성 가능성으로 내구성 판단.
  kind: 개념·운영·예시·조건
  source_lines: 309–381
  destination: platform-infrastructure/redis.md
- id: PIS2-04-04
  knowledge: Primary에서 Replica A/B로 복제, Write Primary/Read Primary 또는 Replica, 장애 대비와 읽기 부하 분산. 비동기 응답·복제 흐름, Primary101/Replica100
    lag 예시, replication과 automatic failover 구분.
  kind: 개념·운영·예시·조건
  source_lines: 382–436
  destination: platform-infrastructure/redis.md
- id: PIS2-04-05
  knowledge: Sentinel monitoring/failover/primary 정보 제공, Primary 장애 후 Replica A 승격, Sentinel 1/2/3 공동 장애 판단, 애플리케이션의
    Sentinel 조회와 새 primary 재연결. Sentinel HA와 Cluster sharding+HA 차이.
  kind: 개념·운영·예시·조건
  source_lines: 437–494
  destination: platform-infrastructure/redis.md
- id: PIS2-04-06
  knowledge: Cluster sharding+replication+failover, Key/hash/slot/node 매핑, node 추가 제거 시 slot resharding, Primary
    A/B/C와 Replica A/B/C. 단일 node 메모리·처리량 초과와 수평 확장 조건.
  kind: 개념·운영·예시·조건
  source_lines: 495–556
  destination: platform-infrastructure/redis.md
- id: PIS2-04-07
  knowledge: Hot key는 Cluster에서도 특정 node에 집중, big key는 CPU/network/latency 부담, eviction·fragmentation 구분, SET A/B/C
    pipelining으로 round trip 감소. 느림 진단의 hot/big key·메모리·network 질문.
  kind: 개념·운영·예시·조건
  source_lines: 557–626
  destination: platform-infrastructure/redis.md
- id: PIS2-04-08
  knowledge: Redis StatefulSet redis-0/1/2 stable identity, Pod/PVC/PV/disk 경로. Kubernetes Pod 재생성과 Sentinel/Cluster
    primary 판단·failover 구분. Persistence와 외부 백업 차이, Operator의 cluster/failover/scaling 자동화.
  kind: 개념·운영·예시·조건
  source_lines: 627–690
  destination: platform-infrastructure/redis.md
- id: PIS2-05-01
  knowledge: PostgreSQL relational architecture Client/DB/Memory+WAL+Disk. Connection별 process 증가가 memory/context
    switching 부담으로 연결. Shared buffers 캐시, WAL 기록 후 디스크 반영 개념과 recovery/replication/PITR 용도.
  kind: 개념·운영·예시·조건
  source_lines: 693–755
  destination: platform-infrastructure/postgresql.md
- id: PIS2-05-02
  knowledge: 100 Pods×20=2,000 connections와 max_connections 상한, 요청별 생성 대신 pool 재사용. Pod 동시 요청과 pool10 병렬 작업, 50
    Pods×20=최대1,000. PgBouncer 예시 application1,000→DB100은 설명용이며 Kubernetes/autoscaling에서 유용.
  kind: 개념·운영·예시·조건
  source_lines: 756–853
  destination: platform-infrastructure/postgresql.md
- id: PIS2-05-03
  knowledge: BEGIN/A차감/B추가/COMMIT와 실패 rollback, isolation 가시성, MVCC reader 이전 버전/writer 새 버전. UPDATE/DELETE old
    versions vacuum/autovacuum, 미동작 시 table/index 증가. read/write 병렬성과 동일 row write/write lock 경쟁.
  kind: 개념·운영·예시·조건
  source_lines: 854–930
  destination: platform-infrastructure/postgresql.md
- id: PIS2-05-04
  knowledge: Index와 B-tree email index SQL 예제, =/< />/범위/정렬, read 이익 대 write·disk 비용. Planner seq/index/join 선택,
    EXPLAIN/EXPLAIN ANALYZE 예제. 누락 index·많은 scan·join·반환량·lock 원인, 느린 query→plan→scan/index/row/lock 순서, Redis보다
    query/index 먼저.
  kind: 개념·운영·예시·조건
  source_lines: 931–1004
  destination: platform-infrastructure/postgresql.md
- id: PIS2-05-05
  knowledge: Primary/standby streaming WAL replication, async 응답 후 standby 추종 및 최근 손실, sync standby 확인 후 응답과 latency
    trade-off. Failover 승격, read replica 부하 분산과 async stale read.
  kind: 개념·운영·예시·조건
  source_lines: 1005–1074
  destination: platform-infrastructure/postgresql.md
- id: PIS2-05-06
  knowledge: 잘못된 DELETE도 standby로 전파되어 HA와 backup 별도. pg_dump logical/schema/table/row 및 physical 파일 backup, WAL
    archive+base backup PITR. 10:00백업·10:45실수→10:44복구 예시. 서버 장애 대 실수/손상 구분.
  kind: 개념·운영·예시·조건
  source_lines: 1075–1149
  destination: platform-infrastructure/postgresql.md
- id: PIS2-05-07
  knowledge: shared_buffers 캐시와 work_mem sort/join, 큰 work_mem×동시 query 총량 위험. dead tuple/autovacuum, checkpoint
    disk I/O와 recovery 영향. query→index/plan→connection→memory→autovacuum→disk 순서.
  kind: 개념·운영·예시·조건
  source_lines: 1150–1207
  destination: platform-infrastructure/postgresql.md
- id: PIS2-05-08
  knowledge: StatefulSet postgres0 primary/1·2 standby 예시, PVC/PV disk, Pod lifecycle와 DB role/replication/failover
    구분. Operator optional; 직접 HA/backup/upgrade/recovery 운영 가능. Operator 방식 cluster→operator→CRD→custom resource→구성
    순서. PV≠backup, DROP TABLE 예시와 WAL/PITR 별도, K8s app→managed PG/EKS→RDS 구조.
  kind: 개념·운영·예시·조건
  source_lines: 1208–1333
  destination: platform-infrastructure/postgresql.md
- id: PIS2-06-01
  knowledge: Replication Factor=3의 leader/follower 도식; ISR 집합과 lag offset 1000/999/500 예; leader 장애와 선출; RF3/ISR2
    under-replication 및 broker/network/disk/CPU 원인
  kind: concept,example,failure
  source_lines: 1336-1415
  destination: platform-infrastructure/kafka.md
- id: PIS2-06-02
  knowledge: 100GB/day×7일=700GB, RF3=2.1TB 산식과 여유; producer/replication/consumer disk·network 경로; partition 병렬성
    및 metadata/file/election/복잡도 trade-off; 용량 입력 9개
  kind: capacity,example,trade-off
  source_lines: 1416-1508
  destination: platform-infrastructure/kafka.md
- id: PIS2-06-03
  knowledge: acks 0/1/all 응답·유실 차이, RF3/minISR2·ISR1 쓰기 거부 예, RF3+acksall+minISR2 production 조합, 안전성/쓰기 가용성 trade-off;
    minISR 적용 조건 보완 필요
  kind: configuration,condition,example
  source_lines: 1509-1565
  destination: platform-infrastructure/kafka.md
- id: PIS2-06-04
  knowledge: TLS 암호화, SASL 인증, ACL 인가 역할과 client→TLS→SASL→ACL 도식; TLS 인증 가능성과 listener별 적용 조건 보완
  kind: security,flow
  source_lines: 1566-1609
  destination: platform-infrastructure/kafka.md
- id: PIS2-06-05
  knowledge: Consumer group rebalance와 broker partition reassignment 구분; 증설·부하·disk 편중 재할당; broker 증설 후 기존 partition
    이동; 순차 rolling restart와 ISR/URP/broker 사전 점검
  kind: operations,procedure,checks
  source_lines: 1610-1664
  destination: platform-infrastructure/kafka.md
- id: PIS2-06-06
  knowledge: Stateful workload, StatefulSet kafka0..2, Pod→PVC→PV→disk, 단일 node 대 3node 배치 도식, anti-affinity/spread,
    Kubernetes lifecycle 대 Kafka 복제 역할, Strimzi operator
  kind: architecture,example,boundary
  source_lines: 1665-1740
  destination: platform-infrastructure/kafka.md
- id: PIS2-07-01
  knowledge: vLLM inference server의 역할, model load→request→prefill→decode→response 흐름, training/inference 차이와 input/output
    token 개념.
  kind: 개념·예시·조건
  source_lines:
  - 1745
  - 1800
  destination: platform-infrastructure/vllm.md
- id: PIS2-07-02
  knowledge: VRAM=weights+KV cache+activation+runtime 구성; FP32 4bytes, FP16/BF16 2bytes, INT8/FP8 약 1byte; 동시 요청·context
    증가에 따른 KV cache 증가.
  kind: 개념·예시·조건
  source_lines:
  - 1806
  - 1859
  destination: platform-infrastructure/vllm.md
- id: PIS2-07-A1
  knowledge: 744B total/40B active MoE 가정; FP32 2.98TB와 B200 180GB 기준 Weight만 최소 17장; BF16 1.49TB/FP8 744GB/FP4
    372GB; 전체 expert Weight와 overhead, compute·context·output·목표 tokens/sec 제약.
  kind: 개념·예시·조건
  source_lines:
  - 1867
  - 1926
  destination: platform-infrastructure/vllm.md
- id: PIS2-07-A2
  knowledge: KV/token=2×layers×KV heads×head dimension×bytes; 80×8×128×BF16 가정에서 320KiB/token; 1K 320MiB/8K 2.5GiB/32K
    10GiB/128K 40GiB; input 8K+output 2K=10K; GQA/MQA와 Weight/KV precision의 독립성.
  kind: 개념·예시·조건
  source_lines:
  - 1932
  - 2012
  destination: platform-infrastructure/vllm.md
- id: PIS2-07-A3
  knowledge: MLA (512+64)×78×2에서 87.8KiB/token 근사; 1M context의 BF16 약 87.8GiB/FP8 약 44GiB; 30개 full context 약 2.57/1.3TiB;
    overhead·평균/P95 context·peak sequence·KV dtype/utilization 확인; 지원 길이와 실제 사용량 구분.
  kind: 개념·예시·조건
  source_lines:
  - 2018
  - 2091
  destination: platform-infrastructure/vllm.md
- id: PIS2-07-A4
  knowledge: 서버당 8 GPU인 B300 2대=총 16 GPU; GLM FP4 replica 3개를 TP=4로 배치하고 4장을 spare로 두는 예시; 288GB/GPU, 2.3TB/server,
    총 4.6TB; 단순 Weight 372GB/약 400GB+ 추정과 replica당 1.15TB; serving/training 경쟁과 전용 GPU 분리; 30명 개발자의 coding agent·긴
    context 부하.
  kind: 개념·예시·조건
  source_lines:
  - 2097
  - 2190
  destination: platform-infrastructure/vllm.md
- id: PIS2-07-03
  knowledge: PagedAttention이 필요한 KV block만 할당하여 fragmentation·낭비를 줄이고 concurrency/throughput을 높이는 원리; Weight나 token
    수 자체는 줄이지 않는 한계.
  kind: 개념·예시·조건
  source_lines:
  - 2196
  - 2227
  destination: platform-infrastructure/vllm.md
- id: PIS2-07-04
  knowledge: Continuous/static batching 비교와 A 20/B 500/C 100 token 예시; 완료한 A/C 자리에 D/E를 넣고 KV block을 할당·반환하는 흐름;
    과도한 concurrency의 queue/TTFT/TPOT 악화.
  kind: 개념·예시·조건
  source_lines:
  - 2233
  - 2275
  destination: platform-infrastructure/vllm.md
- id: PIS2-07-05
  knowledge: 첫 token 전 queue+prefill을 포함한 TTFT; TPOT 50ms≈20tok/s; 서버 전체 output tokens/sec·requests/sec와 queue time;
    concurrency 증가에 따른 throughput/latency 상충.
  kind: 개념·예시·조건
  source_lines:
  - 2281
  - 2345
  destination: platform-infrastructure/vllm.md
- id: PIS2-07-06
  knowledge: TP의 layer 연산 분산, PP의 layer 1–20/21–40/41–60/61–80 분할, DP의 전체 replica 운영; GPU 0–3 및 4–7의 TP=4 replica
    예시; 모델 크기와 사용자 수에 따른 확장 방법 구분.
  kind: 개념·예시·조건
  source_lines:
  - 2351
  - 2402
  destination: platform-infrastructure/vllm.md
- id: PIS2-07-07
  knowledge: Weight quantization의 FP32/FP16·BF16/INT8·FP8/4-bit·FP4=4/2/1/0.5bytes; 필요 GPU·비용 감소와 KV 여유 증가; 품질 저하
    가능성; AWQ/GPTQ; FP8 Weight와 BF16 KV의 별도 설정 가능.
  kind: 개념·예시·조건
  source_lines:
  - 2408
  - 2447
  destination: platform-infrastructure/vllm.md
- id: PIS2-07-08
  knowledge: OpenAI-compatible POST /v1/chat/completions→vLLM→model→GPU 흐름; 서버의 model·GPU·TP·context·utilization·quantization
    설정과 요청의 max_tokens/temperature/top_p.
  kind: 개념·예시·조건
  source_lines:
  - 2453
  - 2484
  destination: platform-infrastructure/vllm.md
- id: PIS2-07-09
  knowledge: Kubernetes GPU limits=1 예시와 label/affinity/taint/toleration; TP=4에 필요한 GPU 4장과 같은 Node 배치 이점; Running≠Ready,
    model load·VRAM 할당·KV 준비; 느린 scale-out과 queue/TTFT/GPU 지표; GPU 부족 시 Pending.
  kind: 개념·예시·조건
  source_lines:
  - 2490
  - 2564
  destination: platform-infrastructure/vllm.md
- id: PIS2-07-10
  knowledge: 장애 시 restart/reload/readiness와 단일 replica의 서비스 영향; 확장에 필요한 GPU capacity; 새 replica readiness 뒤 기존 replica
    제거; GPU·memory·queue·TTFT·TPOT·throughput·error·restart 관측; 새 요청 차단→기존 요청 완료→종료의 graceful shutdown.
  kind: 개념·예시·조건
  source_lines:
  - 2570
  - 2636
  destination: platform-infrastructure/vllm.md
- id: PIS2-08-01
  knowledge: Applications→LiteLLM→vLLM/OpenAI/Anthropic/기타 provider 구조; unified API/routing/load balancing/retry/fallback/auth/rate/quota/budget/cost/cache/observability;
    inference 대 gateway 역할
  kind: concept,architecture
  source_lines: 2642-2685
  destination: platform-infrastructure/litellm.md
- id: PIS2-08-02
  knowledge: qwen32b vLLM A/B/C 동일 모델 pool; internal-chat→사내 vLLM primary/external fallback; weight/latency/load/rate/cost/custom
    기준; session affinity 조건
  kind: routing,example,condition
  source_lines: 2686-2724
  destination: platform-infrastructure/litellm.md
- id: PIS2-08-03
  knowledge: 동일 모델 여러 backend 분산, 1K/100K input 부하 차이, inflight/queue/RPM/TPM/latency/health 관측; Kubernetes Service
    endpoint 대 gateway model/provider/replica routing
  kind: load,comparison,example
  source_lines: 2725-2767
  destination: platform-infrastructure/litellm.md
- id: PIS2-08-04
  knowledge: retry/timeout/fallback/health aware routing; overload→fail→retry→overload storm; retry bound/timeout/backoff;
    GLM→Qwen→external fallback; 재시도와 backend/model 변경 구분
  kind: failure,mitigation,flow
  source_lines: 2768-2820
  destination: platform-infrastructure/litellm.md
- id: PIS2-08-05
  knowledge: Noisy neighbor 방지, RPM/TPM/concurrency, token량과 GPU 부하 관계, user/team/APIkey/app/tenant 적용 단위, rate
    limiting 입구 제한 대 autoscaling capacity 증가
  kind: limits,comparison
  source_lines: 2821-2862
  destination: platform-infrastructure/litellm.md
- id: PIS2-08-06
  knowledge: 분당100req/day100만tokens/month100달러 rate/quota/budget 예, 팀별 일·월 token quota, external spend budget, 내부
    vLLM GPU구매/전력/운영/capacity 비용과 공정성
  kind: quota,budget,example
  source_lines: 2863-2898
  destination: platform-infrastructure/litellm.md
- id: PIS2-08-07
  knowledge: Bearer <API_KEY> placeholder; TeamA/TeamB/ServiceC key 예; rate/quota/budget/model access 기반; 인증 대 인가;
    기업 SSO/IAM 연동 조건
  kind: security,example,condition
  source_lines: 2899-2934
  destination: platform-infrastructure/litellm.md
- id: PIS2-08-08
  knowledge: LLM 이전 응답 재사용 hit/miss 흐름, LiteLLM A/B/C→Redis 공유 cache, exact/semantic 구분, agent/dialog 잘못된 hit 위험,
    latency/GPU/API비용/throughput 효과
  kind: caching,failure,flow
  source_lines: 2935-2983
  destination: platform-infrastructure/litellm.md
- id: PIS2-08-09
  knowledge: Deployment replicas3 gateway, Redis cache/DB usage-key-config/SecretManager 외부화, gateway pod 증가 대 vLLM/GPU
    확장 분리, gateway replica가 GPU capacity는 아님
  kind: deployment,state,scaling
  source_lines: 2984-3026
  destination: platform-infrastructure/litellm.md
- id: PIS2-08-10
  knowledge: 앱/LB/LiteLLM/pool/vLLM/GPU 도식과 external 경로 단순화; gateway 9역할 대 vLLM6역할, 9단계 request flow, gateway/serving/compute
    scaling 계층; CPU/queue/GPUmemory/utilization 병목 예와 단정 한계
  kind: architecture,flow,troubleshooting
  source_lines: 3027-3116
  destination: platform-infrastructure/litellm.md
- id: PIS2-09-01
  knowledge: GPU 병렬 가속기와 CPU 범용 작업/matrix·tensor AI 연산의 차이; CUDA 연결 계층; VRAM의 weights/KV/activation/runtime; VRAM
    95%·util 20%와 VRAM 60%·util 100%로 설명한 memory/compute 진단 예시.
  kind: 개념·예시·조건
  source_lines:
  - 3121
  - 3190
  destination: platform-infrastructure/gpu-infrastructure.md
- id: PIS2-09-02
  knowledge: vLLM→CUDA runtime→Container Toolkit→host NVIDIA driver→GPU 계층; nvidia-smi 확인; host driver와 container
    CUDA runtime의 호환성.
  kind: 개념·예시·조건
  source_lines:
  - 3196
  - 3240
  destination: platform-infrastructure/gpu-infrastructure.md
- id: PIS2-09-03
  knowledge: Device plugin의 nvidia.com/gpu=8 등록, Pod limits=4 요청과 가용 Node scheduling; 정수 1/2/4 GPU 할당과 별도 기술이 필요한
    0.5 GPU 공유; capacity 부족 시 Pending; plugin의 scheduling 역할과 toolkit의 GPU 접근 역할 구분.
  kind: 개념·예시·조건
  source_lines:
  - 3246
  - 3304
  destination: platform-infrastructure/gpu-infrastructure.md
- id: PIS2-09-04
  knowledge: 일반 Node pool과 B300 GPU Node pool 분리; gpu=true/gpu-type=b300 label; taint의 진입 제한, toleration의 허용, affinity의
    배치 선택 역할.
  kind: 개념·예시·조건
  source_lines:
  - 3310
  - 3349
  destination: platform-infrastructure/gpu-infrastructure.md
- id: PIS2-09-05
  knowledge: Dedicated GPU의 성능 예측·간섭 감소; time slicing의 utilization 이점과 간섭·latency 변동; MIG 격리 instance와 MPS CUDA
    process 공유; 대형 production·소규모 실험·강한 격리·process 공유에 따른 선택 감각.
  kind: 개념·예시·조건
  source_lines:
  - 3355
  - 3416
  destination: platform-infrastructure/gpu-infrastructure.md
- id: PIS2-09-06
  knowledge: PCIe/NVLink/NCCL과 GPU 간 통신; TP의 같은 layer 계산 결과 교환; 느린 통신에 따른 대기; 가능하면 같은 Node에 TP GPU 배치.
  kind: 개념·예시·조건
  source_lines:
  - 3422
  - 3463
  destination: platform-infrastructure/gpu-infrastructure.md
- id: PIS2-09-07
  knowledge: 하나의 모델을 여러 GPU 서버에 걸쳐 실행; Node 내부 NVLink와 Node 간 network 차이; CPU 개입을 줄이는 RDMA, 저지연 InfiniBand, multi-node
    NCCL; 한 Node에 모델이 들어가면 single-node 우선.
  kind: 개념·예시·조건
  source_lines:
  - 3469
  - 3509
  destination: platform-infrastructure/gpu-infrastructure.md
- id: PIS2-09-08
  knowledge: Weight=params×precision, VRAM에서 Weight/runtime/activation을 뺀 KV 여유, KV=token당 크기×context×sequence;
    compute/queue 제약; concurrency 1/5/10/20에서 TTFT/TPOT/throughput/GPU/KV/queue 측정; replica당 concurrent 8과 peak
    24에서 3개 및 HA 여유 검토; B300/GLM 확인 지표.
  kind: 개념·예시·조건
  source_lines:
  - 3515
  - 3632
  destination: platform-infrastructure/gpu-infrastructure.md
- id: PIS2-09-09
  knowledge: CUDA OOM과 host OOMKilled 구분; 긴 context·동시 요청·큰 모델·공격적 utilization 원인 및 concurrency/context/dtype/quantization/GPU/TP
    조정 방향; TP=4의 GPU 1개 장애가 전체 replica에 미치는 영향; 4장 필요/2장 여유 시 Pending; 16장 모두 사용과 12장 사용·4장 spare 비교; cordon/drain/점검/재참여;
    health·temperature·error·queue·latency와 memory/compute 병목 가설.
  kind: 개념·예시·조건
  source_lines:
  - 3638
  - 3793
  destination: platform-infrastructure/gpu-infrastructure.md
- id: PIS2-00-02
  knowledge: Redis/PostgreSQL/Kafka/vLLM/LiteLLM/GPU 역할과 Kubernetes 위 전체 연결 구조의 text 도식
  kind: architecture
  source_lines: 3797–3844
  destination: platform-infrastructure/index.md
- id: PIS2-00-03
  knowledge: Basic1~9장 개념 학습 완료·Chapter10 Security 다음·11~15 후속 목차
  kind: scope
  source_lines: 3845–3865
  destination: platform-infrastructure/index.md
---

# 4~9장 상세 선추출 목록

번호 있는 절과 7장의 네 보충 절을 별도 ID로 추적한다. 각 장의 전체 읽기 후 개념·예시·숫자·조건·실패 가정을 추출했으며, 원문 본문·정리·예시의 전문은 해당 원문 구간과 한영 정규 페이지에 보존한다. 서두·통합 구조·전체 진도도 포함한 58개 ID다.
