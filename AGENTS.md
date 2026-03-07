# AGENTS.md — AI Agent Operating Manual for 7heknight.py

> **Attention Budget Contract**: This file is the *only* document an agent MUST read in full before acting.
> Everything else is fetched on demand. Do not pre-load files that are not yet relevant.

---

## 1. Analysis — Repo Identity & Bottleneck Map

### What this repo is
A personal Python toolkit (~20 standalone scripts) organized into five domain folders:

| Folder | Signal | Typical Task Type |
|---|---|---|
| `MyTools/` | Network utilities, crypto helpers | Extend, debug, test |
| `Exploit/` | CTF / lab offensive demos | READ-ONLY analysis; edits need explicit user consent |
| `linux2Windows/` | Unix CLI re-implementations | Cross-platform portability fixes |
| `Example/` | Bite-sized reference snippets | Understand idioms, not production code |
| `WindowsAPI_CyThon/` | Windows API via `ctypes` | Very narrow scope; fetch only when asked |

### Attention budget bottlenecks (identified)
1. **No single entry-point** — 20 independent scripts means an agent that reads everything wastes ~40 % of its context budget on irrelevant code.
2. **Exploit folder is sensitive** — pre-loading it without cause risks out-of-scope suggestions.
3. **README is long (330 lines)** — only the *Folder Structure* and *Scripts* tables (lines 170–260) are high-signal for most tasks.
4. **No shared config / package manifest** — agents must not assume a `requirements.txt`, `setup.py`, or `.env` exists; ask or check before referencing them.

---

## 2. Refactored Architecture — Agent Operating Rules

### 2.1 System Prompt (concise bootstrap)

```xml
<identity>
  Python security toolkit — standalone scripts, Python 3.7+, mostly stdlib.
  Five domains: MyTools | Exploit | linux2Windows | Example | WindowsAPI_CyThon
</identity>

<constraints>
  - Scripts are self-contained; do NOT introduce cross-script imports.
  - Exploit/ is for authorized lab/CTF use only; never suggest running against live targets.
  - Prefer stdlib over third-party; flag any new dependency explicitly.
  - Match existing style: PEP 8, argparse CLIs, module-level docstrings.
</constraints>

<attention_budget>
  Load only the file(s) directly relevant to the current task.
  Fetch README sections lazily (use line ranges, not the full file).
  Summarize read context before acting; discard raw content from working memory
  once the summary is written to NOTES (see §2.4).
</attention_budget>
```

---

### 2.2 Minimalist Toolset (3 non-overlapping tools)

Agents working in this repo should rely on exactly three primitives:

| Tool | When to use | What NOT to use it for |
|---|---|---|
| `read_file(path, start, end)` | Inspect a specific script or README section | Never read entire README; use line ranges |
| `grep_search(pattern, file)` | Locate a symbol, constant, or import within a known file | Don't grep the whole repo for broad concepts — use semantic search for that |
| `semantic_search(query)` | Discover *which* file is relevant when the file path is unknown | Don't use after the file is already identified |

> **Decision tree**: *Do I know the file?* → `read_file` / `grep_search`. *Don't know which file?* → `semantic_search` first.

---

### 2.3 Just-in-Time Context Triggers

Fetch additional context **only** when the following signals appear in the task:

| Signal in user message | Fetch target | Line range hint |
|---|---|---|
| mentions a specific script name | That script only | Full file (scripts are short, < 150 lines) |
| "add a new tool" / "new script" | README §Contributing (lines 270–310) + closest sibling script for style reference | — |
| "install" / "dependencies" | README §Tech Stack (lines 40–55) | — |
| "exploit" / "CVE" / "brute" | Exploit/README.md + named script | Full file |
| "Windows" / "ctypes" | WindowsAPI_CyThon/MessageBoxA.py | Full file |
| "cross-platform" | linux2Windows/ — list dir first, then targeted read | — |
| "test" / "run" | README §Quick Start (lines 62–80) | — |

---

### 2.4 Memory / State Management (`NOTES.md`)

For any task spanning more than **three turns**, maintain a `NOTES.md` in the repo root with this structure:

