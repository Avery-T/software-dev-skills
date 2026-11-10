# pstack model configuration
# Portable defaults for this collection. Values are preferences, not availability claims.
# Reuses upstream pstack role names and model-list syntax.
# Model IDs and effort are separate. inherit-parent means omit that override.
oversight: gpt-6-astra
oversight effort: high
subagents: gpt-6.1-sol
subagent effort: inherit-parent
feature, refactoring: gpt-6.1-sol
bug-fix: gpt-6.1-sol
perf-issue: gpt-6.1-sol
hillclimb: gpt-6.1-sol
judgment and prose: gpt-6.1-sol
hardest tasks: gpt-6.1-sol
how explorer: gpt-6.1-sol
how explainer: gpt-6.1-sol
why investigators: gpt-6.1-sol
why synthesizer: gpt-6.1-sol
reflect tooling: gpt-6.1-sol
reflect judgment, divergent, synthesizer: gpt-6.1-sol
arena runners: gpt-6.1-sol, gpt-6.1-sol
arena cross-judge pool: gpt-6.1-sol
swarm workers: gpt-6.1-sol
architect runners: gpt-6.1-sol, gpt-6.1-sol
interrogate reviewers: gpt-6.1-sol, gpt-6.1-sol
