# TODO

## Fig leaf security (Yes, it isn't for preventing real malice)
- Prohibited file types
- Prohibited modules/methods, e.g. subprocess/os.system
- Test writer bot- disable writing to fish_tank
- Test writer bot- no editing without 1st viewing, cat unlocks edit!
- Is cat folder/* failing?

## Pain points
- no more log folder by convention
- put API log on hold (replace with ordinary file?)

## Demo Bots

- python -m ai_shell.demo_bots.(bot_name)
- Make "fish tank" a resource?
- Start up check
  - Needs a place for logs (api, dialog, cli)
  - Needs a place for config
  - Needs an API key
  - Needs permission from user to write to /src/

## MORE

- check for repetition in replies, e.g "I'm sorry I can't do that", can mean it is stuck.
- can't use certain tools until they're unlocked (e.g no edit w/o looking at file)

## Plugin Architecture
- First, allow for dynamic tools (dynamic schema and dynamic toolkit code)

## Uncategorized

- Aggressively reduce tool count
- Multiple "go-on" prompts
  - Static ("If done, report done, otherwise keep working.")
  - Self Check ("You haven't run the self check tool, keep working")
  - Self Check With Success ("You haven't run the self check tool with a success flag, keep working")
  - Dynamic ("See output of lambda {output}, if done, stop, otherwise keep working")
  - Dynamic with inputs ("See output of lambda(folder, min_pass, max_fail), not good enough, keep working.")
  - 2nd bot "Did this bot achieve the goal? No? What should we tell him."
- Temp folder other than OS temp folder.
- Set pwd in one folder, but only allow certain folders (eg. /src/, but only allow /src/module)

## AI prompt/response size concerns

- Pervasive token checking (not invoked unless set, can specify in lines, tokens or bytes)
- Markdown with more than just plain text (Jinja in progress)
- Plain text trim (How? Cheap bot summarizes for an expensive bot?)

## Missing tools, tool improvements

- Pycat - view parts of python file, e.g. just a function or class
- History - history just for the bot. Different from developer oriented logging.
- fuzzy search based on fuzzy source code search tools
- Regex tester
  - Built into tool, e.g. grep(search_regex, example_hit, example_miss)
  - Standalone, e.g regex_test(search_regex, example_hit, example_miss)
- Regex tester bot, e.g. "Hey bot does regex {regex} make sense for {goal}?"

## Editing

- MORE TOOLS. But what?
- Return entire document after any edit. Expensive, but could solve the "no exception is success" problem
- Formalize "write changes to a new file", e.g. my_file.new.py

## Bash conveniences, for interactive testing

- TODO: Fix subtools

## Assistant tool interface glue

- Let all tools return a variety of mime types without doubling tool count presented to bot

## Base bots

- One-shot bot - Needs testing
- Tool using bot - formalized "static keep going message" vs "lambda with goal status" (e.g. re-running pylint)

## Sub Bots

- improve prompt
- select tools
- git sub-bot (creates branches, thinks up commit message)

## Example bots

- pylint bot
- docstring bot
- mypy bot
- change log bot (look at changes and update changelog)

## Security

- block network traffic?
