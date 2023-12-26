import pytest

import ai_shell.__main__ as cli


def test_just_import():
    assert cli


def test_just_run():
    # The pytest cli args will be useless to the app.
    with pytest.raises(SystemExit) as excinfo:
        cli.run()

    assert excinfo.value.code == 2
