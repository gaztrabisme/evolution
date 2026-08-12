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

`ai-discovery-workshop/EVOLUTION.md` and `harness-operator/EVOLUTION.md`, both at Evolution 0. Each skill claimed the loop and shipped no artifact for it, so the verdict each declared had nowhere to live.

### Validation results (settled by a later run's Phase 2)

- [ ] A second, independent run selects sensibly without the operator overriding triage — the selection mechanism has been exercised exactly once.
- [ ] `references/templates/approval-block.md` is actually opened during a run (check `read-once`, remembering blind spot 3 does **not** apply to a template).
- [ ] A verdict this skill settles to `KEEP` survives a later challenge — nothing has yet been settled *by* this skill and then re-examined.
- [ ] The five `skill-builder` hypotheses the dogfood produced are presented and dispositioned; they are still sitting at the approval gate, unapplied.
- [ ] The friction lexicon is checked for the opposite failure: the first draft was too broad (282 hits), the tightened version matches 115 — confirm it is not now too narrow to catch a real complaint.
- **Verdict: PENDING** — one dogfood, one operator, zero completed runs against a skill this one did not just author. The loop's own rule applies to the skill that carries it: `KEEP` needs ≥2 independent real uses, and self-evolution during construction is not one of them.

### Honest limits

The dogfood found a false claim in a file arguing against unverified claims. That is the loop working, and it is also the measure of how easily this fails: every statistic here was written with the same confidence as the wrong one, and only the ones the critic happened to check are known good. The ledger-level counts in `loop.md` are re-derivable by grep; treat anything in this skill that is not, as `PENDING` regardless of what its verdict line says.

---

## Evolution 2 — 2026-08-12 — the first real run, and the instrument was lying in three places

### Harvest scope

The first **user-invoked** run, as opposed to Evolution 1's dogfood. `/evolution` with no target: triage over 16 skills (1,072 transcripts, 842 MB, since 2026-07-01), four selected, one harvest agent per skill in parallel, one approval block, 14 hypotheses approved as a set.

This entry exists because of what the run produced *about itself*. `evolution` had **no traces since Evolution 1 and was excluded by its own no-trace gate** — correctly. It re-entered on evidence generated by running it: three reproducible bugs in `triage.py`, each found independently by a harvest agent that had no reason to be looking. That is the gate working as intended rather than being bypassed. An excluded skill may re-enter only on traces the run itself creates, never on suspicion.

Why representative: real work, real approval, four unrelated domains. Why not: one operator, one machine, and the run was still evolving skills that live in the same tree as this one.

### Patterns found

1. **The read-once signal dropped 75% of its input** — Impact: H, Effort: L. `marker = "/Work/Skills/"` matched one of the two paths by which every skill file is reachable; 566 of 759 entries arrive via the `~/.claude/skills/` symlink. Found independently by the `skill-builder`, `omlx` and `zalo-platform` harvests, each of which had been handed a list of "unread" references and each of which discovered the list was wrong. Proof: `omlx` reported 8 unread refs; after the fix, 0.
2. **Every invocation date was the transcript's mtime** — Impact: H, Effort: L. A session still open is touched today, so its old invocations read as today's. `zalo-platform`'s "2026-08-12 consultation" was 08-06; `media-gen`'s "2026-07-16" was 07-06. Two harvests caught it separately, both while trying to reconcile a date against a project wiki.
3. **A subagent counted as an independent use of its own parent** — Impact: H, Effort: M. `uses[s] += 1` per transcript file. `zalo-platform` showed 2 invocations and had 1: a parent at `08:09:36Z` and its workflow child at `08:16:34Z`. This one is not cosmetic — `KEEP` is defined as **≥2 independent** uses, so the bug let the loop certify a change on its own echo, and it over-counts precisely the skills that follow the prescribed fan-out.
4. **Friction attribution produces false positives, not false negatives** — Impact: M, Effort: L. `zalo-platform`'s single friction hit was a JD-drafting complaint timestamped **three days before the skill existed**. The lexicon width is fine; same-session attribution is what is wrong, and Evolution 1's open question ("is it now too narrow?") was aimed at the wrong end.
5. **Agent result delivery cannot be relied on** — Impact: M, Effort: M. All four harvest agents signalled idle without returning their reports; three had completed full reports sitting in their transcripts, one had stalled at 60 tool calls and needed a direct instruction to write up. Recovering them meant reading `subagents/*.jsonl` and extracting the last assistant text block. **A fan-out phase needs a recovery path, not just a dispatch path.**

