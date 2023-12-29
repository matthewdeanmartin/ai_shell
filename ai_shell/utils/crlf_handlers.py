"""
This module contains classes for converting line endings between CRLF and LF.
"""


class LineEndingConverter:
    def __init__(self, file_path: str) -> None:
        """
        Initialize the LineEndingConverter class.

        Args:
            file_path (str): The path of the file to convert.
        """
        self.file_path = file_path
        self.lines: list[bytes] = []
        self.line_endings_type = ""

    def check_line_endings(self) -> str:
        """
        Check and store the type of line endings (CRLF, LF, or Mixed).

        Returns:
            str: The type of line endings
        """
        has_crlf = False
        has_lf = False
        self.lines = []

        with open(self.file_path, "rb") as file:
            for line in file:
                self.lines.append(line)
                if line.endswith(b"\r\n"):
                    has_crlf = True
                elif line.endswith(b"\n"):
                    has_lf = True

                if has_crlf and has_lf:
                    self.line_endings_type = "Mixed"
                    return "Mixed"

        if not self.lines:
            self.line_endings_type = "No lines"
            return "No lines"
        if has_crlf:
            self.line_endings_type = "CRLF"
        elif has_lf:
            self.line_endings_type = "LF"
        else:
            self.line_endings_type = "None"

        return self.line_endings_type

    def dos2unix(self) -> None:
        """
        Convert to Unix line endings (LF), using the stored file data.
        """
        if self.lines is None:
            self.check_line_endings()

        if self.line_endings_type != "LF":
            with open(self.file_path, "wb") as file:
                for line in self.lines:
                    line = line.replace(b"\r\n", b"\n")
                    file.write(line)
        self.line_endings_type = "LF"

    def unix2dos(self) -> None:
        """
        Convert to DOS line endings (CRLF), using the stored file data.
        """
        if self.lines is None:
            self.check_line_endings()

        if self.line_endings_type != "CRLF":
            with open(self.file_path, "wb") as file:
                for line in self.lines:
                    if line.endswith(b"\n") and not line.endswith(b"\r\n"):
                        line = line.replace(b"\n", b"\r\n")
                    file.write(line)
        self.line_endings_type = "CRLF"


if __name__ == "__main__":
    # Example usage
    def run() -> None:
        """
        Example usage
        """
        converter = LineEndingConverter(__file__)
        print(converter.check_line_endings())
        converter.unix2dos()

        converter.dos2unix()

    run()
