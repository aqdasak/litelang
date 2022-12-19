from typing import Any, Self

from litelang.error import Error, InvalidSyntaxError
from litelang.position import Position
from .token import TT, Token, BLANK

##################################
# NODES
##################################


class Node:
    pos_start: Position
    pos_end: Position


class NumberNode(Node):
    # TODO: What is the requirement of this class?
    def __init__(self, token: Token) -> None:
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end

    def __repr__(self) -> str:
        return f'{self.token}'


class BinaryOperationNode(Node):
    def __init__(self, left_node: Node, op_token: Token, right_node: Node) -> None:
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

        self.pos_start = left_node.pos_start
        self.pos_end = right_node.pos_end

    def __repr__(self) -> str:
        return f'({self.left_node} {self.op_token} {self.right_node})'


class UnaryOperationNode(Node):
    def __init__(self, op_token: Token, node: Node) -> None:
        self.op_token = op_token
        self.node = node

        self.pos_start = op_token.pos_start
        self.pos_end = node.pos_end

    def __repr__(self) -> str:
        return f'({self.op_token} {self.node})'


##################################
# PARSE RESULT
##################################


class ParseResult:
    def __init__(self) -> None:
        self.node: Node | None = None
        self.error: Error | None = None

    def propagate(self, result) -> Node | Any:
        if isinstance(result, ParseResult):
            # MAYBE TO PROPAGATE ERROR
            # if result.error:
            #     self.error = result.error
            # MAYBE TO PROPAGATE ERROR
            self.error = result.error

            return result.node
        return result

    def success(self, node: Node) -> Self:
        self.node = node
        return self

    def failure(self, error: Error) -> Self:
        self.error = error
        return self


##################################
# PARSER
##################################


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.token_index = -1
        self.current_token = BLANK
        self.advance()

    def advance(self) -> None:
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            # self.current_token = None
            self.current_token = BLANK
        # return self.current_token

    def factor(self):
        res = ParseResult()
        token = self.current_token
        # print('factor()🚨', token)

        if token.type in (TT.PLUS, TT.MINUS):
            res.propagate(self.advance())
            factor = res.propagate(self.factor())
            if res.error:
                print('⭕')
                return res
            return res.success(UnaryOperationNode(token, factor))

        elif token.type in (TT.INT, TT.FLOAT):
            res.propagate(self.advance())
            return res.success(NumberNode(token))

        elif token.type == TT.LEFT_PAREN:
            res.propagate(self.advance())
            expr = res.propagate(self.expression())
            if res.error:
                return res

            if self.current_token.type == TT.RIGHT_PAREN:
                res.propagate(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, "Expected ')'"))

        return res.failure(InvalidSyntaxError(token.pos_start, token.pos_end, 'Expected int or float'))

    def term(self):
        return self.binary_operation(self.factor, (TT.MUL, TT.DIV))

    def expression(self):
        return self.binary_operation(self.term, (TT.PLUS, TT.MINUS))

    def binary_operation(self, func, operators):
        res = ParseResult()
        left = res.propagate(func())
        if res.error:
            return res

        # print('1🚨', left)

        while self.current_token.type in operators:
            op_token = self.current_token
            # print('2🚨', op_token)
            res.propagate(self.advance())
            right = res.propagate(func())
            # print('3🚨', right)
            # print('🚨', type(left), type(op_token), type(right))
            if res.error:
                return res
            left = BinaryOperationNode(left, op_token, right)
            # print('🚨⭕', left)

        return res.success(left)

    def parse(self):
        res = self.expression()
        if not res.error and self.current_token.type != TT.EOF:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, "Expected '+', '-', '*' or '/'"))
        return res
