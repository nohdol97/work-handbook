---
id: platform-infrastructure-kafka
status: studied
last_updated: 2026-10-01
last_reviewed: 2026-10-01
knowledge_ids:
  - PIS2-06-01
  - PIS2-06-02
  - PIS2-06-03
  - PIS2-06-04
  - PIS2-06-05
  - PIS2-06-06
---

# Chapter 6. Kafka for Platform Systems

These are study notes from the supplied Basic Chapter 6. They do not claim that a Kafka cluster was built, reassigned, or restarted. Read [Event architecture](../data-platform/event-architecture.md) for prior concepts and [Kubernetes operations](kubernetes-operations.md) for placement and maintenance.

**Reading guide:** The source core preserves the supplied sentences, numbering, diagrams, and order in translation. Read **Section supplements and corrections** for the ISR and write acknowledgment conditions in 6.1 and 6.3, and the StatefulSet/Strimzi conditions in 6.6. Numbers and configurations are study examples. They were not run or tested for performance or recovery in this environment.

<!-- SOURCE CORE START -->

> Broker / Topic / Partition / Producer / Consumer / Consumer Group / Offset / Ordering / basic semantics and other Kafka concepts are assumed to have been covered in Data Platform Basic. This chapter covers only Platform / Infrastructure operations.

## 6.1 Replication / ISR / Leader Election

Key concepts:

```text
Replication Factor
ISR
Leader
Leader Election
Under-Replicated Partition
```

### Replication Factor

```text
RF = 3

Broker A → Leader
Broker B → Follower
Broker C → Follower
```

### ISR

ISR = In-Sync Replicas.

> The set of replicas keeping up well enough with the leader’s data

Example:

```text
ISR = A, B, C
```

A follower can leave the ISR if it cannot keep up with replication.

### Why ISR matters

A follower is not necessarily a safe replica just because it exists.

```text
Leader offset = 1000
Follower B    = 999
Follower C    = 500
```

A replica far behind, such as C, may be unsuitable as an up-to-date leader candidate.

### Leader Election

```text
Leader failure
↓
Leader Election
↓
New leader
```

### Under-Replicated Partition

```text
RF = 3
ISR = 2
```

Fault tolerance is reduced even if the service is still running.

Common reasons for leaving the ISR:

```text
Broker failure
Network issues
Slow disk
CPU / Broker overload
```

---

## 6.2 Cluster Sizing / Capacity

Key concepts:

```text
Broker count
Partition count
Disk Capacity / Throughput
Network Throughput
```

### Disk Capacity

Example:

```text
100GB/day
× 7 days
= 700GB raw
```

RF=3:

```text
700GB × 3
= 2.1TB
```

Basic estimate:

```text
Required storage
≈ Daily data volume
× Retention days
× Replication Factor
+ Headroom
```

### Disk Throughput

Kafka performs these operations:

```text
Producer Write
Replication Write
Consumer Read
```

It performs them concurrently.

A slow disk can cause follower lag → removal from the ISR.

### Network Throughput

```text
Producer Traffic
+
Replication Traffic
+
Consumer Traffic
```

Consider all of this traffic.

### Partition count

More partitions allow more consumer parallelism.

Too many lead to:

```text
More metadata
More files/resources
More leader election work
More operational complexity
```

### Capacity planning inputs

```text
Data volume per second
Read volume per second
Average event size
Retention
Replication Factor
Partition count
Peak Traffic
Disk utilization
Network utilization
```

---

## 6.3 Reliability settings

Key concepts:

```text
acks
min.insync.replicas
Replication Factor
```

### acks=0

The producer does not wait for a response. This is fast but has a high risk of data loss.

### acks=1

Success once the leader receives the data.

Data can be lost if the leader fails before follower replication.

### acks=all

Success after the data reaches the required ISR replicas.

### min.insync.replicas

Example:

```text
RF = 3
min ISR = 2
```

Writes are allowed only when at least two replicas are in the ISR.

If only one ISR replica remains, writes may be rejected to protect the data.

A common production combination:

```text
RF = 3
acks = all
min.insync.replicas = 2
```

### Trade-off

```text
Safety ↑
→ Chance of write failures during faults ↑

Availability ↑
→ Chance of data loss ↑
```

---

