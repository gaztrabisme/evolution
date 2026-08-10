# evolution

A [Claude Agent Skill](https://agentskills.io/specification) that evolves *other skills* from their own real traces.

You invoke it without naming a target. It reads the evidence — ledgers, per-skill git history, session transcripts, prompt history, file-read telemetry — decides which skills have earned a change, and runs the loop on them. Before proposing anything new, it settles the verdicts previous runs left open.

## Why it exists

A skill that never ingests its own traces is frozen at its authoring assumptions. A skill distilled from documents carries borrowed confidence. The usual fix — "harvest → patterns → hypotheses → apply → validate later" — has a hole in it: *validate later* names no owner and fires on no trigger.

Measured across the constellation this was extracted from: 15 evolution ledgers, ~2,700 lines, and **13 of them had never settled a single verdict**. Everything sat at `PENDING` indefinitely, which reads as humility and functions as amnesia.

So this skill adds the two missing pieces:

- **Triage** — which skill has earned a run, decided from evidence rather than intuition. A skill with no traces since its last entry is *excluded*, not deprioritised; evolving it would mean inventing patterns.
- **Settle first** — every run resolves the previous entry's open verdicts before harvesting anything new. `PENDING → KEEP` finally has a trigger.

## The loop

| Phase | What happens |
|---|---|
| 1 Triage | Score every skill on evidence; pick 3–5; state a skip reason for the rest |
| 2 Settle | *Per selected skill:* resolve open verdicts → `KEEP` / `REVISED` / `REVERT`, or `PENDING` **with a stated reason** |
| 3 Harvest | Gather that skill's real traces since its last entry |
| 4 Patterns | Rank by Impact ÷ Effort, each with the proof it bit |
| 5 Hypotheses | One specific edit per pattern. **Stop for approval — the whole set at once** |
| 6 Apply | One commit per hypothesis, in the skill's own repo |
| 7 Record | The ledger entry, verdict `PENDING` |

Validation is not an eighth step; it is Phase 2 of a later run. That is the whole point.

## Verdicts

`PENDING` → `KEEP` (≥2 independent real uses) · `REVISED` · `REVERT` (+ post-mortem).

`REVISED` is the one people skip and shouldn't. When a change goes unused, the tempting read is "it failed." Usually it was described more broadly than the evidence supported — correct machinery, over-generalised from the one context that produced it. The fix is a selector naming when it applies, not a retraction. Collapsing that into `REVERT` throws away working machinery and teaches the loop never to generalise.

## Install

```bash
git clone https://github.com/gaztrabisme/evolution.git ~/.claude/skills/evolution
```

**Dependency:** this skill references the `core` kernel at `../core/` for the shared spine (integrity constraints, grounding gate, wiki protocol, pushback-and-teach). Without it those links dangle:

```bash
git clone https://github.com/gaztrabisme/core.git ~/.claude/skills/core
```

It composes with [`skill-builder`](https://github.com/gaztrabisme/skill-builder) where that exists — `skill-builder` authors and shapes a skill at birth and distils methodology from documents; this one upgrades a working skill from lessons in completed real work.

## Telemetry it reads

Local only, read-only, never written to:

- `<skill>/EVOLUTION.md` — the ledgers
- `git -C <skill> log` — edits made outside the loop
- `~/.claude/projects/**/*.jsonl` — where skills fired and where they were corrected (streamed and filtered; never read whole)
- `~/.claude/history.jsonl` — friction markers
- `~/.claude/read-once/stats.jsonl` — which reference files actually get opened

That last one is the interesting one. It makes *"was this change even discoverable?"* answerable with a number instead of a guess. It has three blind spots, documented in `references/triage.md` — most importantly that skill-tool injection never traverses the read hook, so **zero reads on a `SKILL.md` is evidence of nothing.**

```bash
python3 evolution/scripts/triage.py          # ~8s over ~1,000 transcripts
python3 evolution/scripts/triage.py --fast   # skip transcripts, <1s
```

Stdlib only. No network.

## Its own verdict

`PENDING`, and it should stay there for a while. One dogfood, one operator, zero completed runs against a skill it did not itself just author. Its `EVOLUTION.md` records what the first fresh-context critic found — including a **false statistic in its own central argument**, which had been inherited from a summary and never verified, in a skill whose stated principle is "evidence or silence."

A log that shows its own failures is worth more than one that doesn't.

## License

MIT
