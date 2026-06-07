# ai_shell

**Safe, token-aware filesystem tools for LLM agents.**

`ai_shell` is a library of familiar shell-like tools — `cat`, `ls`, `grep`,
`find`, `head`/`tail`, `cut`, `sed`, `git`, unified-diff patching, and a few
more — reimplemented in pure Python, **jailed to a root folder**, and tuned to
return useful, **token-bounded** output (with optional markdown variants). They
are **provider-agnostic**: wire them into any agent via the generated JSON Schemas
and a neutral dispatch table. Bring your own agent loop.

> **History:** this started in 2023 as an OpenAI-Assistant shell, before Claude
> Code / aider / open-interpreter existed. That bot runtime has been removed; what
> remains is the part that was actually worth keeping — the safe tools.

## Install

```shell
pip install ai_shell
```

Optional linters/formatters/test-runners used by the goal-checker helpers:

```shell
pip install "ai_shell[checkers]"
```

## Use as a library

Each tool is a small class scoped to a root folder. Tools refuse to read or write
outside that folder.

```python
import ai_shell

config = ai_shell.Config()

cat = ai_shell.CatTool(".", config)
print(cat.cat_markdown(["pyproject.toml"]))

ls = ai_shell.LsTool(".", config)
print(ls.ls_markdown(path="."))
```

## Use with any tool-calling model

`ai_shell` exposes JSON Schemas for the tools and a neutral dispatcher. Register
the schemas with your model, then route each tool call through
`ToolKit.dispatch(name, arguments)`:

```python
import ai_shell
from ai_shell.tools_registry import ALL_TOOLS, initialize_all_tools

# Pick the tools you want to expose.
tool_names = ["ls", "cat_markdown", "grep", "apply_git_patch"]
initialize_all_tools(keeps=tool_names)

toolkit = ai_shell.ToolKit(
    root_folder=".", token_model="gpt-4o", global_max_lines=500,
    permitted_tools=tool_names, config=ai_shell.Config(),
)

# `ALL_TOOLS` holds the JSON Schemas to hand to your model.
# When the model asks for a tool, dispatch it:
result_json = toolkit.dispatch("ls", {"path": "."})
```

`dispatch` enforces the per-session tool allowlist, tracks usage stats, applies
optional media-type conversion, and converts errors to RFC7807 JSON so a model can
read and recover from them.

## CLI (sanity harness)

A generated CLI mirrors the tools — handy for checking a tool behaves before
giving it to a model:

```shell
ais cat_markdown --file-paths pyproject.toml
ais grep --regex "def " --glob-pattern "ai_shell/*.py"
```

## Tools

- **Read:** `ls`, `find`, `cat`, `grep`, `head`/`tail`, `cut`, `pycat`
  (python-aware), `count_tokens`, and read-only `git` (status/diff/log/show/branch).
- **Edit:** `apply_git_patch` (unified diff — the primary edit path), plus
  `replace`, `insert`, `rewrite_file` / `write_new_file` for non-diff edits.
- **Tasking:** a small TODO store (`ai_shell.todo`) for splitting work into
  verifiable items — see [ai_shell/todo/README.md](ai_shell/todo/README.md).

Every file is read and written as UTF-8.

## Project links

- [GitHub](https://github.com/matthewdeanmartin/ai_shell)
- [PyPI](https://pypi.org/project/ai-shell/)
- [Change Log](https://github.com/matthewdeanmartin/ai_shell/blob/main/CHANGELOG.md)
