# Approval Block — the one artifact a human reads

Phase 5's output. The single human gate in the loop, and the only moment the run is asked to justify itself to someone who was not watching it.

It must be judgeable **without opening anything else**: per-hypothesis, so a subset approval is meaningful; blast radius visible before the diff exists; and the discards shown, because a hypothesis list with no rejections means the Wu Wei filter never ran.

One block for the whole run, not one per skill. Reconcile duplicates across skills before presenting — the same pattern found in three places is one hypothesis with three target files, not three hypotheses.

---

## Run scope

- **Triaged:** <N skills> · **selected:** <names> · **excluded by the no-trace gate:** <names>
- **Traces read:** <windows, per skill — "dev: 3 commits + 2 sessions since 2026-07-28">
- **Settled this run:** <n> verdicts → <k> KEEP, <k> REVISED, <k> REVERT, <k> still PENDING (with reasons)

## Verdicts settled (Phase 2)

| Skill | Item | Verdict | Evidence that settled it |
|---|---|---|---|
| | | | |

Settling is the half that historically never ran, so it leads. A run that settles verdicts and proposes nothing is complete and should be presented as such.

## Hypotheses

Ranked by Impact ÷ Effort, across all selected skills. Full format per `../hypothesis-protocol.md`.

### H1: <short name> · `<target-skill>`
**Pattern:** <observation + the trace proving it>
**Root cause:** <mechanism>
**Proposed change:** <the specific edit>
**Target file(s):** <exact paths>
**Predicted effect:** <what changes in future traces, observably>
**Risk:** <what could get worse>
**Validation:** <what a future Phase 2 checks>
**Impact / Effort:** H|M|L / H|M|L

### H2: …

## Rejected during pattern-mining

| Candidate | Why rejected |
|---|---|
| | |

Empty is a red flag, not a clean sheet. If nothing was discarded, either the harvest was thin or the Wu Wei filter was skipped — say which.

## Blast radius

- **Files touched if all approved:** <list>
- **Anything in `core`, any frontmatter, any script, any workflow phase:** <call these out explicitly — they are `Approval only` per the protocol, and their blast radius is the constellation>
- **Commits:** <n> (one per hypothesis) + <k> ledger commits, in each skill's own repo
- **All ship at verdict `PENDING`.**

## The ask

> Approve **all** / a **subset** (name them) / **none**. Nothing has been applied.

---

## Rules for writing it

- **No hypothesis without a target file.** If it isn't there yet, it's a pattern; leave it in the harvest, not here.
- **Never present a `KEEP` you assigned this run to a change applied this run.** Nothing is validated by having just been written.
- **Say what you did not look at.** A run that skipped a trace source names it — silent partial coverage reads as full coverage.
- **Keep it scannable.** If the block needs a second reading to approve a subset, it has failed at its one job.
