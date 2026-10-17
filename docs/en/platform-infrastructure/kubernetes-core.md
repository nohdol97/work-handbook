---
id: platform-infrastructure-kubernetes-core
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - PIS-02-01
  - PIS-02-02
  - PIS-02-03
  - PIS-02-04
  - PIS-02-05
  - PIS-02-06
  - PIS-02-07
  - PIS-02-08
  - PIS-02-09
  - PIS-02-10
  - PIS-02-11
  - PIS-02-12
  - PIS-02-13
  - PIS-02-14
---

# Chapter 2. Kubernetes Core

The configurations and commands are study examples, not results of a deployment or failure test.

<!-- SOURCE CORE START -->

## 2.1 Kubernetes Architecture

Kubernetes works like a thermostat that keeps comparing desired and observed state. Declaring three Pods does not mean they are running or ready for requests; check status and events.

A definition of Kubernetes:

> A system that keeps containers across several servers in the desired state

This is its basic role.

Example:

```text
"Always run three nginx instances"
```

```text
Three running → normal
Only two running → create one more
```

### Overall Structure

```text
Kubernetes Cluster
├─ Control Plane
└─ Worker Node
```

### Control Plane

Core components:

```text
API Server
Scheduler
Controller Manager
etcd
```

#### API Server

The central entry point to Kubernetes.

```bash
kubectl get pods
```

At a high level:

```text
kubectl
↓
API Server
↓
Return cluster information
```

#### Scheduler

Decides which Worker Node will run a new Pod.

#### Controller Manager

Reconciles the current state with the desired state.

```text
Desired State = three Pods
Current State = two Pods
↓
Create one more Pod
```

#### etcd

A database that stores cluster state.

### Worker Node

A server where containers actually run.

Common components:

```text
kubelet
container runtime
kube-proxy
```

#### kubelet

The agent on each Node.

```text
API Server
↓
kubelet
↓
containerd
↓
Run the container
```

#### Container Runtime

Actually runs containers.

A common example is containerd.

#### kube-proxy

Configures networking to forward Service traffic.

### Overall Flow

```text
kubectl apply
↓
API Server
↓
Store state in etcd
↓
Scheduler selects a Node
↓
The kubelet on that Node
↓
container runtime
↓
Run the container
```

Controllers keep checking the desired state.

### Key Points

```text
Control Plane
= Manage the cluster

Worker Node
= Run the actual containers
```

Control Plane:

```text
API Server
→ Central entry point for requests

Scheduler
→ Decide which Node should host a Pod

Controller Manager
→ Maintain the desired state

etcd
→ Store cluster state
```

Worker:

```text
kubelet
→ Manage Pods on the Node

container runtime
→ Run containers

kube-proxy
→ Handle Service networking
```

The API Server, controllers, and Scheduler in the Control Plane and the kubelet on a Worker observe API state and act asynchronously. A successful `kubectl apply` does not mean a Pod is ready. If three replicas are desired and two are running, a controller works to add the missing one, but scheduling, image, or resource constraints can delay it.

---

## 2.2 Kubernetes API / Declarative Model

Usually, you declare the desired state in YAML and let Kubernetes reconcile it.

### Declarative Model

Example:

```yaml
replicas: 3
```

Meaning:

```text
Keep three Pods running
```

Kubernetes keeps reconciling the current state.

### Resource

An entity managed by Kubernetes.

Example:

```text
Pod
Deployment
Service
ConfigMap
Secret
```

### Object

A created instance of a resource is a Kubernetes object.

Example:

```text
The Deployment resource kind
↓
An actual Deployment object named my-api
```

### Basic YAML Structure

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: my-api

spec:
  replicas: 3
