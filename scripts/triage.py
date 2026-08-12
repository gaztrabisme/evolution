#!/usr/bin/env python3
"""Triage: which skills have earned an evolution run?

Computes the signals defined in ../references/triage.md and emits a markdown
candidate table. It proposes; the selection agent disposes -- every number here
is a pointer to a trace, not a verdict.

    python3 triage.py                 # full run, includes transcript mining
    python3 triage.py --fast          # skip transcripts (seconds instead of ~a minute)
    python3 triage.py --skill dev     # one skill, full detail

Stdlib only. Reads nothing outside ~/.claude and the skills tree; writes nothing.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
SKILLS_ROOT = Path(__file__).resolve().parent.parent.parent
CLAUDE = HOME / ".claude"
PROJECTS = CLAUDE / "projects"
HISTORY = CLAUDE / "history.jsonl"
READ_ONCE = CLAUDE / "read-once" / "stats.jsonl"

# Ledger headings, in every convention present in the tree. `delivery` starts at
# Evolution 0; `zalo-platform` uses Birth / Round N. Parsing must not require
# them to have been normalised -- rewriting a ledger's body rewrites the record
# of what was actually thought at the time.
ENTRY_RE = re.compile(
    r"^##\s+(?:Evolution\s+(?P<num>\d+)|(?P<birth>Birth)|Round\s+(?P<round>\d+))\b(?P<rest>.*)$",
    re.IGNORECASE,
)
DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
# The record's own clock, for dating a trace. Cheap enough to run per matching
# line; a full json.loads on every Skill line would cost more than the mining.
TS_RE = re.compile(r'"timestamp":"(\d{4}-\d{2}-\d{2})')
UNCHECKED_RE = re.compile(r"^\s*[-*]\s+\[ \]")
PENDING_RE = re.compile(r"\bPENDING\b")

# What a user says when a skill got in the way. Deliberately narrow: broad
# matching turns ordinary conversation into a friction signal and the number
# stops meaning anything. An earlier draft included "no, ", "wrong " and
# "i said" -- they matched half of every normal session, which is how a signal
# becomes noise while still looking like data.
FRICTION = [
    "too heavy", "unnecessary", "overkill", "don't need", "dont need",
    "no need for", "stop doing", "skip that", "too much ceremony",
    "that was wrong", "you're wrong", "youre wrong", "not what i asked",
    "that's not what i", "thats not what i", "undo that", "too verbose",
    "over-engineered", "overengineered", "way too much", "didn't ask for",
    "didnt ask for",
]


def log(msg: str) -> None:
    print(msg, file=sys.stderr)


# --------------------------------------------------------------------------- #
# Skills                                                                       #
# --------------------------------------------------------------------------- #

# Constellation members that fail every automatic membership test below.
# `harness-operator` is deliberately thin (no references/, no git repo, and it
# mines its siblings rather than referencing core) -- it drops out of this set
# the moment it ships a ledger, which is itself one of the findings.
EXTRA_MEMBERS = {"harness-operator"}

# Corpora and build artefacts. These are content the skill *carries*, not
# references it asks an agent to read, so counting their reads says nothing
# about discoverability.
SKIP_DIRS = {"__pycache__", "knowledge-base", "source", "research-sprint",
             "node_modules", "templates_bin", ".git"}
DOC_EXT = {".md", ".skeleton", ".py", ".sh"}


def is_member(skill: Path) -> bool:
    """Constellation member, or a vendored third-party skill sharing the tree?

    A member has its own git repo, or a ledger, or references the core kernel.
    Vendored skills (docx, xlsx, get-api-docs) have none of the three -- and
    evolving them would mean editing someone else's work.
    """
    if skill.name in EXTRA_MEMBERS:
        return True
    if (skill / ".git").exists() or (skill / "EVOLUTION.md").is_file():
        return True
    try:
        return "../core/" in (skill / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False


def discover_skills() -> list[Path]:
    """Own skills only: a real directory in this tree carrying a SKILL.md.

    Symlinked-in third-party skills are excluded -- they carry no ledger and
    edits would land outside this tree.
    """
    out = []
    for child in sorted(SKILLS_ROOT.iterdir()):
        if child.name.startswith(".") or child.is_symlink() or not child.is_dir():
            continue
        if (child / "SKILL.md").is_file() and is_member(child):
            out.append(child)
    return out


def parse_ledger(skill: Path) -> dict:
    """Last entry, its date, and the debt it left open."""
    led = skill / "EVOLUTION.md"
    if not led.is_file():
        return {"exists": False, "last_label": None, "last_date": None,
                "unchecked": 0, "pending": 0, "entries": 0}

    lines = led.read_text(encoding="utf-8", errors="replace").splitlines()
    starts = []  # (line_index, label)
    for i, line in enumerate(lines):
        m = ENTRY_RE.match(line)
        if not m:
            continue
        if m.group("num") is not None:
            label = f"Evolution {m.group('num')}"
        elif m.group("birth"):
            label = "Birth"
        else:
            label = f"Round {m.group('round')}"
        starts.append((i, label, m.group("rest") or ""))

    if not starts:
        return {"exists": True, "last_label": None, "last_date": None,
                "unchecked": 0, "pending": 0, "entries": 0}

    last_i, last_label, last_rest = starts[-1]
    body = lines[last_i:]

    dm = DATE_RE.search(last_rest) or DATE_RE.search("\n".join(body[:6]))
    last_date = dm.group(0) if dm else None

    return {
        "exists": True,
        "last_label": last_label,
        "last_date": last_date,
        "unchecked": sum(1 for l in body if UNCHECKED_RE.match(l)),
        "pending": sum(1 for l in body if PENDING_RE.search(l)),
        "entries": len(starts),
    }


def git_drift(skill: Path, since: str | None) -> tuple[int, list[str]]:
    """Commits to the skill's own repo since its last entry -- undocumented hypotheses."""
    if not (skill / ".git").exists():
        return (0, [])
    cmd = ["git", "-C", str(skill), "log", "--oneline", "--no-merges"]
    if since:
        cmd.append(f"--since={since}")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except (subprocess.SubprocessError, OSError):
        return (0, [])
    if r.returncode != 0:
        return (0, [])
    commits = [l for l in r.stdout.splitlines() if l.strip()]
    return (len(commits), commits[:5])


