# Work Knowledge Handbook contract

This contract applies to every handbook update. Read it before ingesting sources. User instructions override templates. This is an extensible professional knowledge base, not a single-domain study diary.

## Purpose and scope (mission 1–5)

Support concepts (what, why, how, mental model), engineering (design, trade-offs, alternatives, failure, monitoring, operation), troubleshooting (symptoms, first checks, hypotheses, experiments, recovery, prevention), projects (inputs, steps, decisions, risks, outputs), and LLM work (questions, context, likely errors, validation).
Allow software, data, platform, AI/LLM, infrastructure, cloud, Kubernetes, databases, streaming, observability, distributed systems, architecture, AI serving, engineering operations, methodology, standards, processes, guides, study, interviews and future domains. Add categories when evidence warrants; never force unrelated knowledge into a category.
Accept curricula, extracted Markdown, shared conversations, notes, documentation, architecture, code, configuration, specifications and other work sources. Prefer supplied Markdown over remote links. Read the entire accessible source; record inaccessible portions and never claim full reading when access was partial. Preserve sanitized local evidence under sources/<batch>/ rather than relying on a conversation URL.
Curriculum determines structure; sources supply substance. Preserve reasonable hierarchy but split or merge for maintainability. Preserve useful off-curriculum insights. Unstudied items stay not-started or overview, never invented studied content.

## Preservation and extraction (6–12, 33, 55, 59)

Completeness > conciseness; preservation > elegance; traceability > aggressive editing. Extract before writing pages: concepts, terminology, architecture, workflows, behavior, examples, comparisons, rules, assumptions, constraints, edge cases, failures, production and operational knowledge, troubleshooting, mistakes, misconceptions, decisions, questions and insights. Ignore only greetings, filler, duplicated conversational wording and irrelevant meta discussion.
No meaningful source knowledge may disappear without being accounted for. Move, cross-link, append, generalize or explicitly defer what does not fit. Never shorten technical scope just to shorten a document. Preserve valuable questions as conceptual boundaries.
Assign stable source IDs in content-manifest.md. Map source language, curriculum, primary domain, discovered topics, existing canonical pages, new pairs, duplicates, cross-links and open questions in mapping.md before writing.
Organize reusable concepts, not sessions or import dates. Merge the union of existing correct knowledge and new useful knowledge. Remove correct existing knowledge only for true duplication, stronger superseding evidence, factual correction or explicit user removal; record the reason and migration of source IDs.
Use Included/Merged/Deferred/Excluded per ID. Deferred/Excluded require specific reasons. Source-only knowledge remains accounted for without pretending it was published. Accounted coverage and published coverage are different metrics.

## Canonical bilingual pages (13–25, 32, 35–36, 48–50)

Only docs/ko and docs/en are public handbook content. Every .md page has the same relative path in both trees and a stable shared front matter id. IDs survive path changes; IDs are unique across page pairs. Required status: not-started, overview, studied, deep-dive. last_updated and last_reviewed contain actual dates. tested_with exists only for known tested versions. knowledge_ids lists source IDs represented by the page.
Extract canonical knowledge first, then author Korean and English from it. Both languages preserve the same concepts, examples, constraints, warnings, edge cases, diagrams, tables, failures, guidance and LLM scenarios. Sentence-by-sentence translation is not required. Review both complete pages, not just IDs or matching files. Hash-bound reviews in reviews/bilingual.json must be refreshed after changes and record the actual reviewer. Automation detects stale evidence; it cannot prove semantic truth.
Write natural professional Korean, short clear sentences, concrete examples and consistent standard English technical terms. Use simple, interview-friendly English: one main idea per sentence, active voice, short paragraphs. Prefer use/help/start/before/because/change. Avoid utilize/facilitate/commence/prior to/due to the fact that and academic or AI filler. Never replace standard terms (partition, replication, throughput, latency, schema, snapshot, metadata, backpressure, idempotency, consumer lag, observability, cardinality, transaction, consistency, availability, durability, orchestration) with strange substitutes; explain them plainly.
Use progressive depth: quick understanding, mental model, core concepts, practical use, production concerns, deep dive. Maintain bilingual glossary as terms enter actual knowledge. Links stay in the same language; link canonical concepts rather than repeating entire explanations. Update equivalent navigation. Language switch should keep the same topic, using maintained i18n support rather than custom JavaScript.

## Page types and selective templates (26–31, 34, 37–40)

