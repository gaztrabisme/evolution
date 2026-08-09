# Hypothesis Protocol

How a harvested pattern becomes an approved edit. Generalized from `dev/modes/evolve.md` Phases 3–4, which scoped this to one skill for reasons that were historical rather than principled.

## From pattern to hypothesis

A pattern is an observation. A hypothesis is a **falsifiable edit**. The gap between them is where most evolution runs go wrong — "improve integration guidance" is a wish; "add an integration-patterns section to `nfr-checklist.md` and point Phase 3 at it" is a change you can later prove worked or didn't.

```markdown
### H<n>: <short name>  ·  <target-skill>

**Pattern:**        <what was observed, with the trace that proves it>
**Root cause:**     <why it happens — the mechanism, not the symptom>
**Proposed change:** <the specific modification>
**Target file(s):** <exact paths>
**Predicted effect:** <what should change in future traces, observably>
**Risk:**           <what could get worse>
**Validation:**     <what a future step-0 should look for to settle this>
**Impact / Effort:** H|M|L / H|M|L
```

## The five rules

1. **One change per hypothesis.** No bundles. A bundle cannot be reverted cleanly and cannot be validated at all — when it half-works you learn nothing.
2. **Specific, not vague.** If the hypothesis doesn't name a file, it isn't one yet.
3. **Predict the effect.** If you can't state which future trace would change, the hypothesis is too vague to validate — and it will sit at `PENDING` forever, which is how the constellation got 12 stuck ledgers.
4. **State rollback criteria.** "If the next two runs still show X, revert." Written now, while you still believe in it, not later when you're defending it.
5. **Wu Wei filter.** Does this pattern cause a failure you can point to, or is it theoretical purity? Structure earns existence by being referenced. A gate nobody trips is cost wearing the costume of rigour.

## What may be changed

| Component | Evolution may change it | Why |
|---|---|---|
| Heuristics, reference content, examples, traps | Yes | The substrate the loop exists to refine. |
| Subagent/brief prompts | Yes | Directly measurable in later traces. |
| Trigger words, mode detection | Yes | With the sibling-collision check re-run. |
| Thresholds, process weights | Yes | These are exactly what real use calibrates. |
| Workflow phases (add / remove / reorder) | **Approval only** | Changes the skill's shape, not its content. |
| `description` frontmatter | **Approval only** | It is the retrieval surface; a bad edit silently stops the skill firing. |
| Scripts | **Approval only** | Functional change, not instruction. |
| Anything in `core` | **Approval only** | Every skill inherits it; blast radius is the constellation. |
| **Integrity Constraints** | **Never** | Foundational. A loop that can weaken its own honesty rules is not a loop, it is a ratchet in the wrong direction. The human edits these directly. |
| **The Wu Wei filter** | **Never** | Philosophy doesn't optimize; it guides. |

The two `Never` rows exist because a self-modifying system's first optimization is always to relax whatever constrains it. They are inherited, verbatim, from `dev/modes/evolve.md` — the one part of that file that was never scoped to `dev`.

## The approval gate

**STOP.** Present the *entire* hypothesis set — every selected skill's hypotheses in one block, ranked by Impact ÷ Effort, each with its target file and predicted effect. The human approves the set, a subset, or none.

One stop, not one per skill. The whole point of front-loading is that approval is a single interaction: triage, harvest and pattern-mining run unattended, and the human is asked exactly once, at the moment the run is about to write to disk.

What the block must make possible without opening anything else:
- Judging each hypothesis on its own (so a subset approval is meaningful).
- Seeing which files change, so blast radius is visible before the diff exists.
- Seeing what was *rejected* during pattern-mining and why — a hypothesis list with no discards means the Wu Wei filter didn't run.

Never self-modify without approval. A convenient exception is how this stops being a loop and starts being drift.

## Applying

1. **Edit** — smallest change that closes the pattern. Match the surrounding voice; skills are read by humans and by fresh-context agents, and both notice a section written in a different register.
2. **Commit, one per hypothesis**, in the *skill's own git repo* (each skill is its own repo; the outer `Skills` repo is not live). Message shape, following the established convention:
   ```
   Evolve H2: cover the axis, not an example
   ```
   Body carries the hypothesis's pattern and predicted effect.
3. **Record** — the ledger entry, then a separate commit for it:
   ```
   Evolution 9 log: <theme, including the honest limits>
   ```
4. **Verdict `PENDING`** on everything applied, with the validation checklist a future step 0 will settle. An applied change is a hypothesis until traces say otherwise — including the ones you are confident about, especially those.

## Anti-patterns

- A hypothesis with no target file — it's still a pattern.
- Bundling several edits under one hypothesis to reduce the count.
- Applying anything before the approval gate.
- Writing a validation checklist that no future run could actually check ("confirm the skill feels better").
- Recording `KEEP` on the same run that applied the change. Nothing is validated by having just been written.
- Skipping the ledger entry because the change was small. That is precisely the change nobody will remember making.
