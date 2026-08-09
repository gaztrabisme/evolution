# Harvest Brief — one agent, one skill

Fill and dispatch one per selected skill. They run in parallel; each returns a structured report, not prose. The synthesizer reconciles them into a single ranked hypothesis block.

---

**You are harvesting real traces for the `<SKILL>` skill. Do not edit any file.**

## Read first
- `<SKILL>/SKILL.md` and every file under `<SKILL>/references/`.
- `<SKILL>/EVOLUTION.md` — in full. The last entry with an unresolved verdict is your first job.
- `evolution/references/loop.md` — the verdict vocabulary and the non-adoption ladder.

## Step 0 — settle the open verdicts (do this before looking for anything new)
For each unchecked `- [ ]` and each `PENDING` in the most recent unresolved entry:
- Did traces since that entry actually exercise the change? **Name the trace** (commit, transcript quote, file, date) or state that none exists.
- Propose `KEEP` / `REVISED` / `REVERT` per the ladder — scoped-too-broadly → discoverable? → too heavy? → only then wrong.
- If it stays `PENDING`, say *why it is still unsettled*. A reason-free PENDING is unfinished work.

## Step 1 — harvest
Trace sources, in order of signal density. Bound the window: since the last entry's date.

| Source | Command / path | Extract |
|---|---|---|
| Skill's own git log | `git -C <SKILL> log --since=<date> --stat` | Edits made outside the loop — each is an undocumented hypothesis |
| Session transcripts | `~/.claude/projects/**/*.jsonl` | Where the skill fired, what it was asked, where the user corrected it. **Stream and filter — never read a file whole; the largest are 60 MB+** |
| Prompt history | `~/.claude/history.jsonl` | Friction lexicon: "too heavy", "unnecessary", "don't", "actually", "no,", "wrong", "just" |
| Read-once stats | `~/.claude/read-once/stats.jsonl` | Which of this skill's files are actually read; which are never opened |
| Project wikis | `Work/*/wiki/{log,decisions,gotchas}.md` | Rejected Approaches, revert post-mortems — where dev/BI/SA/delivery traces actually live |
| Downstream skills | siblings that name this one | Corrections owed upstream (e.g. delivery → solution-architect on an ambiguous criterion) |

## Step 2 — classify what you found
- **Gaps** — something the skill should have given you and didn't.
- **Friction** — ceremony that got skipped, or that the user pushed back on. Note *how many times*.
- **Contradictions** — the skill says X, the traces did Y, and Y was right.
- **Falsified claims** — a stated fact the substrate contradicted. Include the reproducing command.
- **Dead weight** — a reference nothing links and nothing reads (Wu Wei).
- **Late catches** — what a downstream review found that this skill's own gates missed.

## Output — return exactly this, nothing else

```
## <SKILL>
### Settled verdicts
- <item> → KEEP | REVISED | REVERT | PENDING(<reason>) — evidence: <trace>

### Patterns found
1. <pattern> — Impact: H/M/L, Effort: H/M/L — proof: <the trace where it bit>

### Traces examined
<what you actually read, and the window>

### Nothing-found
<what you looked for and did not find — this is a result, not a blank>
```

## Rules
- **Evidence or silence.** Every pattern names the trace that produced it. A pattern you cannot point at does not go in the list.
- **`Nothing-found` is a required section.** A harvest that reports only hits is a harvest that stopped looking early.
- Do not propose edits. Patterns only — hypothesis-writing happens at synthesis, where cross-skill duplicates get merged.
- Do not modify any file.