Choose Learn, Reference, How-to, Runbook, Decision, Architecture or Methodology; never force a single template or leave empty headings.
Concept: overview, why, mental model, architecture, core concepts, how, example, production, failure, observability, misunderstandings, related topics, decision guide, interview summary, takeaways, meaningful LLM practice.
Workflow: purpose, context, preconditions, inputs, end-to-end flow, components, decisions, outputs, failures, validation, mistakes, related topics, meaningful LLM practice.
Methodology: objective, when, inputs, process, outputs, roles, checklist, decisions, risks, mistakes, example, meaningful LLM practice.
Runbook: symptoms, impact, initial checks, investigation flow, possible causes, verification, resolution, recovery, prevention, monitoring, escalation, meaningful LLM practice.
Architecture: context, requirements, constraints, options, trade-offs, actual decision, architecture, failures, operations, security, cost, open questions, related topics, meaningful LLM practice. Never invent a decision.
Use Mermaid when architecture, request/data flow, sequence, states, replication, dependencies or failure flow become clearer. Validate syntax with the Mermaid parser. Prefer neutral labels; localized versions must carry equivalent information.
Add LLM in Practice only for real uses: learning, architecture/design/code/SQL/YAML/configuration review, troubleshooting, logs/metrics/traces/incidents, capacity/migration planning, runbooks/checklists, implementation review.
Each scenario has Situation; Context to Give the LLM; Example Prompt in a closed text fence; Expected Output; What the LLM Can Get Wrong; How to Validate. Prompts provide equivalent Korean and simple-English versions in language tabs, use multiple short lines with specific inputs and outputs, and separate observations, assumptions, constraints, hypotheses, missing evidence and next checks. Authored prompt examples link to existing canonical knowledge and do not create claims of studied content, actual work experience, or measured model performance. Do not redesign before assessing a design; do not confuse correlation with causation.
LLM output is a working hypothesis or assistance, never authoritative truth. Validate using official docs, actual configuration/state, logs, metrics, traces, tests, controlled experiments and real requirements.

## Evidence, freshness and privacy (41–45)

Distinguish fact, recommendation, example, hypothesis, personal understanding and unresolved question. Verify version-sensitive behavior, security advice, limits, defaults, APIs and vendor implementation with current primary sources. Record actual versions and review dates, never invented freshness or production-readiness.
Distinguish studied concept, hypothetical example, recommended practice and actual experience. Claim personal implementation only when sources explicitly support it, in both languages.
Assume Pages is public. No company secrets, internal URLs/identifiers, credentials, personal/payment data, proprietary code, restricted architecture or private datasets in public pages. Generalize reusable knowledge and apply the same redaction to both languages. Never commit sensitive raw sources; keep only sanitized evidence. Source tracking, control contracts and reviews stay outside the generated public site, but all tracked files and history are public in this repository. Only sanitized, publishable sources may be committed. The cloud-synced vault has the same privacy boundary as stored Markdown; do not mirror private/credential/runtime folders.
Store reusable runnable examples under examples/, configs/, scripts/ and link from both languages. Validate executable behavior when practical. Never claim an unrun example was tested.

## Required update workflow (46–58)

1. Inspect repo, contracts, existing KO/EN and navigation; read curriculum and complete sources.
2. Extract IDs, complete manifest and mapping before final pages; classify domains and locate existing canonical topics.
3. Merge useful knowledge, author both languages, review easy English and equivalent scope; add useful diagrams, cross-links, glossary, meaningful LLM scenarios, metadata, navigation and examples.
4. Complete coverage matrix; generate coverage report and distinguish total/accounted/published/KO/EN/sync rates. Exclusions and deferrals remain visible.
5. Review semantic scope, simple English and privacy; record current page hashes with real review evidence. Check structural pairs, duplicate IDs, links, navigation/orphans, Mermaid and executable examples.
6. Run full validation and strict MkDocs build. Inspect generated language alternates and verify control/source files are absent from site. Resolve every error.
7. Sync generated first-party Markdown to the configured vault, verify byte hashes and fail on edited vault copies. Git Markdown remains authoritative; no reverse sync, silent overwrite or delete. A successful local finalize includes vault sync; CI has no vault access.
8. Stage named paths, inspect sanitized diff, commit and push verified work to this public source repository. The user explicitly authorized making this repository public and activating Pages. Main pushes now validate/build/deploy under that continuing authorization; do not ask again for routine authorized updates. New publication destinations or broader disclosures still require authorization.
9. Concise final report: sources and curricula processed, domains, created/updated pairs, merged topics, X/Y IDs accounted, KO/EN/matched/missing counts, MkDocs/structure/semantic/simple-English/links/Mermaid/privacy/vault results and open issues. Report source read, extraction, canonical mapping, all validation and language switching accurately. Do not report full completion if any required check fails.

Markdown is canonical; MkDocs Material generates responsive searchable HTML with syntax highlighting, tables, admonitions and Mermaid. Git is long-term evidence. Sources are not final chronological documentation. HTML is never hand-maintained. This contract intentionally preserves all 59 mission sections as grouped obligations.
