---
id: aws-cloud-databases-cache
status: studied
last_updated: 2026-10-03
last_reviewed: 2026-10-03
knowledge_ids:
  - AWS-05-01
  - AWS-05-02
  - AWS-05-03
---

# Chapter 5. Database / Cache

제공된 Chapter 5의 제목·순서·문단·표·예시를 원문 그대로 보존했다. 5.1의 Multi-AZ 유형, 5.2의 Aurora endpoint·Serverless, 5.3의 엔진별 복제·세션 조건은 본문 뒤 **보완 및 적용 조건**을 함께 읽는다. Basic 개념 학습이며 실제 AWS 리소스 생성·장애조치·성능 시험 기록이 아니다.

<!-- SOURCE CORE START -->

## 5.1 RDS

RDS = **Relational Database Service**

> AWS가 많은 운영 작업을 대신해주는 Managed 관계형 DB 서비스

예:

```text
Application
   ↓
RDS PostgreSQL
```

### 대표 DB Engine

- PostgreSQL
- MySQL
- MariaDB
- Oracle
- SQL Server

RDS 자체가 DB Engine이 아니라 여러 DB Engine을 Managed 형태로 제공하는 서비스다.

### EC2 PostgreSQL vs RDS

직접 운영:

```text
EC2
 ↓
PostgreSQL
```

직접 관리:

- OS
- PostgreSQL 설치
- Disk
- Backup
- Patch
- Monitoring
- Failover
- Replication

RDS:

```text
Application
 ↓
RDS PostgreSQL
```

AWS가 많은 인프라 운영을 담당.

사용자는 주로:

- Schema
- Query
- Index
- Application Connection
- DB Parameter

등에 집중.

### RDS는 보통 Private Subnet

```text
VPC
│
├─ Public Subnet
│   └─ ALB
│
└─ Private Subnet
    ├─ Application
    └─ RDS
```

### DB Subnet Group

RDS가 어느 Subnet/AZ들에 배치될 수 있는지 정의하는 Subnet 목록.

```text
DB Subnet Group
├─ Private Subnet A
├─ Private Subnet B
└─ Private Subnet C
```

### Security Group

PostgreSQL:

```text
TCP 5432
Source: APP-SG
```

### RDS Endpoint

Application은 DB IP가 아니라 Endpoint를 사용.

```text
mydb.xxxxxx.ap-northeast-2.rds.amazonaws.com
```

장애조치/인프라 변경 시 실제 DB 인스턴스가 바뀌어도 Endpoint를 통해 접근 가능.

### Multi-AZ

```text
AZ A
└─ Primary RDS

AZ B
└─ Standby RDS
```

Primary 장애 시 Standby로 Failover.

목적:

```text
Multi-AZ
= High Availability
```

### Read Replica

```text
             Primary
             /     \
      Replica A   Replica B
```

- Write → Primary
- Read → Replica

목적:

```text
Read Replica
= Read Scaling
```

### Multi-AZ vs Read Replica

```text
Multi-AZ
→ 장애 대응

Read Replica
→ 읽기 부하 분산
```

### Backup / Snapshot

- Automated Backup
- Point-in-Time Recovery
- Manual Snapshot

### Storage

사용자는 Storage Size, Type, IOPS 등을 설정하지만 EBS를 직접 attach/detach하는 방식은 아니다.

### Scaling

Instance Class 변경을 통한 Vertical Scaling.

Read Replica를 통한 Read Scaling.

### Connection 문제

Pod 수 증가 시 DB Connection도 같이 증가한다.

예:

```text
Pod 100
×
Connection 20
=
2,000 DB Connections
```

Connection Pool 관리가 중요.

필요 시 RDS Proxy도 고려.

### EKS + RDS

```text
Internet
 ↓
ALB
 ↓
EKS
├─ Pod
├─ Pod
└─ Pod
   ↓
RDS PostgreSQL
```

애플리케이션은 Stateless하게, 영속적 Transactional Data는 RDS에 저장.

