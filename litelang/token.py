
from enum import Enum

from litelang.position import Position

##################################
# CONSTANTS
##################################

DIGITS = '0123456789'


##################################
# TOKEN TYPES
##################################

class TT(Enum):
    INT = 'Int'
    FLOAT = 'Float'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    LEFT_PAREN = 'LParen'
    RIGHT_PAREN = 'RParen'
    BLANKTYPE = 'BlankType'
    EOF = 'EOF'

    # def __repr__(self) -> str:
    #     return str(self.value)

    def __str__(self) -> str:
        return str(self.value)


class Token:
    def __init__(self, type_: TT, value=None, pos_start: Position = None, pos_end: Position = None) -> None:
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def __repr__(self) -> str:
        if self.value:
            return f'{self.type}:{self.value}'
        return str(self.type)


class BlankType(Token):
    def __init__(self) -> None:
        super().__init__(TT.BLANKTYPE, TT.BLANKTYPE)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, BlankType):
            return True
        return False


BLANK = BlankType()