# --------------------------------------------------------------------------- #
# Signals                                                                      #
# --------------------------------------------------------------------------- #

def read_once_counts() -> tuple[dict[str, int], dict[str, list[tuple[float, str]]], str | None]:
    """Per-file read counts from the read-once hook log, plus per-skill read events.

    Returns (counts_by_path, {skill: [(ts, session)]}, window_start).

    The read events matter as much as the counts: `core` and `conductor` are
    consumed by *reading*, not by a Skill invocation, so counting only tool-use
    would report them as unused and exclude them from every run -- which is
    exactly backwards for the kernel every other skill inherits.

    Zero reads is evidence of non-reading only over the window this log covers.
    Callers must state the window.
    """
    counts: dict[str, int] = {}
    reads: dict[str, list[tuple[float, str]]] = {}
    earliest = None
    if not READ_ONCE.is_file():
        return counts, reads, None
    # Every skill file is reachable by two paths: the tree's own
    # `.../Work/Skills/<skill>/...` and `~/.claude/skills/<skill>/...`, which is
    # a symlink to it. The hook logs whichever path the reader used, and *75% of
    # reads arrive under the symlink* (566 of 759, measured 2026-08-12). Matching
    # one arm reported 6 of 8 zalo digests and 5 of 5 omlx references as
    # never-opened when several had been read -- a measurement artifact that
    # reads exactly like a "trim this, nothing opens it" verdict. Normalise both
    # arms onto the tree path so `unread_refs` compares like with like.
    markers = ("/Work/Skills/", "/.claude/skills/")
    with READ_ONCE.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not any(m in line for m in markers):
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            raw = rec.get("path", "")
            tail = next((raw.split(m, 1)[1] for m in markers if m in raw), None)
            if tail is None:
                continue
            p = str(SKILLS_ROOT / tail)
            counts[p] = counts.get(p, 0) + 1
            ts = rec.get("ts")
            if isinstance(ts, (int, float)):
                if earliest is None or ts < earliest:
                    earliest = ts
                name = tail.split("/", 1)[0]
                reads.setdefault(name, []).append((float(ts), rec.get("session", "")))
    window = (datetime.fromtimestamp(earliest, tz=timezone.utc).strftime("%Y-%m-%d")
              if earliest else None)
    return counts, reads, window


