from ai_shell.utils.json_utils import try_everything

# Doesn't apply to orjson?
# def test_encoder():
#     assert LoosyGoosyEncoder().default(set()) == []
#
#     def foo():
#         yield 1
#
#     assert LoosyGoosyEncoder().default(foo()) == [1]
#
#     @dataclasses.dataclass
#     class Foo:
#         """A simple dataclass"""
#
#         x: int
#
#     thing = LoosyGoosyEncoder().default(Foo(1))
#     assert thing["x"] == 1


def test_try_everything():
    assert (
        try_everything(
            r"""{
        "glob_pattern": "*.py",
        "regex": "(logger|logging\.|print)",
        "maximum_matches": 1
    }"""
        )
        == {"glob_pattern": "*.py", "regex": r"(logger|logging\.|print)", "maximum_matches": 1}
    )