## 6.4 Security

Key concepts:

```text
TLS
SASL
ACL
```

### TLS

Communication encryption.

### SASL

Authentication.

```text
Who are you?
```

### ACL

Authorization.

```text
What are you allowed to do?
```

Overall flow:

```text
Client
↓ TLS
Communication encryption
↓ SASL
Authentication
↓ ACL
Permission check
```

---

## 6.5 Operations

Key concepts:

```text
Rebalancing
Partition Reassignment
Broker Expansion
Rolling Restart
```

### Rebalancing

Redistribute partition assignments within a consumer group.

### Partition Reassignment

Move partitions to other brokers.

Use cases:

```text
Adding brokers
Load concentrated on specific brokers
Uneven disk usage
```

### Broker Expansion

After adding a broker, move existing partitions to it to distribute the actual load.

### Rolling Restart

Restart brokers one at a time.

```text
Broker A restart
↓
Check health
↓
Broker B restart
```

Before the operation:

```text
Is the ISR healthy?
No under-replicated partitions?
Are the brokers healthy?
```

Check these conditions.

---

## 6.6 Kafka on Kubernetes

Kafka is a stateful workload.

Key concepts:

```text
StatefulSet
Persistent Storage
Anti-Affinity
Operator
Failure Handling
```

### StatefulSet

```text
kafka-0
kafka-1
kafka-2
```

### Persistent Storage

```text
Kafka Pod
↓
PVC
↓
PV
↓
Persistent Disk
```

### Spreading brokers

Bad example:

```text
Node A
├─ kafka-0
├─ kafka-1
└─ kafka-2
```

Good example:

```text
Node A → kafka-0
Node B → kafka-1
Node C → kafka-2
```

Use:

```text
Pod Anti-Affinity
Topology Spread
```

### Separate Kubernetes and Kafka responsibilities

```text
Kubernetes
= Broker Process / Pod lifecycle

Kafka
= Partition / Replication / Leader
```

### Operator

A Kafka operator such as Strimzi can be used.

---

<!-- SOURCE CORE END -->

## Section supplements and corrections

Official documentation was checked on 2026-10-01. These conditions supplement the source. Kafka references use the 4.3 documentation; check the target cluster’s version and feature flags separately.

### 6.1 Supplement: offset examples and leader eligibility

