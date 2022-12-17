from .token import TT, Token

##################################
# NODES
##################################


class NumberNode:
    def __init__(self, token: Token) -> None:
        self.token = token

    def __repr__(self) -> str:
        return f'{self.token}'


class BinaryOperationNode:
    def __init__(self, left_token, op_token, right_token) -> None:
        self.left_token = left_token
        self.op_token = op_token
        self.right_token = right_token

    def __repr__(self) -> str:
        return f'({self.left_token} {self.op_token} {self.right_token})'

##################################
# PARSER
##################################


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.token_index = -1
        self.current_token = None
        self.advance()

    def advance(self) -> None:
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        # else:
            # self.current_token = None
        return self.current_token

    def factor(self):
        token = self.current_token

        if token in (TT.INT, TT.FLOAT):
            self.advance()
            return NumberNode(token)

    def term(self):
        return self.binary_operation(self.factor, (TT.MUL, TT.DIV))

    def expression(self):
        return self.binary_operation(self.term, (TT.PLUS, TT.MINUS))

    def binary_operation(self, func, operators):
        left = func()

        while self.current_token.type in operators:
            op_token = self.current_token
            self.advance()
            right = func()
            left = BinaryOperationNode(left, op_token, right)

        return left

    def parse(self):
        return self.expression()
