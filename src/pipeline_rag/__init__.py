# TODO: not yet implemented — see ARCHITECTURE.md §2.5 (LLM RAG Pipeline, Path 2).
#
# Document Processing -> Vector Database Construction -> retrieval-grounded
# Role Search -> Subrole Search -> Persona Generation. RAG applies across all
# stages, not just generation. Must stay independent from pipeline_llm/ — see
# GOALS.md §5. Vector DB choice not yet finalized (ARCHITECTURE.md §7) — ask
# before picking one.
#
# Expected submodules per ARCHITECTURE.md §6: vectorstore.py, retrieval.py
