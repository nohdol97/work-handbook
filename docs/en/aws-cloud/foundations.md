---
id: aws-cloud-foundations
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - AWSC-01-01
  - AWSC-01-02
  - AWSC-01-03
  - AWSC-01-04
---

# Chapter 1. AWS Foundation

The configurations are study examples, not results from a running AWS environment.

<!-- SOURCE CORE START -->

## 1.1 Region / Availability Zone

An AWS account is like a building management boundary; IAM controls who may enter each room. Separating accounts and granting only the actions a role needs are different design decisions.

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


Deploying across AZs still requires verification of application and data replication, failure routing, and remaining capacity. Multi-AZ alone does not guarantee recovery from a Region-wide outage.

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


SCPs require an organization with all features enabled and apply to member-account root users. They do not apply to management-account users and roles or service-linked roles. Prefer federation and temporary credentials for routine human access, and use MFA. [AWS SCP documentation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html), [IAM security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html).

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


The source JSON is one statement, not a complete policy. Wrap it in `Statement` and specify the policy language `Version` in an actual policy document. `Condition` is optional. A Trust Policy that permits a principal to assume a role does not replace its Permission Policy's service permissions. Temporary credentials are also secrets and must be refreshed securely before expiration. The ARN account number `123456789012` is illustrative. [IAM policy elements](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html), [IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html).

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

## Key points

Accounts set management boundaries, while IAM sets permission boundaries. Separate role assumption from service permissions when applying least privilege.

## LLM practice: review permission boundaries for an S3 read role


**Prompt:**

=== "한국어"

    ```text {.prompt}
    S3의 example-study-bucket/reports/* 읽기 요청을 위한 IAM 정책 PR을 검토해 줘. 역할 수임 조건, 서비스 권한, SCP 제한을 구분하고 필요한 최소 권한을 제안해 줘. 비밀값은 다루지 말고 정책을 적용하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review an IAM policy PR for reading example-study-bucket/reports/*. Separate role assumption, service permissions, and SCP restrictions, then suggest the minimum needed permissions. Do not handle secrets or apply the policy.
    ```

**Key point:** A minimal IAM JSON draft for required actions/resources and a review of excess/missing permissions by trust, SCP, and account scope. It may respond to AccessDenied with Resource:* or administrator access, or treat an SCP as a permission grant. Check the complete policy structure and object ARN against expected allowed/denied action-resource cases. Reject access-allowed verdicts that assume missing trust or SCP content.
