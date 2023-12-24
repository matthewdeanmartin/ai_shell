## Code Generation

A code generation tool generates all the OpenAI assistant code

- jsonschema, as generated from the method signatures
- toolkit, the python tool invocation code, as generated from the jsonschema
- a CLI interface in `__main__.py` that invokes the tool for human testing, not intended for bot use.

## JSON

The tools expect chaotic JSON from the bot.

- truncated JSON
- Invalid escape codes
- Function args sometimes are the wrong type, e.g. string instead of list of strings.

All messages returned are JSON, even if the return value is plaintext markdown, it is wrapped in a layer of JSON.

Error messages for the bot also need to be json, so I used RFC-7807 as inspiration.

## Toolkit Safety

The bot sometimes attempts to call tools that don't exist, e.g. `parallel` Sometimes this means the bot knows about a
feature not
yet known to the openai client. To be safe, you have to whitelist tools that the bot can use. Otherwise it could
potentially call a tool by guessing its name.

## Mime Types

"Mime types for API". Rather than give the bot two or more formats, I will implement a mimetype, so that the APIs
are configured to either return markdown or structure, depending on config. The mime type is still wrapped in JSON!
Just less of it.

The bot sometimes fills in mime type when it is submitting a file thinking that the mime type is for classifying input.

## Editing

The bot finds it difficult to edit files. For many techniques, it can get close. In chat dialogs, the bot wants to
regenerate the whole document to edit even a single character. Or it wants to use ad hoc diffs. This is problematic
for programatic use.

### Linux-Like Editing Strategies

The bot knows unix tools and often can get really close to using a function that behaves like that tool.

- ed. Ed is such a bad editor even the bot has hard time with it.
- edlin/dedlin. Edlin's commands almost can be used as an executable script.
- patch. git diffs/unidiffs. The bot can sometimes generate a diff. Sometimes the diff is corrupt because it requires
  careful line counting. Sometimes the bot create a diff for a hallucinated target file.
- sed. Fancy replace.

### Simpler Ad Hoc Tools.

- replace. This has no equivalent in unix, it is a replacer that doesn't require line numbers.
- insert. This has no equivalent in unix, it is an inserter that doesn't require line numbers.
- rewrite. This has no equivalent in unix, it is a tool to rewrite a file, or create a new one, e.g. a corrected copy.

A surprising with all of these approaches is that the bot doesn't check its work (won't run a cat after an edit), and
often just assumes everything worked because it didn't get an error message. It assumes that the success message means
the user really is happy and the task is done.

## Viewing Strategies

- Cat.
- Head/Tail.
- PyCat. Work in progress, view python code either aggregated or compressed.

## File Browsing Strategies

- Ls. Returns directory tree if bot tries to browse a directory that doesn't exist.
- Grep.
- Find.
- Cut. Primitive CSV browser

## Safety Tools

- Git. Particularly to allow for commit/revert
- Diff tool.

## Logging

At least three kinds of logging

- REST API calls. Each API call to OpenAPI written as JSON document.
- Tool commands. This is a nearly executable bash script to replay what the bot did.
- The dialog. This is a chat log style log.

## Config

Config is intended to bound the behavior of certain tools, to persist a bot and to enable helper bots.

Helper bots attempt to help the bot use tools by letting specialized bot focus on a narrow part of the problem of
using tool.
