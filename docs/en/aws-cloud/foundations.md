---
id: aws-cloud-foundations
status: studied
last_updated: 2026-10-03
last_reviewed: 2026-10-03
knowledge_ids:
  - AWS-01-01
  - AWS-01-02
  - AWS-01-03
---

# Chapter 1. AWS foundations

These are supplied AWS Cloud Basic study notes. The numbering, order, examples, and intervening supplements are preserved in translation. They are not a record of creating AWS resources or applying policies or routes. **Reading guide:** The **Supplements and corrections by source section** explain AZ identification, SCP scope, and IAM policy and temporary credential conditions.

<!-- SOURCE CORE START -->

## 1.1 Region / Availability Zone

Region and Availability Zone (AZ) are the first concepts to understand in AWS.

- **Region**: A large geographic area operated by AWS
- **AZ**: A separate failure domain within a Region

Seoul Region example:

```text
Region
ap-northeast-2
```

It contains multiple AZs.

```text
ap-northeast-2a
ap-northeast-2b
ap-northeast-2c
ap-northeast-2d
```

Structure:

```text
AWS
│
├─ Seoul Region (ap-northeast-2)
│   ├─ AZ A
│   ├─ AZ B
│   ├─ AZ C
│   └─ AZ D
│
├─ Tokyo Region
└─ Virginia Region
```

### Why are Regions needed?

Choose a Region based on distance between users and servers, data regulations, service availability, and cost.

For example, the Seoul Region is generally considered for a service targeting users in Korea.

```text
Seoul Region
ap-northeast-2
```

Main criteria for choosing a Region:

- Distance from users
- Data storage location / regulations
- Service availability
- Cost

### Why are AZs needed?

If every service is placed in one data center, a failure there can stop the entire service.

AWS therefore divides a Region into multiple AZs to separate failure domains.

```text
Seoul Region
│
├─ AZ A
│   └─ Server A
├─ AZ B
│   └─ Server B
└─ AZ C
    └─ Server C
```

If one AZ fails, other AZs can continue serving users.

This is called a **Multi-AZ Architecture**.

### Difference between Regions and AZs

| Concept | Meaning |
|---|---|
| Region | A large geographic area where AWS operates |
| AZ | An independent failure domain within a Region |
| Example Region | `ap-northeast-2` |
| Example AZ | `ap-northeast-2a` |
| Main purpose | Choose a geographic location |
| Main purpose of an AZ | High availability |

Important:

```text
Handling a Region failure
≠
Handling an AZ failure
```

Multi-AZ handles AZ failures within a Region.

### Practical placement

A poor structure:

```text
AZ A

EC2
 ↓
EC2
 ↓
Database
```

An AZ A failure causes a complete service outage.

A common structure:

```text
              Internet
                 │
                ALB
              /     \
           AZ A      AZ B
            │          │
          EC2        EC2
             \        /
              \      /
               RDS
            Multi-AZ
```

### Connection to Kubernetes

```text
EKS Cluster

AZ A
 └ Node

AZ B
 └ Node

AZ C
 └ Node
```

Kubernetes high availability can therefore be built on AWS Multi-AZ infrastructure.

### Does an AZ equal one data center?

Not exactly.

Think of an AZ as an **independent failure domain** that can contain one or more physical data centers.

Key points:

```text
Region
= A large geographic area

AZ
= An independent failure domain within a Region

Practical baseline
= Single Region + Multi-AZ
```

---

## 1.2 AWS Account

An AWS Account is more than a login account: it is a **major management boundary for resources, costs, and permissions**.

```text
AWS Account
│
├─ EC2
├─ S3
├─ RDS
├─ EKS
└─ IAM
```

### Separate environments by account

Dev and Prod can share one account, but this can increase the risk of operational mistakes.

```text
AWS Organization
│
├─ Dev Account
├─ Staging Account
└─ Production Account
```

In other words:

> Account separation = Isolation at a broad level

### Difference between accounts and Regions

One AWS Account can use multiple Regions.

```text
AWS Account
│
├─ Seoul Region
├─ Tokyo Region
└─ Virginia Region
```

Summary:

```text
Account
= A management / permission / cost boundary

Region
= A geographic placement area
```

### Account ID

Each AWS Account has a unique 12-digit account ID.

Example:

```text
123456789012
```

ARN example:

```text
arn:aws:iam::123456789012:role/MyRole
```

### Root User

The root user is the account's highest-level user.

```text
AWS Account
   │
 Root User
```

The standard practice is to avoid using the root user for everyday operations.

```text
Root User
→ Initial setup / very limited tasks

IAM / SSO
→ Everyday operations
```

### IAM users and accounts

```text
AWS Account
│
├─ IAM User A
├─ IAM User B
└─ IAM Role
```

