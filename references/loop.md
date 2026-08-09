# The Evolution Loop

The mechanism that turns a skill from "current instinct / borrowed confidence" into earned, refined judgment. A skill that never ingests its own real traces is frozen at its authoring assumptions; a skill *distilled from documents* is a confident hypothesis until fire-tested. The loop fixes both.

> Canonical home. Moved here from `core/references/evolution-loop.md` on 2026-08-09 when the machinery was consolidated into this skill; `core` keeps spine item #8 (the *gate*: ship an `EVOLUTION.md`, keep its verdict honest) and points here for the *mechanism*.

## The loop

0. **Settle** — before harvesting anything new, resolve what the last entry left open. Every `PENDING` verdict and every unchecked `- [ ]` in the ledger is a question this run is obliged to answer if the traces now exist to answer it. See §Settling first.
1. **Harvest** — gather real traces of the skill in use. Real traces only — not imagined use. Sources per skill: `harvest-sources` table below and `triage.md`.
2. **Patterns** — extract what recurred: friction, gaps, contradictions, silent-skip near-misses, things you *needed* that the skill didn't give you. Tag each `Impact: H/M/L, Effort: H/M/L`. Prioritize `Impact ÷ Effort`.
3. **Hypotheses** — turn each kept pattern into a *specific* edit (file + change), not a vibe. "Add an integration-patterns section to nfr-checklist and point Phase 3 at it," not "improve integration guidance." Format and approval gate: `hypothesis-protocol.md`.
4. **Apply** — make the edits. Record which pattern each closes.
5. **Record** — write the entry. The loop is not done until the ledger says so.
6. **Validate** — in a *later* harvest, i.e. step 0 of a future run.

## The artifact

Each skill repo carries an **`EVOLUTION.md`** (projects use `wiki/decisions.md` + `log.md`). Same section convention across all skills so they're greppable and comparable:

```
# Evolution Log — <skill-name>
<preamble: mechanism pointer + harvest source>

## Evolution N — <date> — <one-line theme>
### Harvest scope        (what traces, why representative)
### Patterns found       (ranked, Impact/Effort, with the proof each bit)
### Hypotheses applied   (each mapped to file(s) changed + pattern closed)
### Validation results   (measured in a later harvest; verdict per change)
```

Four ledgers in the constellation predate this convention and diverge in ways that are *history*, not error — `delivery` starts at Evolution 0 (Birth), `zalo-platform` uses `Birth` / `Round N`. Leave them. Normalizing a ledger's body rewrites the record of what was actually thought at the time. New entries use the canonical shape; `scripts/triage.py` parses both.

## Verdict vocabulary (one set, no synonyms)

| Verdict | Means | Earned when |
|---|---|---|
| `PENDING` | A hypothesis. Applied but unproven. | Default for every new change. |
| `KEEP` | Proven. | **≥2 independent real uses** exercised it without new friction. |
| `REVISED` | Correct machinery, wrong scope. Survives with a selector naming when it applies. | Steps 1–3 of the non-adoption ladder below. The new selector inherits `PENDING`. |
| `REVERT` | Wrong. Removed. | Step 4 of the ladder, **plus a post-mortem recording the mechanism of failure**. |

`dev/modes/evolve.md`'s older `[keep/revert/refine]` triple is retired — `refine` collapsed the scoping case and the wrongness case into one word, which is exactly the mistake §non-adoption exists to prevent.

## The PENDING discipline (the anti-overconfidence rule)

- A change from a **single trace**, or **distilled from documents** and never run, ships with verdict **`PENDING`**.
- It earns **`KEEP`** only after **≥2 independent real uses** exercise it without new friction.
- A change that fails in the field gets **`REVERT` + a post-mortem** recording the *mechanism* of failure, so nobody re-runs the dead end. A documented negative result is reusable knowledge; an undocumented one gets repeated.

This is why `solution-architect` and `ms-ai-discovery` (both document-distilled) must sit at `PENDING` until real engagements validate them — borrowed confidence is not evidence.

## Non-adoption is a scoping signal before it is a validity signal

When a later engagement **doesn't use** something the skill told it to use, the tempting read is "the hypothesis failed." Usually it didn't. Usually the hypothesis was **described more broadly than the evidence supported** — correct machinery, over-generalized from the one context that produced it.

Before writing `REVERT`, ask in this order:

