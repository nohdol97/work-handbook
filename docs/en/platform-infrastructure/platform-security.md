---
id: platform-infrastructure-platform-security
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - PIS3-10-01
  - PIS3-10-02
  - PIS3-10-03
  - PIS3-10-04
  - PIS3-10-05
  - PIS3-10-06
  - PIS3-10-07
  - PIS3-10-08
---

# Chapter 10. Platform Security

The configurations and commands are study examples, not results of a deployment or failure test.

Related: [Kubernetes core](kubernetes-core.md), [LiteLLM](litellm.md)

<!-- SOURCE CORE START -->

## 10.1 Authentication / Authorization

Platform security is more than one locked door. Check image provenance, runtime permissions, networking, service authentication, and secret access as separate layers.

The first distinction to make in security is between:

```text
Authentication
Authorization
```

These are different concepts.

### Authentication

Authentication means:

> Checking who someone is

This is identity verification.

Examples:

```text
User login
API Key
Service Account
SSO
```

Flow:

```text
Request
↓
Check identity
↓
Determine "who it is"
```

### Authorization

Authorization means:

> Deciding what that user is allowed to do

This is permission control.

Examples:

```text
User A
→ Can view models
→ Cannot modify deployments

Admin
→ Can modify deployments
→ Can manage secrets
```

In other words:

```text
Authentication
= Who are you?

Authorization
= What are you allowed to do?
```

### IAM

IAM = Identity and Access Management.

In simple terms:

> A system for centrally managing users, services, and permissions

This is the basic idea.

Examples:

```text
User
Team
Service
Role
Permission
```

In cloud environments, AWS IAM is a common example.

### Service Identity

Services have identities, just as people do.

Examples:

```text
Backend API
↓
PostgreSQL

LiteLLM
↓
vLLM

Application
↓
Kafka
```

In these cases:

```text
"Which service sent this request?"
```

This must be possible to check.

This is the idea of service identity.

### User Identity vs Service Identity

```text
User Identity
→ A person

Service Identity
→ Application / Pod / Service
```

Examples:

```text
Developer A
→ Permission to view Kubernetes resources

Backend Service
→ Permission to connect to PostgreSQL
```

### Least Privilege

An important security principle:

> Grant only the minimum permissions needed.

Bad example:

```text
Every service
→ Admin permissions
```

Good examples:

```text
Backend
→ Access only a specific database

LiteLLM
→ Read only specific secrets

Monitoring
→ Read-only permissions
```

### Key points

```text
Authentication
= Who are you?

Authorization
= What are you allowed to do?

IAM
= A system for managing users / services / permissions

Service Identity
= The identity of a service itself

Least Privilege
= Grant only the minimum permissions needed
```

**Scope of Kubernetes permissions**

