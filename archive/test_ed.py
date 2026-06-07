import pytest

from ai_shell.ed_tool import EdTool
from tests.util import config_for_tests


# Test fixture to set up and tear down for each test
@pytest.fixture
def ed_tool(tmpdir):
    # Create an instance of EdTool with a temporary directory
    tool = EdTool(str(tmpdir), config=config_for_tests())
    yield tool
    # Clean up (if needed) after test runs


# Test for 'a' (append) command
def test_append_command(ed_tool):
    script = """
a
> Test Line 1
.
1a
> Test Line 2
.
w
q"""
    ed_tool.ed(script, "test1.txt")
    with open(ed_tool.root_folder + "test1.txt") as f:
        lines = f.readlines()
    assert lines == ["Test Line 1\n", "Test Line 2\n"]


# Add more tests for other commands (e.g., 'k', 'i', 'x', 'm', 'c', 'p', 'l', 'n', 'y', 'd', 'j', 't')
# Here's an example for the 'd' (delete) command
def test_delete_command(ed_tool):
    script = """
a
> Line 1
> Line 2
.
2d
w
q"""
    ed_tool.ed(script, "test2.txt")
    with open(ed_tool.root_folder + "test2.txt") as f:
        lines = f.readlines()
    assert lines == ["Line 1\n"]  # Line 2 should be deleted

    # Test for 'k' (mark) and 'y' (yank) commands
    # def test_mark_and_yank_commands(ed_tool):
    #     # Assuming your implementation of 'ed' supports 'k' for mark and 'y' for yank
    #     commands = """
    # # This part starts the append mode where you can add new lines to the buffer.
    # # After entering the append mode ('a'), each line starting with '> ' is added to the buffer.
    # # The append mode is exited with a single '.' on a new line.
    # a
    # > Line 1
    # > Line 2
    # .
    #
    # # '1ka' sets a mark 'a' at line 1.
    # # 'k' is the command to set a mark, and '1' specifies the line number.
    # 1ka
    #
    # # Similarly, '2kb' sets a mark 'b' at line 2.
    # 2kb
    #
    # # 'ya' moves to the line marked by 'a'.
    # # However, this command might not work as expected in standard 'ed', as 'y' is not a traditional 'ed' command.
    # # You might need to check if your version of 'ed' or the Buffer class supports this.
    # ya
    #
    # # 'yb' similarly attempts to move to the line marked by 'b', with the same caveat as above.
    # yb
    #
    # # 'w' writes the current buffer to the file specified in the script.
    # # 'q' quits the editor.
    # w
    # q
    # """
    #     # I don't think the `ed` package supports `y` with letters/marks?
    #     ed_tool.run(commands, "test.txt")
    #     with open(ed_tool.root_folder + "test.txt", "r") as f:
    #         lines = f.readlines()
    #     assert lines == ["Line 1\n"]  # Who knows

    # okay, many variations on find and replace and this doesn't work.
    # def test_modify_hello_world(ed_tool):
    #     # Assuming ed_tool is an instance of your EdTool class
    #     script = """
    # e filename.py
    # # /print("hello world")/
    # 1s/hello world/hello universe/
    # w
    # q
    #     """
    #     with open(ed_tool.root_folder + "filename.py", "w") as f:
    #         f.write("print(\"hello universe\")")
    #     ed_tool.run(script, "filename.py")

    # # Now read the file and assert the change
    # with open("filename.py", "r") as file:
    #     contents = file.read()
    #     assert 'print("hello universe")' in contents
