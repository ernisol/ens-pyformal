"""Contains generic classes for equation definition."""
from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class Operation:
    name: str
    children: Optional[List[Any]] = None

    def evaluate(self, **kwargs) -> float:
        pass

    def derivative(self, variable_name: str):
        pass


class Variable(Operation):
    def __init__(self, name):
        super().__init__(name=name)

    def evaluate(self, **kwargs) -> float:
        if self.name not in kwargs:
            raise ValueError(
                f"Attempted to evaluate variable {self.name} but value was not provided."
            )
        return kwargs[self.name]

    def derivative(self, variable_name: str) -> Operation:
        return Constant(value=1) if self.name==variable_name else Constant(value=0)



class Constant(Operation):
    def __init__(self, value: float) -> None:
        super().__init__(name=str(value))
        self.value= value
    
    def evaluate(self, **kwargs) -> float:
        return self.value
    
    def derivative(self, _) -> Operation:
        return Constant(value=0)


class InvalidDefinitionError(Exception):
    """Raised when an operation was not correctly defined."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidEvaluationError(Exception):
    """Raised when an operation was not correctly defined."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