```

Key elements:

```text
apiVersion
kind
metadata
spec
```

### spec vs status

**spec**
- The desired state
- Desired State

**status**
- The current state
- Current State

Kubernetes keeps comparing the two.

```text
spec != status
→ Kubernetes reconciles them again
```

### How the Flow Works

```bash
kubectl apply -f deployment.yaml
```

```text
YAML
↓
API Server
↓
Create a Kubernetes object
↓
Store it in etcd
↓
Controller checks the spec
↓
Reconcile the actual state
```

**Declarative API: Resources, Objects, spec, and status**

Resources are API-managed entities such as Pods, Deployments, Services, ConfigMaps, and Secrets. A Deployment named `my-api` is an actual object of the Deployment kind. A declarative model says what state should exist rather than listing every execution step.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-api
spec:
  replicas: 3
```

This is an **incomplete teaching fragment** showing `apiVersion`, `kind`, `metadata`, and `spec`. It is not a complete deployable Deployment. Required fields such as a selector and Pod template are missing. `spec` describes desired state. `status` reports the state observed by the system. Controllers reconcile their goals with observations; they do not simply compare two JSON documents for equality.

With a complete manifest, the command form is `kubectl apply -f deployment.yaml`. The flow is YAML submission → object creation or update through the API Server → etcd storage → controller observation of spec → state reconciliation. An accepted API request does not mean the workload is ready.

---

## 2.3 Pod

A Pod is the smallest unit for running containers in Kubernetes.

> Pod = an execution unit that wraps one or more containers

### Usually One Container

```text
Pod
└─ Container
   └─ App
```

### Multi-container Pod

```text
Pod
├─ App Container
└─ Sidecar Container
```

Containers in the same Pod share networking and some resources.

They can communicate through `localhost`.

### Pod IP

A Pod usually has its own IP address.

Example:

```text
Pod A → 10.244.1.10
Pod B → 10.244.2.15
```

A Pod can be recreated with a different IP, so use a Service rather than depending directly on its IP.

### Pod Lifecycle

```text
Pending
↓
Running
↓
Succeeded / Failed
```

A Pod is a disposable execution unit.

### Restart Policy

```text
Always
OnFailure
Never
```

### Init Container

Runs before the main container.

```text
Init Container
↓
Prepare configuration files
↓
Run the main container
```

### Sidecar

A container that supports the main application.

Example:

```text
Pod
├─ App
└─ Log collector
```

A proxy is another example.

### Key Points

```text
Pod
= The smallest execution unit in Kubernetes

Inside a Pod,
there are one or more containers

A Pod can have its own IP

A Pod is not permanent
→ It can be recreated at any time

Init Container
→ Preparation before the main app

Sidecar
→ Support the main app
```

**Pods: The Container Execution Unit**

A Pod is the smallest deployable unit in Kubernetes. It groups one or more containers. A common layout is `Pod → Container → App`. Another is `Pod → App + Sidecar`. Containers in the same Pod share an IP and port space, so they can use `localhost`. They can share configured volumes. This does not mean all filesystems and resources are shared automatically.

Example addresses are Pod A `10.244.1.10` and Pod B `10.244.2.15`. Replacement Pods may have different IPs, so clients normally use a Service. A Pod is a replaceable execution unit, not a permanent server.

| Concept | Meaning and example |
| --- | --- |
| Lifecycle | The basic flow is `Pending → Running → Succeeded / Failed`. `Unknown` is a separate phase when state cannot be obtained |
| `Always` | The default Pod restart policy restarts a terminated container regardless of its exit result |
| `OnFailure` | Restarts a container after a failure exit |
| `Never` | Does not restart a container under that policy |
| Regular init container | Completes preparation, such as creating a config file, before the main app |
| Sidecar | Runs a helper such as a log collector or proxy alongside the app |

`Running` does not mean all containers are ready to accept requests. A container can restart within an existing Pod. A replacement created by a controller is a new Pod object. Status descriptions such as `CrashLoopBackOff` are not Pod phases. Distinguish ordinary init-container completion from Kubernetes' dedicated sidecar lifecycle support. [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/), [Sidecar containers](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/)

---

## 2.4 ReplicaSet / Deployment

### ReplicaSet

Role:

```text
Maintain N Pods
```

Example:

```text
replicas = 3
```

- If two remain, create one
- If four exist, remove one

### Deployment

Manages ReplicaSets and provides deployment, updates, and rollback.

