import ai_shell.code_generate as generate


def test_generate_schema(tmp_path):
    target_file = str(tmp_path / "schema.py")
    generate.generate_the_schema(target_file)


def test_generate_toolkit(tmp_path):
    target_file = str(tmp_path / "toolkit.py")
    generate.generate_the_toolkit(target_file)


def test_generate_cli(tmp_path):
    target_file = str(tmp_path / "cli.py")
    generate.generate_the_cli(target_file)
