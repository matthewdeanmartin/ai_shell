## Features

### General Features

- Tools are similar to common shell commands like ls, grep, head, tail, and git for easy use by the bot.
- Handle bot "accessibility". The bot can't see, hear, or interact with the console display.
- Designed to minimize token usage in both input and output
- Supports maximum row response for output.
- Supports mime_types
- Outputs in Markdown to reduce token repetition through sections and subsection headers.
- Implementation is simplified with no command chaining.

### Text and Size Management

- TODO: Maximum output limits, both by config and by bot.
- Capability to count tokens, with a maximum limit and fallbacks to word or byte count.
- Implements whitespace and other lossless/lossy text compressions.

### Source Code Display and Analysis

- Converts code to Markdown (.md) files, including minified versions.
- TODO: AST (Abstract Syntax Tree) display and search capabilities using pycodesearch.
- TODO: Features for displaying source code of functions, classes in imported modules.
- TODO: Simplified directory listings (dir(module)) and module help (help(module)) focusing on key elements.

## Security Constraints

### General Security Measures

- Provides multiple output formats: plain text, light markdown, and JSON (structured objects).
- TODO: Ignores files specified in .gitignore.
- TODO: Skips files hidden by the operating system.
- Prevents parent directory traversal. Disallows file system modification outside of specified folders.
- No direct shell access and write permissions are restricted.
- Limited write access to source code, isolated within a specific git branch.
- File writes are permitted only in a designated branch.
- No network access.

## Bots and Subbots

(in progress)

I created this so I could create a swarm of bots to collaboratively work on a task. As it turns out, sub-bots or
subbots, would be useful for tool usage.

### Subbots

- tool selection. Too many tools or extraneous tools confuse the bot.
- prompt improvement. The bot can often write a better prompt.
- todo management. Splitting up tasks and managing them and doing the task makes the task execution part worse.

Subbot usage requires an editable config file for storing assistant ids.
