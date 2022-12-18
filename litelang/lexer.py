from .position import Position
from .token import Token, TT, DIGITS
from .error import IllegalCharError, Error

##################################
# LEXER
##################################


class Lexer:
    def __init__(self, filename: str, text: str) -> None:
        self.text = text
        self.pos = Position(-1, 0, -1, filename, text)
        self.current_char = None
        self.advance()

    def advance(self) -> None:
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(
            self.text) else None

    # def unadvance(self):
    #     self.pos -= 2
    #     self.advance()

    def make_tokens(self) -> tuple[list[Token], Error | None]:
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
                pass
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT.PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT.MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT.MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT.DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT.LEFT_PAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT.RIGHT_PAREN, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{self.current_char}'")

        tokens.append(Token(TT.EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self) -> Token:
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in DIGITS+'.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1

            num_str += self.current_char
            self.advance()

        # self.unadvance()
        if dot_count == 0:
            return Token(TT.INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT.FLOAT, float(num_str), pos_start, self.pos)