1. **Was it scoped too broadly?** Did the trace that produced it share a context (deal type, project size, domain, team shape) that the skill silently assumed was universal? → the fix is a **selector** that names when it applies, not a retraction.
2. **Was it discoverable?** Buried in a reference nothing points at is not a validity result. This is now *measurable* — `~/.claude/read-once/stats.jsonl` records every file read; a reference with zero reads since the change landed answers this question empirically instead of by intuition.
3. **Was it too heavy for the case?** A 15-sheet instrument on a two-week job gets skipped for cost, not correctness. → state a lighter floor.
4. **Only then: was it wrong?** → `REVERT` + post-mortem.

Record the outcome as **`REVISED`** when 1–3 apply: the change survives, its applicability gets named, and the new selector inherits verdict `PENDING`. Collapsing all of these into `REVERT` throws away machinery that works, and — worse — teaches the loop that the safe move is to never generalize.

The corollary for **harvesting**: the second engagement's greatest value is rarely confirming the first. It's exposing which parts of the first were *context* wearing the costume of *principle*. Go in looking for that.

## Settling first (step 0)

The loop's second half is the half that doesn't happen. Measured across this constellation on 2026-08-09: 13 ledgers, 2,622 lines, and only three changes ever reached `KEEP` — because "validate in a *later* harvest" named no owner and fired on no trigger. Every other entry sits at `PENDING` indefinitely, which reads as humility and functions as amnesia.

So **step 0 runs before step 1, every time**, and it is the cheapest high-value work in the loop:

1. Read the skill's most recent entry with an unresolved verdict.
2. For each unchecked `- [ ]`: did the traces since that entry actually exercise the change? Name the trace or say there is none.
3. Assign `KEEP` / `REVISED` / `REVERT` per the ladder — or leave `PENDING` **with the reason it is still unsettled** ("two runs since, neither touched this path"). A `PENDING` that carries no reason is unfinished work, not honesty.
4. Only then harvest for new patterns.

A run that settles verdicts and finds nothing new to change is a **successful run**. It closed the loop.

## Validation approaches

How to get the ≥2 independent uses that a `KEEP` requires:

| Approach | When | How |
|---|---|---|
| **Next natural use** | Default | Wait for the skill to fire on its own in real work; compare against the harvest baseline at the next run. Cheapest, and the only one that tests discoverability too. |
| **Replay** | A specific failure pattern | Re-run a previous task against the evolved skill; compare outcomes. Tests correctness, not discoverability — the replay knows where to look. |
| **Canary** | Risky or structural changes | Apply to one skill/project first, hold the siblings on the previous shape until it proves out. |

Comparison signals, generalized (each skill substitutes its own): recurrence of the pattern that motivated the change · friction markers in traces (corrections, gate skips) · whether the changed file is read at all · whether the change introduced a *new* pattern. That last one is the one people forget to look for.

## Role variants of "harvest"

| Skill | Harvest source | Turns into |
|-------|----------------|------------|
| `dev` | build commits, wiki decisions/gotchas | mode + heuristic edits |
| `business-intelligence` | win/loss debriefs, deal outcomes | framework/positioning/gate edits — learning about *the skill*, not just the deal |
| `solution-architect` | response outcomes, RFP conversion, dogfood runs | lifecycle/reference/template edits |
| `delivery` | completed engagements: estimate vs actual, contested criteria, obligation slippage | lifecycle/tracker edits — **and a correction pushed back to `solution-architect`**, since a contested criterion was written ambiguously upstream |
| `ms-ai-discovery` | workshop outcomes vs distilled method | method/script edits; validate the PDF's claims |
| `skill-builder` | skills authored + their later EVOLUTION verdicts | convention/checklist edits |
| `conductor` | run ledgers in project `wiki/log.md`; forks decided forward | routing-table + protocol edits |
| execution-layer (`omlx`, `gsheets`, `media-gen`, `zalo-platform`, `drawio`, `pptx`) | sessions that called the substrate; claims contradicted by the tool's actual behaviour | corrected claims **with the reproducing command**, trap/troubleshooting edits |
| `evolution` (this skill) | its own runs: which selections were right, which hypotheses later reverted | triage-weighting + protocol edits |

The discipline is identical; only the substrate changes. Keep the loop cheap (one retro per real engagement) — its value is compounding, not ceremony.
