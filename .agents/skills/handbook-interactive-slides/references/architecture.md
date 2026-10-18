# Architecture and extension guide

## Pipeline and ownership

`mkdocs.yml` nav is the public document adapter. `scripts/interactive_slides.py` discovers paired `docs/ko` and `docs/en` pages, parses front matter and Markdown blocks, analyzes source blocks and applies explicitly reviewed explanation designs, creates schema version 1, validates substantive line coverage, and exports standalone HTML. The React renderer in `assets/renderer/` is common to every document. `scripts/check_site.py` validates publication boundaries and original/slide links. `tests/test_slides_study_browser.mjs` audits every study section and source text; `tests/test_slides_browser.mjs` exercises presentation geometry and navigation in an offline browser context.

The public source ID, relative path, language and nav path stay in each schema. Each slide carries source evidence, stable section/unit identity, visible explanation blocks, design status, optional interaction data, supplementary notes and references. Source coverage is separate from visible explanatory completeness. Generated schemas live under `_workspace/handbook-slides/schema/` and are excluded from the public `site/slides` copy. The manifest stores source and renderer hashes, source/slide URLs, sections and coverage. No per-document JSX is generated. A renderer or analyzer change invalidates the build hash for all decks; a source change invalidates its two language decks as needed.

## Schema contract

The top level provides `schema_version`, `document_id`, `source_path`, `source_hash`, `language`, `title`, `nav`, `knowledge_ids`, `outline`, `coverage`, `source_url`, `alternate_url`, `related`, and `slides`. Each slide provides `id`, `title`, `section`, `objective`, `concepts`, `visualization`, `interaction`, `parameters`, `example_data`, `validation_rules`, `body_html`, `notes_html`, `source`, and `references`. `interaction` has `type`, `data`, and `model_note`. Its type is an entry in the renderer registry. The model note states what the activity actually models.

## Adding an activity

1. Establish a reviewed explanatory advantage over static source and independent expected input/output cases. A Markdown shape alone never qualifies. Define a source pattern and a rule that cannot invent facts. Extract bounded data and cite source lines in the schema. For a numerical model, specify an actual source formula, input domain, deterministic result, boundary cases, and the real-system difference. A Python plugin file exposes `register(register_interaction)` and calls `register_interaction(name, matches, create, priority=0)`. `matches(raw, heading, language)` is content based; `create` returns `{type, data, model_note}`. Pass the file with `--plugin path/to/plugin.py`. Plugin bytes join the build hash, so editing it invalidates generated decks.
2. Add a renderer component to the interaction registry in `main.jsx`. It must allow keyboard and touch input, show observable state/result, provide reset, and respect reduced motion. Keep it independent of document paths and product names.
3. Add a failing Python test for classification and data accuracy and a browser test that changes input, verifies the result and resets it. Check Korean and English examples.
4. Run the complete build and inspect a representative deck at desktop and mobile widths. The generated report must retain all substantive source lines and no failures.

For another document format, add a discovery/parser adapter that produces the same schema without changing the React renderer. For another export format, consume the schema as an exporter rather than parsing Markdown again. Search storage may be added behind separate interfaces; there is no server or database in version 1.

## Publication

`make validate` first builds the common React bundle and all decks, then runs strict MkDocs and copies the successful standalone HTML into `site/slides`. It injects `data-slide-link` into each built source page, while each slide contains `data-source-link` and `data-language-link`. The site checker requires all 166 current page/slide pairs plus an index and rejects any extra HTML or private control directory. A partial build is for local inspection; publish only after a full successful build. Canonical Markdown and the vault mirror never contain generated slides.

The reviewed upstream `slides-generator` components and standalone build settings are pinned and documented in `third_party/slides-generator-template/PROVENANCE.md`. The explanation-first renderer no longer imports a transition wrapper; the pinned template remains a design and provenance reference. Its original Navigation needs Tailwind and does not meet this bilingual responsive UI; its export path loses interactions. Review the upstream license and provenance before reusing other files.

## Explanation review boundary

Spec 012 R4–R5 and R10–R17, and ADR 015 govern current design. The parser preserves source meaning and headers; the separate reviewed-design registry provides bounded bilingual examples and rationale. `none` is a successful design result, not a missing feature. Static fallback must never be described as reviewed explanation quality. Quiz, grading, flashcard and mandatory-editing components are outside the schema/renderer contract.

The default study renderer groups units by stable source section and permits document vertical reading, without nested scroll containers. The presentation renderer paginates semantic blocks to the viewport without hiding text. Mode changes preserve the current explanatory unit. A parameter panel has semantic `panel=parameter` identity so viewport reflow does not confuse it with an obsolete numeric content fragment; preserve its live input and result during resize. Browser assertions wait for rendered semantic identity and focus completion, not stale DOM presence. Wide study tables may repeat their first column beside each remaining column, retaining all headers, cells and links. Stable explanation identity, rather than rendered page number, owns language/history/resize position. Validate source fidelity, visible content, layout, navigation and technical explanation independently. Adding a reviewed type requires source-pair reading, direct design review, independent expected outcomes and browser evidence before applying that type elsewhere.

### Stable identity and stale reviews

`scripts/slide_sections.json` persists paired source-section identities, looked up independently in each language by heading ancestry fingerprints. Its initial structural pairing is not semantic review. Keep existing IDs when registering renamed sections; do not silently align new headings by current page/slide order. Unknown sections are explicitly `unpaired`. Canonical explicit anchors and reviewed design IDs take precedence. Register reviewed design section IDs in the source registry too, so invalidating a review cannot change the section identity when the renderer falls back to static source. The registry bytes participate in incremental invalidation.

`scripts/slide_explanations.py` holds source-span fingerprints for reviewed designs. A design may also depend on a full-document fingerprint when its rationale cites later sections, as the QLoRA flow does. A changed source span falls back to static source until the design is reread and reviewed; never refresh a review hash merely to make a check green. Keep this guard distinct from the full source-line coverage report.
