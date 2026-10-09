# TODO: not yet implemented — see ARCHITECTURE.md §2.4 (LLM Pipeline, Path 1).
#
# Baseline path: filtered data goes directly to the LLM, no retrieval.
# Role Search -> Subrole Search -> Persona Generation, all LLM-reasoned
# (not pre-assigned). Must stay independent from pipeline_rag/ — see
# GOALS.md §5 ("two independent pipelines, always compared, never merged").
