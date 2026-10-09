# TODO: not yet implemented — see ARCHITECTURE.md §2.3 (Data Quality Filtering)
# and GOALS.md §5.
#
# HARD RULE: this module must stay role-blind. Layers here may judge domain
# relevance only — never user type/role. Do not add a parameter, prompt, or
# classifier here that distinguishes user roles; that belongs to Role Search
# inside pipeline_llm/ and pipeline_rag/, and must be LLM-discovered there,
# not pre-assigned here.
#
# Three layers (cheapest to most expensive):
#   1. Noise removal (rule-based): min length, duplicates, language
#   2. Domain relevance (semantic similarity, sentence-transformers)
#   3. Context validation (LLM-as-judge, binary YES/NO, domain relevance only)
#
# Thresholds are per-source (tweet/news/review), configurable, never a single
# global constant — log every change in experiments/.