Analogy:

```text
Company = AWS Account
Employee account = IAM User
Job role / temporary permissions = IAM Role
```

### AWS Organizations

Multiple accounts can be managed centrally.

```text
AWS Organizations
│
├─ Management Account
├─ Dev Account
├─ Prod Account
├─ Security Account
└─ Data Account
```

### OU

Organizational Unit.

A group or folder of accounts.

```text
AWS Organization
│
├─ Production OU
│   ├─ AI Platform Prod
│   └─ Data Platform Prod
│
└─ Non-Production OU
    ├─ Dev
    └─ Test
```

### SCP

Service Control Policy.

It limits the **maximum scope** of permissions available to accounts/OUs at organization level.

```text
IAM Policy
= Grant actual permissions

SCP
= Limit the maximum permissions allowed by the organization
```

An SCP does not grant permissions by itself.

### Separate costs

Costs become easier to view by account.

```text
Dev Account       $1,000
Prod Account      $10,000
Data Account      $5,000
AI Account        $20,000
```

### Summary

```text
AWS Organization
        │
      Account
        │
      Region
        │
        AZ
        │
     Resources
```

More precisely, one account can use multiple Regions.

Key points:

- AWS Account = A major management boundary for resources / costs / permissions
- Root User = The account's highest-level user
- AWS Organizations = Central management of multiple accounts
- Dev / Prod and other environments are often separated by account in practice

---

## 1.3 IAM basics

IAM = **Identity and Access Management**

> A system that manages who can do what with which AWS resources

Key elements:

```text
IAM User
IAM Role
IAM Policy
```

Meaning:

```text
User
= A person or fixed user

Role
= Permissions assumed when needed

Policy
= Define which actions to allow or deny
```

### IAM User

A user within an AWS Account.

In enterprise environments, SSO / IAM Identity Center plus roles are more often considered than giving people long-term access keys.

### IAM Policy

Permission rules.

Example:

```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-bucket/*"
}
```

Meaning:

- Effect = Allow
- Action = Read S3 objects
- Resource = Objects inside a specific bucket

Key fields:

```text
Effect
Action
Resource
Condition
```

### IAM Role

A role is a **set of permissions**, not an account tied to a particular user.

```text
User
  ↓
Assume Role
  ↓
AdminRole
  ↓
Administrator permissions
```

### Why are roles needed?

A bad structure:

```text
EC2
└─ Store access keys
```

A good structure:

```text
EC2
 ↓
IAM Role
 ↓
S3
```

There is no need to store fixed access keys in the application.

### Temporary Credential

Using a role allows you to obtain temporary credentials.

```text
Application
    ↓
IAM Role
    ↓
Temporary Credential
    ↓
AWS API
```

These generally include:

- Access Key
- Secret Key
- Session Token
- Expiration

### EC2 + IAM Role

```text
EC2
 │
 └─ IAM Role
      │
      └─ Policy
           └─ s3:GetObject
```

An application can use role-based temporary credentials through the AWS SDK.

### What about EKS?

If a Pod accesses S3:

```text
Pod
 ↓
IAM Role
 ↓
S3
```

IRSA or EKS Pod Identity can be used for this.

### Trust Policy

There are two perspectives on a role.

```text
Role
│
├─ Permission Policy
│    └─ What this role can do
│
└─ Trust Policy
     └─ Who can assume this role
```

### Least Privilege

Grant only the minimum permissions required.

Bad example:

```text
s3:*
Resource: *
```

Good example:

```text
s3:GetObject
Resource: my-bucket/*
```

### Allow and Deny

Access is denied by default when no permission is granted.

An explicit Deny takes precedence over an Allow.

```text
Explicit Deny
> Allow
```

### Permission structures for people and services

People:

```text
Developer
    ↓
SSO / Identity Center
    ↓
IAM Role
    ↓
AWS Resource
```

EC2:

```text
EC2
 ↓
IAM Role
 ↓
S3 / DynamoDB / etc
```

EKS Pod:

```text
Pod
 ↓
Pod Identity / IRSA
 ↓
IAM Role
 ↓
AWS Resource
```

### IAM and Kubernetes RBAC

```text
Pod → Access the Kubernetes API
= Kubernetes RBAC

Pod → Access S3
= AWS IAM
```

In other words:

```text
Permissions inside Kubernetes
= RBAC

Permissions for AWS resources
= IAM
```

---

<!-- SOURCE CORE END -->

## Supplements and corrections by source section

Official documentation checked on 2026-10-03. These are conditions to check when applying the source, not results of creating accounts, granting permissions, or testing failures.

### 1.1: AZ names and availability scope