```text
Deployment
   ↓
ReplicaSet
   ↓
Pod
```

Usually, use a Deployment rather than creating a ReplicaSet directly.

### Rolling Update

Example:

```text
v1 v1 v1
↓
v2 v1 v1
↓
v2 v2 v1
↓
v2 v2 v2
```

### Rollback

Return to the previous version if the new version has problems.

### Revision

Each deployment change creates history.

```text
Revision 1 → image v1
Revision 2 → image v2
Revision 3 → image v3
```

### Key Points

```text
ReplicaSet
= Maintain the Pod count

Deployment
= Manage ReplicaSets while
  providing deployment, updates, and rollback

Rolling Update
= Gradually replace Pods with a new version

Rollback
= Return to a previous version
```

**ReplicaSets and Deployments**

Read the replica-count, rolling-update, and revision examples in [source 2.4](#24-replicaset-deployment) with these conditions.

The source sequence illustrates gradual replacement. Actual concurrent Pod counts depend on rollout settings and readiness. The source's “a revision for each deployment change” means a **Pod template change that triggers a rollout**. Scaling alone does not create a revision. Rollback restores the Pod template from a retained revision. It does not undo external database changes. [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

---

## 2.5 StatefulSet

A StatefulSet is used:

> When each Pod needs to keep its own identity and storage

This is the use case it addresses.

### Difference from Deployment

Pods in a Deployment are interchangeable.

A StatefulSet is used:

```text
postgres-0
postgres-1
postgres-2
```

In this example, each Pod's identity can matter.

### Stable Identity

If `db-1` fails, it can be recreated as `db-1`, preserving its name and identity.

### Persistent Storage

Storage can be kept for each Pod.

```text
db-0 → Volume 0
db-1 → Volume 1
db-2 → Volume 2
```

### Ordered Startup

Pods can start and stop in order when needed.

```text
db-0
↓
db-1
↓
db-2
```

### Common Use Cases

```text
PostgreSQL
Kafka
Redis Cluster
ZooKeeper-family systems
```

Operators are often used alongside it in production.

### Key Points

```text
Deployment
= Pods are interchangeable
= Suits stateless applications

StatefulSet
= Preserve Pod identity
= Preserve storage for each Pod
= Support workloads where order matters
```

**StatefulSets: Stable Identity and Storage**

Deployment Pods are generally interchangeable and suit stateless apps. Use a StatefulSet when each Pod needs a stable name, network identity, and its own storage.

```text
postgres-0, postgres-1, postgres-2

db-0 → Volume 0
db-1 → Volume 1
db-2 → Volume 2

Ordered startup: db-0 → db-1 → db-2
```

A replacement for `db-1` can use the same ordinal name and associated storage. It is not the same Pod object, UID, or necessarily IP. PostgreSQL, Kafka, Redis Cluster, and ZooKeeper-family systems are learning examples. An Operator can add application-specific operations.

The default `OrderedReady` policy respects order and readiness. Pods are created in ascending ordinal order and terminated in reverse order during scale-down. This does not guarantee ordered shutdown when the StatefulSet resource itself is deleted. `Parallel` relaxes the ordering rules. A StatefulSet does not implement database replication, consensus, or backup by itself. You must provision storage and define application recovery separately. [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)

---

## 2.6 DaemonSet / Job / CronJob

### DaemonSet

> When you want to run one Pod on each Node

Use it for this purpose.

Common uses:
- Log collection agents
- Monitoring agents
- Network agents

### Job

> Work that runs once and finishes

Example:

```text
Data migration
Batch processing
One-time file conversion
Database initialization
```

### CronJob

> Run Jobs repeatedly at scheduled times

Example:

```text
Every day at 2 a.m. → backup
Every hour → aggregate statistics
```

### Key Points

```text
DaemonSet
= Run a Pod on each Node

Job
= One-time work

CronJob
= Scheduled recurring Jobs
```

**Choosing DaemonSet, Job, or CronJob**

| Resource | Purpose | Source examples |
| --- | --- | --- |
| DaemonSet | Runs a Pod on each eligible Node | Log, monitoring, and network agents |
| Job | Runs work and tracks completion | Data migration, batch processing, one-time file conversion, database initialization |
| CronJob | Creates Jobs on a schedule | A backup at 2 a.m. each day; hourly statistics |

“Each Node” means Nodes that meet placement rules, including selectors and taints. “One-time work” does not guarantee exactly-once execution. Jobs can retry failures. Scheduled work must also account for duplicate or missed runs. Review time zones, concurrency, retries, and idempotency against operational requirements. The schedules above are examples, not live settings. [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/), [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)

---

## 2.7 Service

A recreated Pod can have a different IP.

A Service is:

> A Kubernetes resource that provides a fixed access point in front of several Pods

### Basic Structure

```text
Client
  ↓
Service
  ↓
Pod A / Pod B / Pod C
```

### Label Selector

A Service usually finds target Pods with a label selector.

Example:

```text
Pod A: app=my-api
Pod B: app=my-api
Pod C: app=my-api
```

Service selector:

```text
app=my-api
```

### ClusterIP

Accessible only from inside the cluster.

### NodePort

Opens a specific Node port for external access.

```text
NodeIP:30080
      ↓
   Service
      ↓
     Pod
```

### LoadBalancer

Connects to a cloud load balancer.

```text
Internet
   ↓
Cloud Load Balancer
   ↓
Kubernetes Service
   ↓
Pods
```

### Headless Service

Allows discovery of individual Pod addresses without providing one virtual IP.

Common uses include StatefulSets, database clusters, and Kafka.

### Key Points

```text
Pod IPs can change.

Service
= A stable access point in front of Pods

ClusterIP
= For use inside the cluster

NodePort
= Access through a Node port

LoadBalancer
= Connect an external load balancer

Headless Service
= For cases that need access to individual Pods
```

**Services: An Access Point for Changing Pods**

A Service gives a stable abstraction for reaching a changing set of Pods. It usually selects Pods by labels. If Pods A, B, and C have `app=my-api` and the Service has that selector, they become target candidates. Readiness and other conditions affect actual delivery.

```text
Client → Service → Pod A / Pod B / Pod C
```

| Type | Purpose | Example and boundary |
| --- | --- | --- |
| ClusterIP | A virtual IP for access inside the cluster | Separates the access address from Pod replacement |
| NodePort | Access through a chosen port on Node addresses | `NodeIP:30080 → Service → Pod`; external reachability depends on routing, firewalls, and Node address settings |
| LoadBalancer | Integrates an external load balancer | `Internet → Cloud Load Balancer → Service → Pods`; a supporting implementation is required |
| Headless | Discovers endpoints without a virtual ClusterIP | `clusterIP: None`; useful for individual addresses in StatefulSets, database clusters, and Kafka |

A Service does not always provide one fixed virtual IP. Headless Services are an exception. A Kubernetes declaration also cannot create an external load balancer in every environment without a supporting implementation. [Service](https://kubernetes.io/docs/concepts/services-networking/service/)

---

## 2.8 Ingress / Gateway API

Ingress is:

> A routing layer that decides which Service receives external HTTP/HTTPS traffic

### Host Routing

```text
api.example.com → API Service
web.example.com → Web Service
```

### Path Routing

```text
example.com/api → API Service
example.com/web → Web Service
```

### Ingress Controller

An Ingress resource alone does not process actual traffic.

An implementation is needed to handle requests.

```text
Ingress Resource
↓
Ingress Controller
↓
Service
↓
Pod
```

### TLS Termination

HTTPS certificate handling can terminate at Ingress.

```text
Client
  ↓ HTTPS
Ingress
  ↓ HTTP or HTTPS
Service
  ↓
Pod
```

### Gateway API

A newer Kubernetes networking API that extends beyond Ingress.

At a high level:

```text
Gateway
↓
HTTPRoute
↓
Service
```

### Difference between Service and Ingress

```text
Service
= Group Pods behind one stable address

Ingress
= Decide which Service receives an external HTTP request
```

**Ingress and Gateway API: Routing HTTP Requests**

Services expose sets of Pods. Ingress defines which Service should receive an external HTTP/HTTPS request based on its host or path.

```text
api.example.com → API Service
web.example.com → Web Service
example.com/api → API Service
example.com/web → Web Service

Ingress Resource → Ingress Controller → Service → Pod
Client --HTTPS--> Ingress --HTTP or HTTPS--> Service → Pod
Gateway → HTTPRoute → Service
```

An Ingress resource alone does not process traffic. An Ingress controller must implement its rules. TLS termination ends the client's HTTPS connection at the edge. Whether the backend connection uses HTTP or HTTPS depends on separate configuration and implementation support.

Gateway API offers extensible APIs such as `GatewayClass`, `Gateway`, and `HTTPRoute` with clearer role and routing boundaries. It also needs installed APIs and a supporting controller. Official guidance states that Ingress API is frozen and recommends Gateway API for new development. This does not mean existing Ingress is about to be removed. Check feature support against the selected implementation and version. [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/), [Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/)

---

## 2.9 ConfigMap / Secret

Kubernetes can manage application settings separately instead of putting them directly in the image.

### ConfigMap

Ordinary, non-sensitive settings.

Example:

```text
APP_ENV=production
LOG_LEVEL=info
API_URL=http://backend
```

### Secret

Sensitive settings.

Example:

```text
DB_PASSWORD
API_KEY
TOKEN
```

A Kubernetes Secret is not a complete secure store by itself. Production systems can combine it with tools such as Vault or External Secrets.

### Ways to Pass Settings to a Pod

**Environment Variable**

```text
DB_HOST=postgres
DB_PASSWORD=***
```

**File Mount**

```text
ConfigMap
↓
/app/config.yaml
```

### Separate Images and Settings

```text
Container Image
= Application code

ConfigMap / Secret
= Environment-specific settings
```

The same image can be reused in dev, staging, and production.

**ConfigMaps and Secrets: Separate Configuration from Images**

| Item | Content | Example |
| --- | --- | --- |
| Container image | Application code and runtime artifacts | Reuse the same image in dev, staging, and production |
| ConfigMap | Non-sensitive environment settings | `APP_ENV=production`, `LOG_LEVEL=info`, `API_URL=http://backend` |
| Secret | Sensitive settings such as credentials | Key names `DB_PASSWORD`, `API_KEY`, `TOKEN`; no real values are shown |

Pass settings to a Pod through environment variables or file mounts. `DB_HOST=postgres` and `DB_PASSWORD=***` illustrate the shape. The asterisks are not a password. A ConfigMap can also appear as `/app/config.yaml`.

Base64 in a Secret is not encryption. Review API storage encryption at rest, least-privilege RBAC, workload access, log exposure, and rotation. Tools such as Vault or External Secrets can help, but do not guarantee complete security. Check the copy and access boundaries between external storage and Kubernetes Secrets. Do not paste real secrets into YAML, Git, or prompts. [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/), [Secret good practices](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)

---

## 2.10 Storage

Key elements:

```text
Volume
PV
PVC
StorageClass
```

### Volume

Storage attached to a Pod.

### PV

PersistentVolume.

> Actual storage that a Kubernetes cluster can use

Example:

```text
AWS EBS
NFS
Cloud Disk
```

### PVC

PersistentVolumeClaim.

A resource through which a Pod requests the storage it needs.

```text
Pod
 ↓
PVC
 ↓
PV
 ↓
Disk
```

```text
PV  = Actual storage
PVC = A storage request
```

### StorageClass

Defines which kind of storage to create.

Example:

```text
fast-ssd
standard
high-iops
```

### Dynamic Provisioning

A PVC request uses the StorageClass to create a real disk and PV automatically.

```text
Create a PVC
↓
Check the StorageClass
↓
Create the real disk automatically
↓
Create a PV
↓
Bind it to the PVC
```

### Connection to StatefulSet

```text
postgres-0
↓
PVC-0
↓
Disk-0

postgres-1
↓
PVC-1
↓
Disk-1
```

**Volumes, PVs, PVCs, and StorageClasses**

| Term | Role |
| --- | --- |
| Volume | Storage or a data source used by a Pod; not every volume is persistent |
| PersistentVolume, PV | A cluster storage resource representing backing storage such as AWS EBS, NFS, or a cloud disk |
| PersistentVolumeClaim, PVC | A resource requesting storage capacity and access conditions for a workload |
| StorageClass | Defines a provisioner and storage type or policy. Example names are `fast-ssd`, `standard`, and `high-iops` |

```text
Pod → PVC → PV → Disk
PVC request → StorageClass → Provisioner → Disk + PV → PVC binding
postgres-0 → PVC-0 → Disk-0
postgres-1 → PVC-1 → Disk-1
```

Dynamic provisioning creates storage and a PV when a suitable StorageClass and provisioner are available. The arrows show logical dependencies. Binding timing depends on policy. A PV is an API object representing storage, not the disk itself. Even with a separate PVC for each StatefulSet Pod, review access modes, topology, reclaim policy, and backup. [Persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/), [Dynamic provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/)

---

## 2.11 Scheduling

The Scheduler decides which Node will host a new Pod.

### Node Selector

Place the Pod only on Nodes with specific labels.

```yaml
nodeSelector:
  gpu: "true"
```

### Node Affinity

More flexible conditions than a Node Selector.

- `required` = must be met
- `preferred` = meet it if possible

### Pod Affinity

Place the Pod close to specific Pods.

### Pod Anti-Affinity

Place specific Pods apart.

Example:

```text
Pod A → Node 1
Pod B → Node 2
Pod C → Node 3
```

### Taint / Toleration

**Taint**
- The Node restricts placement: “Do not place ordinary Pods here”

**Toleration**
- The Pod permits placement: “I can enter even with that taint”

Often used for GPU Nodes.

### Topology Spread

Spread Pods evenly across Nodes or AZs.

### Key Differences

```text
Node Selector / Node Affinity
→ Where should this Pod go?

Taint / Toleration
→ Which Pods may enter this Node?

Pod Anti-Affinity
→ Place similar Pods apart
```

**Scheduling: Where Should a Pod Run?**

This teaching fragment belongs inside a Pod spec. `gpu: "true"` selects a label. It does not request an actual GPU allocation.

```yaml
nodeSelector:
  gpu: "true"
```

| Mechanism | Question and role |
| --- | --- |
| Node Selector | Does the Node have the required label? |
| Node Affinity | More flexible Node conditions: `required` is mandatory; `preferred` is a preference |
| Pod Affinity | Should the Pod run close to certain Pods in the same topology domain? |
| Pod Anti-Affinity | Should certain Pods run apart? Example: A→Node 1, B→Node 2, C→Node 3 |
| Taint | Which Pods should a Node restrict? Behavior depends on the effect |
| Toleration | Can this Pod tolerate a taint? It neither guarantees placement nor attracts the Pod to the Node |
| Topology Spread | How evenly should Pods be spread across Nodes or availability zones? |

Node Selector/Affinity asks where a Pod should go. Taints/tolerations control which Pods a Node permits. They can be combined for dedicated GPU Nodes. Strict anti-affinity or spread rules can prevent scheduling even when resources are available. [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/), [Taints and tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)

---

## 2.12 Resource Management

Key elements:

```text
request
limit
```

### Request

> The minimum resources this Pod needs

Example:

```yaml
resources:
  requests:
    cpu: "500m"
    memory: "1Gi"
```

The Scheduler uses this value to decide whether the Pod can fit.

### Limit

> The maximum resources a Pod can use

```yaml
resources:
  limits:
    cpu: "1"
    memory: "2Gi"
```

### CPU

```text
request = 0.5 CPU
limit   = 1 CPU
```

Exceeding the CPU limit:

```text
CPU throttling
```

### Memory

Exceeding the memory limit:

```text
OOM
↓
Container termination
↓
OOMKilled
```

### The Scheduler Uses Requests

If a Node has two CPUs left and the Pod requests three, it cannot be scheduled there.

### QoS Class

Common examples:

```text
Guaranteed
Burstable
BestEffort
```

A basic model:

```text
Guaranteed
→ Explicitly set requests and limits

Burstable
→ Set only some resources, or request < limit

BestEffort
→ No requests or limits
```

### Key Points

```text
Request
= Minimum required resources used by the Scheduler

Limit
= Maximum resources that can actually be used

CPU limit exceeded
→ throttling

Memory limit exceeded
→ Possible OOMKilled

QoS
= Resource protection level based on request and limit settings
```

**Requests, Limits, and QoS**

This is a teaching fragment for a container's `resources` field.

```yaml
resources:
  requests:
    cpu: "500m"
    memory: "1Gi"
  limits:
    cpu: "1"
    memory: "2Gi"
```

A CPU request of `500m` means `0.5 CPU`. A limit of `1` means `1 CPU`. The Scheduler uses requests for resource accounting. If a Node has **two CPUs left in request-based allocation** and a new Pod requests three, it cannot fit. Low measured CPU use is not enough. The source's “minimum required resource” refers to this reservation and scheduling model. A request is not a usage ceiling.

A CPU limit restricts CPU time and can cause throttling. A memory limit can lead to a kernel OOM kill, observed with a reason such as `OOMKilled`. CPU and memory enforcement differ. A brief memory-limit overrun does not always appear as an immediate termination. Check the active cgroup and kubelet settings as well. [Resource management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

The following basic model uses per-container CPU and memory settings.

| QoS | Classification criteria |
| --- | --- |
| Guaranteed | Every container has positive CPU and memory requests and limits, with request equal to limit for each resource |
| Burstable | Not Guaranteed, but at least one CPU or memory request or limit exists |
| BestEffort | No container has CPU or memory requests or limits |

Explicit requests and limits alone do not imply Guaranteed. The example has unequal values and is Burstable. With Pod-level resources in supported versions and configurations, Pod-level values also affect classification. Check the actual `status.qosClass`. QoS influences treatment under resource pressure. It is not a performance SLA or immunity from failure. [Pod QoS](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/)

---

## 2.13 Health Checks

Key elements:

```text
Liveness Probe
Readiness Probe
Startup Probe
```

### Liveness Probe

> Is this application alive?

Repeated failures can cause the container to restart.

```text
Liveness failure
→ Possible container restart
```

### Readiness Probe

> Is it ready to receive requests now?

On failure, remove the Pod from Service traffic targets without killing it.

```text
Readiness failure
→ The Pod stays alive
→ But requests are not sent to it
```

### Startup Probe

Used for applications that take a long time to start.

Example:

```text
vLLM
↓
Model Load
↓
Prepare GPU memory
↓
Ready after several minutes
```

Liveness checks can wait until startup finishes.

### Key Distinctions

```text
Startup Probe
= Has startup finished?

Readiness Probe
= Is it ready to receive requests?

Liveness Probe
= Is the application alive and working normally?
```

**Health Checks: Alive, Ready, and Started**

| Probe | Question | Meaning of failure |
| --- | --- | --- |
| Liveness | Can the app keep working correctly? | At the configured failure condition, the container is terminated and restarted according to its restart policy |
| Readiness | Can the app accept requests now? | Marks the Pod unready, removing it from the normal ready endpoints of a Service; probe failure alone does not restart the container |
| Startup | Has startup finished? | Liveness and readiness probes wait until it succeeds; reaching its failure threshold can trigger restart handling |

A hypothetical vLLM sequence is `start → model load → GPU memory preparation → Ready after several minutes`. Size the startup-probe budget from measurements so slow initialization is not mistaken for a liveness failure. “Several minutes” is not a fixed recommendation. A Running Pod may not be Ready. Restarting is not always the right response to a readiness failure. Also check exceptions such as a Service configured to publish unready endpoints. [Probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/)

---

## 2.14 Kubernetes Networking Basics

Key elements:

```text
Pod ↔ Pod
Pod ↔ Service
Pod ↔ DNS
```

### Pod-to-Pod

Each Pod can have its own IP.

```text
Pod A → 10.244.1.10
Pod B → 10.244.2.20
```

CNI implements the actual network connectivity.

### CNI

Container Network Interface.

> Assign Pod IPs and connect the network between Pods

Common examples:

```text
Calico
Cilium
```

### Pod-to-Service

Use a Service to communicate because Pod IPs can change.

```text
Client Pod
   ↓
Service
   ↓
Pod A
Pod B
Pod C
```

### Kubernetes DNS

Services receive DNS names.

Example:

```text
http://my-api:8080
```

CoreDNS resolves Service names to addresses.

### kube-proxy

A component traditionally responsible for network configuration that forwards Service traffic to Pods.

### Connecting the External Request Path

```text
Internet
   ↓
Ingress
   ↓
Service
   ↓
Pod
   ↓
Container
   ↓
Process
```

### Key Points

```text
Each Pod can have an IP.

CNI
= Handle Pod networking and IP addresses

Service
= Group changing Pods behind a fixed address

CoreDNS
= Resolve Service names to addresses

kube-proxy
= Implement Service-to-Pod traffic forwarding
```

**Networking Roles: Pods, Services, DNS, and CNI**

In the example, Pod A `10.244.1.10` talks to Pod B `10.244.2.20`. The Pod network implementation provides addresses and connectivity across Nodes. CNI stands for Container Network Interface. Implementations such as Calico and Cilium handle related networking roles. Distinguish the Kubernetes networking model from the features of a specific CNI plugin.

Service access follows `Client Pod → Service → Pod A/B/C`. A name such as `http://my-api:8080` works in the matching namespace and DNS search context. Normal Service DNS resolves the Service address. Headless Service DNS helps discover ready endpoint addresses. CoreDNS is a common cluster DNS implementation.

kube-proxy configures network rules that forward Service traffic to endpoints. This does not mean every packet passes through the kube-proxy process. Some network implementations replace kube-proxy with their own Service proxy. Treating CNI, DNS, and Service routing as the same component can lead to the wrong diagnosis. [Kubernetes networking](https://kubernetes.io/docs/concepts/services-networking/), [Service DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)

```mermaid
flowchart LR
    Internet --> Ingress[Ingress implementation]
    Ingress --> Service
    Service --> Pod
    Pod --> Container
    Container --> Process
```

The diagram shows the logical route from an external request to an application process. The actual packet path may go directly to Pod endpoints, depending on the Ingress and Service implementation.

For an interview, connect these ideas first: the API stores desired state; controllers reconcile it; the Scheduler places Pods; kubelet and the runtime execute them; a Service abstracts access; readiness describes the ability to accept requests. In a real incident, compare objects, events, state, logs, configuration, and measurements. Continue with [Linux and containers](linux-containers.md) and [Kubernetes operations](kubernetes-operations.md).

---

<!-- SOURCE CORE END -->

## Key points

Kubernetes desired and actual state can differ. Check Pod execution and service readiness separately.

## LLM in Practice: Separate Running from Ready for a Model Server

**Prompt:**

=== "한국어"

    ```text {.prompt}
    배포 뒤 Pod는 Running인데 Service 요청이 실패해. manifest diff, Pod 상태와 EndpointSlice를 보고 selector·port·readiness 중 어느 경계에서 실패했는지 검토해 줘. Running을 Ready로 간주하거나 구성을 변경하지 마.
    ```

=== "English"

    ```text {.prompt}
    After deployment, Pods are Running but Service requests fail. Use the manifest diff, Pod status, and EndpointSlice to locate a selector, port, or readiness failure. Do not treat Running as Ready or change the configuration.
    ```

**Key point:** Review comments for the Deployment/Service diff, the failing request boundary, and validation/recovery conditions for minimal fixes. It may blame every 503 on liveness or recommend restarting a Pod solely because readiness fails. Match selector-selected Pods to actual EndpointSlices and readiness, and distinguish the consequences of each failed probe. Each fix must state how startup time and request success will be checked.

Related: [Platform infrastructure guide](index.md) · [Handbook home](../index.md)
