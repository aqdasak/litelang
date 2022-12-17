
from enum import Enum

##################################
# CONSTANTS
##################################

DIGITS = '0123456789'


##################################
# TOKENS
##################################

class TT(Enum):
    INT = 'INT'
    FLOAT = 'FLOAT'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    LEFT_PAREN = 'LPAREN'
    RIGHT_PAREN = 'RPAREN'

    # def __repr__(self) -> str:
    #     return str(self.value)

    def __str__(self) -> str:
        return str(self.value)


class Token:
    def __init__(self, type_: TT, value=None) -> None:
        self.type = type_
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f'{self.type}:{self.value}'
        return str(self.type)
