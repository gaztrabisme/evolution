---
name: evolution
description: "Evolve the skills themselves from their own real traces — pick which ones have earned a change, harvest the evidence, propose specific edits, apply them, and settle the verdicts previous runs left open. USE WHEN you say evolve/meta/improve my skills (with or without naming one), when a gate keeps getting skipped or a correction keeps recurring, after a stretch of real use, or when EVOLUTION.md ledgers have gone stale at PENDING. Not `skill-builder` — that authors and shapes a skill at birth, and distils lessons from *documents*; this upgrades a working skill from lessons in *completed real work*. Not `core` — that states the gate; this is the mechanism. Keywords: evolve, evolution, meta, self-improve, retrospective, harvest, EVOLUTION.md, PENDING, KEEP, REVISED, validate, skill drift, lessons learned, upgrade the skill, what went wrong, improve the skill, triage skills, post-engagement retro."
license: MIT
---

# Evolution

Turns the constellation's own traces into skill improvements. You invoke it without naming a target: it reads the evidence, picks the skills that have earned a change, and runs the loop on them — settling what the last run left open before proposing anything new.

> Inherits the `core` kernel — see `../core/SKILL.md`. Obey its Integrity Constraints; declare its gates; reference its files, don't copy them.

## When it fires — and when a sibling owns it

- **This skill:** "evolve my skills", "meta session", "improve the skill", "what have we learned" — and the unprompted cases: a gate the user keeps skipping, a correction that has recurred, a ledger stuck at `PENDING` while the skill kept being used.
- **`skill-builder` instead:** creating a new skill, splitting/merging, distilling a methodology, fixing frontmatter or structure, publishing. Birth and shape.
- **`core` instead:** you want the canonical statement of an inherited gate. `core` spine #8 declares that skills must evolve; this skill is *how*.
- **`dev` instead:** the thing being improved is software, not a skill.

> **Disambiguation:** on **artifact**. `skill-builder` produces a skill that didn't exist or a structure that was wrong. `evolution` produces a **diff plus a ledger entry** on a skill that already works, justified by a trace. When a refine needs both — new structure *and* evidence — `skill-builder` shapes it and hands the ledger step here.

## Principles

1. **No trace, no change.** A skill with no use since its last entry is excluded from the run, not deprioritized. An invented pattern applied as a real edit is the exact failure this discipline exists to prevent.
2. **Settle before you harvest.** Phase 2 resolves the previous entry's open verdicts *before* looking for new patterns. This is the half of the loop that never ran: measured 2026-08-09, **13 of 15 ledgers had never settled a single verdict** — only `dev` and `solution-architect` ever moved anything off `PENDING`. A run that only settles verdicts and finds nothing new is a successful run.
3. **Non-adoption is a scoping signal before it is a validity signal.** Before `REVERT`, ask in order: scoped too broadly (→ add a selector, verdict `REVISED`) · undiscoverable · too heavy · only then wrong. Collapsing these teaches the loop never to generalize.
4. **A hypothesis names a file.** "Improve X" is a pattern, not a hypothesis. If you can't predict which future trace changes, it can't be validated and it will sit at `PENDING` forever.
5. **One approval stop.** Everything up to writing runs unattended; the whole hypothesis set is presented once. Never self-modify without approval — and never weaken an Integrity Constraint or the Wu Wei filter at all.
6. **Evidence or silence.** Every pattern names the trace that produced it. Every skipped skill gets a one-line skip reason. A skip by omission is an oversight wearing the costume of focus.

## The flow (at a glance)

| Phase | Goal | Primary artifact |
|---|---|---|
| **1 Triage** | Score every skill on evidence; pick 3–5; state a skip reason for the rest | candidate table (`scripts/triage.py`) |
| **2 Settle** | *Per selected skill, before harvesting it:* resolve the last entry's open `- [ ]` and `PENDING` → `KEEP` / `REVISED` / `REVERT`, or `PENDING` *with a stated reason*. `KEEP` needs **≥2 independent real uses** | verdict updates in that ledger |
| **3 Harvest** | Gather that skill's real traces since its last entry | harvest report per skill |
| **4 Patterns** | Rank recurring gaps/friction by Impact ÷ Effort, each with its proof | ranked pattern list |
| **5 Hypotheses** | One specific edit per pattern. **Stop for approval — the whole set at once.** | approval block (`references/templates/approval-block.md`) |
| **6 Apply** | Edit; one commit per hypothesis, in the skill's own repo | diffs |
| **7 Record** | The entry, verdict `PENDING`, with the checklist a future Phase 2 will settle | `<skill>/EVOLUTION.md` |

