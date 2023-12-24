bot_name = "apply_git_patch, ls and cat user"
bot_instructions = (
    "You are excellent at understanding code and writing the docstrings for python code. "
    " You will use the cat tool to read files, and the patch tool to edit files. The apply_git_patch tool"
    " uses git patch file format."
)
#     """You know how to write scripts for an edlin-clone, in this format:
#
# ```edlin
# # Insert at line 1, 2, and 3.
# 1 INSERT TODO
# # Any insert/edit values with space need double quotes.
# 2 INSERT Buy soymilk
# 3 INSERT Buy tofu
# # All lines are command mode, you must always specify INSERT or EDIT. No need for "." as command!
# # EXIT saves! Not wq, not w!
# EXIT
# ```
#
# """
request = (
    "Use the edlin tool, create a groceries.md file, insert some random vegan grocery items. "
    "Use the ls and cat toolkit_factory to see if it worked. Remember to quote your Inserts. Then delete the last item."
    " Don't forget to verify with cat. Say 'DONE' when you are done."
)
request = (
    "Use the grep tool to find python file with # TODO in them. Use the edin file to create a work.md file."
    "Put the TODO items into the todo.md. Then SORT them. "
    "Don't forget to quote your Inserts. Say 'DONE' when you are done."
)
request = (
    "You are a tester for a new edlin clone. You are testing out the tool to create a file, to insert some data"
    " and then use it again to edit the document. The file should be walrus facts, use markdown."
)
request = (
    "Please write a grocery list in markdown. Use edlin. It should be for a vegan taco party. Sort the list. "
    " Then after that, add some space and then write a list of Mexican themed party decorations. Then you are done."
)
request = (
    "Please write a grocery list in markdown. Use edlin. It should be for a vegan new year's party. Sort the list. "
    " Then after that, add some space and then write a list of Walrus themed party decorations. Then you are done."
)
request = (
    "Please write a vacation todo list in markdown. Use edlin. It should be for  trip to virginia beach. Sort the list. "
    " Then after that, add some space and then write a list of Library of congress themed party decorations. Then you are done."
)
request = (
    "Use the grep tool to find python file with # TODO in them. Use the edin file to create a work.md file."
    "Put the TODO items into the todo.md. Then SORT them. "
    "Don't forget to quote your Inserts. Say 'DONE' when you are done."
)

# request = "Use the grep, git, find, cat, head, tail, or ls toolkit_factory as appropriate " \
#           "to find which python files " \
#           "have `# BUG` comments and recommend a fix. As soon as you send me the fix you are DONE."
#           # "have TODO items."
# request = "Use the grep, find, ls, and edlin toolkit_factory as appropriate " \
#           "to find which python files " \
#           "have `# TODO` items. Put al the TODO items into a TODO.md file and save it."
#           # "have `# BUG` comments and recommend a fix. As soon as you send me the fix you are DONE."

request = (
    "Use the grep tool to find python file with # TODO in them. Use the edlin tool to create a work.md file."
    "Put the TODO items into the todo.md. Then SORT them. "
    "Say 'DONE' when you are done."
)

request = "Please add the missing docstrings to the crlf_handlers.py file. When done, say DONE."