### EKS에서 PostgreSQL 직접 운영 vs RDS

직접 운영 시:

- StatefulSet
- PVC
- EBS
- Replication
- Backup
- Failover
- Upgrade
- Operator

등을 직접 운영해야 한다.

RDS 사용 시 운영 부담을 크게 줄일 수 있다.

단, RDS라도 다음은 여전히 신경 써야 한다.

- Slow Query
- Index
- Schema
- Connection Pool
- Transaction
- Lock
- Vacuum
- Capacity Planning

---

## 5.2 Aurora

Aurora는 AWS가 만든 **클라우드용 관계형 DB 엔진**이다.

RDS 관계:

```text
Amazon RDS
├─ PostgreSQL
├─ MySQL
├─ MariaDB
├─ Oracle
├─ SQL Server
└─ Aurora
```

즉:

> RDS = Managed DB 서비스  
> Aurora = RDS에서 사용할 수 있는 DB Engine 중 하나

### PostgreSQL / MySQL Compatible

- Aurora PostgreSQL-Compatible
- Aurora MySQL-Compatible

AWS가 만든 엔진이지만 PostgreSQL/MySQL 호환 인터페이스를 제공.

### Compute와 Storage 분리

일반 RDS PostgreSQL:

```text
DB Instance
   ↓
Storage
```

Aurora:

```text
         Shared Aurora Storage
          ↑       ↑       ↑
        DB 1    DB 2    DB 3
```

핵심 설계:

> 여러 DB Instance가 Shared Distributed Storage Layer를 사용

### Writer / Reader

```text
              Aurora Cluster
                   │
          ┌────────┴────────┐
          │                 │
       Writer            Readers
          │              /     \
          │          Reader1  Reader2
          │
          └──── Shared Storage ────
```

- Writer = INSERT / UPDATE / DELETE
- Reader = SELECT / Read Scaling

### Endpoint

Cluster Endpoint:

```text
Application Write
      ↓
Cluster Endpoint
      ↓
Writer
```

Reader Endpoint:

```text
Application Read
      ↓
Reader Endpoint
     /      \
Reader1    Reader2
```

### Failover

Writer 장애 시 Reader 중 하나를 새로운 Writer로 승격 가능.

애플리케이션은 Cluster Endpoint를 계속 바라본다.

### Multi-AZ

Aurora Storage는 Multi-AZ 고가용성을 강하게 고려한 분산 스토리지 구조를 사용한다.

### Storage 자동 확장

데이터 증가에 따라 Storage Capacity가 자동으로 확장되는 구조를 제공한다.

### Aurora Serverless

사용자가 고정 DB Instance Size를 직접 관리하는 부담을 줄이고 수요에 따라 Compute Capacity를 조절한다.

```text
Provisioned
= 서버 크기 직접 선택

Serverless
= Compute를 탄력적으로 운영
```

### Aurora가 항상 더 좋은 것은 아니다

고려 요소:

- 비용
- 기능 차이
- PostgreSQL 버전 / Extension 호환성
- AWS 종속성
- 운영 복잡도

작고 단순한 서비스는 RDS PostgreSQL로 충분할 수 있다.

규모가 커지고 HA/Read Scaling이 중요하면 Aurora PostgreSQL을 고려할 수 있다.

### Connection Pool 문제

Aurora에서도 DB Connection 관리는 필요하다.

```text
Application
 ↓
Connection Pool
 ↓
RDS Proxy (필요 시)
 ↓
Aurora
```

### RDS PostgreSQL vs Aurora PostgreSQL

| 항목 | RDS PostgreSQL | Aurora PostgreSQL |
|---|---|---|
| DB 엔진 | PostgreSQL | AWS 자체 PostgreSQL-compatible |
| Storage 구조 | Instance 중심 Managed Storage | Shared Distributed Storage |
| HA | Multi-AZ | Multi-AZ 중심 설계 |
| Read Scaling | Read Replica | Aurora Reader |
| Failover | 지원 | Cluster 구조 기반 |
| Storage 확장 | 관리 요소 있음 | 더 자동화됨 |
| 비용/구조 | 상대적으로 단순 | 상대적으로 복잡/비쌀 수 있음 |

