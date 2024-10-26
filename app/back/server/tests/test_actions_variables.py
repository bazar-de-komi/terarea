"""_summary_
    File in charge of testing the variables class
"""
import os
import sys

sys.path.append(os.path.join("..", os.getcwd()))
sys.path.append(os.getcwd())

try:
    import constants as TCONST
except ImportError as e:
    raise ImportError("Failed to import the unit test constants module") from e

try:
    from src.lib.actions.variables import Variables
except ImportError as e:
    raise ImportError("Failed to import the src module") from e


ERROR = TCONST.ERROR
SUCCESS = TCONST.SUCCESS
DEBUG = TCONST.DEBUG

VI = Variables(
    success=SUCCESS,
    error=ERROR,
    debug=DEBUG
)


def test_add_variable() -> None:
    """_summary_
        Function in charge of testing the add_variable function.
    """
    VI.variables = {}
    assert VI.add_variable("test1", 1, int) == SUCCESS
    assert VI.add_variable("test2", 1, str) == ERROR
    assert VI.add_variable("test3", "1", str) == SUCCESS
    assert VI.variables["test1"] == {"data": 1, "type": int}
    assert "test2" not in VI.variables
    assert VI.variables["test3"] == {"data": "1", "type": str}


def test_update_variable() -> None:
    """_summary_
        Function in charge of testing the update_variable function.
    """
    node1 = {"data": 1, "type": int}
    node2 = {"data": "1", "type": str}
    node3 = {"data": "1", "type": str}
    VI.variables = {
        "test1": node1,
        "test2": node2,
        "test3": node3
    }
    assert VI.update_variable("not_present", 1, int) == ERROR
    assert VI.update_variable("test1", 1, int) == SUCCESS
    assert VI.update_variable("test2", 1, str) == ERROR
    assert VI.update_variable("test3", "1", str) == SUCCESS
    assert "not_present" not in VI.variables
    assert VI.variables["test1"] == node1
    assert VI.variables["test2"] == node2
    assert VI.variables["test3"] == node3


def test_insert_or_update_variable() -> None:
    """_summary_
        Function in charge of testing the insert_or_update function.
    """
    VI.variables = {
        "test4": {"data": "1", "type": str},
        "test5": {"data": "1", "type": str}
    }
    assert VI.insert_or_update("test1", 1, int) == SUCCESS
    assert VI.insert_or_update("test2", 1, str) == ERROR
    assert VI.insert_or_update("test3", "1", str) == SUCCESS
    assert VI.insert_or_update("test4", "1", str) == SUCCESS
    assert VI.insert_or_update("test5", "1", int) == ERROR
    assert VI.variables["test1"] == {"data": 1, "type": int}
    assert "test2" not in VI.variables
    assert VI.variables["test3"] == {"data": "1", "type": str}
    assert VI.variables["test4"] == {"data": "1", "type": str}
    assert VI.variables["test5"] == {"data": "1", "type": str}


def test_has_variable() -> None:
    """_summary_
        Function in charge of testing the has_variable function.
    """
    VI.variables = {
        "test": {"data": "1", "type": str}
    }
    assert VI.has_variable("test") is True
    assert VI.has_variable("test2") is False


def test_get_variable() -> None:
    """_summary_
        Function in charge of testing the get_variable function.
    """
    VI.variables = {
        "test": {"data": "1", "type": str}
    }
    assert VI.get_variable("test") == "1"
    assert VI.get_variable("test2") == ERROR


def test_get_variables() -> None:
    """_summary_
        Function in charge of testing the get_variables function.
    """
    node = {
        "test": {"data": "1", "type": str},
        "test2": {"data": 1, "type": int},
        "test3": {"data": 1.0, "type": float}
    }
    VI.variables = node.copy()
    assert VI.get_variables() == node


def test_get_variable_type() -> None:
    """_summary_
        Function in charge of testing the get_variable_type function.
    """
    VI.variables = {
        "test": {"data": "1", "type": str}
    }
    assert VI.get_variable_type("test") == str
    assert VI.get_variable_type("test2") == ERROR


def test_remove_variable() -> None:
    """_summary_
        Function in charge of testing the remove_variable function.
    """
    VI.variables = {
        "test": {"data": "1", "type": str}
    }
    assert VI.remove_variable("test") == SUCCESS
    assert VI.remove_variable("test") == ERROR
    assert VI.remove_variable("test2") == ERROR
    assert not VI.variables
    VI.variables = {
        "test": {"data": "1", "type": str},
        "test2": {"data": 1, "type": int},
        "test3": {"data": 1.0, "type": float}
    }
    assert VI.remove_variable("test2") == SUCCESS
    assert VI.remove_variable("test") == SUCCESS
    assert VI.remove_variable("test4") == ERROR
    assert "test3" in VI.variables


def test_clear_variables() -> None:
    """_summary_
        Function in charge of testing the clear_variables function.
    """
    VI.variables = {
        "test": {"data": "1", "type": str},
        "test2": {"data": 1, "type": int},
        "test3": {"data": 1.0, "type": float}
    }
    assert VI.clear_variables() == SUCCESS
    assert not VI.variables
