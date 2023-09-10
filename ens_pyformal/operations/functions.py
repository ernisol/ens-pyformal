"""Module defining usual functions (sin, cos, power...)."""

from typing import List

import numpy as np

from ens_pyformal.operations.generic import InvalidDefinitionError, Operation, Constant
from ens_pyformal.operations.operators import Multiply


class Sin(Operation):
    def __init__(self, children: List[Operation]) -> None:
        if len(children) != 1:
            raise InvalidDefinitionError(
                f"Sin function expects one child, but {len(children)} were provided."
            )
        super().__init__(name="sin", children=children)

    def evaluate(self, **kwargs) -> float:
        return np.sin(self.children[0].evaluate(**kwargs))

    def derivative(self, variable_name: str):
        return Multiply([self.children[0].derivative(variable_name), Cos(children=self.children)])


class Cos(Operation):
    def __init__(self, children: List[Operation]) -> None:
        if len(children) != 1:
            raise InvalidDefinitionError(
                f"Cos function expects one child, but {len(children)} were provided."
            )
        super().__init__(name="cos", children=children)

    def evaluate(self, **kwargs) -> float:
        return np.cos(self.children[0].evaluate(**kwargs))
    
    def derivative(self, variable_name: str):
        return Multiply([Constant(value=-1), self.children[0].derivative(variable_name), Sin(children=self.children)])