---

## 5.3 ElastiCache

ElastiCache:

> AWS가 운영해주는 Managed In-Memory Cache 서비스

Redis 계열 캐시를 AWS Managed 형태로 운영할 수 있다.

### 왜 Cache가 필요한가?

모든 요청이 RDS로 가면 DB 부하가 커진다.

```text
Application
   ↓
ElastiCache
   ↓ Cache Miss
RDS
```

### Cache Aside

조회 흐름:

```text
Application
    ↓
ElastiCache
    ↓
Key 존재?
```

Cache Hit:
- Redis에서 바로 반환

Cache Miss:
1. RDS 조회
2. Redis 저장
3. 사용자 반환

### RDS를 대체하지 않는다

```text
RDS
= Source of Truth

ElastiCache
= 빠른 임시 데이터 / Cache
```

### 대표 용도

- Cache
- Session
- Rate Limit
- Counter
- Leaderboard
- Temporary State

### 직접 Redis 운영 vs ElastiCache

직접 Redis 운영:

```text
EKS
└─ Redis StatefulSet
   ├─ PVC
   ├─ Replication
   ├─ Failover
   ├─ Backup
   └─ Upgrade
```

ElastiCache:

```text
Application
   ↓
Managed Cache
```

유사 철학:

```text
PostgreSQL 직접 운영 → RDS
Redis 직접 운영      → ElastiCache
```

### Private Network

보통 VPC Private Network에 둔다.

```text
VPC
│
├─ Public Subnet
│   └─ ALB
└─ Private Subnet
    ├─ EKS
    ├─ RDS
    └─ ElastiCache
```

### Security Group

Redis-compatible 서비스는 일반적으로 `6379` 포트를 사용.

```text
CACHE-SG
Inbound
6379 ← APP-SG
```

### Primary / Replica

```text
Primary
   ↓ Replication
Replica
```

고가용성과 Read Scaling에 활용.

### Multi-AZ

```text
AZ A
└─ Primary

AZ B
└─ Replica
```

Primary 장애 시 Replica를 승격 가능.

### Sharding

데이터가 한 노드 메모리에 모두 들어가지 않을 때 여러 Shard로 분할.

```text
Cluster
├─ Shard 1
│  ├─ Primary
│  └─ Replica
└─ Shard 2
   ├─ Primary
   └─ Replica
```

### Replica vs Shard

```text
Replica
= 같은 데이터 복제
= HA / Read Scaling

Shard
= 데이터 분할
= Capacity / Write Scaling
```

### TTL

```text
user:123
TTL = 600초
```

세션, 캐시, Token, Rate Limit 등에 유용.

### Cache Invalidation

DB 값은 바뀌었지만 Cache에 옛 값이 남아 stale data가 될 수 있다.

따라서:

```text
DB Update
 ↓
Cache Delete / Update
```

또는 TTL을 사용한다.

### Session 저장

여러 Pod가 있는 경우 세션을 Pod Local Memory에 저장하면 문제가 생길 수 있다.

```text
        ElastiCache
        /    |    \
     Pod A Pod B Pod C
```

세션을 외부 저장소로 분리하면 Application을 Stateless하게 유지할 수 있다.

### Auto Scaling과 연결

```text
Application
= Stateless

Session / Cache
= ElastiCache

Persistent Data
= RDS

Object
= S3
```

### RDS vs ElastiCache

| 항목 | RDS | ElastiCache |
|---|---|---|
| 저장 위치 | Disk 중심 | Memory 중심 |
| 데이터 | 영구 데이터 | 임시/캐시 데이터 |
| 속도 | 상대적으로 느림 | 매우 빠름 |
| 대표 용도 | 사용자/주문/설정 | Cache/Session |
| 원본 데이터 | 주로 O | 보통 X |

### Redis를 무조건 넣어야 하는가?

아니다.