The source’s `1000 / 999 / 500` illustrates lag. A fixed offset gap alone does not determine ISR membership. Check the removal conditions and actual replica state. Nor is every replica outside the ISR always unsafe. Kafka’s Eligible Leader Replicas (ELR) can provide safe election candidates tracked separately. Check the current ISR, ELR setting/state, and unclean election policy together. [Kafka ELR](https://kafka.apache.org/43/operations/eligible-leader-replicas/)

### 6.2 Supplement: the capacity estimate’s scope

`2.1TB` is a study estimate of total replica data using the source’s inputs. It does not specify one broker’s needs or purchased capacity. For an operational review, measure compressed storage size, retention policy, broker skew, index/segment headroom, recovery/reassignment space, and read/replication traffic. More partitions raise the ceiling for parallelism but do not automatically fix a hot key or slow consumer. These checks are derived from the source’s estimate and partition trade-offs.

### 6.3 Correction: acks=all and minimum ISR

`acks=all` does not mean waiting for only `min.insync.replicas` replicas. A successful acknowledgment requires the full current ISR. With three ISR members and minimum ISR two, all three are involved. The leader counts toward minimum ISR. With `acks=all`, writes fail below that minimum. Do not assume the same producer acknowledgment guarantee for `acks=1`. Also distinguish the high watermark condition for consumer visibility from producer acknowledgment. [Producer acks](https://kafka.apache.org/43/configuration/producer-configs/), [Topic min.insync.replicas](https://kafka.apache.org/43/configuration/topic-configs/)

This combination alone does not guarantee deduplication or end-to-end exactly-once processing. Producer idempotence, retries, consumer processing, and offset commits need separate review. The `RF=3` example also needs an assessment of failure domains and acceptable write interruptions.

### 6.4 Supplement: configure security explicitly

TLS can provide certificate-based authentication as well as encryption. SASL provides authentication and must not be equated with transport encryption. The source flow shows one conceptual combination. Check each listener’s security protocol, authentication method, and authorizer/ACLs. Installing Kafka does not enable all of them. [Kafka security overview](https://kafka.apache.org/43/security/security-overview/)

### 6.5 Supplement: reassignment and maintenance

Adding a broker generally does not redistribute existing partitions automatically. Even with automation, check the reassignment plan, target brokers, replication progress, and throttling. A healthy state before maintenance is not enough to proceed to the next broker restart. Check ISR recovery and actual availability after each step. These are conditions for applying the source checklist to an operational plan, not permission to execute it. [Kafka operations](https://kafka.apache.org/43/operations/basic-kafka-operations/)

### 6.6 Supplement: StatefulSet and operator boundaries

StatefulSet is a basic concept for understanding stateful workloads. Do not assume every Kafka operator creates StatefulSets. Current Strimzi manages its own resources, including `StrimziPodSet`. Check the chosen operator version’s resources and storage/rack placement settings. [Strimzi deployment guide](https://strimzi.io/docs/operators/latest/full/deploying.html)

Placing pods on different nodes is also different from placing replicas across zones or failure domains. Having a PVC does not mean backup and recovery tests have been completed. Review placement and disruption conditions alongside [Kubernetes operations](kubernetes-operations.md).

## LLM in Practice

### Review maintenance with a shrinking ISR

**Situation:** Assess broker maintenance for a hypothetical Kafka topic whose ISR has shrunk. Connect the supplements for 6.1, 6.3, and 6.5 with disruption conditions in [Kubernetes operations](kubernetes-operations.md).

**Context to Give the LLM:** Sanitized topic/producer settings, Kafka version and ELR state, ISR changes, per-broker disk/network metrics, error codes, and maintenance constraints. Exclude credentials and real internal addresses.

**Example Prompt:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 Kafka topic은 RF=3, acks=all, min.insync.replicas=2다.
    현재 ISR은 2개이고 follower 하나의 disk latency가 증가했다.
    버전과 ELR 설정: [확인한 값 또는 미확인]
    ISR 변화, broker별 disk/network, producer 오류: [비식별 관측값]
    아직 재시작이나 재할당은 하지 않았다.
    [요청]
    현재 상태와 유지보수 계획을 먼저 검토하라.
    관측 사실, 가정, 원인 가설, 누락 근거를 구분하라.
    ISR이 1개로 줄 때 producer 응답과 쓰기 가용성을 설명하라.
    min ISR=2가 항상 2개 응답만 기다린다는 뜻인지 검토하라.
    [출력]
    읽기 전용 확인 순서, 진행 조건, 중단 조건을 표로 제시하라.
    원인 확인 없이 acks나 min ISR을 낮추는 변경을 권하지 말라.
    [검증]
    실제 topic/producer 설정과 해당 버전 공식 문서로 대조하라.
    변경 실행은 별도 승인 절차가 필요하다고 명시하라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    A hypothetical Kafka topic uses RF=3, acks=all, and min.insync.replicas=2.
    The ISR has 2 members, and one follower has rising disk latency.
    Version and ELR settings: [verified values or unknown]
    ISR changes, broker disk/network metrics, producer errors: [sanitized observations]
    No restart or reassignment has been performed.
    [Task]
    Review the current state and maintenance plan first.
    Separate observations, assumptions, hypotheses, and missing evidence.
    Explain producer responses and write availability if the ISR falls to 1.
    Check whether minimum ISR=2 means waiting for only 2 acknowledgments every time.
    [Output]
    Give a table of read-only checks, go conditions, and stop conditions.
    Do not recommend lowering acks or minimum ISR without finding the cause.
    [Checks]
    Compare actual topic/producer settings with the version-specific official docs.
    State that executing a change needs a separate approval process.
    ```

**Expected Output:** A table separating write acknowledgment conditions, possible lag causes, distinguishing checks, and stop conditions.

**What the LLM Can Get Wrong:** It may treat two ISR members as ample safety margin, confuse minimum ISR with the number of replicas to wait for, or generalize election rules without version/ELR differences.

**How to Validate:** A person compares actual settings, errors, and metrics with the version-specific official docs. Run tests and changes separately in an approved environment. This is an authored usage example, not a claim that an LLM response or actual recovery was verified.