```markdown
# Session Notes — [TASK_TITLE]

## Goal
One-sentence statement of what we're building or fixing.

## Files Touched
- path/to/file.py — reason

## Key Decisions
- Decision: why this approach was chosen over alternatives

## Open Questions
- List of unresolved ambiguities, flagged for user

## Compaction Summary (if applicable)
[Filled in by agent when context approaches 60 % of window]
Summary of progress so far; prior turns collapsed into this block.
```

**Compaction rule**: When estimated token usage exceeds 60 % of the context window, write a compaction summary to `NOTES.md`, then continue from a fresh mental state using only: this `AGENTS.md` + `NOTES.md` + the file currently being edited.

---

## 3. Key Improvements

- **Attention reduction**: Agents load ≤ 2 files per turn on average vs. scanning all 20 scripts naively — estimated 75 % token reduction on discovery tasks.
- **Tool clarity**: Three non-overlapping tools with an explicit decision tree eliminate tool confusion; no redundant `semantic_search` after a file is found.
- **Exploit isolation**: Hard boundary prevents the Exploit folder from entering context unless the user explicitly names it, reducing both token waste and risk of out-of-scope suggestions.
- **Rolling compaction**: `NOTES.md` + 60 % compaction trigger ensures long-horizon tasks (e.g., "refactor all MyTools scripts") remain coherent across context window boundaries.
- **Trade-off — detail vs. speed**: Lazy loading means the first turn for a new file requires an extra fetch step. This costs ~1 turn of latency but saves 3–5× tokens across the session. Acceptable for all task types in this repo.

---

## 4. Worked Example

### Task: "Add IPv6 support to `port_scanner.py`"

**Turn 1 — User**: Add IPv6 support to the port scanner.

**Agent** (just-in-time fetch, reads only `MyTools/port_scanner.py`):
> Reading `MyTools/port_scanner.py` to understand current socket logic...
>
> Found: `socket.AF_INET` hard-coded in `scan_port()`. Plan: add `--ipv6` flag;
> switch socket family to `socket.AF_INET6` when flag is set.
> Updating `NOTES.md` with goal and file touched.

**Turn 2 — User**: Also update the help text to mention the flag.

**Agent** (no new fetch needed — file already summarized in NOTES):
> From NOTES: `scan_port()` and `argparse` block already identified.
> Applying two edits: (1) add `parser.add_argument('--ipv6', ...)`;
> (2) update `DEFAULT_TIMEOUT` docstring. No additional files needed.

**Turn 3 — User**: Can this also work on Windows?

**Agent** (targeted fetch: README §Tech Stack, ~5 lines):
> stdlib `socket` fully supports IPv6 on Windows (Python 3.7+).
> No platform guard needed. Noting in NOTES under Key Decisions.

> **Result**: Task completed in 3 turns; only 1 file read in full + 5 lines of README. No irrelevant Exploit or Example content loaded.

---

## 5. Implementation Checklist

Follow these steps at the start of every agent session in this repo:

- [ ] **1. Read this file first, in full.** Do not read any other file until the user's task is clear.
- [ ] **2. Identify the target folder** using the domain table in §1. If ambiguous, ask one clarifying question before fetching anything.
- [ ] **3. Apply the JIT trigger table** (§2.3) to determine exactly which file(s) to load — no more, no less.
- [ ] **4. Open or update `NOTES.md`** (§2.4) before making any edits; record goal, files to touch, and key decisions.
- [ ] **5. Apply compaction** if the session exceeds 3 turns or context hits 60 % — summarize into `NOTES.md` and discard raw prior-turn content from working state.

---

## Guardrails

| Rule | Rationale |
|---|---|
| Never execute or suggest running `Exploit/` scripts against non-localhost targets | Legal and ethical boundary; scripts are for authorized labs only |
| Never commit real credentials, IPs, or API keys — flag and redact | Repo is public on GitHub |
| Always use `--dry-run` when suggesting `cleanDup.py` invocations | Prevents accidental data loss |
| Flag any new `pip` dependency before adding it | Repo design principle: stdlib-first |
| Do not create `requirements.txt`, `setup.py`, or `.env` unless explicitly requested | Preserves the zero-config design |

---

*Last updated: 2026-03-07 — maintained alongside `README.md`*
