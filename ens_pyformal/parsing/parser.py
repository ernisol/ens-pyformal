"""Module for parsing formulas."""

import ast
from ens_pyformal.operations.operators import Sum, Multiply, Divide
from ens_pyformal.operations.generic import Constant, Variable, Operation
from ens_pyformal import constants as cst


def parse(equation: str) -> Operation:
    ast_object: ast.AST = ast.parse(source=equation).body[0].value
    return recursive_parser(ast_object=ast_object)


def recursive_parser(ast_object: ast.AST) -> Operation:
    if isinstance(ast_object, ast.BinOp):
        operation_kind = ast_object.op
        left_member = recursive_parser(ast_object=ast_object.left)
        right_member = recursive_parser(ast_object=ast_object.right)
        if isinstance(operation_kind, ast.Add):
            return Sum(children=[left_member, right_member])
        elif isinstance(operation_kind, ast.Sub):
            return Sum(
                children=[
                    left_member,
                    Multiply(children=[Constant(value=-1), right_member]),
                ]
            )
        elif isinstance(operation_kind, ast.Mult):
            return Multiply(children=[left_member, right_member])
        elif isinstance(operation_kind, ast.Div):
            return Divide(children=[left_member, right_member])
        else:
            raise UnrecognizedOperationException(
                f"{operation_kind} is not handled by the parser."
            )
    elif isinstance(ast_object, ast.Name):
        return Variable(name=ast_object.id)
    elif isinstance(ast_object, ast.Constant):
        return Constant(value=ast_object.value)
    elif isinstance(ast_object, ast.Call):
        return parse_function(ast_object=ast_object)


def parse_function(ast_object: ast.Call) -> Operation:
    function_name = ast_object.func.id.lower()
    if not function_name in cst.IMPLEMENTED_FUNCTIONS:
        raise UnrecognizedOperationException(
            f"Function not implemented: {function_name}"
        )
    children = [recursive_parser(ast_object=child) for child in ast_object.args]
    return cst.IMPLEMENTED_FUNCTIONS[function_name](children=children)


class UnrecognizedOperationException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
