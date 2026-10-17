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

Read the full selected source and its other-language peer before claiming educational accuracy. The deterministic parser preserves headings, code, tables, examples, knowledge IDs and source line ranges in the Slide Schema. It chooses table comparison and source-row quiz, ordered-list steps or scenario, diagram component exploration, quoted-example flashcards, and editable prompt practice where evidence supports them. Ordinary prose stays static. Do not add arbitrary sliders, calculations, failure outcomes, measurements, or technical claims absent from the source. A simplified interaction must display its model boundary. Place full source detail in notes when the visible slide is shortened.

After generation, inspect `report.json` and `manifest.json`. Resolve every failed page and unmapped source line. For meaningful changes, compare the complete Korean and English decks with their Markdown sources. Automatic line coverage proves traceability, not semantic correctness. Review representative architecture, operations, AI development, English learning, and prompt decks in an actual browser, including interaction state and reset, small screens, keyboard use, and offline `file://`.

## Extend

Use the shared Slide Schema and renderer for normal pages. Add a new interaction only when its input, state transition, output, reset behavior and source evidence can be specified and tested. Keep domain-specific models in separate registered modules; do not branch on a technology or directory name in the generic parser. Follow SDD/TDD and ADR when behavior or durable structure changes. Run the official skill validator, `make validate`, `make finalize`, and fresh Git verification before a completion claim.

The fixed bmad template under `third_party/slides-generator-template` contributes the React slide transition and reviewed design/build references. Follow its provenance limits; do not use its omitted export path or CDN font. The sylvial928 skill informs activity design but is not an installed dependency.