Do not compare physical locations across accounts using only the letter in an AZ name. Some older Regions and accounts retain differences in name-to-AZ mappings; use AZ IDs for cross-account comparisons. Do not generalize that names map differently in every Region either. [AWS AZ IDs](https://docs.aws.amazon.com/global-infrastructure/latest/regions/az-ids.html)

The source's Multi-AZ diagrams are design examples. Placing resources in another AZ does not automatically verify application replication, routing, data failover, or remaining capacity. Single Region plus Multi-AZ is distinct from a recovery strategy for a whole-Region outage. These are design-review criteria derived from the source's distinction between failure domains.

### 1.2: Actual scope of root access and SCPs

Use federation and temporary credentials for everyday work, restrict root access, and protect it with MFA. Do not interpret “initial setup” as running every provisioning task as root. [AWS IAM security practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

SCPs do not grant permissions. They restrict member-account root users, but do not apply to management-account users or roles, or to service-linked roles. They require Organizations with all features enabled. The source's hierarchy also does not mean every resource belongs to an AZ. Services such as IAM have global scope, so check scope per resource. [AWS SCPs](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)

### 1.3: Policy examples and role credentials

The source's JSON is a **Statement fragment** illustrating `Effect`, `Action`, and `Resource`, not a complete policy document. Put it inside `Statement` and check the appropriate policy language `Version` and other elements. `Condition` is optional. `my-bucket/*` illustrates object scope, which differs from a bucket-level action's ARN. [IAM JSON policy elements](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html)

A role is an IAM identity that can be assumed, not a policy itself. Review trust and permission policies together, and check EC2 instance profiles, Pod Identity/IRSA, and SDK credential-provider configuration. Temporary credentials are still secrets and require expiry and refresh handling. Removing long-term keys alone does not establish least privilege. [AWS IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)

Account ID `123456789012`, the ARN and bucket names, and costs are illustrative. They are not actual accounts, bills, or measurements. API communication may fail without a [network path](networking.md) even when IAM allows it; successful connectivity does not establish IAM authorization either.

## LLM in Practice

### Review account, failure-domain, and permission boundaries separately

**Situation:** A hypothetical Dev/Prod service reads S3 objects from EC2. Connect this with [platform security](../platform-infrastructure/platform-security.md) and review the existing design's boundaries first.

**Context to Give the LLM:** Sanitized account/Region/AZ-ID placement, service failure requirements, role trust and permission policy summaries, and SDK credential handling. Exclude actual account identifiers, keys, and tokens.

**Example Prompt:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 Dev/Prod 서비스는 EC2에서 지정 S3 객체를 읽는다.
    배치와 장애 요구: [비식별 Account·Region·AZ ID·복구 조건]
    Role trust/permission policy와 SDK 자격 증명 방식: [비식별 요약]
    [요청]
    현재 구성을 먼저 검토하고 관측·가정·가설·누락 증거를 구분하라.
    계정 격리, AZ 장애, Region 장애, IAM 권한을 각각 평가하라.
    [출력]
    경계 / 현재 근거 / 실패 가능성 / 다음 확인 표를 작성하라.
    Trust와 permission policy를 구분하고 최소 권한 후보를 설명하라.
    [검증]
    Multi-AZ나 Role 사용만으로 복구·접근 성공을 단정하지 말라.
    공식 문서와 실제 비식별 구성으로 사람이 검증할 항목을 제시하라.
    키·토큰을 요구하거나 정책·계정을 변경하지 말라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    A hypothetical Dev/Prod service reads specified S3 objects from EC2.
    Placement and failure requirements: [sanitized accounts, Regions, AZ IDs, recovery conditions]
    Role trust/permission policies and SDK credential handling: [sanitized summary]
    [Task]
    Review the current design first; separate observations, assumptions, hypotheses, and missing evidence.
    Assess account isolation, AZ failure, Region failure, and IAM permissions separately.
    [Output]
    Create a table: boundary / current evidence / possible failure / next check.
    Distinguish trust from permission policies and explain least-privilege candidates.
    [Checks]
    Do not infer successful recovery or access from Multi-AZ or role use alone.
    List checks for a person to make against official docs and actual sanitized configuration.
    Do not request keys or tokens or change policies or accounts.
    ```

**Expected Output:** A review table separating failure domains from permission boundaries, with evidence needed to verify behavior and unresolved conditions.

**What the LLM Can Get Wrong:** It may treat Multi-AZ as Region-disaster recovery, view an SCP as a permission grant, or infer S3 read access from a trust policy alone.

**How to Validate:** A person checks AZ IDs, policy evaluation, the actual credential provider, and network configuration. Run any required tests separately in an approved isolated environment. This is an authored scenario, not a record of actual model responses or AWS operations.
