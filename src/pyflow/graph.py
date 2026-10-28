from dataclasses import dataclass, field

from pyflow.models import Task


class WorkflowValidationError(ValueError):
    """Raised when a workflow contains invalid dependencies or cycles."""


@dataclass
class Workflow:
    tasks: dict[str, Task] = field(default_factory=dict)

    def add_task(self, task: Task) -> None:
        if task.name in self.tasks:
            raise ValueError(f"Task '{task.name}' already exists")

        self.tasks[task.name] = task

    def validate(self) -> None:
        for task in self.tasks.values():
            for dependency in task.dependencies:
                if dependency not in self.tasks:
                    raise WorkflowValidationError(
                        f"Task '{task.name}' depends on missing task "
                        f"'{dependency}'"
                    )

       
            topological_order(self)

def topological_order(workflow: Workflow) -> list[str]:
    workflow_tasks = workflow.tasks

    in_degree = {
        name: len(task.dependencies)
        for name, task in workflow_tasks.items()
    }

    ready = sorted(
        name for name, degree in in_degree.items()
        if degree == 0
    )

    result = []

    while ready:
        current = ready.pop(0)
        result.append(current)

        for name in sorted(workflow_tasks):
            if current in workflow_tasks[name].dependencies:
                in_degree[name] -= 1

                if in_degree[name] == 0:
                    ready.append(name)
                    ready.sort()

    if len(result) != len(workflow_tasks):
        raise WorkflowValidationError("Workflow contains a cycle")

    return result
    
def execution_layers(workflow: Workflow) -> list[list[str]]:
    workflow.validate()

    remaining = set(workflow.tasks)
    completed = set()
    layers = []

    while remaining:
        ready = sorted(
            name
            for name in remaining
            if workflow.tasks[name].dependencies <= completed
        )

        if not ready:
            raise WorkflowValidationError("Workflow contains a cycle")

        layers.append(ready)
        completed.update(ready)
        remaining.difference_update(ready)

    return layers