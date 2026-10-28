import pytest

from pyflow import Task


def example_function(inputs, params):
    return None


def test_create_task():
    task = Task(name="extract", function=example_function)

    assert task.name == "extract"
    assert task.dependencies == frozenset()
    assert task.params == {}


def test_task_with_dependencies_and_params():
    task = Task(
        name="clean",
        function=example_function,
        dependencies=frozenset({"extract"}),
        params={"limit": 10},
    )

    assert task.dependencies == frozenset({"extract"})
    assert task.params == {"limit": 10}


def test_task_cannot_have_empty_name():
    with pytest.raises(ValueError):
        Task(name="", function=example_function)


def test_task_cannot_depend_on_itself():
    with pytest.raises(ValueError):
        Task(
            name="clean",
            function=example_function,
            dependencies=frozenset({"clean"}),
        )