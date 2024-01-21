# Document Editing

The bot has a hard time with editing files.

Some top level strategies

- editor-like tools, eg ed and edlin
- text replacement tools, e.g. sed, regex, replace
- full document replacement
- write only new files
- multiline insert tool
- diff/patch tool
- well known tools vs simpler ad-hoc tools
- validated format
- Guided edit

## Editors

The bot cannot consistently edit a document with ed or edlin. It gets confused about the state of the document, the syntax of editor, etc.

## Text Replacers

It gets confused about the syntax of sed and regex.

It also has to keep straight complex escaping patterns as it
write JSON that has to be escaped for JSON, which wraps editor syntax, which can included regex.

## Full Text replacement

It constantly confused rewriting an entire document with modifications with writing just the modified lines,
creating non-stop mass, accidental deletions.

## Writing only new files

This shift the burden of merging document to a human.

### Multiline Insert

This is similar to the sed and regex tool, but with simpler syntax. The cost for simplicity is that the bot has no
background knowledge of how to use the multiline insert tool, while it has lots of knowledge of sed and regex.

## Success vs Failure

When the bot gets a success flag, it thinks the job is done and stops early. When the bot gets a failure, it
sometimes assumes the task is impossible and gives up.  This is mitigated a little bit by returning the entire
document after each edit so it can see what happened.

## Diff/Patch

To create a well known Patch format, the bot has to be able to count lines perfectly. It often can't so the Patch
tool rejects the patches and after a few attempts the bot gives up. Common patch tools provide almost no feedback
because the bot is failing in a way that normal tools don't, so why would they provide helpful feedback?

## Validated Format

In the case of, say python code, the syntax can be validated and if the bot messed up the document, it can be
reverted adn the bot can try again.

## Guided Edit

An example of guided edit is feeding the bot one line or paragraph of text and asking it to transform it or
otherwise do something with it. Then ordinary code merges it in a predictable format. For example, show the bot a
function, then ask for a docstring.
