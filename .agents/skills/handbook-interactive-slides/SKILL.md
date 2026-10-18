---
name: handbook-interactive-slides
description: Build or update source-traced, bilingual interactive HTML learning slides from the public MkDocs Work Handbook. Use for handbook slide generation, interaction review, incremental rebuilds, and slide renderer extension; not for editing canonical Markdown.
---

# Handbook interactive slides

Create independent learning decks from the public MkDocs navigation. The canonical Korean and English Markdown remains authoritative. Read `handbook-contract.md` and [the architecture guide](references/architecture.md) before changing the engine, renderer, or publication flow.

## Run

At the repository root, install pinned Python and npm dependencies, then run `make slides` for all public documents. For one public Markdown path or directory, first run `npm run build:slides-renderer`, then:

```bash
.venv/bin/python scripts/interactive_slides.py build \
  --bundle _workspace/slides-renderer/renderer.js \
  --select data-platform/architecture.md
```

Use `--force` for an explicit full regeneration. Selection is relative to either language tree and applies to both languages. `make validate` rebuilds the complete site and slides, publishes the reciprocal links into `site/`, audits the mapping, and runs browser checks. `make finalize` also verifies the local Markdown vault mirror. Generated source manifests and HTML remain under ignored `_workspace/handbook-slides`; deployable copies are under ignored `site/slides`.

## Content decisions

Read the full selected source and its other-language peer before claiming educational accuracy. Separate discovery, source analysis, explanation design, reviewable content data, common rendering, and verification. Document discovery never authorizes an interaction. Default to faithful static source. Tables, lists, quotations, and incident words are not semantic evidence for a control. Never generate quizzes, grading, score, flashcards, required editing, or completion measurement.

For reviewed explanation units record the concept, purpose and use, relationships, concrete input/process/result, likely confusion, source, assumptions and limits as appropriate to the document. Do not repeat formal learning objectives or treat field counts as quality. An interaction needs a stated explanatory advantage over a static diagram/table and independent expected outcomes. Preserve the established Statistics range tool and its uncertainty. Domain-specific designs belong in registered data/modules, never technology-name branches in the generic parser.

Keep essential definitions, conditions and examples visible without operation. Notes are supplementary; full-source mapping and visible meaning are separate checks. Preserve table row/column headers, cell associations and links; preserve diagram nodes, edges, directions and containment. Parse the canonical Markdown extensions or explicitly structure tabs/code/quotes. Unreviewed material remains static source or clearly marked pending.

Use a calm light neutral background, dark text, one restrained accent, alignment and readable hierarchy. Default to web study mode: keep a coherent source section together so definitions, relationships, examples and limits can be read in context. Document-level vertical scrolling is allowed in study mode; density is not a goal, and nested scrolling, horizontal overflow, clipping and unreadable shrinking are forbidden. In presentation mode, fit the complete slide including chrome within the actual viewport and safe area without horizontal or vertical scrolling. Split at meaningful explanation boundaries, repeat table headers, and retain code context. Never hide, truncate or delete essentials to make content fit. TOC and supplementary notes use bounded pagination in both modes. Preserve reading position by stable bilingual section/unit IDs across mode changes, resize, rotation, refresh, history and language switching. Register reviewed section IDs independently of review status, so stale-review fallback retains the same location. A source-section identity mapping is not proof of bilingual semantic equivalence.

Remove visible previous/next buttons. Navigate via left/right background click or tap, keyboard arrows and accessible named navigation. Do not overlay large invisible controls on content. Exclude links, controls, diagrams, text selections and drags; move one page per gesture, without wrapping at the ends. TOC/notes dialogs need focus entry, containment, Escape and restoration. Keep control keyboard semantics separate from global navigation.
After generation, inspect `report.json` and `manifest.json`. Resolve every failed page and unmapped source line. For meaningful changes, compare the complete Korean and English decks with their Markdown sources. Automatic line coverage proves traceability, not semantic correctness. Review representative architecture, operations, AI development, English learning, and prompt decks in an actual browser, including actual mixed-content pages, longest result, reset, notes and TOC, 320×568, 390×844, 768×1024, 1280×720, mobile landscape, enlarged text, rotation, keyboard use, and offline `file://`. Check element/text bounds and overlap, not just scrollbars. Capture before/after screenshots. Await observable rendered section/unit/panel identity and focus restoration before assertions; the presence of an element from the previous render or a click returning does not prove navigation has finished. Keep actual resize/input-state regressions distinct from test synchronization fixes. Audit all generated study sections for visible source text, pending substitutions, horizontal overflow and nested scrolling separately from the presentation viewport matrix. Report full-deck loading and layout checks separately from reviewed explanation quality. Accessibility-tree inspection is not screen-reader speech testing; disclose actual screen-reader, physical-device and user-understanding scope. Never claim improved understanding has been measured without a user study.

## Extend

Use the shared Slide Schema and renderer for normal pages. Add a new interaction only when its input, state transition, output, reset behavior and source evidence can be specified and tested. Keep domain-specific models in separate registered modules; do not branch on a technology or directory name in the generic parser. Follow SDD/TDD and ADR when behavior or durable structure changes. Run the official skill validator, `make validate`, `make finalize`, and fresh Git verification before a completion claim.

The fixed bmad template under `third_party/slides-generator-template` remains a provenance and design/build reference. The current renderer uses direct React layout so viewport measurement does not depend on a transition wrapper. Follow its provenance limits; do not use its omitted export path or CDN font. The sylvial928 skill informs activity design but is not an installed dependency.
