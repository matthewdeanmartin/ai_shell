# Build script bot

A series of bots that do the same thing as a typical build script.

- Write docs
  - Docstrings
  - Example code
- Write tests
  - pytest
  - coverage tests
  - docstring tests
- Add type annotations
  - missing
  - wrong
- Fix lint issues
  - Full report
  - One issue, one file at a time (likely better!)
- Fix mypy issues
  - Full report
  - One issue, one file at a time (likely better!)
- Find TODOs
  - Comment TODOs
  - Suggestions from bot
  - Work TODO
  - Record/Close TODO issues

## Write tests

- Stop it from changing code under test
- Stop calls to os.system, subprocess

## Docs

- Blows away all code leaving just the docs

## All bots that edit

- Is willing to edit without viewing
- Happy to write corrupt python

## Mypy bot

- Need to write it.
