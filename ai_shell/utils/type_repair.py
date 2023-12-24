"""
Bot frequently does lists in 3 different ways.
"""


def convert_to_list(possible_list: str) -> list[str]:
    # Check for list mess up.
    if isinstance(possible_list, str):
        if ", " in possible_list:
            # TODO: detect "foo.py, bar.py" as opposed to "'foo bar.py'"
            possible_list = possible_list.split(", ")
        elif "," in possible_list:
            # TODO: detect "foo.py,bar.py" as opposed to "'foo bar.py'"
            possible_list = possible_list.split(",")
        else:
            possible_list = [possible_list]
    return possible_list
