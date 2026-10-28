import pytest

from pyflow import (
    Task,
    Workflow,
    WorkflowValidationError,
    topological_order,
    execution_layers,
)


def example_function(inputs, params):
    return None


def make_task(name, dependencies=frozenset()):
    return Task(
        name=name,
        function=example_function,
        dependencies=frozenset(dependencies),
    )


def test_empty_workflow():
    workflow = Workflow()

    assert topological_order(workflow) == []
    workflow.validate()


def test_single_task():
    workflow = Workflow()
    workflow.add_task(make_task("extract"))

    assert topological_order(workflow) == ["extract"]


def test_task_chain():
    workflow = Workflow()
    workflow.add_task(make_task("extract"))
    workflow.add_task(make_task("clean", {"extract"}))
    workflow.add_task(make_task("report", {"clean"}))

    assert topological_order(workflow) == [
        "extract",
        "clean",
        "report",
    ]


def test_independent_tasks_are_sorted():
    workflow = Workflow()
    workflow.add_task(make_task("zebra"))
    workflow.add_task(make_task("apple"))

    assert topological_order(workflow) == ["apple", "zebra"]


def test_duplicate_task_is_rejected():
    workflow = Workflow()
    workflow.add_task(make_task("extract"))

    with pytest.raises(ValueError):
        workflow.add_task(make_task("extract"))


def test_missing_dependency_is_detected():
    workflow = Workflow()
    workflow.add_task(make_task("clean", {"extract"}))

    with pytest.raises(WorkflowValidationError):
        workflow.validate()


def test_cycle_is_detected():
    workflow = Workflow()
    workflow.add_task(make_task("a", {"b"}))
    workflow.add_task(make_task("b", {"a"}))

    with pytest.raises(WorkflowValidationError):
        workflow.validate()


def test_order_is_deterministic():
    workflow = Workflow()
    workflow.add_task(make_task("c"))
    workflow.add_task(make_task("b"))
    workflow.add_task(make_task("a"))

    first = topological_order(workflow)
    second = topological_order(workflow)

    assert first == second == ["a", "b", "c"]

def test_execution_layers():
    workflow = Workflow()
    workflow.add_task(make_task("extract"))
    workflow.add_task(make_task("clean_a", {"extract"}))
    workflow.add_task(make_task("clean_b", {"extract"}))
    workflow.add_task(make_task("report", {"clean_a", "clean_b"}))

    assert execution_layers(workflow) == [
        ["extract"],
        ["clean_a", "clean_b"],
        ["report"],
    ]