# Last Call for Features — `ai_shell`

> Status: planning doc for the **final** version of `ai_shell`.
> Goal: make this useful for the *narrow* thing it actually is, then stop.
>
> This app predates Claude Code / aider / open-interpreter and originally had
> broad agentic ambitions on the OpenAI **Assistants Beta** API. The world has
> since standardized on the OpenAI chat-completions tool-calling interface, and
> dedicated coding agents now cover the "agent" use case far better. What remains
> genuinely differentiated is the **safe, token-optimized, reimplemented CLI
> toolset** — usable as a plain Python library by *any* agent.

---

## 1. Decisions (from the owner)

| Question | Decision |
| --- | --- |
| **Core identity** | **Safe-tools library, provider-agnostic.** Lead with the ~30 reimplemented safe CLI tools + the safety layer as a clean library that returns plain values / markdown. The bot loop and OpenAI glue are demoted. |
| **OpenAI Assistants Beta glue** | **Rip out / archive it.** Remove `TaskBot`, `loop_tools`, the `openai_multi_tool_use_parallel_patch` monkeypatch, OpenAI-specific schema/runner. Keep tools fully usable without it. |
| **TODO loop** | The current `ai_todo` was written by GPT-4 and uses a bespoke dual-TOML store. There is **no `grep`-level standard** TODO tool, but a de-facto convention exists (Markdown task files w/ YAML frontmatter + "Done when"). **Realign `ai_todo` to that convention** so it's the closest thing to a standard, not a private format. (See §6.) |
| **Stubs / half-built** | **Cut all stubs**, keep the working plugin loader (marked experimental). |
| **Editing** | **Unified diffs are the headline edit path.** `ed`/`edlin` line-editor editing was a mistake — **CUT** both. Consolidate `diff_tool`+`patch_tool` into one `apply_diff`. Keep `replace`/`insert`/`rewrite` as secondary no-diff edits. (§5.1) |
| **git** | **Shell out** via `safe_subprocess`; **drop `gitpython`** (it's just sugar over the git CLI). (§5.2) |
| **Markdown deps** | Corrected: only `markpickle` is a runtime import; the other four are doc/dev tooling → move out of core. (§5.3) |
| **Packaging** | **Replace Poetry with uv + PEP 621** `[project]`. (§5.5) |

---

## 2. The thesis for the final version

`ai_shell` becomes: **a library of familiar Unix-ish tools, reimplemented in pure
Python, jailed to a root folder, and tuned so an LLM gets useful, token-bounded,
optionally-markdown output.** No vendor lock-in. No agent runtime required.

The three things that were actually good and should survive:

1. **Familiar tools with a safety layer / reimplemented safely** — root-folder
   jail (`is_file_in_root_folder`, `safe_glob`, path-traversal sanitizing),
   utf-8-normalization, backup-on-write, read-only mode. This is the moat.
2. **An agentic *toolkit* library** — i.e. ready-to-register tool functions with
   clean signatures + auto-generated JSON Schema, that you drop into *your* agent.
   Not an agent runtime — just the tools and their schemas.
3. **The TODO-list / goal loop idea** — "the goal function is also a work queue":
   split work into items, hand one at a time to a bot, verify it did the one
   thing, move on. Keep the *idea* and the `ai_todo` data model; drop the OpenAI
   bot driver that wrapped it.

---

## 3. Inventory & disposition

Legend: **KEEP** (core, polish) · **EXTRACT** (could be its own lib) ·
**OBE** (obsoleted by standardization) · **STUB** (never implemented) ·
**REPLACE** (use an existing safe tool) · **CUT** (delete) · **DEMOTE** (keep but
move out of the headline path).

### 3.1 Core safe tools — KEEP (this is the product)

| Module | Disposition | Notes |
| --- | --- | --- |
| `cat_tool.py` | KEEP | + markdown variant, line numbering, squeeze-blank. |
| `ls_tool.py` | KEEP | + markdown, long, all-files. |
| `grep_tool.py` | KEEP | match limits, skip, per-file caps — genuinely LLM-tuned. |
| `find_tool.py` | KEEP | name/regex/size/type. |
| `head_tail_tool.py` | KEEP | bytes or lines, head/tail/both. |
| `cut_tool.py` | KEEP | char ranges, fields, fields-by-name. |
| `sed_tool.py` | KEEP | safety-reviewed sed subset. |
| `ed_tool.py`, `edlin_tool.py` | **CUT** | Line-editor editing was a mistake. LLMs do better with unified diffs (see §5.1). Rip both out. |
| `replace_tool.py` | KEEP | all / line-by-line / regex. Still useful as a no-diff quick edit. |
| `insert_tool.py` | KEEP | after-context / multiline / start-end. |
| `rewrite_tool.py` | KEEP | rewrite + write-new, backup first (whole-file path). |
| `patch_tool.py` + `diff_tool.py` | **KEEP, CONSOLIDATE** | **The primary editing path.** Both implement `apply_git_patch` via `unidiff`; `diff_tool.py` isn't even wired into the toolkit/CLI. Merge into ONE unified-diff tool and make it the headline edit mechanism (see §5.1). |
| `pycat_tool.py` / `read_py_source.py` | KEEP | python-aware view (strip comments/docs). |
| `token_tool.py` | KEEP | tiktoken token counting — useful standalone. |
| `git_tool.py` | **KEEP, REWORK** | status/diff/log/show/branch/gitignore. Read-only by design — good. **Shell out via `safe_subprocess` instead of `gitpython`** — gitpython is just sugar over the git CLI (see §5.2). Drop the `gitpython` dep. |
| `backup_restore.py` | KEEP | underpins safe writes (`.bak`, `.bad`). |
| `answer_tool.py` | DEMOTE | "report_*" structured-answer collector only matters to the bot loop. Keep the typed-report helpers, drop the self-certification coupling. |

### 3.2 Safety / FS layer — KEEP (the moat)

| Module | Disposition | Notes |
| --- | --- | --- |
| `utils/read_fs.py` | KEEP | `is_file_in_root_folder`, `safe_glob`, `sanitize_path`, tree, size. Core jail. |
| `utils/cwd_utils.py`, `crlf_handlers.py`, `type_repair.py`, `json_utils.py`, `medias.py` | KEEP | supporting utilities; audit for dead code. |
| `utils/config_manager.py` | KEEP, **REWORK** | Strip bot/thread persistence (OpenAI-only). Keep flags/values/lists + read-only mode + plugin_folder. The `bots`/`threads` tables become OBE. |

### 3.3 OpenAI Assistants Beta glue — OBE / RIP OUT

| Module | Disposition | Notes |
| --- | --- | --- |
| `bot_glue/bot.py` (`TaskBot`) | OBE → archive | Assistants Beta threads/assistants/runs runner + keep-going loop. The *loop idea* survives in docs; the *code* goes. |
| `bot_glue/tool_utils.py` (`loop_tools`) | OBE → archive | Polls Beta runs, submits tool outputs. Beta-specific. |
| `openai_support.py` (`ToolKitBase.process_tool_calls`) | OBE → REPLACE | Reads `run.required_action.submit_tool_outputs` (Beta shape). Replace with a provider-neutral `dispatch(name, arguments)` that any caller can use. Keep the permission-gating + usage-stats logic — that part is good. |
| `openai_toolkit.py` (`ToolKit`) | KEEP shape, REGEN | The generated `name -> method(arguments)` dispatch table is reusable as a neutral registry. Regenerate without OpenAI assumptions. |
| `openai_tools.py`, `openai_schemas.py` | KEEP as schema source, RENAME | JSON Schema is the lingua franca for tool-calling across vendors. Keep schema generation; drop "openai" from the framing/names. |
| `openai_multi_tool_use_parallel_patch` (dep + import) | CUT | Monkeypatch for a Beta parallel-tool-call bug. Remove dep and the `if True: import ...` blocks. |
| `subbots/tool_picker.py` | STUB → CUT | Docstring only. |
| `subbots/__init__.py` | CUT | Empty package once tool_picker is gone. |

### 3.4 Agentic toolkit library — KEEP & REFRAME

| Module | Disposition | Notes |
| --- | --- | --- |
| `code_generate/method_to_jsonschema.py` | KEEP | Introspects tool classes → JSON Schema from docstrings/types. Reusable, vendor-neutral. |
| `code_generate/generate_schema.py` | KEEP | Generates `*_schemas.py`. |
| `code_generate/generate_toolkit.py` | KEEP | Generates the dispatch `ToolKit`. |
| `code_generate/generate_cli.py` | KEEP | Generates the `ais` argparse CLI. The CLI is the honest "is this tool sane?" harness. |
| `import_plugins.py` + `plugins/` | KEEP, mark **EXPERIMENTAL** | Working file-drop plugin loader (`*_tool.py` → schema → registry). Per owner: keep the working loader, cut the stubs. Document limits (no mime/folder/error handling parity). |

### 3.5 Stubs / dead config — CUT

| Item | Disposition |
| --- | --- |
| `regex_tester_tool.py` | STUB → CUT (docstring only). |
| `subbots/tool_picker.py` | STUB → CUT. |
| Config flags `enable_tool_selector_bot`, `enable_regex_tester_bot`, `enable_prompt_improver_bot` | CUT (no implementation). |
| `enable_api_log`, `enable_shell_log`, `enable_dialog_log` | REVIEW — keep only the loggers that survive the bot-loop removal. |
| Self-certification path (`allow_self_certification`, `tool_answer_collector` plumbing in the loop) | CUT with the bot loop. |

### 3.6 Logging — DEMOTE / SIMPLIFY

| Module | Disposition | Notes |
| --- | --- | --- |
| `ai_logs/log_to_markdown.py` (`DialogLoggerWithMarkdown`) | DEMOTE | Conversation logger for the bot loop. Goes dormant when the loop is removed; keep only if a slim demo keeps it alive, else CUT. |
| `ai_logs/log_to_bash.py` (`@log()`) | KEEP | Per-tool call logging decorator — useful in library mode. |
| `ai_logs/json_log_handler.py`, `logging_utils.py`, `pretty_errors_log.py` | REVIEW | Keep `configure_logging`; trim the rest. `bug-trail-core` dep is heavy — consider dropping. |
| `logs/*.sh` | CUT | Stray sample shell logs. |

### 3.7 Externals (subprocess goal-checkers) — DEMOTE

| Module | Disposition | Notes |
| --- | --- | --- |
| `externals/subprocess_utils.py` (`safe_subprocess`) | KEEP | Tidy `shell=False` wrapper; useful. |
| `externals/{pylint,pytest,ruff,black,mypy,pygount}_call.py` | DEMOTE → optional extra | These existed as *goal-function* checkers for the bot loop. Without the loop they're just thin subprocess wrappers around tools the user already has. Move behind an optional `[checkers]` extra or **REPLACE** by telling users to call the real tools. Drop the heavyweight pinned deps (`pylint`, `pytest`, `ruff`, `black`, `mypy`) from core. |

### 3.8 Demo bots — OBE

| Module | Disposition | Notes |
| --- | --- | --- |
| `demo_bots/*` (pylint/test-writer/docs/tool-tester/todo bots, `example_tiny_bot.py`) | OBE → archive | All built on `TaskBot` + Assistants Beta. Replace with **one** tiny, current example showing how to register the tools with a modern tool-calling call (chat-completions style), provider-neutral. |
| `fish_tank.zip` | CUT | Demo fixture for the bots. |

---

## 4. Things that can be REPLACED with pre-existing safe tools

- **External linters/formatters/test runners** (`externals/*_call.py`): users
  already have `ruff`, `pytest`, etc. Don't ship them as core deps; document
  "point your agent at the real binary via `safe_subprocess`, or install the
  `[checkers]` extra."
- **`git_tool.py`**: stays (it's read-only and token-shaped), but note that
  `gitpython` is a real dep cost; consider shelling to `git` via `safe_subprocess`
  for the few read commands to drop the dep. (Trade-off — see §5.)
- **JSON Schema generation**: this is the one piece worth *keeping in-house*
  because it's tied to our docstring/type conventions; do **not** swap for a
  generic introspection lib (history shows several were tried and dropped — see
  the commented-out deps in `pyproject.toml`).

---

## 5. Settled decisions on trade-offs

### 5.1 Editing → unified diffs are the headline; cut the line editors
**Decided.** Editing via `ed`/`edlin` was a mistake — **LLMs do better with
unified diffs**, and that pattern was already started here (`diff_tool.py`,
`patch_tool.py`).

- **CUT** `ed_tool.py` and `edlin_tool.py` entirely (+ their `ed` / `dedlin`
  deps, schemas, CLI commands, tests).
- **Consolidate** `diff_tool.py` + `patch_tool.py` into **one** unified-diff tool
  and make it the primary edit mechanism. Notes:
  - Both currently expose `apply_git_patch` via `unidiff`. `diff_tool.py` is
    **not wired into the toolkit or CLI** — dead but useful code; fold its
    per-file `target_file` apply + `auto_cat` return into the surviving tool.
  - Keep `unidiff` (this is where it earns its keep) and the `auto_cat`
    "return file after patching" behavior — that solves the "no exception ≠
    success" problem the old TODO complained about.
  - Keep the secondary edit tools that don't need a diff: `replace_*`,
    `insert_*`, `rewrite_file` / `write_new_file`. They're cheap and don't
    require the model to produce a valid hunk.

### 5.2 git → shell out, drop `gitpython`
**Decided.** `gitpython` is just syntactic sugar over the git CLI. Reimplement
`git_tool.py`'s read commands (status/diff/log/show/branch/gitignore) on top of
`externals/subprocess_utils.safe_subprocess` and **drop the `gitpython` dep**.
(`is_ignored_by_gitignore` already shells/parses manually; the rest is
`Repo(...)` calls that map 1:1 to `git <subcommand>`.)

### 5.3 "Markdown stack" — mostly a non-issue (corrected)
My earlier "five markdown deps" was wrong. **Only `markpickle` is imported in
runtime `.py` code** (`ai_logs/log_to_markdown.py`, `read_py_source.py`).
`html2text`, `markdown-it-py`, `mdit-plain`, `mdformat` appear **only** in
build/doc config (`pyproject.toml`, `Makefile`, `mdbuild.sh`, pre-commit) — dev
tooling, not runtime. So:
- Move `html2text`, `markdown-it-py`, `mdit-plain`, `mdformat` to dev/docs deps
  (or drop if unused after the bot-loop + dialog-logger removal).
- `markpickle` (python-object → markdown) stays only if `read_py_source` /
  surviving markdown tool variants still use it; otherwise cut.

### 5.4 `bug-trail-core` logging dep — cut in library mode
Heavy logging dependency tied to the old dialog/api logging. Drop for the library.

### 5.5 Packaging → uv + PEP 621
**Decided.** Replace **Poetry** with **uv** + a standard PEP 621
`[project]` table. `pyproject.toml` still has `[tool.poetry]` while the repo
already uses `uv.lock` / `[tool.uv]`. Migrate fully and delete `poetry.lock`.

---

## 6. `ai_todo` — realign to the emerging standard (don't invent a format)

**Finding:** there is no universally-known TODO tool ("the grep of TODOs").
But across the agent ecosystem a **de-facto convention** has formed:
**Markdown task files with YAML frontmatter** (`id`, `status`, `priority`,
`tags`) and a body with a **"Done when"** acceptance section. (See sources.)

Current `ai_todo` uses a **bespoke dual-TOML store** (`todo_completed.toml` /
`todo_incomplete.toml`) — private, not what other agents read.

**Plan:**

- **Keep** the data model (`Task`, `Work`, assignees, query-by-assignee /
  by-regex, stats) and the `TaskManager` public API — that's solid.
- **Swap the on-disk format** to Markdown-with-frontmatter (one file per task or
  a single `TODO.md` with frontmatter blocks), so the files are human- and
  agent-readable by convention, not just by this library.
- Add an explicit **"Done when" / acceptance** field to each task — this is what
  makes the goal-loop pattern work ("verify the bot did the one thing").
- **EXTRACT**: `ai_todo` becomes its own publishable package (it already has its
  own `README`, `py.typed`, templates). `ai_shell` depends on it for the
  `add_todo`/`query_todos_*` tools.
- Document the **"goal function = work queue"** loop as the headline idea in
  `ai_todo`'s README, since the bot-runner that demonstrated it is being removed.

---

## 7. Proposed final shape

```
ai_shell/                 # the safe-tools library (the product)
  tools/
    read/                 # cat, ls, grep, find, head_tail, cut, pycat, token, git (read-only, shells out)
    edit/                 # apply_diff (unified-diff, PRIMARY) + replace, insert, rewrite/write_new
  safety/                 # read_fs (jail), backup_restore, read-only mode
  registry/               # JSON-Schema generation + neutral dispatch (ToolKit)
  cli/                    # generated `ais` CLI (the sanity harness)
  plugins/                # experimental file-drop plugin loader
  examples/               # ONE current, provider-neutral tool-calling example
  (optional extras)       # [checkers] externals

ai_todo/                  # extracted: markdown+frontmatter task store + goal-loop docs

archive/  (or a git tag)  # bot_glue, openai_* runner, demo_bots, monkeypatch, ed/edlin
```

### Naming / framing
- Drop "openai" from module names and docstrings ("optimized for LLMs, not
  OpenAI specifically" is already the true description in the code comments).
- README: lead with "safe, token-aware filesystem tools for *any* LLM agent,"
  not "OpenAI-centric shell." Keep the archived-notice but reframe what survives.

---

## 8. Work phases

### Phase 0 — Snapshot & archive (no behavior change)
- Tag the current commit (`v1.0.4-assistants-beta`) so the OpenAI-Beta version is
  recoverable.
- Create `archive/` (or rely on the tag) for `bot_glue/`, `openai_support` runner
  bits, `demo_bots/`, `example_tiny_bot.py`.

### Phase 1 — Rip out OBE OpenAI glue
- Remove `TaskBot`, `loop_tools`, `openai_multi_tool_use_parallel_patch` (code +
  dep), the `if True: import ...` patch blocks.
- Replace `process_tool_calls` with a neutral `dispatch(name, arguments)` keeping
  permission-gating + usage stats.
- Strip bot/thread persistence from `Config`.
- Regenerate `ToolKit` / schemas / CLI without OpenAI assumptions.

### Phase 2 — Cut stubs, dead config, and the line editors
- Delete `regex_tester_tool.py`, `subbots/`, dead `enable_*_bot` flags,
  self-certification path, `logs/*.sh`, `fish_tank.zip`.
- **Delete `ed_tool.py` + `edlin_tool.py`** (+ `ed` / `dedlin` deps, their
  schemas, CLI commands, tests). (§5.1)
- Audit and trim logging modules; drop `bug-trail-core`. (§5.3, §5.4)

### Phase 3 — Make unified diffs the headline edit path
- Consolidate `diff_tool.py` + `patch_tool.py` into a single `apply_diff` tool;
  keep `unidiff` + `auto_cat` return-file-after-patch. (§5.1)
- Reframe `replace`/`insert`/`rewrite` as the secondary, no-diff edit tools.
- Regenerate schemas + CLI for the new edit surface.

### Phase 4 — Reframe as a library
- Reorg into the §7 layout (or at least the namespacing/docstrings).
- One modern, provider-neutral example (register tools → chat-completions tool
  call → `dispatch`).
- Rewrite README around the safe-tools identity.

### Phase 5 — `ai_todo` realignment & extraction
- Switch storage to markdown+frontmatter, add "Done when".
- Extract to its own package; `ai_shell` depends on it.
- Document the goal-loop / work-queue pattern.

### Phase 6 — Dependency diet & packaging
- `git_tool` → shell out, drop `gitpython`. (§5.2)
- Move `html2text`/`markdown-it-py`/`mdit-plain`/`mdformat` to dev/docs; reassess
  `markpickle`. (§5.3)
- Move linters/formatters/test-runners to a `[checkers]` extra.
- **Replace Poetry with uv + PEP 621 `[project]`**; delete `poetry.lock`. (§5.5)

### Phase 7 — Final polish
- Tests green on the surviving surface; mypy/ruff clean.
- Regenerate API docs.
- Final README + CHANGELOG entry describing what was removed and why
  (honesty: this is the last release for the narrow thing it is).

---

## 9. Explicit "not doing" list
- Not modernizing the Assistants-Beta runner to chat-completions (per owner: rip
  out, don't replace the runner). We provide tools + schemas + dispatch; the user
  brings their own agent loop.
- Not building the tool-selector / regex-tester / prompt-improver sub-bots.
- Not keeping line-editor editing (`ed`/`edlin`) — unified diffs are the path.
- Not inventing a new TODO format — adopting the markdown+frontmatter convention.
- Not shipping linters/test-runners, `gitpython`, or doc-only markdown deps as
  core dependencies.

---

### Sources (TODO-format convention)
- [The Case for Markdown as Your Agent's Task Format — dev.to](https://dev.to/battyterm/the-case-for-markdown-as-your-agents-task-format-6mp)
- [Custom instructions with AGENTS.md — OpenAI Developers](https://developers.openai.com/codex/guides/agents-md)
- [The Agent Skills Standard (SKILL.md) — Medium](https://medium.com/@loccarrre/the-agent-skills-standard-how-a-simple-skill-md-file-turns-ai-agents-into-on-demand-specialists-172af1d9737d)
