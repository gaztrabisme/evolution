# Evolution Log — evolution

The loop that turns real use into skill improvements. Mechanism: `references/loop.md` (this skill owns it). Harvest source: its own runs — which triage selections turned out right, which hypotheses were later reverted, and whether the verdicts it settles stay settled.

---

## Evolution 1 — 2026-08-09 — birth by extraction, and a dogfood that caught a false statistic

### Harvest scope

**Authored**, not distilled — the machinery already existed and was fire-tested in three places; this run consolidated it. Sources: `core/references/evolution-loop.md` (the definition), `dev/modes/evolve.md` (the only executable form), `skill-builder`'s ledger skeleton and dogfood brief. All three removed at their old paths in the same day's commits; ~22 references repointed across 14 skills.

Then one **fresh-context dogfood** per `skill-builder/references/templates/dogfood-brief.md`: an agent with no prior context ran a real pass — `triage.py` over 1,067 transcripts, selection, Phase 2 settling on `skill-builder`, harvest, and five hypotheses stopped at the approval gate. Nothing was applied by the critic.

Why representative: it exercised the whole flow including the parts that only bite under real use — the selection gate, the non-adoption ladder, and the approval block. Why *not* representative: one run, one operator, and the skill was evolving the constellation it lives in, so the traces include its own construction.

### Patterns found

Ranked (Impact ÷ Effort), with the proof each bit. The dogfood returned 12 findings; these are the ones that changed the skill.

1. **A load-bearing statistic was false, in the direction that flattered the skill** — Impact: H, Effort: L. `SKILL.md` and `loop.md` both claimed "three changes ever reaching `KEEP`". Actual: `dev`, `solution-architect` and `drawio` carry a dozen between them. Inherited from an exploration summary and never verified — in a skill whose Principle 6 is "Evidence or silence". Proof: `grep -c KEEP */EVOLUTION.md`.
2. **The one artifact a human reads had no template** — Impact: H, Effort: L. `hypothesis-protocol.md` specified what the approval block must contain and shipped no shape for it. Upstream (harvest brief) and downstream (ledger skeleton) both had one; the single human gate did not. Proof: the critic had to invent the merge-and-present format while writing it.
3. **Two incompatible phase numberings for one loop** — Impact: H, Effort: L. `SKILL.md` numbered 0–6 with Triage at 1; `loop.md` numbered 0–6 without Triage. "Phases 4–6" resolved to different work in each. Proof: `SKILL.md:45` vs `loop.md:9-15` as first written.
4. **Phase 0 could not be executed where it was placed** — Impact: H, Effort: L. Settling before triage means opening all 15 ledgers, the exact cost triage exists to avoid — while `harvest-brief.md` already put settling *inside* the per-skill agent. The critic had to pick an order and contradicted the table. Proof: the two files disagreed.
5. **The triage script mined the traces its own selection gate demands, then discarded them** — Impact: M, Effort: L. `triage.md` requires a named trace per pick; the script emitted only counts. Proof: the critic hand-grepped `~/.claude/projects` to recover the two `skill-builder` invocation args the script had already parsed.
6. **"Uses since" summed incommensurable counts and included disqualified sessions** — Impact: M, Effort: L. Invocations + read-sessions were added, and reads on the entry's own date counted as "since" — including the session that *wrote* the entry, and the session then building this skill. Inflated `skill-builder` from 2 real uses to 4. Proof: session ids `1d7ef244f327` (entry date) and `610365bf08d2` (this build).
7. **The discoverability instrument had two undisclosed blind spots** — Impact: M, Effort: L. Subagent reads attribute to the parent session (under-counting the fan-out this skill prescribes), and Skill-tool injection never traverses the read hook, so **zero reads on a `SKILL.md` is evidence of nothing**. Without that, "zero reads" over-reads as "undiscoverable" for the one file that is always discoverable. Proof: `skill-builder` invoked 2026-07-14 and 2026-08-02, zero `stats.jsonl` entries on either date.
8. **Eight citations pointed at a file deleted the same day** — Impact: M, Effort: L. `dev/modes/evolve.md` was cited as a live source for a live rule. Proof: `git -C dev log --diff-filter=D` → `e2fe315`.

### Hypotheses applied

1. **Replace the KEEP count with a countable ledger-level claim** (`SKILL.md`, `references/loop.md`) — "13 of 15 ledgers had never settled a single verdict", verifiable with one grep, and the correction recorded in `loop.md` rather than quietly fixed. Closes 1.
2. **Add `references/templates/approval-block.md`** and point `hypothesis-protocol.md` and Phase 5 at it. Closes 2.
3. **One numbering, 1–7, in both files**, with Triage as Phase 1 and validation stated as "Phase 2 of a later run, not an eighth step". Closes 3 and 4.
4. **`triage.py` prints each invocation as `<date> — <args>`**, the way it already printed drift commits. Closes 5.
5. **`triage.py` reports `invoked` and `read-in` separately, never summed**, and excludes reads on or before the entry date. Closes 6.
6. **Document all three discoverability blind spots** in `triage.md`, with the inversion called out explicitly. Closes 7.
7. **Reword the eight citations as the retired predecessor** with its removal commit. Closes 8.
8. **Sharpen the `skill-builder` boundary on both sides** — lessons from a completed engagement here, lessons from documents there. The measured 2026-07-14 turn ("upgrade solution-architect with lessons distilled from the final deliverables") sat on the wrong side of both descriptions.

Not modified (validated as already-sound): the no-trace gate, the non-adoption ladder, the immutables table, the `harvest-brief.md` trace-source table. The dogfood exercised all four and reported them working — the ladder changed a verdict it had already written as `KEEP`.

### Also shipped this run (not hypotheses — integrity gaps closed on sight)

`ms-ai-discovery/EVOLUTION.md` and `harness-operator/EVOLUTION.md`, both at Evolution 0. Each skill claimed the loop and shipped no artifact for it, so the verdict each declared had nowhere to live.

### Validation results (settled by a later run's Phase 2)

- [ ] A second, independent run selects sensibly without the operator overriding triage — the selection mechanism has been exercised exactly once.
- [ ] `references/templates/approval-block.md` is actually opened during a run (check `read-once`, remembering blind spot 3 does **not** apply to a template).
- [ ] A verdict this skill settles to `KEEP` survives a later challenge — nothing has yet been settled *by* this skill and then re-examined.
- [ ] The five `skill-builder` hypotheses the dogfood produced are presented and dispositioned; they are still sitting at the approval gate, unapplied.
- [ ] The friction lexicon is checked for the opposite failure: the first draft was too broad (282 hits), the tightened version matches 115 — confirm it is not now too narrow to catch a real complaint.
- **Verdict: PENDING** — one dogfood, one operator, zero completed runs against a skill this one did not just author. The loop's own rule applies to the skill that carries it: `KEEP` needs ≥2 independent real uses, and self-evolution during construction is not one of them.

### Honest limits

The dogfood found a false claim in a file arguing against unverified claims. That is the loop working, and it is also the measure of how easily this fails: every statistic here was written with the same confidence as the wrong one, and only the ones the critic happened to check are known good. The ledger-level counts in `loop.md` are re-derivable by grep; treat anything in this skill that is not, as `PENDING` regardless of what its verdict line says.