def unread_refs(skill: Path, counts: dict[str, int]) -> list[str]:
    """Reference/script files with zero recorded reads.

    Either dead weight (Wu Wei: trim) or undiscoverable (nothing points at it).
    Distinguish by grepping whether SKILL.md links them -- this only finds them.
    """
    out = []
    for sub in ("references", "scripts", "modes"):
        d = skill / sub
        if not d.is_dir():
            continue
        for f in sorted(d.rglob("*")):
            if not f.is_file() or f.name.startswith("."):
                continue
            if f.suffix not in DOC_EXT:
                continue
            if SKIP_DIRS & set(f.relative_to(skill).parts):
                continue
            if counts.get(str(f), 0) == 0:
                out.append(str(f.relative_to(skill)))
    return out


def history_friction() -> list[tuple[float, str, str]]:
    """(timestamp_seconds, project, prompt) for prompts carrying friction markers."""
    hits = []
    if not HISTORY.is_file():
        return hits
    with HISTORY.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            low = line.lower()
            if not any(f in low for f in FRICTION):
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            disp = (rec.get("display") or "").strip()
            if not disp:
                continue
            ts = rec.get("timestamp", 0)
            hits.append((ts / 1000.0 if ts > 1e11 else float(ts),
                         rec.get("project", ""), disp))
    return hits


def _session_key(path: Path) -> str:
    """The parent session a transcript belongs to.

    A subagent writes its own `.jsonl` under `<session-uuid>/subagents/...`, so
    counting *files* counts one consultation as several. `zalo-platform` showed
    two invocations and had one: a parent at 08:09:36Z and its own workflow
    child at 08:16:34Z -- same session, same project, same task.

    That matters more than a tidy number. `KEEP` is defined as **>=2
    independent real uses**, so a bug that splits one use into two lets the loop
    certify its own changes on its own echo. Collapse children onto their parent.
    """
    parts = path.parts
    if "subagents" in parts:
        i = parts.index("subagents")
        return "/".join(parts[max(0, i - 2):i])
    return f"{path.parent.name}/{path.stem}"


