---
id: platform-terraform-iac
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - PIS4-12-01
  - PIS4-12-02
  - PIS4-12-03
  - PIS4-12-04
  - PIS4-12-05
  - PIS4-12-06
  - PIS4-12-07
  - PIS4-12-08
  - PIS4-12-09
  - PIS4-12-10
---

# Chapter 12. Terraform & Infrastructure as Code

This page preserves the supplied study source’s numbering, order, and examples. See the separate supplement for State security, S3 locking, and approved-plan conditions in 12.3–12.5, and workspace isolation limits in 12.9. The examples are not results of infrastructure runs.

<!-- SOURCE CORE START -->

## 12.1 IaC Fundamentals

Infrastructure as Code (IaC) declares and manages infrastructure in code instead of creating it manually in a console.

Main goals:

- Track infrastructure changes
- Build repeatable environments
- Keep environments consistent
- Make changes reviewable
- Automate creation, updates, and deletion

A common division of responsibilities is:

```text
Terraform
= Create cloud infrastructure

Argo CD + Helm
= Deploy Kubernetes applications
```

Example:

```text
Terraform
↓
VPC
Subnet
Security Group
Load Balancer
EKS
Node Pool
GPU Node Pool
RDS
Storage
IAM
```

On top of that:

```text
Argo CD
↓
Backend
LiteLLM
vLLM
Worker
```

Deploy these applications.

---

## 12.2 Terraform Building Blocks

### Provider

Defines which platform API Terraform communicates with.

Example:

```text
AWS Provider
Kubernetes Provider
GitHub Provider
```

### Resource

An object that Terraform creates and manages directly.

Example:

```text
aws_vpc
aws_subnet
aws_eks_cluster
aws_db_instance
```

### Data Source

Reads information about existing resources without creating them directly.

Example:

```text
Look up an existing VPC
Look up an existing AMI
Look up an existing IAM role
```

### Variable

Accepts external values so the same code can be reused across environments.

Example:

```text
environment = dev
environment = prod
```

### Output

Exposes information about the created infrastructure.

Example:

```text
VPC ID
Cluster Endpoint
Database Endpoint
```

---

## 12.3 Terraform State

**State** is an important concept in Terraform.

Terraform State:

```text
Terraform Resource Address
↔
Actual Cloud Resource ID
```

Stores this mapping.

Example:

```text
aws_vpc.main
↔
vpc-123456
```

State also stores the last known resource attributes.

A typical Terraform workflow:

```text
Terraform Code
↓
Check State
↓
Read the actual resource through the provider
↓
Compare desired state with actual state
↓
Create a Plan
↓
Apply
↓
Update State
```

### Difference between Git and State

```text
Git
= Store the desired infrastructure structure as code

State
= Store the mapping between Terraform resources and actual resources
```

Having Git alone does not make Terraform automatically recognize existing resources as objects it manages.

If State is lost, Terraform can lose its mapping to existing resources.

You can use `import` to bring an existing resource under Terraform management.

---

## 12.4 Remote State

Using only personal local State is not suitable for teamwork.

Teams commonly use Remote State.

Example in AWS:

```text
S3
→ Store Terraform State

State Locking
→ Prevent problems from several people applying at the same time
```

The current Terraform S3 backend supports S3 lockfiles (`use_lockfile=true`); the older DynamoDB locking approach is being deprecated.

The following matter for State storage.

- Access permissions
- Versioning
- Backups
- Encryption
- Locking

Enabling S3 Versioning helps recover State.

---

## 12.5 Terraform Plan / Apply Workflow

A typical team workflow:

```text
Developer
↓
Pull Request
↓
CI
↓
terraform plan
↓
Review
↓
Merge / Approval
↓
terraform apply
↓
Remote State Update
```

`plan`:

> Check which changes will occur

`apply`:

> Apply changes to actual infrastructure

These are their roles.

They can be separate stages in one pipeline or separate workflows.

The important point:

```text
Plan
↓
Review / Approval
↓
Apply
```

Keep this gate in the workflow.

---

## 12.6 Terraform Module

A module is a reusable infrastructure package.

Example:

```text
modules/
└─ vpc/
   ├─ main.tf
   ├─ variables.tf
   └─ outputs.tf
```

Across environments:

```text
dev
↓
VPC Module

prod
↓
Same VPC Module
```

The module can be reused.

Example modules:

```text
VPC Module
EKS Module
GPU Node Module
Database Module
```

