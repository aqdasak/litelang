from typing import Any, Self
from litelang.error import Error, RTError
from litelang.parser import Node, NumberNode, BinaryOperationNode, UnaryOperationNode
from litelang.position import Position
from litelang.token import TT


##################################
# NUMBER
##################################

class Number:
    def __init__(self, value) -> None:
        # print(type(value))
        self.value = value
        # self.set_pos(None, None)

    # def set_pos(self, pos_start: Position | None, pos_end: Position | None):
    def set_pos(self, pos_start: Position, pos_end: Position):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def added_to(self, other: Self) -> tuple[Self, None] | tuple[None, RTError]:
        return Number(self.value+other.value), None

    def subtracted_by(self, other: Self) -> tuple[Self, None] | tuple[None, RTError]:
        return Number(self.value-other.value), None

    def multiplied_by(self, other: Self) -> tuple[Self, None] | tuple[None, RTError]:
        return Number(self.value*other.value), None

    def divided_by(self, other: Self) -> tuple[Self, None] | tuple[None, RTError]:
        if other.value == 0:
            return None, RTError(other.pos_start, other.pos_end, 'Division by zero error')

        return Number(self.value/other.value), None

    def __repr__(self) -> str:
        return str(self.value)


##################################
# RUNTIME RESULT
##################################


class RTResult:
    def __init__(self) -> None:
        self.value: Number | None = None
        self.error: Error | None = None

    def propagate(self, result: Self) -> Number:
        self.error = result.error
        return result.value

    def success(self, value: Number) -> Self:
        self.value = value
        return self

    def failure(self, error: Error) -> Self:
        self.error = error
        return self


##################################
# INTERPRETER
##################################


class Interpreter:
    def visit(self, node: Node) -> RTResult:
        # print('$', node)
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node: Node):
        raise Exception(f'No visit_{type(node).__name__} defined')

########################

    def visit_NumberNode(self, node: NumberNode) -> RTResult:
        return RTResult().success(
            Number(node.token.value).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinaryOperationNode(self, node: BinaryOperationNode):
        # print('visit_BinaryOperationNode')
        res = RTResult()
        left_num = res.propagate(self.visit(node.left_node))
        if res.error:
            return res

        right_num = res.propagate(self.visit(node.right_node))
        if res.error:
            return res

        op_token = node.op_token

        # if op_token.type == TT.PLUS:
        #     return left_num.added_to(right_num)
        # elif op_token.type == TT.MINUS:
        #     return left_num.subtracted_by(right_num)
        # elif op_token.type == TT.MUL:
        #     return left_num.multiplied_by(right_num)
        # elif op_token.type == TT.DIV:
        #     return left_num.divided_by(right_num)

        error = None
        if op_token.type == TT.PLUS:
            result, error = left_num.added_to(right_num)
        elif op_token.type == TT.MINUS:
            result, error = left_num.subtracted_by(right_num)
        elif op_token.type == TT.MUL:
            result, error = left_num.multiplied_by(right_num)
        elif op_token.type == TT.DIV:
            result, error = left_num.divided_by(right_num)

        if error:
            return res.failure(error)
        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOperationNode(self, node: UnaryOperationNode):
        # print('visit_UnaryOperationNode')
        res = RTResult()
        num = res.propagate(self.visit(node.node))
        if res.error:
            return res
        # print('⭕', num)

        error = None
        if node.op_token.type == TT.MINUS:
            num, error = num.multiplied_by(Number(-1))

        if error:
            return res.failure(error)
        return res.success(num.set_pos(node.pos_start, node.pos_end))