def mine_transcripts(cutoff_ts: float) -> tuple[dict[str, int], dict[str, int],
                                                dict[str, list[str]], dict[str, list[str]]]:
    """Stream session transcripts for Skill invocations and in-session friction.

    Never reads a file whole into memory -- the largest sessions exceed 60 MB.
    Files are pre-filtered by mtime, then lines are substring-screened before
    any JSON parsing.

    Friction attribution is coarse: a friction turn is credited to every skill
    invoked in the same session file. Treat the number as "look here", not proof.
    """
    uses: dict[str, int] = {}
    friction: dict[str, int] = {}
    quotes: dict[str, list[str]] = {}
    invocations: dict[str, list[str]] = {}
    # skill -> parent sessions that invoked it. `uses` is the size of this set,
    # not a file count -- see _session_key.
    sessions: dict[str, set[str]] = {}
    if not PROJECTS.is_dir():
        return uses, friction, quotes, invocations

    files = [p for p in PROJECTS.rglob("*.jsonl")]
    files = [p for p in files if p.stat().st_mtime >= cutoff_ts]
    # Parents before their subagents, so the invocation kept for a session is the
    # one the *user* made -- its args and its timestamp -- rather than whichever
    # child rglob happened to reach first.
    files.sort(key=lambda p: ("subagents" in p.parts, str(p)))
    total_mb = sum(p.stat().st_size for p in files) / 1e6
    log(f"  transcripts: {len(files)} files, {total_mb:.0f} MB since cutoff")

    for i, path in enumerate(files, 1):
        if i % 100 == 0:
            log(f"    ...{i}/{len(files)}")
        seen: set[str] = set()
        frictions: list[str] = []
        args_seen: dict[str, str] = {}
        day_seen: dict[str, str] = {}
        try:
            with path.open(encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if '"name":"Skill"' in line:
                        # Capture the args too: triage.md's selection gate demands a
                        # *trace* per pick, and a bare count is not one. Mining these
                        # and discarding them forced the first dogfood to re-grep the
                        # transcripts by hand.
                        #
                        # And take the date off the *record*, not the file. A session
                        # that is still open gets touched today, so file mtime stamps
                        # every invocation in it with today's date -- zalo's "2026-08-12
                        # use" was 08-06, media-gen's "07-16" was 07-06. A wrong date on
                        # a trace is worse than no date: it is what the selection gate
                        # reads as recency.
                        stamp = TS_RE.search(line)
                        for m in re.finditer(
                                r'"name":"Skill","input":\{"skill":"([^"]+)"'
                                r'(?:,"args":"((?:[^"\\]|\\.){0,160}))?', line):
                            seen.add(m.group(1))
                            if stamp and m.group(1) not in day_seen:
                                day_seen[m.group(1)] = stamp.group(1)
                            if m.group(2) and m.group(1) not in args_seen:
                                args_seen[m.group(1)] = m.group(2)
                    elif '"role":"user"' in line or '"type":"user"' in line:
                        low = line.lower()
                        if any(f in low for f in FRICTION):
                            try:
                                rec = json.loads(line)
                            except json.JSONDecodeError:
                                continue
                            txt = _user_text(rec)
                            if txt and len(txt) < 400:
                                frictions.append(txt)
        except OSError:
            continue

        # mtime survives only as the fallback for a record carrying no timestamp.
        mtime_day = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d")
        key = _session_key(path)
        for s in seen:
            known = sessions.setdefault(s, set())
            fresh = key not in known
            known.add(key)
            if not fresh:
                continue        # a subagent of a session already counted
            day = day_seen.get(s, mtime_day)
            a = args_seen.get(s, "")
            invocations.setdefault(s, []).append(
                f"{day} — {a[:100]}" + ("…" if len(a) > 100 else "") if a else f"{day} — (no args)")
            if frictions:
                friction[s] = friction.get(s, 0) + len(frictions)
                quotes.setdefault(s, []).extend(frictions[:2])
    uses = {s: len(v) for s, v in sessions.items()}

    return uses, friction, quotes, invocations


def _user_text(rec: dict) -> str:
    msg = rec.get("message") or {}
    content = msg.get("content") if isinstance(msg, dict) else None
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                return (part.get("text") or "").strip()
    return ""


# --------------------------------------------------------------------------- #
# Report                                                                       #
# --------------------------------------------------------------------------- #

def to_ts(datestr: str | None, default_days: int = 365) -> float:
    if datestr:
        try:
            return datetime.strptime(datestr, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()
        except ValueError:
            pass
    return time.time() - default_days * 86400


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fast", action="store_true",
                    help="skip transcript mining (drops the usage gate to history.jsonl only)")
    ap.add_argument("--skill", help="restrict to one skill")
    args = ap.parse_args()

    skills = discover_skills()
    if args.skill:
        skills = [s for s in skills if s.name == args.skill]
        if not skills:
            log(f"no such skill: {args.skill}")
            return 1

    log(f"triage: {len(skills)} skills under {SKILLS_ROOT}")

    ledgers = {s.name: parse_ledger(s) for s in skills}
    counts, reads, ro_window = read_once_counts()

    dates = [to_ts(ledgers[s.name]["last_date"]) for s in skills]
    cutoff = min(dates) if dates else time.time() - 365 * 86400

    if args.fast:
        uses, friction, quotes, invocations = {}, {}, {}, {}
        log("  --fast: transcripts skipped; usage gate is advisory this run")
    else:
        uses, friction, quotes, invocations = mine_transcripts(cutoff)

    hist = history_friction()

    rows = []
    for s in skills:
        led = ledgers[s.name]
        n_commits, sample = git_drift(s, led["last_date"])
        # Strictly AFTER the entry date: a read on the entry's own day is the
        # session that WROTE the entry, not evidence of later use. Counting it
        # inflated skill-builder from 2 real uses to 4 on the first dogfood.
        since_ts = to_ts(led["last_date"]) + 86400 if led["last_date"] else to_ts(None)
        # A "use" is an invocation OR a session that read the skill's files --
        # kernel-type skills are consumed by reference and never invoked. The two
        # are reported separately and never summed; they are different evidence.
        read_sessions = {sess for ts, sess in reads.get(s.name, [])
                         if ts >= since_ts and sess}
        rows.append({
            "skill": s.name,
            "path": s,
            "led": led,
            "uses": max(uses.get(s.name, 0), len(read_sessions)),
            "invoked": uses.get(s.name, 0),
            "read_sessions": len(read_sessions),
            "invocations": invocations.get(s.name, [])[:4],
            "friction": friction.get(s.name, 0),
            "quotes": quotes.get(s.name, [])[:2],
            "drift": n_commits,
            "drift_sample": sample,
            "unread": unread_refs(s, counts),
        })

    def rank(r):
        led = r["led"]
        gated = (r["uses"] == 0 and not args.fast) and led["exists"]
        return (
            0 if not led["exists"] else 1,      # missing ledger first
            0 if not gated else 1,              # then anything with traces
            -(led["unchecked"] * 3 + led["pending"] * 2 + r["friction"] * 2 + r["drift"]),
        )

    rows.sort(key=rank)

    print("# Evolution triage\n")
    print(f"- Skills tree: `{SKILLS_ROOT}`")
    print(f"- Trace window: since {datetime.fromtimestamp(cutoff, tz=timezone.utc):%Y-%m-%d} "
          f"(oldest last-entry date across the constellation)")
    print(f"- read-once log covers: {ro_window or 'n/a'} onward — "
          "zero reads is evidence of non-reading only within this window")
    print(f"- Transcript mining: {'SKIPPED (--fast)' if args.fast else 'on'}")
    print(f"- history.jsonl friction hits (all projects): {len(hist)}\n")

    print("| skill | last entry | invoked | read-in | unchecked | PENDING | drift | friction | unread refs |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        led = r["led"]
        last = "**none**" if not led["exists"] else (
            f"{led['last_label']} ({led['last_date'] or 'undated'})" if led["last_label"] else "empty")
        print(f"| `{r['skill']}` | {last} | {r['invoked']} | {r['read_sessions']} | "
              f"{led['unchecked']} | {led['pending']} | {r['drift']} | {r['friction']} | "
              f"{len(r['unread'])} |")
    print("\n`invoked` = Skill tool-use sessions. `read-in` = distinct sessions that read the "
          "skill's files since its last entry (how kernel-type skills are actually consumed). "
          "Either one satisfies the usage gate. `friction` attribution is same-session and "
          "therefore coarse — treat it as \"look here\", not as proof.")

    print("\n## Evidence\n")
    for r in rows:
        led = r["led"]
        if not led["exists"]:
            print(f"### `{r['skill']}` — NO LEDGER")
            print("- Integrity gap: skill ships no `EVOLUTION.md`. Always a candidate; "
                  "the missing artifact is itself the finding.\n")
            continue
        gated = r["uses"] == 0 and not args.fast
        print(f"### `{r['skill']}`" + ("  — EXCLUDED: no recorded uses since last entry" if gated else ""))
        if gated:
            print("- No traces since the last entry. Evolving it would mean inventing patterns.\n")
            continue
        if led["unchecked"] or led["pending"]:
            settle = ("usage unknown (--fast)" if args.fast
                      else f"settleable — invoked in {r['invoked']}, read in {r['read_sessions']} "
                           f"session(s) since (never summed; different evidence)")
            print(f"- Validation debt: {led['unchecked']} unchecked box(es), "
                  f"{led['pending']} PENDING mention(s) in {led['last_label']}. {settle}.")
        for inv in r["invocations"]:
            print(f"- Invoked: {inv}")
        if r["drift"]:
            print(f"- Undigested drift: {r['drift']} commit(s) since {led['last_date']}:")
            for c in r["drift_sample"]:
                print(f"    - {c}")
        for q in r["quotes"]:
            print(f"- Friction (same-session, coarse attribution): \"{q[:180]}\"")
        if r["unread"]:
            shown = ", ".join(f"`{u}`" for u in r["unread"][:6])
            more = f" (+{len(r['unread']) - 6} more)" if len(r["unread"]) > 6 else ""
            print(f"- Zero recorded reads: {shown}{more}")
        if not any([led["unchecked"], led["pending"], r["drift"], r["quotes"], r["unread"]]):
            print("- Nothing found. A stable skill nothing needed to change is working, not neglected.")
        print()

    print("---")
    print("Next: hand this table plus the candidate ledgers to a selection agent "
          "(`references/triage.md` §Selection). Cap the run at 3-5 skills; every pick "
          "names its trace, every skip names its reason.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
