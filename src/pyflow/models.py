from dataclasses import dataclass, field
from collections.abc import Callable, Mapping
from typing import Any


@dataclass
class Task:
    name: str
    function: Callable[[Mapping[str, Any], Mapping[str, Any]], Any]
    dependencies: frozenset[str] = field(default_factory=frozenset)
    params: Mapping[str, Any] = field(default_factory=dict)
    description: str = ""

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Task name cannot be empty")

        if self.name in self.dependencies:
            raise ValueError("Task cannot depend on itself")

        self.dependencies = frozenset(self.dependencies)
        self.params = dict(self.params)