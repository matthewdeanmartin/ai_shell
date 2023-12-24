# not the recomended way to use this

# usage: ais [-h]
#           {cat,cat_markdown,find_files,find_files_markdown,get_current_branch,get_recent_commits,git_diff,git_diff_commit,git_log_file,git_log_search,git_show,git_status,is_ignored_by_gitignore,ls,ls_markdown,grep,grep_markdown,count_tokens}
#           ...
#
#AI Shell Command Line Interface
#
#positional arguments:
#  {cat,cat_markdown,find_files,find_files_markdown,get_current_branch,get_recent_commits,git_diff,git_diff_commit,git_log_file,git_log_search,git_show,git_status,is_ignored_by_gitignore,ls,ls_markdown,grep,grep_markdown,count_tokens}
#                        sub-command help
#    cat                 Mimics the basic functionalities of the 'cat' command in Unix..
#    cat_markdown        Concatenates the content of given file paths and formats them as markdown..
#    find_files          Recursively search for files or directories matching given criteria in a directory and its subdirectories..
#    find_files_markdown
#                        Recursively search for files or directories matching given criteria in a directory and its subdirectories..
#    get_current_branch  Retrieves the current branch name of the repository..
#    get_recent_commits  Retrieves the most recent commit hashes from the current branch..
#    git_diff            Returns the differences in the working directory..
#    git_diff_commit     Shows changes between two commits..
#    git_log_file        Returns the commit history for a specific file..
#    git_log_search      Returns the commit history that matches the search string..
#    git_show            Shows various types of objects (commits, tags, etc.)..
#    git_status          Returns the status of the repository..
#    is_ignored_by_gitignore
#                        Check if a file is ignored by .gitignore..
#    ls                  List directory contents, with options to include all files and detailed view..
#    ls_markdown         List directory contents, with options to include all files and detailed view..
#    grep                Search for lines matching a regular expression in files specified by a glob pattern..
#    grep_markdown       Search for lines matching a regular expression in markdown files and returns formatted results..
#    count_tokens        Count the number of tokens in a string..
#
#options:
#  -h, --help            show this help message and exit

# usage: ais cat [-h] [--file-paths] [--number-lines] [--squeeze-blank]
#
#options:
#  -h, --help       show this help message and exit
#  --file-paths     A list of file paths to concatenate.
#  --number-lines   If True, number all output lines.
#  --squeeze-blank  If True, consecutive blank lines are squeezed to one.
ais cat --file-paths "minimal_shell_example.sh" --number-lines --squeeze-blank --squeeze-blank