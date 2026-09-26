# Triage — picking which skills to evolve

The loop assumes you already know what to work on. Across 15 constellation skills you don't. Triage is the step that turns "evolve my skills" into a defensible short list, and its output is **evidence, not a ranking you have to trust**.

`scripts/triage.py` computes the signals. This file says what they mean and how to choose. The script proposes; the selection agent disposes.

## The gate that comes first

**No new traces since the last entry → do not evolve that skill.** Not "low priority" — excluded. Evolving a skill nothing has used since its last harvest means inventing patterns, and an invented pattern applied as a real edit is the failure mode this whole discipline exists to prevent. The retired `dev` evolve mode stated it as "when NOT to evolve: after a single build, mid-build, when traces are sparse." It is a gate, not a preference.

The one exception: a skill with **no ledger at all** is always a candidate, because the missing artifact is itself the finding.

## Signals

| Signal | Source | Reads as | Weight |
|---|---|---|---|
| **Validation debt** | unchecked `- [ ]` and `PENDING` verdicts in `<skill>/EVOLUTION.md` | Open questions the loop already committed to answering. Highest value because settling them is cheap and it is the half that never runs. | Highest |
| **Usage since last entry** | `Skill` tool_use entries in `~/.claude/projects/**/*.jsonl`; project tags in `~/.claude/history.jsonl` | **The gate.** Zero → excluded. Also the denominator for everything else: 40 uses with no friction is a different signal from 2 uses with no friction. | Gate |
| **Undigested drift** | `git -C <skill> log --since=<last entry date>` | Edits made outside the loop. Each is an undocumented hypothesis — someone changed the skill and no ledger records why or what would falsify it. | High |
| **Friction markers** | `history.jsonl` `.display` fields and user turns in transcripts, matched against the friction lexicon | The "that was unnecessary" / "too heavy" / "actually, no" signal. The retired `dev` evolve mode said to act on a repeatedly-skipped gate *immediately*, without waiting for a formal cycle. | High |
| **Discoverability** | `~/.claude/read-once/stats.jsonl` filtered to `Documents/Work/tools/skills/` | Per-file read counts. A reference with zero reads is either dead weight (Wu Wei: trim it) or undiscoverable (nothing points at it). Distinguish by grepping whether `SKILL.md` links it. | Medium |
| **Missing ledger** | no `EVOLUTION.md` on a skill whose `SKILL.md` claims the spine | Integrity gap: the skill declared a gate and ships no artifact for it. | Always a candidate |
| **Age** | days since last entry | Weak on its own. A stable skill that nothing has needed to change is *working*, not neglected. Use only to break ties. | Lowest |

### On the discoverability signal

This is the one genuinely new instrument, and it is worth understanding before trusting it. `~/.claude/read-once/stats.jsonl` exists to deduplicate file reads, but as a side effect it is a complete log of which skill files were actually opened, when, by which session, and at what token cost.

That makes step 2 of the non-adoption ladder — *"was it discoverable?"* — answerable with a number for the first time. Previously, when a change went unused, you had to guess whether it was wrong or merely buried. Now:

- Reference exists, `SKILL.md` links it, **zero reads** → undiscoverable in practice, or the link is in a section nobody reaches. `REVISED`, not `REVERT`.
- Reference exists, **nothing links it**, zero reads → orphan. Trim it (Wu Wei) or wire it in.
- Reference read often, change still unused → now you have a real validity signal.

**Three blind spots, all measured — disclose them whenever you cite this signal.**

1. **The window.** The log starts when the read-once hook was installed; a file read before that is invisible. Zero reads is evidence of non-reading only over the window the log covers. State the window.
2. **Subagent reads are attributed to the parent session.** A parent plus N harvest agents collapses into one session id. Since per-skill fan-out is this skill's own Phase 3 architecture, the instrument systematically under-counts the very consumption pattern the skill prescribes. Use read *counts*, not distinct-session counts, when the question is "was this file opened at all".

   **For invocations the same collapsing runs the other way, and that direction is dangerous.** A subagent writes its own transcript under `<session-uuid>/subagents/`, so counting transcript *files* splits one consultation into several. Measured 2026-08-12: `zalo-platform` showed two invocations and had one — a parent at `08:09:36Z` and its own workflow child at `08:16:34Z`, same session, same task. `KEEP` is defined as **≥2 independent real uses**, so this let the loop certify a change on its own echo. `triage.py` now counts distinct *parent sessions* (`_session_key`). Reads are still counted per event; only invocations collapse.
3. **Skill-tool injection does not traverse the hook.** When a skill fires via the `Skill` tool, its `SKILL.md` is injected, not `Read`. So a `SKILL.md` can have zero recorded reads across sessions that used it heavily. **Zero reads on a `SKILL.md` is evidence of nothing.** The signal is only meaningful for `references/` and `scripts/` — the files an agent must choose to open.

Blind spot 3 is the sharp one: it inverts the inference. Without it you will read "zero reads" as "undiscoverable" for exactly the file that is always discoverable.

### Two limits that keep the numbers honest

**The current session is invisible.** Transcripts are read from disk, and the session you are running in has not been flushed. A skill invoked *this turn* shows zero uses. Never conclude "unused" about a skill you just used — check the table against what you know you did.

**A "use" is an invocation *or* a read.** `core` and `conductor` are consumed by being read, not by a `Skill` tool call. Counting only tool-use reported the kernel every other skill inherits as unused, which would have excluded it from every run forever. The script counts distinct sessions that read a skill's files as uses too; either satisfies the gate.

## Scoring

The script emits per-skill rows, not a single number, because the signals are not commensurable and collapsing them hides the reason:

```
| skill | last entry | invoked | read-in | unchecked | PENDING | drift | friction | unread refs |
```

`invoked` and `read-in` stay in separate columns deliberately — they are different kinds of evidence and summing them produces a number that means nothing. Either one satisfies the gate.

Rank by validation debt first, then friction, then drift. Usage gates every row.

## Selection

Hand the table plus the candidate ledgers to a selection agent and have it think hard. Its output is a decision, and it is subject to gate-by-artifact like everything else:

**For each skill it picks:** name the specific trace that justifies the pick — a commit hash, a transcript quote, an unchecked box, a file with zero reads. "Seems stale" is not a trace.

**For each skill it skips:** one line on why. A skip with a stated reason is a decision; a skip by omission is an oversight wearing the costume of focus.

**Cap the run.** Three to five skills is a working session. More than that and the hypothesis block becomes unreviewable, which defeats the single approval stop.

Prefer, in this order:
1. Skills with settleable validation debt (cheap, closes the loop, no new hypotheses needed).
2. Skills with friction markers (the user has already told you something is wrong).
3. Skills with undigested drift (undocumented changes accumulating).
4. Skills missing a ledger entirely.

Deprioritize: a skill evolved in the last run (let the change breathe — you cannot validate what has not been used); a skill whose only signal is age.

## What triage must not do

- **Score a skill into the run that has no traces.** The gate is absolute.
- **Rank on volume of open items.** A ledger with 12 unchecked boxes and no uses since is not the top candidate; it is a stalled one. Uses since the entry is what makes debt settleable.
- **Treat a quiet skill as a failing skill.** Nothing needed changing is the most common reason nothing changed.
- **Read whole transcripts.** The session files run to 63 MB. Stream and filter, or the triage costs more than the evolution.
