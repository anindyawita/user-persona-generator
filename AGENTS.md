# AGENTS.md

Guidance for Codex working in this repo. Read `ARCHITECTURE.md` first before touching anything in `src/filtering/`, `src/pipeline_llm/`, or `src/pipeline_rag/` — there are methodological decisions baked in there that, if changed carelessly, can undermine this thesis's research validity.

## Project Context

This is not an ordinary software project — it's an **experimental implementation for an undergraduate thesis**. Every technical decision (threshold, prompt, architecture) has methodological consequences that must be defensible in a thesis defense. If you're unsure whether a change alters the semantics of the experiment, ASK the user before proceeding — don't assume "it works" is enough.

## Hard Rules (do not break without explicit confirmation)

1. **Never pre-assign role/subrole outside the LLM.** All role and subrole classification must come from LLM reasoning (in both the LLM Pipeline and the LLM RAG Pipeline). If you need to reduce noise/candidate count, do it at the *post-generation validation* stage (confidence-score threshold), not at the input stage.
2. **Filtering must be role-blind.** Filtering prompts/logic (`src/filtering/`) must never reference or ask about user type. If you write a prompt like "is this text about [role X]," that's WRONG — filtering may only judge general domain relevance.
3. **The two paths (LLM Pipeline vs. LLM RAG Pipeline) must stay independent.** Don't merge them, cross-filter them, or let one validate the other — their outputs are compared separately at the evaluation stage. If you're tempted to "reuse" a component between the two paths while refactoring, keep the reuse at the infrastructure level (e.g., an embedding function), never at the decision level (a role found in path 1 must never be used to filter path 2).
4. **Every persona attribute needs traceable evidence back to source data.** Don't let the LLM fill an attribute from general knowledge without evidence — if the data is insufficient, use `null`/`"Not specified in the available data"`.
5. **Thresholds must never be hardcoded as one global value.** Make them configurable per data source (app review / news / tweet), and log every change — the user needs to write up this sensitivity in the thesis's limitations section.

## Code Conventions

- Python. Follow the folder structure in `ARCHITECTURE.md` §6 — confirm before reorganizing it.
- All prompt templates live as separate files under `prompts/`, not inline strings in code — so they can be cited directly in Chapter III (Algorithm/Prompt tables).
- Variable and function names use consistent research terminology: `role_search`, `subrole_search`, `persona_generation`, not unclear abbreviations.
- Every experiment (threshold change, model swap, prompt edit) gets logged in `experiments/` with: date, change, rationale, brief result. This becomes material for Chapters IV/V.
- Code comments: explain *why*, not *what* — especially around methodologically significant decisions (see the `anthropic-skills:clean-comments` skill for style guidance if needed).

## Language & Naming

- Project/variable names in code: English (standard coding convention).
- Technical docs (README, long docstrings): mixed is fine, but key terms (role, subrole, persona, evidence, confidence score) stay in English to stay consistent with the attribute table in Chapter III (Table 3.1).
- If asked to write output meant to be pasted directly into the thesis draft (Chapter III/IV), follow the project's writing style: 4–6 sentence paragraphs, simple but precise Bahasa Indonesia, Times New Roman 12pt / tables 10pt (relevant if auto-generating report text, not the code itself).

## Before Running Large Tasks

- If a task touches the evaluation pipeline (`src/evaluation/`): check first whether the ground truth is finalized (see `ARCHITECTURE.md` §4, "Known Design Tensions"). The draft still contradicts itself here — DO NOT assume one or the other without confirming with the user.
- If a task touches the vector database (`src/pipeline_rag/vectorstore.py`): the vector DB choice isn't finalized. If it's not already in config, ask before picking one yourself (don't silently install Chroma/FAISS/etc. without saying so).
- If asked to "add feature X" that could change the experimental design (e.g., adding a new data source, changing how roles are discovered) — think through the implications for internal/construct validity first, and surface that to the user before implementing, rather than just quietly doing it.

## Testing & Reproducibility

- Every experiment run must be reproducible: fix the random seed, log the model version, log the prompt version (if a prompt changes, keep the old version instead of overwriting it).
- Unit tests for `src/filtering/` must include cases verifying the filter does NOT leak role signal (e.g., assert that the filtering function neither accepts a role parameter nor produces output that names a role).

## What Does NOT Need Re-Confirming

- The persona attribute schema is final (see `ARCHITECTURE.md` §3) — no need to re-confirm every time you touch code that uses it, unless the user explicitly asks to change the schema.
- The two-path design (LLM vs. LLM+RAG) is final as the thesis's core experimental design — don't re-question it, just implement per `ARCHITECTURE.md` §2.4–2.5.