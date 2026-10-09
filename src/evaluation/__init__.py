# TODO: not yet implemented — see ARCHITECTURE.md §2.6 and §4.2, GOALS.md §7.
#
# Ground truth choice (project description vs. expert-annotated) is an open
# research question, NOT settled — do not hardcode one without confirming
# with Anin first (ARCHITECTURE.md §7, GOALS.md §9).
#
# Expected submodules per ARCHITECTURE.md §6:
#   performance.py   - cosine similarity, BLEU, ROUGE (LLM vs LLM+RAG output)
#   expert_eval.py    - Likert instrument (representativeness, usefulness,
#                        consistency), score aggregation
