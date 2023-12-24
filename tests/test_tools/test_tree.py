from ai_shell.utils.read_fs import tree  # Adjust the import statement as necessary


def test_empty_directory(tmp_path):
    assert tree(tmp_path) == f"{tmp_path.name}\n\n0 directories\n"


def test_non_empty_directory(tmp_path):
    (tmp_path / "dir1").mkdir()
    (tmp_path / "file1.txt").touch()
    expected_output = "\n".join([f"{tmp_path.name}", "├── dir1", "└── file1.txt", "", "1 directories, 1 files", ""])
    assert tree(tmp_path) == expected_output


def test_limit_to_directories(tmp_path):
    (tmp_path / "dir1").mkdir()
    (tmp_path / "file1.txt").touch()
    expected_output = "\n".join([f"{tmp_path.name}", "└── dir1", "", "1 directories", ""])
    assert tree(tmp_path, limit_to_directories=True) == expected_output


# ... additional tests for depth limit, length limit, and various directory structures ...