### Hypotheses applied

- **H1a** — `read_once_counts` normalises both path arms onto the tree path (`scripts/triage.py`). Closes 1.
- **H1b** — invocations dated from the record's own `timestamp`, mtime only as fallback (`scripts/triage.py`). Closes 2.
- **H1c** — `_session_key` collapses subagent transcripts onto their parent; `uses` counts distinct parent sessions; files sorted parents-first so the retained invocation is the user's. `references/triage.md` corrected — it documented the subagent effect as under-counting, which is true for reads and backwards for invocations. Closes 3.

Measured on the fixed script: unread refs `omlx` 8→0, `media-gen` 4→0, `solution-architect` 17→7, `delivery` 8→1; `zalo-platform` invoked 2→1 and dated 08-06; `media-gen` dated 07-06.

Not applied, and named so they are not silently lost: pattern 4 (friction attribution — the fix is per-turn attribution, which is a bigger change than this run should make on one instance) and pattern 5 (agent recovery path — belongs in `harvest-brief.md` or the Phase 3 dispatch guidance, and needs a second occurrence before I know whether it is the harness or the brief).

### Validation results

Settling Evolution 1's list, from this run:

- **A second, independent run selects sensibly without the operator overriding triage** → **REVISED**. The ranking held: all four picks returned real findings and every skip survived scrutiny. But it held *despite* three corrupted columns, so what was validated is the ranking's robustness, not the numbers. The operator also re-added one skill (`evolution`) on new evidence — a legitimate override the mechanism has no rule for. New selector: re-validate on a run whose inputs are correct. Inherits `PENDING`.
- **`approval-block.md` is actually opened during a run** → **PENDING** (opened and followed once, this run; the standard is ≥2 independent uses and this is the first).
- **A verdict settled to `KEEP` survives a later challenge** → **PENDING** (this run settled the skill's first-ever `KEEP` — `skill-builder`'s dogfood brief, on 3 independent uses. Nothing has re-examined it yet, which is exactly the point of the box).
- **The five `skill-builder` hypotheses from the dogfood are dispositioned** → **PENDING**, but no longer lost: the harvest recovered the full block from the 2026-08-09 transcript and it is now written into `skill-builder/EVOLUTION.md` Evolution 2. Still unapplied.
- **The friction lexicon is not too narrow** → **REVISED**. Wrong question. It is not too narrow; it is mis-attributed. See pattern 4. New selector inherits `PENDING`.

New, for a later run to settle:

- [ ] Re-run triage on corrected inputs and confirm the selection would have been the same — if the fixed numbers would have picked different skills, the ranking is less robust than this entry claims.
- [ ] No skill's `invoked` exceeds its count of distinct parent sessions.
- [ ] A reference previously reported unread turns out to have been read all along in some *other* skill — i.e. check whether H1a changed any earlier `REVERT`-leaning judgement that was already acted on.
- [ ] Whether the agent-delivery failure recurs, and whether it is the harness or the brief.

**Verdict: PENDING** on all three hypotheses. They were measured on this run's data and predicted correctly, and a change is not validated by having just been written.

### Honest limits

Two runs now, and both found that the loop's own instrument was misreporting. Evolution 1 found a false statistic in the file arguing against false statistics; Evolution 2 found that the selection table was wrong in three columns while being right in its conclusions. The pattern to watch is not "the numbers are wrong" — it is that **this skill's failures are all in the measuring, and the measuring is what everything else is built on**. Every remaining number in `triage.py`'s output has had exactly as much scrutiny as the three that turned out wrong, which is to say: it was believed until someone checked.

Also worth stating plainly: the harvest agents caught all three bugs, and the parent session caught none of them from the table alone. The table looked completely reasonable. Fan-out is not just parallelism here — it is the only reason these were found.
