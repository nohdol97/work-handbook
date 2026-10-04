---
id: handbook-glossary
status: overview
last_updated: 2026-10-04
last_reviewed: 2026-10-04
knowledge_ids: []
---

# Glossary

| Term | Meaning |
|---|---|
| Canonical knowledge | A shared set of useful knowledge merged from several sources. |
| Canonical page ID | A stable page identifier that stays the same when a path changes. A Korean and English pair shares one ID. |
| Content manifest | A list of meaningful source items with stable IDs. |
| Coverage matrix | A table that tracks where each ID is included, merged, deferred, or excluded, and why. |
| Semantic audit | A review of whether both languages keep the same concepts, examples, constraints, and warnings. |
| Source of truth | The original used to guide changes and decisions. Here, it is Markdown in Git. |

## Data platform terms

| Term | Meaning | Canonical topic |
|---|---|---|
| OLTP | A workload for small service transactions. | [foundations](../data-platform/foundations.md) |
| OLAP | An analytical workload that scans, aggregates, and joins large histories. | [foundations](../data-platform/foundations.md) |
| Column pruning | Reading only the columns a query needs. | [foundations](../data-platform/foundations.md) |
| Partition / pruning | A rule that divides data / skipping regions that cannot match a query. | [foundations](../data-platform/foundations.md) |
| Cardinality | The number of distinct values. | [foundations](../data-platform/foundations.md) |
| Compaction | Maintenance that combines small files into suitable sizes. | [foundations](../data-platform/foundations.md) |
| Schema | A definition of data structure, such as fields and types. | [event-architecture](../data-platform/event-architecture.md) |
| Idempotency | Repeating an operation does not duplicate its intended effect. | [event-architecture](../data-platform/event-architecture.md) |
| Consumer lag | A measure of how far a consumer is behind, often a log-position gap. | [event-architecture](../data-platform/event-architecture.md) |
| Snapshot | A consistent view of table or processing state at a point in time; scope depends on the type. | [lakehouse-iceberg](../data-platform/lakehouse-iceberg.md) |
| Shuffle | Moving data between processing nodes for operations such as grouping by key. | [spark](../data-platform/spark.md) |
| Data skew | Uneven data or work across keys or tasks. | [spark](../data-platform/spark.md) |
| Watermark | An estimate of event-time progress used for late data and state handling. | [flink](../data-platform/flink.md) |
| Checkpoint / savepoint | A state snapshot for recovery / a state snapshot used for planned operational changes. | [flink](../data-platform/flink.md) |
| Backpressure | Pressure sent upstream when downstream processing cannot keep up. | [flink](../data-platform/flink.md) |
| CDC | Capturing source changes such as inserts, updates, and deletes. | [cdc-debezium](../data-platform/cdc-debezium.md) |
| WAL | A write-ahead log of database changes used for recovery and replication. | [cdc-debezium](../data-platform/cdc-debezium.md) |
| Tombstone | A null-value record marking key removal in a Kafka compacted topic. | [cdc-debezium](../data-platform/cdc-debezium.md) |
| Orchestration / DAG | Managing task dependencies and execution / a directed graph without cycles. | [orchestration](../data-platform/orchestration.md) |
| Backfill | Filling or recomputing data for a past range. | [orchestration](../data-platform/orchestration.md) |
| Grain | What one row in a table represents. | [analytical-modeling](../data-platform/analytical-modeling.md) |
| Fact / dimension | Measured events or values / attributes that describe them. | [analytical-modeling](../data-platform/analytical-modeling.md) |
| SCD Type 2 | A model that preserves attribute history with new rows and validity periods. | [analytical-modeling](../data-platform/analytical-modeling.md) |
| Semantic layer | A layer defining reusable meanings and calculations for metrics and dimensions. | [analytical-modeling](../data-platform/analytical-modeling.md) |
| Predicate pushdown | Passing filter processing closer to the data source. | [trino](../data-platform/trino.md) |
| Data quality | Whether data meets requirements such as accuracy, completeness, and validity. | [data-quality](../data-platform/data-quality.md) |
| Quarantine | Separating invalid data from the normal path for investigation and recovery. | [data-quality](../data-platform/data-quality.md) |
| SLI / SLO | A measured service-level indicator / its target. | [data-observability](../data-platform/data-observability.md) |
| Freshness | Whether data is recent enough for its use. | [data-observability](../data-platform/data-observability.md) |
| Observability | Understanding system or data state and change through observed signals. | [data-observability](../data-platform/data-observability.md) |
| Lineage | Relationships showing how data is created, moved, and transformed. | [lineage-metadata](../data-platform/lineage-metadata.md) |
| Metadata / catalog | Information about data / a system for finding and exploring that information. | [lineage-metadata](../data-platform/lineage-metadata.md) |
| Data contract | An agreement covering schema, meaning, quality, freshness, and ownership. | [governance](../data-platform/governance.md) |
| RBAC | Access control that grants permissions by role. | [governance](../data-platform/governance.md) |
| Retention | How long and under which conditions data and derived copies are kept. | [governance](../data-platform/governance.md) |
| Trace / observation / session | An execution flow / an individual step / a group of related executions. | [ai-ready-data](../data-platform/ai-ready-data.md) |
| Provenance | Information tracing the origin and production context of data or AI output. | [ai-ready-data](../data-platform/ai-ready-data.md) |
| Reproducibility | The ability to restore experiment conditions; it does not guarantee identical LLM wording. | [ai-ready-data](../data-platform/ai-ready-data.md) |
| Regression dataset | Evaluation cases used to check whether past failures return. | [ai-ready-data](../data-platform/ai-ready-data.md) |
| Online evaluation | Attaching feedback, rule checks, or judge signals to real AI executions. | [online-evaluation](../data-platform/ai-evaluation.md#161-online-evaluation-events) |

[Knowledge workflow](../methodologies/knowledge-workflow.md) · [Home](../index.md)

## Evaluation, managed platforms, and recovery

| Term | Meaning | Canonical topic |
|---|---|---|
| Rubric | Scoring and decision criteria for each evaluation dimension. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| Groundedness | How well a response is supported by the supplied evidence. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| Inter-rater agreement | Agreement among people evaluating the same cases. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| Bundle version | A version of the combined agent, prompt, tool, model, and retrieval configuration. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| TTFT | Time to first token: the delay from a request to its first output token. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| Cost per success | Total cost divided by successful executions, with explicit success criteria and measurement scope. | [ai-evaluation](../data-platform/ai-evaluation.md) |
| DBU | A Databricks usage unit. Check compute type, contract, and other factors for actual charges. | [databricks](../data-platform/databricks.md) |
| Photon | A vectorized query execution engine in Databricks. | [databricks](../data-platform/databricks.md) |
| UniForm | Provides metadata for Iceberg readers of Delta tables; it does not imply equal writer support. | [databricks](../data-platform/databricks.md) |
| Micro-partition | A Snowflake-managed columnar storage unit with metadata used for pruning. | [snowflake](../data-platform/snowflake.md) |
| Dynamic Table | A Snowflake object that refreshes a declared query result toward a target lag. | [snowflake](../data-platform/snowflake.md) |
| RTO | Recovery time objective: the target time allowed for recovery. | [production-operations](../data-platform/production-operations.md) |
| RPO | Recovery point objective: acceptable data loss expressed as a time window. | [production-operations](../data-platform/production-operations.md) |

## Platform and infrastructure basics

| Term | Meaning | Canonical topic |
|---|---|---|
| Process / PID | A running program / its identifier within a PID namespace. | [linux-containers](../platform-infrastructure/linux-containers.md) |
| File descriptor (FD) | An integer a process uses to refer to an open file, socket, or other I/O object. | [linux-containers](../platform-infrastructure/linux-containers.md) |
| Linux namespace | A kernel feature that isolates views such as PIDs, networking, and mounts. | [linux-containers](../platform-infrastructure/linux-containers.md) |
| cgroup | A Linux feature for controlling and accounting for resource use by groups of processes. | [linux-containers](../platform-infrastructure/linux-containers.md) |
| OCI | Open Container Initiative, which defines compatibility specifications such as image and runtime formats. | [linux-containers](../platform-infrastructure/linux-containers.md) |
| Pod | The basic Kubernetes deployment and scheduling unit. Its colocated containers share execution context such as networking. | [kubernetes-core](../platform-infrastructure/kubernetes-core.md) |
| Reconciliation | A controller continually adjusting observed state toward declared desired state. | [kubernetes-core](../platform-infrastructure/kubernetes-core.md) |
| Request / Limit | Requested resources used for scheduling and allocation / runtime resource limits. CPU and memory limits behave differently. | [kubernetes-core](../platform-infrastructure/kubernetes-core.md) |
| Readiness / Liveness / Startup probe | Checks that distinguish traffic readiness, health requiring restart, and completion of startup. | [kubernetes-core](../platform-infrastructure/kubernetes-core.md) |
| CNI | A standard plugin interface for configuring container networking. | [kubernetes-operations](../platform-infrastructure/kubernetes-operations.md) |
| CSI | Container Storage Interface, which connects orchestrators and storage drivers. | [kubernetes-operations](../platform-infrastructure/kubernetes-operations.md) |
| etcd / Quorum | A distributed key-value store for Kubernetes API state / the majority needed for consensus. | [kubernetes-operations](../platform-infrastructure/kubernetes-operations.md) |
| HPA / VPA | Autoscaling approaches that adjust workload replica count / container resource requests. | [kubernetes-operations](../platform-infrastructure/kubernetes-operations.md) |
| Cluster Autoscaler | A component that adjusts node count using conditions such as unschedulable Pods. | [kubernetes-operations](../platform-infrastructure/kubernetes-operations.md) |
| PodDisruptionBudget (PDB) | A budget limiting voluntary disruptions through the Eviction API. It does not prevent every failure. | [kubernetes-operations](../platform-infrastructure/kubernetes-operations.md) |
| Cordon / Drain | Mark a node unschedulable / perform Pod eviction and related work for node maintenance. | [kubernetes-operations](../platform-infrastructure/kubernetes-operations.md) |

## Data services, AI serving, and GPUs

| Term | Meaning | Canonical topic |
|---|---|---|
| TTL | An expiry duration limiting how long an entry stays valid, often used for cache or session retention. | [redis](../platform-infrastructure/redis.md) |
| RDB / AOF | Redis persistence through point-in-time snapshots / recorded write commands. Recovery and loss depend on configuration. | [redis](../platform-infrastructure/redis.md) |
| Sentinel / Redis Cluster | Redis failure detection and failover coordination / a cluster that partitions data with hash slots. | [redis](../platform-infrastructure/redis.md) |
| MVCC | A method that manages visible row versions to support concurrent transactions. | [postgresql](../platform-infrastructure/postgresql.md) |
| Connection pool | A set of database connections reused by client requests. It does not create unlimited database capacity. | [postgresql](../platform-infrastructure/postgresql.md) |
| WAL | Write-Ahead Log used to recover data changes and managed for backup, replication, and PITR. | [postgresql](../platform-infrastructure/postgresql.md) |
| PITR | Point-in-Time Recovery using a base backup and the required logs to reach a target time. | [postgresql](../platform-infrastructure/postgresql.md) |
| ISR | The Kafka set of In-Sync Replicas tracked as sufficiently caught up with the leader. | [kafka](../platform-infrastructure/kafka.md) |
| min.insync.replicas | The minimum ISR size required to acknowledge Kafka writes using acks=all successfully. | [kafka](../platform-infrastructure/kafka.md) |
| Prefill / Decode | The phase that processes input prompt tokens / the phase that repeatedly generates the next token. | [vllm](../platform-infrastructure/vllm.md) |
| KV Cache | Memory storing attention key/value state from previous tokens for reuse during generation. | [vllm](../platform-infrastructure/vllm.md) |
| Continuous batching | Batching inference work by adding new requests and removing completed requests from the active set. | [vllm](../platform-infrastructure/vllm.md) |
| Tensor parallelism | Parallel execution that divides model tensor computations across multiple GPUs. | [vllm](../platform-infrastructure/vllm.md) |
| Virtual key | An access key used by an LLM gateway to assign permissions and limits to users or teams. | [litellm](../platform-infrastructure/litellm.md) |
| Fallback | An alternate path that sends a request to another model or provider when the primary path is unavailable. | [litellm](../platform-infrastructure/litellm.md) |
| MIG | Multi-Instance GPU, which partitions supported NVIDIA GPUs into instances with assigned resources. | [gpu-infrastructure](../platform-infrastructure/gpu-infrastructure.md) |
| GPU time-slicing | Sharing GPU execution time across workloads, distinct from guaranteed memory isolation. | [gpu-infrastructure](../platform-infrastructure/gpu-infrastructure.md) |
| TTIT / ITL | Time between generated tokens, distinct from TTFT, the time to the first token. | [vllm](../platform-infrastructure/vllm.md) |

## Platform security and deployment

| Term | Meaning | Canonical topic |
|---|---|---|
| Authentication / Authorization | Verifying identity / deciding which actions that identity may perform. | [platform-security](../platform-infrastructure/platform-security.md) |
| Least privilege | Granting only the permissions needed for a task. | [platform-security](../platform-infrastructure/platform-security.md) |
| Role / RoleBinding | Kubernetes namespace permission rules / an object that assigns permissions to subjects. | [platform-security](../platform-infrastructure/platform-security.md) |
| ServiceAccount | A service identity used by a Kubernetes workload. Permissions are granted separately. | [platform-security](../platform-infrastructure/platform-security.md) |
| Secret rotation | Replacing credentials and moving consumers to the new values. | [platform-security](../platform-infrastructure/platform-security.md) |
| NetworkPolicy | Pod traffic allowance rules enforced by a supporting network plugin. | [platform-security](../platform-infrastructure/platform-security.md) |
| mTLS | TLS where client and server verify each other’s certificates. Authorization policy is still needed. | [platform-security](../platform-infrastructure/platform-security.md) |
| SBOM | An inventory of the components in software. | [platform-security](../platform-infrastructure/platform-security.md) |
| Image digest | A hash value identifying container image content. | [platform-security](../platform-infrastructure/platform-security.md) |
| Helm chart / Release | A package of Kubernetes resource templates / an installed instance managed by Helm. | [cicd-gitops](../platform-infrastructure/cicd-gitops.md) |
| GitOps / Drift | An operating approach that reconciles state declared in Git / a difference between desired and actual state. | [cicd-gitops](../platform-infrastructure/cicd-gitops.md) |
| Sync / Health | Agreement with desired declarations / a health assessment of resource state. Neither guarantees application quality. | [cicd-gitops](../platform-infrastructure/cicd-gitops.md) |
| Canary | A deployment approach that sends some traffic to a new version, checks it, then expands gradually. | [cicd-gitops](../platform-infrastructure/cicd-gitops.md) |
| Spare GPU capacity | Available resources beyond current serving that can fit a new model, KV Cache, parallel layout, and target load. | [cicd-gitops](../platform-infrastructure/cicd-gitops.md) |

## AWS cloud basics

| Term | Meaning | Canonical topic |
|---|---|---|
| Region / Availability Zone | An AWS geographic Region / a separate availability zone within it. An AZ is not necessarily one data center. | [foundations](../aws-cloud/foundations.md) |
| AWS Account | An AWS account boundary for resources, permissions, and billing, distinct from a Region. | [foundations](../aws-cloud/foundations.md) |
| AWS Organizations / OU | A service for managing multiple accounts / an organizational unit that groups accounts. | [foundations](../aws-cloud/foundations.md) |
| SCP | An Organizations policy that limits allowed permissions. It does not itself grant IAM permissions. | [foundations](../aws-cloud/foundations.md) |
| IAM Role / Temporary credentials | An AWS permission role that can be assumed under a trust policy / credentials with a limited lifetime. | [foundations](../aws-cloud/foundations.md) |
| VPC / Subnet | A virtual network in an AWS Region / an IP address range within an AZ. | [networking](../aws-cloud/networking.md) |
| CIDR | A notation that expresses an IP address range using an address and prefix length. | [networking](../aws-cloud/networking.md) |
| Route table / Longest prefix match | Traffic paths by destination / a rule selecting the most specific matching prefix. | [networking](../aws-cloud/networking.md) |
| Internet Gateway (IGW) | A gateway supporting communication between a VPC and the internet. Access also needs suitable addresses, routes, and security settings. | [networking](../aws-cloud/networking.md) |
| NAT Gateway | A managed gateway providing address translation. Distinguish public/private and zonal/regional configurations. | [networking](../aws-cloud/networking.md) |
| Security Group | Stateful network allowance rules for resources, distinct from a route table that supplies paths. | [networking](../aws-cloud/networking.md) |
| ALB / Target group | A load balancer distributing requests at the HTTP layer / a group of targets and health-check settings. | [compute](../aws-cloud/compute.md) |
| EC2 / AMI | An AWS virtual server / an OS and software image used to launch it. | [compute](../aws-cloud/compute.md) |
| Auto Scaling Group (ASG) | A configuration managing a group of EC2 instances using minimum, desired, and maximum capacity and scaling policies. | [compute](../aws-cloud/compute.md) |
| EBS / Snapshot | Block storage attached to services such as EC2 / a point-in-time volume copy used for recovery. | [storage-databases](../aws-cloud/storage-databases.md) |
| S3 Bucket / Object key | A management container for S3 objects / a key identifying an object within a bucket. | [storage-databases](../aws-cloud/storage-databases.md) |
| EFS / Mount target | A managed shared filesystem / a network endpoint for connecting to it from a VPC. | [storage-databases](../aws-cloud/storage-databases.md) |
| RDS Multi-AZ / Read replica | Availability placement that varies by configuration / a replicated database used for purposes such as read scaling. Check standby and reader roles by deployment type. | [storage-databases](../aws-cloud/storage-databases.md) |
| Aurora Writer / Reader endpoint | Endpoints for the current writer / reader connections. Connection distribution differs from query distribution. | [storage-databases](../aws-cloud/storage-databases.md) |
| ElastiCache Replica / Shard | A copy of the same data / a unit of data partitioning. Roles depend on engine and deployment mode. | [storage-databases](../aws-cloud/storage-databases.md) |
| ARN | A naming format that identifies an AWS resource. Components vary by service and resource. | [foundations](../aws-cloud/foundations.md) |
| NLB | A load balancer that distributes transport-layer traffic, such as TCP/UDP, to targets. | [compute](../aws-cloud/compute.md) |
| EKS / Managed node group | A managed Kubernetes service / a configuration where EKS helps manage EC2 worker node lifecycles. | [eks](../aws-cloud/eks.md) |
| Amazon VPC CNI | A plugin connecting EKS Pod networking to the VPC network. Address allocation depends on configuration. | [eks](../aws-cloud/eks.md) |
| AWS Load Balancer Controller | A controller managing AWS load balancer resources from Kubernetes declarations. | [eks](../aws-cloud/eks.md) |
| EBS / EFS CSI driver | Drivers connecting Kubernetes volume requests to AWS EBS/EFS storage. | [eks](../aws-cloud/eks.md) |
| ECR | An AWS registry storing container images in repositories. | [eks](../aws-cloud/eks.md) |
| EKS Pod Identity / IRSA | Ways to link Kubernetes ServiceAccounts to AWS IAM roles for workload permissions. Their implementation and support conditions differ. | [eks](../aws-cloud/eks.md) |
