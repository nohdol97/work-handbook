---
id: aws-cloud-foundations
status: studied
last_updated: 2026-10-04
last_reviewed: 2026-10-04
knowledge_ids:
  - AWSC-01-01
  - AWSC-01-02
  - AWSC-01-03
  - AWSC-01-04
---

# Chapter 1. AWS Foundation

These study notes preserve the supplied compact source’s order and examples in translation. They are not actual AWS operating results. **Reading guide:** The supplement below clarifies Multi-AZ and SCP scope, and conditions for the IAM policy example.

<!-- SOURCE CORE START -->

## 1.1 Region / Availability Zone

### Region
A large geographic area where AWS operates.

Example:
```text
Seoul Region
ap-northeast-2
```

Main considerations when choosing a Region:
- Distance from users / latency
- Data storage location and regulations
- AWS service availability in that Region
- Cost

### Availability Zone
An AZ is an independent failure domain within a Region.

```text
Seoul Region
├─ AZ A
├─ AZ B
├─ AZ C
└─ AZ D
```

Think of an AZ as an independent failure domain that can contain one or more data centers, rather than assuming it is exactly one data center.

### Multi-AZ
Placing a service in only one AZ can turn an AZ failure into a complete service outage.

```text
ALB
├─ AZ A → Application
└─ AZ B → Application
```

Distributing production resources across multiple AZs within one Region is therefore a basic pattern.

Key points:
```text
Region = A large geographic area
AZ = An independent failure domain within a Region
Basic operating pattern = Single Region + Multi-AZ
```

---

## 1.2 AWS Account / Organizations

An AWS Account is more than a login account: it is a major management boundary for resources, costs, and permissions.

```text
AWS Account
├─ EC2
├─ S3
├─ RDS
├─ EKS
└─ IAM
```

One account can use multiple Regions.

```text
Account = A management / permission / cost boundary
Region = A geographic placement area
```

In practice, accounts may be separated by environment or organizational needs.

```text
AWS Organization
├─ Dev Account
├─ Staging Account
├─ Prod Account
├─ Security Account
└─ Data Account
```

Benefits:
- Isolate operational mistakes
- Separate permissions
- Separate costs
- Strengthen security boundaries

### Root User
The account's highest-level user. The basic practice is to avoid it for everyday operations and use it only for initial setup or very limited tasks.

### AWS Organizations
Centrally manages multiple AWS accounts.

### OU
Organizational Unit. A logical group of accounts.

### SCP
Service Control Policy. Limits the maximum allowed permissions at organization/OU/account level.

```text
IAM Policy = Grant actual permissions
SCP = Limit the maximum permissions allowed by the organization
```

An SCP does not grant permissions by itself.

---

## 1.3 IAM User / Role / Policy

IAM = Identity and Access Management.

> Manages who can do what with which AWS resources.

Key points:
```text
IAM User
IAM Role
IAM Policy
```

### IAM User
A fixed user identity within an AWS account.

Enterprises often consider SSO / IAM Identity Center plus roles instead of directly giving people long-term access keys.

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

Key elements:
```text
Effect
Action
Resource
Condition
```

### IAM Role
A set of permissions assumed when needed.

```text
Identity
 ↓
AssumeRole
 ↓
IAM Role
 ↓
AWS Resource
```

Role-based authentication can use temporary credentials with an expiration time.

These generally include:
- Access Key
- Secret Key
- Session Token
- Expiration

### Trust Policy vs Permission Policy
```text
Trust Policy = Who can assume this role
Permission Policy = What can be done when assuming the role
```

### Least Privilege
Grant only the minimum permissions needed.

```text
Bad example
s3:* / Resource: *

Good example
s3:GetObject / specific bucket/*
```

### IAM and Kubernetes RBAC
```text
Pod → Kubernetes API = Kubernetes RBAC
Pod → S3 / SQS / Secrets Manager = AWS IAM
```

---

## 1.4 AWS Resource / ARN

Examples of AWS resources:
- EC2 Instance
- S3 Bucket
- IAM Role
- RDS Instance
- EKS Cluster

Many AWS resources are identified by an ARN (Amazon Resource Name).

Example:
```text
arn:aws:iam::123456789012:role/MyRole
```

---

<!-- SOURCE CORE END -->

## Supplement: conditions for 1.1–1.4

Official documentation checked: 2026-10-04.

**1.1 Multi-AZ:** Deploying across AZs still requires verification of application and data replication, failure routing, and remaining capacity. Multi-AZ alone does not guarantee recovery from a Region-wide outage.

**1.2 Accounts and SCPs:** SCPs require an organization with all features enabled and apply to member-account root users. They do not apply to management-account users and roles or service-linked roles. Prefer federation and temporary credentials for routine human access, and use MFA. [AWS SCP documentation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html), [IAM security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html).

**1.3–1.4 Policy example:** The source JSON is one statement, not a complete policy. Wrap it in `Statement` and specify the policy language `Version` in an actual policy document. `Condition` is optional. A Trust Policy that permits a principal to assume a role does not replace its Permission Policy's service permissions. Temporary credentials are also secrets and must be refreshed securely before expiration. The ARN account number `123456789012` is illustrative. [IAM policy elements](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html), [IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html).

## LLM practice: review permission boundaries for an S3 read role

- **Situation:** Distinguish the app's S3 read permissions from permission to assume its role.
- **Context to give the LLM:** An app role in a fictional member account must read only `example-study-bucket/reports/*`. The actual SCP and Trust Policy are unavailable.
- **Expected output:** A least-privilege statement draft and a table separating role-assumption and SCP checks from unknown assumptions.
- **How to validate:** Use `s3:GetObject` and an object ARN; do not claim that a Trust Policy or SCP automatically grants service permissions.
- **Cautions:** Do not include real account IDs, keys, or tokens. A human must review the generated policy before deployment.
- **What the LLM can get wrong:** It may claim that an SCP grants S3 permissions or that a Trust Policy alone permits object access.
- **Example prompt:** Use the two language tabs below.
- **Source connection:** 1.2–1.4, AWSC-01-02–04.

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 AWS 멤버 계정의 앱 역할이 example-study-bucket/reports/* 객체만 읽어야 한다. SCP와 Trust Policy는 미제공이다.
    [요청]
    최소 권한 IAM statement를 작성하고 역할 수임, 서비스 접근, SCP 제한을 구분해 검토하라.
    [출력]
    statement JSON과 확인 항목/근거/미확인 전제 표를 작성하라.
    [검증]
    s3:GetObject와 객체 ARN을 사용하라. SCP나 Trust Policy를 권한 부여의 충분조건으로 보지 말고 실제 계정 정보나 자격 증명을 요구하지 마라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    An app role in a fictional AWS member account must read only objects under example-study-bucket/reports/*. The SCP and Trust Policy are unavailable.
    [Task]
    Draft a least-privilege IAM statement and distinguish role assumption, service access, and SCP restrictions.
    [Output]
    Provide statement JSON and a table of checks, rationale, and unknown assumptions.
    [Checks]
    Use s3:GetObject and an object ARN. Do not treat an SCP or Trust Policy as sufficient to grant access, and do not request real account information or credentials.
    ```