초기 서비스가 RDS만으로 충분하면 Redis를 넣지 않아도 된다.

Redis를 추가하면 다음 복잡성이 생긴다.

- Cache Policy
- TTL
- Invalidation
- Memory 관리
- Failover

따라서 실제 DB 부하나 Latency 문제가 있을 때 도입하는 접근이 좋다.

---

<!-- SOURCE CORE END -->

## 보완 및 적용 조건

공식 문서 확인일: 2026-10-03. 아래는 원문과 분리한 정정·조건이며, 배포나 장애조치 명령을 실행한 결과가 아니다.

### 5.1 RDS 엔진과 Multi-AZ 유형

원문의 엔진 목록은 예시다. 현재 RDS 문서는 Db2도 포함한다. 엔진·버전·리전별 기능과 지원 범위를 확인한다. [RDS DB 인스턴스](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.DBInstance.html).

원문의 Primary/Standby 그림은 **Multi-AZ DB instance deployment**에 해당한다. 이 유형의 standby는 읽기를 처리하지 않는다. **Multi-AZ DB cluster deployment**는 writer와 읽기를 처리할 수 있는 두 standby를 갖는다. 따라서 “Multi-AZ는 HA, Read Replica는 읽기 확장”이라는 원문 구분을 모든 배포 유형에 그대로 적용하지 않는다. [RDS Multi-AZ 유형](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html).

Endpoint 유지가 기존 연결이나 진행 중 transaction의 무중단을 보장하지는 않는다. Failover 후 DNS 변경 반영과 재연결이 필요하다. 재시도는 transaction 결과 확인과 중복 처리 방지도 함께 설계한다. [RDS Multi-AZ failover](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.Failover.html).

`100 × 20 = 2,000`은 Pod마다 20개 연결을 보유한다는 가정의 계산이다. 실제 동시 연결 수·pool 상한·idle 연결·DB 한도를 확인한다. RDS Proxy를 추가한다는 이유만으로 DB 처리 용량이 무한히 늘어나지는 않는다.

### 5.2 Aurora endpoint·장애조치·Serverless

Reader endpoint는 **연결 단위**로 분산하며 한 연결의 개별 query를 여러 reader로 나누지 않는다. Reader가 없는 cluster에서는 writer로 연결된다. 원문의 Writer/Reader 구분은 역할 설명이며 writer도 읽기를 처리할 수 있다. [Aurora reader endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Endpoints.Reader.html).

Writer 장애 시 기존 replica를 승격하거나 새 primary를 생성할 수 있다. Cluster endpoint로 재연결해야 하며 기존 연결이 자동으로 보존되는 것은 아니다. Reader endpoint가 failover 중 잠시 새 writer로 연결할 수도 있다. [Aurora endpoint와 HA](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.Endpoints.html).

Serverless도 용량 범위와 지원 엔진·리전·기능을 확인해야 한다. 무제한 용량이나 무조건 낮은 비용을 뜻하지 않는다. [Aurora Serverless](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html). 0 ACU 자동 일시 중지는 지원 엔진 버전과 설정 조건을 만족해야 하며, 연결 시 재개 지연이 생길 수 있다. [자동 일시 중지와 재개](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2-auto-pause.html).

### 5.3 ElastiCache 엔진·복제·샤딩

ElastiCache는 Valkey, Redis OSS, Memcached를 지원하고 node-based와 Serverless 방식이 있다. 원문의 primary/replica/shard 설명은 주로 Valkey·Redis OSS의 node-based 구성을 설명한다. [ElastiCache 개요](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html).

Node-based Memcached에는 같은 방식의 replica 기반 HA나 자동 failover가 없다. Valkey·Redis OSS는 cluster mode disabled이면 한 shard, enabled이면 여러 shard로 분할할 수 있다. Serverless 내부 구성을 node-based 그림과 동일하다고 가정하지 않는다. [엔진 비교](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/SelectEngine.html).