Phases 2–4 run **inside** one agent per selected skill, in parallel — settling is scoped to the skills triage picked, never to all 15 ledgers. Phase 5 reconciles them into a single block. This numbering is the same in `references/loop.md`; nowhere in this skill does a bare phase number mean two things.

Run it: `python3 evolution/scripts/triage.py` from the Skills root (add `--fast` to skip transcript mining), then dispatch `references/templates/harvest-brief.md` per selected skill.

**Scale to the ask.** "Evolve everything" gets the full run. "That gate was unnecessary" gets phases 5–7 on one skill — the trace already exists, it's the user's own sentence, and the retired `dev` evolve mode's rule was to trim immediately rather than wait for a cycle. Ceremony on a one-line correction is the anti-pattern, not the discipline.

## Gates (declared, inherited from core)

- **Grounding gate** — substrate is the trace corpus: `<skill>/EVOLUTION.md`, per-skill `git log`, `~/.claude/projects/**/*.jsonl`, `~/.claude/history.jsonl`, `~/.claude/read-once/stats.jsonl`, project `wiki/`. Record `Grounded: <traces read, window> → <what constrains this run>`. See `../core/references/grounding-gate.md`.
- **Output Contract** — a run is not done until every touched skill has an `## Evolution N` entry on disk with an honest verdict. "I improved it" is a proxy; the ledger is the artifact. See `../core/references/wiki-protocol.md`.
- **Pushback & teach** — when a requested change would weaken a gate, say so and explain the mechanism rather than applying it quietly. See `../core/references/pushback-and-teach.md`.
- **Approach declaration** — state the engine before dispatch: inline for a single-skill trim, fan-out for a multi-skill run. (core SKILL.md §7.)
- **Integrity constraints** — especially: never mark `KEEP` on the same run that applied the change, and never silently drop a skill from the run without naming it.

## Anti-patterns (hard no-list)

- **Evolving a skill with no traces.** The gate is absolute; "it's probably stale" is not evidence.
- **Skipping step 0** because new patterns are more interesting than old verdicts. This is why the ledgers stalled.
- **`REVERT` where `REVISED` was right** — throwing away working machinery because it was described too broadly.
- **A hypothesis with no target file**, or several edits bundled under one so the count looks tidy.
- **Recording `KEEP` on application day.** Nothing is validated by having just been written.
- **Reading whole transcripts.** The largest session files exceed 60 MB; stream and filter or the triage costs more than the evolution.
- **A `PENDING` with no reason.** That is unfinished work, not honesty.
- **Weakening an Integrity Constraint or the Wu Wei filter.** A self-modifying system's first optimization is always to relax what constrains it.

## Composition

- **Inherits:** `core` — integrity constraints, gate-by-artifact, grounding gate, wiki protocol, pushback-and-teach.
- **Owns, because it was scattered:** the loop definition (from `core`), the executable cycle (from the retired `dev` evolve mode), the ledger skeleton (from `skill-builder`), and — new — the triage that picks the targets.
- **Hands off to:** `skill-builder` when a hypothesis turns out to need new structure rather than new content; `dev` when the finding is about software rather than a skill.
- **Consumed by:** every skill in the constellation. Each ledger's preamble points here for the mechanism.
- **Origin:** extracted 2026-08-09 from the loop definition then in `core`, the evolve mode then in `dev`, and `skill-builder`'s ledger template — all three removed at their old paths in that day's commits, after the constellation reached 15 skills and 13 ledgers with no way to decide which one to open.

## References

- `references/loop.md` — the canonical loop, the `PENDING/KEEP/REVISED/REVERT` vocabulary, the non-adoption ladder, settle-first, validation approaches, per-role harvest sources.
- `references/triage.md` — the selection mechanism: signals, the no-trace gate, what the discoverability data can and cannot prove, how to choose and how to record a skip.
- `references/hypothesis-protocol.md` — hypothesis format, the five rules, what may and may not be modified, the approval gate, commit and record discipline.
- `references/templates/approval-block.md` — the Phase 5 artifact: settled verdicts, ranked hypotheses, the rejected list, blast radius, the ask. The one thing a human reads.
- `references/templates/EVOLUTION.md.skeleton` — the ledger shape a new skill starts from.
- `references/templates/harvest-brief.md` — the per-skill harvest agent brief, including the trace-source table and the required `Nothing-found` section.
- `scripts/triage.py` — computes the candidate table from ledgers, git logs, read-once stats, prompt history and session transcripts. `--fast` skips transcripts.
