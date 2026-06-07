# ai_shell

**Safe, token-aware filesystem tools for LLM agents.**

`ai_shell` provides familiar shell-like tools such as `cat`, `ls`, `grep`,
`find`, `head`/`tail`, `cut`, `sed`, `git`, and unified-diff patching as
Python classes that are jailed to a root folder and tuned for token-bounded
agent output.

The package is provider-agnostic: use the generated JSON Schemas with any
tool-calling model, then dispatch approved calls through `ToolKit`.

## Install

```shell
pip install ai-shell
```

Optional checker integrations:

```shell
pip install "ai-shell[checkers]"
```

## Quick Example

```python
import ai_shell

config = ai_shell.Config()

cat = ai_shell.CatTool(".", config)
print(cat.cat_markdown(["pyproject.toml"]))

ls = ai_shell.LsTool(".", config)
print(ls.ls_markdown(path="."))
```

## Documentation

- [Narrative documentation](https://ai-shell.readthedocs.io/)
- [API reference](https://matthewdeanmartin.github.io/ai_shell/)
- [Source repository](https://github.com/matthewdeanmartin/ai_shell)
- [PyPI package](https://pypi.org/project/ai-shell/)