일반 비동기 복제는 failover 시 최근 쓰기를 잃을 수 있다. Multi-AZ와 replica 배치·자동 failover 조건을 확인한다. 일부 Valkey 구성에는 별도의 durability 기능이 있으므로 “모든 ElastiCache는 임시 데이터만 저장하고 내구성이 없다”로 일반화하지 않는다. 복구 보장은 엔진·버전·durability 활성 여부·쓰기 모드에 따라 확인한다. [복제와 durability 조건](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Replication.html), [Multi-AZ failover](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/AutoFailover.html).

### 5.3 TTL·세션·캐시 도입 판단

TTL `600초`는 원문 예시이며 즉시 정합성 보장이 아니다. Cache-aside에서 만료 전 stale 값이 남을 수 있다. DB 갱신과 cache 무효화가 분리되므로 실패·경합 시나리오도 검토한다. [AWS 캐시 전략](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html).

세션을 외부화하면 Pod 교체와 독립적으로 공유할 수 있지만, 세션이 영구 보존된다는 뜻은 아니다. 만료·메모리 정책에 따른 제거·복제 손실·재로그인·폐기 시 동작을 정의한다. 이는 원문의 세션 설계에서 확인해야 할 운영 조건이다. 일반 캐시 데이터의 재생성과 세션 소실의 사용자 영향을 구분한다. 원문의 “RDS보다 매우 빠름”은 workload별 측정치를 대신하지 않는다. Cache hit/miss·DB 부하·추가 네트워크 지연을 실제 요구와 대조한다.

[PostgreSQL 운영](../platform-infrastructure/postgresql.md) · [Redis 운영](../platform-infrastructure/redis.md)

## LLM 실무: DB 연결 증가와 캐시 제안 검토

- **상황:** Pod 확장 뒤 DB 연결이 늘어나고, Redis 도입을 제안받았다.
- **LLM에 줄 맥락:** 비식별 Pod·pool 수, DB 엔진·배포 유형, 연결·query 지표, session 요구와 허용 stale 시간.
- **예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    Pod 수와 Pod별 pool 상한: [비식별 설정]
    RDS/Aurora 엔진·버전·배포 유형과 연결·query 지표: [자료]
    Cache 엔진·모드, session 손실 허용, stale 허용 시간: [확인값 또는 모름]
    [요청]
    연결 증가의 관측과 가정을 나누고 pool 조정·DB 검토·캐시 도입안을 평가하세요.
    [출력]
    100×20 예시와 실제 수치를 구분한 연결 예산, 가설별 근거와 다음 읽기 전용 확인을 작성하세요.
    [검증]
    Multi-AZ 유형별 읽기 기능, reader endpoint의 연결 분산, 캐시 손실 조건을 확인하세요.
    지연 지표 하나로 원인을 단정하거나 리소스 변경·장애조치를 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Pod count and pool limit per Pod: [sanitized settings]
    RDS/Aurora engine, version, deployment type, and connection/query metrics: [material]
    Cache engine and mode, acceptable session loss, and stale-data duration: [known values or unknown]
    [Task]
    Separate observations from assumptions about connection growth and assess pool changes, database review, and cache adoption.
    [Output]
    Provide a connection budget separating the 100×20 example from actual numbers, evidence for each hypothesis, and next read-only checks.
    [Checks]
    Check read support by Multi-AZ type, connection balancing at reader endpoints, and cache data-loss conditions.
    Do not infer a cause from one latency metric alone or execute resource changes or failover.
    ```

- **기대 출력:** 연결 예산, 가설별 증거·누락 정보, 캐시 도입 효과와 정합성·세션 손실 조건의 비교.
- **LLM이 틀릴 수 있는 점:** 모든 Multi-AZ standby가 읽기를 처리한다고 생각하거나 Redis가 connection 폭증을 자동으로 해결한다고 단정할 수 있다.
- **검증 방법:** AWS 공식 문서, 실제 pool·배포 설정과 같은 시간대 지표를 대조한다. 필요 실험은 별도 격리 환경에서 승인된 범위로 수행한다. 이 페이지에서는 실험을 실행하지 않았다.