A ClusterRole is a cluster-scoped **object**, but does not always grant permissions in every namespace. A RoleBinding grants its permissions within that namespace; a ClusterRoleBinding grants them cluster-wide. Kubernetes RBAC controls Kubernetes API permissions. Having a ServiceAccount does not itself configure application authentication or authorization for PostgreSQL, LiteLLM, or vLLM. [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

---

## 10.2 Kubernetes RBAC

RBAC = Role-Based Access Control.

> A way to control who can perform which operations in Kubernetes

Key concepts:

```text
Role
ClusterRole
RoleBinding
ServiceAccount
```

### Role

Defines permissions within a specific namespace.

Example:

```text
developer-role

pods
→ get
→ list

deployments
→ get
→ update
```

In other words:

> Role = A definition of permissions at namespace scope

### RoleBinding

Connects a role to an actual user or ServiceAccount.

```text
developer-role
↓
RoleBinding
↓
User A
```

### ClusterRole

Cluster-scoped permissions that are not limited to one namespace.

Examples:

```text
View pods across all namespaces
View nodes
View resources across the cluster
```

Distinction:

```text
Role
→ Namespace scope

ClusterRole
→ Cluster scope
```

### ServiceAccount

The identity a pod uses to call the Kubernetes API.

Example:

```text
Backup Pod
↓
Kubernetes API
↓
Read information about a specific PVC
```

Structure:

```text
Pod
↓
ServiceAccount
↓
RoleBinding
↓
Role
```

### Why ServiceAccounts matter

Bad example:

```text
Every pod
→ Cluster Admin
```

A single compromised pod could put the whole cluster at risk.

Good examples:

```text
Monitoring Pod
→ Read only

Deployment Controller
→ Modify only the required deployments

Backup Pod
→ Access only the required storage resources
```

### Key points

```text
Role
= A definition of permissions within a namespace

ClusterRole
= A definition of permissions at cluster scope

RoleBinding
= Connect permissions to a user / ServiceAccount

ServiceAccount
= A Kubernetes identity for a pod / application
```

---

## 10.3 Secrets

Secret management means:

> Safely managing sensitive values such as passwords, API keys, tokens, and certificates

Key concepts:

```text
Kubernetes Secret
External Secrets
Vault / Secret Manager
Secret Rotation
```

### Kubernetes Secret

Examples:

```text
DB_PASSWORD
API_KEY
JWT_SECRET
```

Pods can use:

```text
Environment Variable
or
File Mount
```

These are the available forms.

```text
Pod
↓
Kubernetes Secret
↓
DB_PASSWORD
```

### Kubernetes Secrets are not automatically completely safe

In particular, putting secret values directly in a manifest and uploading it to Git can lead to:

```text
Git Repository
↓
Secret exposure
```

This is a possible outcome.

Basic principle:

> Do not put secret values in Git as plaintext.

### External Secret Store

In production, the original secret values are often kept outside Kubernetes.

Examples:

```text
AWS Secrets Manager
HashiCorp Vault
Cloud Secret Manager
```

Structure:

```text
External Secret Store
↓
External Secrets Controller
↓
Kubernetes Secret
↓
Pod
```

### Vault

Systems such as Vault are dedicated to secret management.

Examples:

```text
Database Password
API Token
Certificate
```

Benefits:

```text
Access control
Audit
Secret Rotation
Dynamic credentials
```

For a basic understanding:

> Vault = A central vault for secrets

This is a useful starting point.

### Secret Rotation

Changing secret values periodically.

Example:

```text
DB Password v1
↓
Create a new password v2
↓
Change application configuration
↓
Retire v1
```

### Do not hardcode secrets in the application

Bad example:

```python
DB_PASSWORD = "password123"
```

A good structure:

```text
Application
↓
Environment Variable / Mounted Secret
↓
Secret Store
```

In other words:

```text
Code / Image
≠
Secret
```

### Connection to least privilege

```text
LiteLLM Pod
→ Only API keys related to LiteLLM

Backend Pod
→ Only the relevant database password

Kafka Client
→ Only Kafka credentials
```

### Key points

```text
Kubernetes Secret
= Deliver sensitive configuration to pods

Do not store secret values as plaintext in Git

External Secret Store
= Centrally manage actual secrets externally

Vault / Secrets Manager
= Systems dedicated to secret management

Secret Rotation
= Replace secret values periodically
```

**Secret storage, access, and rotation**

A Secret's base64 representation is not encryption. By default, Secrets in etcd are not encrypted without additional configuration. Configure encryption at rest and least privilege together. Even without Secret API read access, someone who can create a Pod using that Secret in the same namespace can expose its value. ServiceAccount API permissions alone therefore do not complete Secret isolation. [Secret security practices](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)

Secrets injected as environment variables do not update automatically in running containers. Ordinary Secret volume updates can be delayed, and `subPath` mounts do not update automatically. Verify rotation including application reloads or restarts and revocation of old credentials. Check these conditions even when an external store synchronizes to a Kubernetes Secret. The source's `password123` is an intentionally bad hardcoding example. [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

---

## 10.4 Network Security

Network security means:

> Restricting which services can communicate with which other services

Key concepts:

```text
NetworkPolicy
Firewall
Security Group
Service-to-Service Isolation
```

### Allowing everything by default is risky

Example:

```text
Frontend
Backend
PostgreSQL
Redis
Kafka
```

A good structure:

```text
Frontend
→ Access only the backend

Backend
→ Access PostgreSQL / Redis

Frontend
→ No direct access to PostgreSQL
```

### NetworkPolicy

A Kubernetes resource that restricts communication between pods.

Example:

```text
Backend Pod
↓
PostgreSQL Pod
```

Allow only this connection and block other pods.

In other words:

> NetworkPolicy = Network access control at pod level

### Ingress / Egress

Ingress:

```text
Client
→ Pod
```

Traffic entering a pod.

Egress:

```text
Pod
→ PostgreSQL
```

Traffic leaving a pod.

Example:

```text
LiteLLM
→ Allow vLLM
→ Restrict direct internet access
```

### Firewall / Security Group

Usually at node or cloud-network level.

```text
Internet
↓
Firewall / Security Group
↓
Load Balancer
↓
Kubernetes
```

Distinction:

```text
Security Group / Firewall
→ Network / server level

NetworkPolicy
→ Kubernetes pod level
```

### Service-to-Service Isolation

AI platform example:

```text
User
↓
LiteLLM
↓
vLLM
```

Allow only this path.

Also:

```text
LiteLLM
→ Allow Redis
→ Allow PostgreSQL

vLLM
→ Redis access is unnecessary
→ Block
```

### Default Deny

```text
Deny by default
→ Allow only required communication
```

Example:

```text
Block all pod communication
↓
Allow Backend → PostgreSQL
Allow LiteLLM → vLLM
Allow Monitoring → Metrics Port
```

### Connection to the CNI

```text
NetworkPolicy
↓
Calico / Cilium
↓
Actually allow / block packets
```

In other words:

```text
Kubernetes
→ Define the policy

CNI
→ Enforce the policy
```

### Supplement: ingress/egress between LiteLLM and vLLM

If LiteLLM initiates a connection to vLLM:

```text
LiteLLM Pod
   ↓
 egress
   ↓
vLLM Pod
 ingress
```

In other words:

```text
On the LiteLLM side
→ Allow egress to vLLM

On the vLLM side
→ Allow ingress from LiteLLM
```

Once a connection is allowed, response packets for that connection can travel back.

A useful way to remember:

```text
A → B

From A’s perspective
= Egress

From B’s perspective
= Ingress
```

### Key points

```text
NetworkPolicy
= Control communication between pods

Ingress
= Incoming traffic

Egress
= Outgoing traffic

Firewall / Security Group
= Network / node-level controls

Default Deny
= Deny by default, then allow only required communication
```

**Check NetworkPolicy enforcement conditions**

A network plugin that enforces NetworkPolicy is required. A direction not selected by policies is not isolated by default. Allow rules form a union; they are not sequential firewall deny rules. Communication must be allowed by both an isolated source's egress and an isolated destination's ingress policies; reply traffic for an allowed connection is implicitly allowed. Review required dependencies such as DNS when introducing default deny. These policies alone do not provide TLS encryption or application authorization. [Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

---

## 10.5 TLS / mTLS

TLS:

> A technology that encrypts data traveling over a network

Key concepts:

```text
TLS
Certificate
mTLS
Certificate Rotation
```

### Why TLS is needed

Example:

```text
LiteLLM
↓ HTTP
vLLM
```

LLM requests may contain:

```text
Prompt
Internal company data
Source Code
API information
```

These are examples of possible contents.

Using TLS:

```text
LiteLLM
↓ HTTPS / Encryption
vLLM
```

### Certificate

Used in TLS to verify the server’s identity.

```text
Client
↓
"Is this really the server I intended to contact?"
↓
Verify the server certificate
```

### Ordinary TLS

Usually:

```text
Client
→ Verify the server certificate
```

User authentication is separate:

```text
API Key
JWT
SSO
```

These are examples of authentication methods.

### mTLS

mTLS = Mutual TLS.

The server and client verify each other’s certificates.

```text
LiteLLM
Certificate
   ↕
Certificate
vLLM
```

In other words:

```text
LiteLLM
→ "Are you really vLLM?"

vLLM
→ "Are you really an allowed LiteLLM service?"
```

### mTLS and service identity

A certificate can be issued to each service to prove its service identity.

```text
LiteLLM Certificate
vLLM Certificate
Backend Certificate
```

### Difference between NetworkPolicy and TLS

```text
NetworkPolicy
= Who can connect

TLS
= Encrypt the contents of an established connection

mTLS
= Encryption + Mutual verification of service identity
```

### Certificate Rotation

```text
Certificate v1
↓
Nearing expiry
↓
Issue certificate v2
↓
Replace the certificate used by the service
↓
Retire v1
```

### Key points

```text
TLS
= Communication encryption + Server identity verification

Certificate
= Prove a service’s identity

mTLS
= The client and server verify each other’s certificates

Certificate Rotation
= Renew certificates periodically
```

**Distinguish mTLS authentication from service authorization**

mTLS verifies peer identity according to certificates and trust configuration. A separate authorization policy determines whether that identity may perform a service operation. Do not read the source's “Are you really an allowed LiteLLM service?” as meaning that installing certificates also settles every access permission. Check certificate renewal and whether renewed certificates actually take effect. [Istio authentication and authorization](https://istio.io/latest/docs/concepts/security/)

---

## 10.6 Container Security

Main objective:

> Limit the damage to the host or other containers even if a container is compromised

Key concepts:

```text
Non-root
Linux Capabilities
Seccomp
Read-only Filesystem
```

### Non-root

Bad example:

```text
Container Process
→ root
```

Where possible:

```text
Container Process
→ A regular user
```

Kubernetes example:

```yaml
securityContext:
  runAsNonRoot: true
```

### Linux Capabilities

The concept of splitting root privileges into specific capabilities.

Principle:

```text
Minimize default capabilities
↓
Add only what is truly needed
```

### Privileged Container

A container with very powerful host privileges.

```text
Container
↓
Access host devices / kernel features
```

Avoid this for ordinary apps; use it only as an exception for specialized agents and similar cases.

### Seccomp

Restrict the Linux syscalls a process can use.

```text
Container Process
↓
System Call
↓
Seccomp Policy
├─ Allow
└─ Block
```

### Read-only Filesystem

Set the container root filesystem to read-only.

```text
/app
/bin
/etc
→ Cannot modify
```

Only the required writable paths:

```text
/tmp
/data
```

Allow these separately through volumes.

### Kubernetes securityContext

Where Linux security privileges for pods/containers are configured.

Example:

```yaml
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
```

### Key points

```text
Non-root
= Do not run as root

Linux Capabilities
= Allow only the required Linux privileges

Privileged Container
= Very powerful privileges
= Avoid for ordinary apps

Seccomp
= Restrict available syscalls

Read-only Filesystem
= Limit changes inside the container
```

**securityContext location and filesystem scope**

The source's two-field example is not a complete Pod manifest. `readOnlyRootFilesystem` is a container field under `.spec.containers[*].securityContext`, not the Pod-level `.spec.securityContext`. Making the root filesystem read-only does not remove write permissions on separate mounts. `runAsNonRoot` does not automatically choose an arbitrary non-root UID; also check the image and execution UID. [Kubernetes security context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

---

## 10.7 Supply Chain Security

Supply Chain Security:

> Checking the security of the container images and libraries being deployed

Key concepts:

```text
Image Scanning
SBOM
Image Signing
Registry Security
```

### Image Scanning

```text
my-app:v1
↓
Image Scanner
↓
OpenSSL vulnerability found
```

This can be included in CI.

```text
Code
↓
Image Build
↓
Security Scan
↓
Registry Push
```

### SBOM

SBOM = Software Bill of Materials.

> An inventory of the components included in software

Example:

```text
Application Image
├─ Ubuntu
├─ Python
├─ FastAPI
├─ OpenSSL
├─ requests
└─ Other libraries
```

### Image Signing

```text
Image Build
↓
Signing
↓
Signed Image
↓
Registry
```

The signature can be verified at deployment time.

### Tag vs Digest

```text
Tag
→ A human-readable version
→ Can change

Digest
→ A fixed identifier for specific image content
```

### Registry Security

Things to manage:

```text
Who can push?
Who can pull?
Who can delete?
Vulnerability scanning?
```

A good structure:

```text
Developer
→ Cannot modify production images directly

CI Pipeline
→ Push after verification

Production
→ Pull only from approved registries
```

### Connection to the full CI/CD flow

```text
Code
↓
Build
↓
Test
↓
Container Image
↓
Image Scan
↓
SBOM
↓
Image Signing
↓
Registry
↓
Kubernetes Deploy
```

**A signature is not a safety verdict**

Image signature verification must check a trusted key or signer identity and issuer, together with the digest that will actually be deployed. A signature or pinned digest alone does not establish the absence of vulnerabilities. An SBOM is an inventory, and a scan reports results within its detection coverage. This distinction is a reasoning aid for reading the source's supply-chain stages together. [Sigstore signature verification](https://docs.sigstore.dev/cosign/verifying/verify/)

---

## 10.8 Multi-tenant Security

Multi-tenancy:

> A structure in which multiple teams or services share one platform / Kubernetes cluster

Key concepts:

```text
Namespace Isolation
RBAC
Network Isolation
Secret Isolation
Resource Isolation
```

### Namespace Isolation

Example:

```text
namespace: team-a
namespace: team-b
namespace: team-c
```

A namespace is a basic unit of logical isolation.

But a namespace alone does not provide complete security isolation.

### RBAC Isolation

```text
Developer A
→ Access only team-a

Developer B
→ Access only team-b
```

### Network Isolation

```text
team-a Pod
→ No access to the team-b database
```

Deny by default, then allow only required communication.

### Secret Isolation

Restrict each ServiceAccount to accessing only its own secrets.

### Resource Isolation

To keep one team from monopolizing CPU/memory/GPUs:

```text
ResourceQuota
LimitRange
GPU Quota
```

Use these controls.

### Namespaces are not only for teams

Criteria for namespace design:

```text
Service
Team
Environment
Security Boundary
Lifecycle
```

A common practical pattern:

```text
<service>-<environment>
```

Examples:

```text
payment-dev
payment-staging
payment-prod

agent-platform-dev
agent-platform-prod
```

Within each namespace:

```text
frontend
backend
worker
ConfigMap
Secret
Service
```

These resources can be placed together.

### Service-based example

```text
my-service-dev
├─ frontend
├─ backend
├─ worker
└─ postgres

my-service-prod
├─ frontend
├─ backend
├─ worker
└─ postgres
```

### Team + environment pattern

```text
team-a-dev
team-a-prod
team-b-dev
team-b-prod
```

Multiple services can be placed inside.

### The database need not be in the same namespace

Example:

```text
shopping-prod
├─ frontend
├─ backend
└─ worker

database-prod
└─ PostgreSQL
```

A managed database can also be used.

### Separating development and production

```text
myapp-dev
myapp-staging
myapp-prod
```

When stronger isolation is needed:

```text
Dev Cluster
Prod Cluster
```

The clusters themselves may be separated.

### Chapter 10 summary

```text
Identity
↓
RBAC
↓
Secret
↓
NetworkPolicy
↓
TLS / mTLS
↓
Container Hardening
↓
Supply Chain Security
↓
Multi-tenant Isolation
```

**Limits of namespace separation**

A namespace is a logical boundary, not a guarantee of an independent security sandbox. Review RBAC, networking, Pod security, and node or cluster separation according to mutual trust. Quotas limit resource consumption; they do not guarantee performance or GPU fault isolation. [Kubernetes multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/), [GPU infrastructure](gpu-infrastructure.md)

---

<!-- SOURCE CORE END -->

## Key points

Platform security checks image supply chains, runtime permissions, networks, and tenant boundaries together.

## LLM in Practice
### Review service security boundaries without exposing Secrets

**Prompt:**

=== "한국어"

    ```text {.prompt}
    서비스 배포 PR의 Kubernetes 권한, Secret 주입, 네트워크와 서비스 인증을 검토해 줘. 변경 diff에서 과도한 접근이나 회전 실패 위험을 찾아 최소 수정안을 제안해 줘. 실제 Secret 값을 요구하지 말고 정책도 적용하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review Kubernetes permissions, Secret injection, networking, and service authentication in this deployment PR. Find excessive access and secret-rotation risks in the diff, then suggest minimal changes. Do not request real secret values or apply policies.
    ```

**Key point:** Exposure paths for permissions, Secrets, and communication by manifest field, minimal fixes, and an allow/deny/rotation test matrix. It may treat the presence of a policy as successful enforcement or assume denying Secret reads also blocks Pod mounts. Check binding scope, Secret access through Pods, both NetworkPolicy directions, and mTLS authorization against actual settings. Test conditions must retain legitimate DNS dependencies and cover Secret updates.
