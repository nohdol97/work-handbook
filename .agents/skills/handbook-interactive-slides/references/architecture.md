# Architecture and extension guide

## Pipeline and ownership

`mkdocs.yml` nav is the public document adapter. `scripts/interactive_slides.py` discovers paired `docs/ko` and `docs/en` pages, parses front matter and Markdown blocks, classifies source-backed learning activities, creates schema version 1, validates substantive line coverage, and exports standalone HTML. The React renderer in `assets/renderer/` is common to every document. `scripts/check_site.py` validates publication boundaries and original/slide links. `tests/test_slides_browser.mjs` exercises file URLs in an offline browser context.

The public source ID, relative path, language and nav path stay in each schema. Every slide has an objective, concept, explanation, interaction type and data, source line interval, complete source notes, references, and validation rules. Generated schemas live under `_workspace/handbook-slides/schema/` and are excluded from the public `site/slides` copy. The manifest stores source and renderer hashes, source/slide URLs, sections and coverage. No per-document JSX is generated. A renderer or analyzer change invalidates the build hash for all decks; a source change invalidates its two language decks as needed.

## Schema contract

The top level provides `schema_version`, `document_id`, `source_path`, `source_hash`, `language`, `title`, `nav`, `knowledge_ids`, `outline`, `coverage`, `source_url`, `alternate_url`, `related`, and `slides`. Each slide provides `id`, `title`, `section`, `objective`, `concepts`, `visualization`, `interaction`, `parameters`, `example_data`, `validation_rules`, `body_html`, `notes_html`, `source`, and `references`. `interaction` has `type`, `data`, and `model_note`. Its type is an entry in the renderer registry. The model note states what the activity actually models.

## Adding an activity

1. Define a source pattern and a rule that cannot invent facts. Extract bounded data and cite source lines in the schema. For a numerical model, specify an actual source formula, input domain, deterministic result, boundary cases, and the real-system difference. A Python plugin file exposes `register(register_interaction)` and calls `register_interaction(name, matches, create, priority=0)`. `matches(raw, heading, language)` is content based; `create` returns `{type, data, model_note}`. Pass the file with `--plugin path/to/plugin.py`. Plugin bytes join the build hash, so editing it invalidates generated decks.
2. Add a renderer component to the interaction registry in `main.jsx`. It must allow keyboard and touch input, show observable state/result, provide reset, and respect reduced motion. Keep it independent of document paths and product names.
3. Add a failing Python test for classification and data accuracy and a browser test that changes input, verifies the result and resets it. Check Korean and English examples.
4. Run the complete build and inspect a representative deck at desktop and mobile widths. The generated report must retain all substantive source lines and no failures.

For another document format, add a discovery/parser adapter that produces the same schema without changing the React renderer. For another export format, consume the schema as an exporter rather than parsing Markdown again. Progress/search storage may be added behind separate interfaces; there is no server or database in version 1.

## Publication

`make validate` first builds the common React bundle and all decks, then runs strict MkDocs and copies the successful standalone HTML into `site/slides`. It injects `data-slide-link` into each built source page, while each slide contains `data-source-link` and `data-language-link`. The site checker requires all 166 current page/slide pairs plus an index and rejects any extra HTML or private control directory. A partial build is for local inspection; publish only after a full successful build. Canonical Markdown and the vault mirror never contain generated slides.

The reviewed upstream `slides-generator` components and standalone build settings are pinned and documented in `third_party/slides-generator-template/PROVENANCE.md`. Only `SlideTransition` is imported in the renderer. Its original Navigation needs Tailwind and does not meet this bilingual responsive UI; its export path loses interactions. Review the upstream license and provenance before reusing other files.
