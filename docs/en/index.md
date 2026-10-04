---
id: handbook-home
status: overview
last_updated: 2026-10-03
last_reviewed: 2026-10-03
knowledge_ids: []
---

# Work Knowledge Handbook

This handbook keeps useful knowledge from work and study. It supports concepts, design, operations, troubleshooting, projects, and LLM use.

## Current scope

The complete data platform source for Chapters 1–21 and the infrastructure sources for Chapters 1–11 cover storage, events, processing, analytics, quality, observability, governance, AI evaluation, managed platforms, operations, and final architecture. There are 22 data-platform topic, architecture, and curriculum pairs, 12 platform/infrastructure pairs, 18 prompt library pairs, and the home, workflow, and glossary: 55 Korean/English pairs in total.

The data-platform continuation completes the conceptual scope of Phases 1–21. The first source labels Chapters 1–4 as reconstructed notes; Snowflake remains a condensed treatment. Studied concepts are not presented as actual implementation, production, or incident-drill experience.

New topics: [AI evaluation](data-platform/ai-evaluation.md), [Databricks](data-platform/databricks.md), [Snowflake](data-platform/snowflake.md), [platform comparison](data-platform/platform-comparison.md), and [operations and recovery](data-platform/production-operations.md). The [architecture](data-platform/architecture.md) now includes consistency, recovery, scaling, cost, smaller-scale choices, and open/managed alternatives.

The new [platform and infrastructure basics](platform-infrastructure/index.md) section covers [Linux and containers](platform-infrastructure/linux-containers.md), [Kubernetes core](platform-infrastructure/kubernetes-core.md), and [Kubernetes operations](platform-infrastructure/kubernetes-operations.md). Chapters 1–3 represent Basic conceptual study. The continuation adds [Redis](platform-infrastructure/redis.md), [PostgreSQL](platform-infrastructure/postgresql.md), [Kafka operations](platform-infrastructure/kafka.md), [vLLM](platform-infrastructure/vllm.md), [LiteLLM](platform-infrastructure/litellm.md), and [GPU infrastructure](platform-infrastructure/gpu-infrastructure.md) in Chapters 4–9. Chapters 10–11 add [platform security](platform-infrastructure/platform-security.md) and [CI/CD, Helm, Argo CD, and GitOps](platform-infrastructure/cicd-gitops.md). Chapters 12–15 remain unstudied future topics, with Terraform & Infrastructure as Code next.

The handbook expands into software, data, AI, platforms, infrastructure, architecture, and operations when source material is available. New roles and technologies do not need to fit an unrelated category.

## Practical examples to adapt

The [practical prompt library](prompts/index.md) contains 100 new examples by topic. All 134 examples, including 34 on concept pages, have Korean/English tabs and copy buttons. Inputs, tasks, outputs, and checks use separate lines. These are authored applications of study concepts, not actual production results.

## Source and supplements

Study pages retain the supplied Markdown headings, numbers, order, paragraphs, lists, and examples. The original language stays verbatim; the other language follows the same structure in translation. Additional explanations, corrections, and conditions appear after the source body. Read the linked conditions when a source statement is simplified.

## How to read

Start with the [data platform architecture](data-platform/architecture.md) to understand tool roles. Use [study scope and next steps](data-platform/curriculum.md) to find a topic. The [knowledge workflow](methodologies/knowledge-workflow.md) explains how sources become handbook pages. The [glossary](glossary/index.md) defines key terms and links to canonical topics.

Every public page has a Korean and an English version with the same knowledge. Use the language selector to stay on the same topic.