Modules can encode company standards.

Example:

```text
Enable logging by default
Require encryption
Tagging rules
Security settings
```

Comparison:

```text
Helm Chart
= Reuse Kubernetes application structure

Terraform Module
= Reuse infrastructure structure
```

---

## 12.7 Cloud Infrastructure Composition

Terraform can create cloud resources such as these.

```text
Network
├─ VPC
├─ Subnet
├─ Route Table
├─ Security Group
└─ Load Balancer

Compute
├─ EKS
├─ General Node Pool
└─ GPU Node Pool

Data
├─ RDS
└─ Storage
```

Terraform references can express dependencies between resources.

Example:

```text
Subnet
↓
Reference the VPC ID
```

Terraform computes a dependency graph to determine the creation order.

---

## 12.8 Boundary between Terraform and Kubernetes Resources

Common recommended roles:

```text
Terraform
→ Cluster / Node / Cloud Infrastructure

Argo CD
→ Kubernetes Application
```

Terraform:

```text
EKS
GPU Node Pool
IAM
Cloud Storage
RDS
```

Argo CD:

```text
Deployment
Service
Ingress
ConfigMap
Application workload
```

Both tools can manage some resources, such as namespaces and RBAC.

Important principle:

> Do not let Terraform and Argo CD manage the same resource at the same time.

Terraform can bootstrap Argo CD itself.

---

## 12.9 Environment Strategy

It is useful to reuse modules and separate State by environment.

Example:

```text
infra/
├─ modules/
│  ├─ vpc/
│  ├─ eks/
│  └─ database/
└─ env/
   ├─ dev/
   ├─ staging/
   └─ prod/
```

State:

```text
dev state
staging state
prod state
```

As production grows, State can be split further.

Example:

```text
network state
eks state
database state
gpu state
```

Terraform workspaces are another option, but directories/root modules with separate State are often clearer in production.

Instead of separating environments with long-lived branches:

```text
main
+
environment directory
+
separate state
```

This approach is generally easier to manage.

---

## 12.10 Terraform Operations

### Drift

A difference between Terraform code and the actual cloud state.

Example:

```text
No SG rule in Terraform
Add a rule manually in the cloud console
```

The next Plan can detect drift.

Prefer changes through Terraform over direct console changes when possible.

### Replace

Changing some attributes may require replacing a resource instead of updating it.

In the Plan:

```text
update
replace
destroy
create
```

Check these actions.

### Import

Connect an existing cloud resource to Terraform State.

### State Recovery

Use Remote State versioning and backups to make recovery possible.

Direct State edits are risky, so keep them to a minimum.

---

<!-- SOURCE CORE END -->

## Supplement — State protection and execution boundaries

Official documentation checked on 2026-10-05. No Terraform runs, cloud changes, or State recovery were performed.

### 12.3 / 12.4 Sensitive data in State and Plans

State and saved Plans can contain sensitive values such as passwords. `sensitive = true` hides their display; it does not remove values from files. Keep State and Plans out of Git and public CI logs. Manage storage access, encryption, and retention together. [Terraform sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)

### 12.4 Enable S3 locking explicitly

The S3 backend defaults `use_lockfile` to `false`. Remote State alone does not protect concurrent writes. When enabling locking, check read, write, and delete permissions on the `.tflock` object. DynamoDB locking is officially deprecated; both methods can be configured during migration. Also check bucket versioning for State recovery. [Terraform S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3)

### 12.5 / 12.10 Reviewed Plans and actual execution

Running `terraform apply` without a Plan file creates a new Plan. To apply reviewed changes, bind the saved Plan to the approval. Passing a saved Plan executes it without another interactive confirmation, so put the approval gate before that step. A partially successful Apply does not automatically roll back on failure. Review State recovery separately from recovery of actual cloud changes. [Terraform apply](https://developer.hashicorp.com/terraform/cli/commands/apply)

### 12.9 CLI workspaces and access boundaries

Workspace here means a Terraform CLI State workspace. These workspaces are not suitable for deployments needing separate credentials and access controls, or for system decomposition. Separate directories alone do not separate permissions. Check backend State locations and execution credentials together. [Terraform workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces)

## Related topics

- [Platform study map](index.md)
- [CI/CD and GitOps](cicd-gitops.md)
- [Platform security](platform-security.md)
- [Multi-tenancy and cost](multitenancy-cost.md)
