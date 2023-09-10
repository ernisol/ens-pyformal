"""Module defining common operators (sum, multiplication, division...)."""

from typing import List

from ens_pyformal.operations.generic import Constant, InvalidDefinitionError, Operation


class Sum(Operation):
    def __init__(self, children: List[Operation]) -> None:
        super().__init__(name="sum", children=children)

    def evaluate(self, **kwargs) -> float:
        return sum([child.evaluate(**kwargs) for child in self.children])

    def derivative(self, variable_name: str) -> Operation:
        return Sum(
            children=[
                child.derivative(variable_name=variable_name) for child in self.children
            ]
        )


class Multiply(Operation):
    def __init__(self, children: List[Operation]) -> None:
        super().__init__(name="multiply", children=children)

    def evaluate(self, **kwargs) -> float:
        result = 1
        for child in self.children:
            result *= child.evaluate(**kwargs)
        return result

    def derivative(self, variable_name: str) -> Operation:
        terms = []
        for i, child in enumerate(self.children):
            terms.append(
                Multiply(
                    children=[
                        child.derivative(variable_name),
                        *[
                            other_child
                            for j, other_child in enumerate(self.children)
                            if i != j
                        ],
                    ]
                )
            )
        return Sum(children=terms)


class Divide(Operation):
    def __init__(self, children: List[Operation]) -> None:
        if len(children) != 2:
            raise InvalidDefinitionError(
                f"Divide operator requires two children, {len(children)} provided."
            )
        super().__init__(name="divide", children=children)

    def evaluate(self, **kwargs) -> float:
        return self.children[0].evaluate(**kwargs) / self.children[1].evaluate(**kwargs)

    def derivative(self, variable_name: str):
        u = self.children[0]
        v = self.children[1]
        numerator = Sum(
            [
                Multiply([u.derivative(variable_name), v]),
                Multiply([v.derivative(variable_name), u, Constant(value=-1)]),
            ]
        )
        denominator = Multiply([v, v])
        return Divide([numerator, denominator])
