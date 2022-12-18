from typing import Self

##################################
# POSITION
##################################


class Position:
    def __init__(self, index: int, line, column: int, filename: str, text: str) -> None:
        self.index = index
        self.line = line
        self.column = column
        self.filename = filename
        self.text = text

    def advance(self, current_char=None) -> Self:
        self.index += 1
        self.column += 1

        if current_char == '\n':
            self.line += 1
            self.column = 0

        return self

    def copy(self) -> Self:
        return Position(self.index, self.line, self.column, self.filename, self.text)
