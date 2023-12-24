from ai_shell.read_py_source import astify, minify


def test_minify():
    assert minify(__file__)


def test_astify():
    assert astify(__file__)
