"""_summary_
    File in charge of testing the variables class
"""
import os
import sys

import pytest

sys.path.append(os.path.join("..", os.getcwd()))
sys.path.append(os.getcwd())

try:
    import constants as TCONST
except ImportError as e:
    raise ImportError("Failed to import the unit test constants module") from e

try:
    from src.lib.actions.variables import Variables, ScopeError, VariableNotFoundError
except ImportError as e:
    raise ImportError("Failed to import the src module") from e


ERROR = TCONST.ERROR
SUCCESS = TCONST.SUCCESS
DEBUG = TCONST.DEBUG

SCOPE = "test_scope"

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
    assert VI.add_variable("test1", 1, int, scope=SCOPE) == SUCCESS
    with pytest.raises(TypeError):
        VI.add_variable("test2", 1, str, scope=SCOPE)
    assert VI.add_variable("test3", "1", str, scope=SCOPE) == SUCCESS
    assert SCOPE in VI.variables
    assert VI.variables[SCOPE]["test1"] == {"data": 1, "type": int}
    assert "test2" not in VI.variables[SCOPE]
    assert VI.variables[SCOPE]["test3"] == {"data": "1", "type": str}


def test_update_variable() -> None:
    """_summary_
        Function in charge of testing the update_variable function.
    """
    node1 = {"data": 1, "type": int}
    node2 = {"data": "1", "type": str}
    node3 = {"data": "1", "type": str}
    VI.variables = {
        SCOPE: {
            "test1": node1,
            "test2": node2,
            "test3": node3
        }
    }
    with pytest.raises(ScopeError):
        VI.update_variable("not_present", 1, int)
    with pytest.raises(VariableNotFoundError):
        VI.update_variable("not_present", 1, int,  scope=SCOPE)
    with pytest.raises(ScopeError):
        VI.update_variable("test1", 1, int)
    with pytest.raises(ScopeError):
        VI.update_variable("test2", 1, str)
    with pytest.raises(ScopeError):
        VI.update_variable("test3", "1", str)
    assert VI.update_variable("test1", 1, int, scope=SCOPE) == SUCCESS
    with pytest.raises(TypeError):
        VI.update_variable("test2", 1, str, scope=SCOPE)
    assert VI.update_variable("test3", "1", str, scope=SCOPE) == SUCCESS
    assert SCOPE in VI.variables
    assert "not_present" not in VI.variables[SCOPE]
    assert VI.variables[SCOPE]["test1"] == node1
    assert VI.variables[SCOPE]["test2"] == node2
    assert VI.variables[SCOPE]["test3"] == node3


def test_insert_or_update_variable() -> None:
    """_summary_
        Function in charge of testing the insert_or_update function.
    """
    VI.variables = {
        SCOPE: {
            "test4": {"data": "1", "type": str},
            "test5": {"data": "1", "type": str}
        }
    }
    assert VI.insert_or_update("test1", 1, int) == SUCCESS
    with pytest.raises(TypeError):
        VI.insert_or_update("test2", 1, str)
    assert VI.insert_or_update("test3", "1", str) == SUCCESS
    assert VI.insert_or_update("test4", "1", str) == SUCCESS
    assert VI.insert_or_update("test5", 1.0, float) == SUCCESS
    with pytest.raises(TypeError):
        VI.insert_or_update("test5", "1", int)
    assert VI.insert_or_update("test1", 1, int, scope=SCOPE) == SUCCESS
    with pytest.raises(TypeError):
        VI.insert_or_update("test2", 1, str, scope=SCOPE)
    assert VI.insert_or_update("test3", "1", str, scope=SCOPE) == SUCCESS
    assert VI.insert_or_update("test4", "1", str, scope=SCOPE) == SUCCESS
    with pytest.raises(TypeError):
        VI.insert_or_update("test5", "1", int, scope=SCOPE)
    assert SCOPE in VI.variables
    assert VI.variables[SCOPE]["test1"] == {"data": 1, "type": int}
    assert "test2" not in VI.variables[SCOPE]
    assert VI.variables[SCOPE]["test3"] == {"data": "1", "type": str}
    assert VI.variables[SCOPE]["test4"] == {"data": "1", "type": str}
    assert VI.variables[SCOPE]["test5"] == {"data": "1", "type": str}
    assert "default_scope" in VI.variables
    assert VI.variables["default_scope"]["test1"] == {"data": 1, "type": int}
    assert "test2" not in VI.variables["default_scope"]
    assert VI.variables["default_scope"]["test3"] == {"data": "1", "type": str}
    assert VI.variables["default_scope"]["test4"] == {"data": "1", "type": str}
    assert VI.variables["default_scope"]["test5"] == {
        "data": 1.0, "type": float
    }


def test_has_variable() -> None:
    """_summary_
        Function in charge of testing the has_variable function.
    """
    VI.variables = {
        SCOPE: {
            "test": {"data": "1", "type": str}
        },
        "default_scope": {
            "test": {"data": "1", "type": str}
        }
    }
    assert VI.has_variable("test") is True
    assert VI.has_variable("test2") is False
    assert VI.has_variable("test", scope=SCOPE) is True
    assert VI.has_variable("test2", scope=SCOPE) is False
    with pytest.raises(ScopeError):
        VI.has_variable("test", scope="not_a_scope")
    with pytest.raises(ScopeError):
        VI.has_variable("test2", scope="not_a_scope")


def test_get_variable() -> None:
    """_summary_
        Function in charge of testing the get_variable function.
    """
    VI.variables = {
        SCOPE: {
            "test": {"data": "1", "type": str}
        }
    }
    assert VI.get_variable("test", scope=SCOPE) == "1"
    with pytest.raises(ScopeError):
        VI.get_variable("test")
    with pytest.raises(ScopeError):
        VI.get_variable("not_a_variable")
    with pytest.raises(ValueError):
        VI.get_variable("not_a_variable", scope=SCOPE)


def test_get_variables() -> None:
    """_summary_
        Function in charge of testing the get_variables function.
    """
    node = {
        "test": {"data": "1", "type": str},
        "test2": {"data": 1, "type": int},
        "test3": {"data": 1.0, "type": float}
    }
    VI.variables[SCOPE] = node.copy()
    assert VI.get_variables(scope=SCOPE) == node
    assert VI.get_variables("*") == {SCOPE: node}
    with pytest.raises(ScopeError):
        VI.get_variables()


def test_get_variable_type() -> None:
    """_summary_
        Function in charge of testing the get_variable_type function.
    """
    VI.variables = {
        SCOPE: {
            "test": {"data": "1", "type": str}
        }
    }
    with pytest.raises(ScopeError):
        VI.get_variable_type("test")
    with pytest.raises(ScopeError):
        VI.get_variable_type("test2")
    assert VI.get_variable_type("test", scope=SCOPE) == str
    with pytest.raises(ValueError):
        VI.get_variable_type("test2", scope=SCOPE)


def test_remove_variable() -> None:
    """_summary_
        Function in charge of testing the remove_variable function.
    """
    VI.variables = {
        SCOPE: {
            "test": {"data": "1", "type": str}
        }
    }
    assert SCOPE in VI.variables
    with pytest.raises(ScopeError):
        VI.remove_variable("test")
    with pytest.raises(ScopeError):
        VI.remove_variable("test")
    with pytest.raises(ScopeError):
        VI.remove_variable("test2")
    assert VI.remove_variable("test", scope=SCOPE) == SUCCESS
    with pytest.raises(VariableNotFoundError):
        VI.remove_variable("test", scope=SCOPE)
    with pytest.raises(VariableNotFoundError):
        VI.remove_variable("test2", scope=SCOPE)
    assert not VI.variables[SCOPE]


def test_remove_variables_different_types() -> None:
    """_summary_
        Function in charge of testing the remove_variable function with different types.
    """
    VI.variables = {
        SCOPE: {
            "test": {"data": "1", "type": str},
            "test2": {"data": 1, "type": int},
            "test3": {"data": 1.0, "type": float}
        }
    }
    assert SCOPE in VI.variables
    assert VI.remove_variable("test2", scope=SCOPE) == SUCCESS
    assert VI.remove_variable("test", scope=SCOPE) == SUCCESS
    with pytest.raises(VariableNotFoundError):
        VI.remove_variable("test4", scope=SCOPE)
    assert "test3" in VI.variables[SCOPE]


def test_clear_variables_default_scope() -> None:
    """_summary_
        Function in charge of testing the clear_variables function with the "default_scope" variable.
    """
    VI.variables = {
        SCOPE: {
            "test": {"data": "1", "type": str},
            "test2": {"data": 1, "type": int},
            "test3": {"data": 1.0, "type": float}
        },
        "default_scope": {
            "test": {"data": "1", "type": str},
            "test2": {"data": 1, "type": int},
            "test3": {"data": 1.0, "type": float}
        }
    }
    assert VI.clear_variables() == SUCCESS
    with pytest.raises(ScopeError):
        VI.clear_variables(scope="not_a_scope")
    assert "default_scope" in VI.variables
    assert SCOPE in VI.variables
    assert not VI.variables["default_scope"]
    assert len(VI.variables[SCOPE]) > 0


def test_clear_variables_custom_scope() -> None:
    """_summary_
        Function in charge of testing the clear_variables function with the SCOPE variable.
    """
    VI.variables = {
        SCOPE: {
            "test": {"data": "1", "type": str},
            "test2": {"data": 1, "type": int},
            "test3": {"data": 1.0, "type": float}
        },
        "default_scope": {
            "test": {"data": "1", "type": str},
            "test2": {"data": 1, "type": int},
            "test3": {"data": 1.0, "type": float}
        }
    }
    assert VI.clear_variables(scope=SCOPE) == SUCCESS
    with pytest.raises(ScopeError):
        VI.clear_variables(scope="not_a_scope")
    assert SCOPE in VI.variables
    assert "default_scope" in VI.variables
    assert not VI.variables[SCOPE]
    assert len(VI.variables["default_scope"]) > 0


def test_clear_variables_all_scopes() -> None:
    """_summary_
        Function in charge of testing the clear_variables function with the * argument.
    """
    VI.variables = {
        SCOPE: {
            "test": {"data": "1", "type": str},
            "test2": {"data": 1, "type": int},
            "test3": {"data": 1.0, "type": float}
        },
        "default_scope": {
            "test": {"data": "1", "type": str},
            "test2": {"data": 1, "type": int},
            "test3": {"data": 1.0, "type": float}
        }
    }
    assert VI.clear_variables(scope="*") == SUCCESS
    assert "default_scope" in VI.variables
    assert SCOPE in VI.variables
    assert not VI.variables[SCOPE]
    assert not VI.variables["default_scope"]


def test_clear_scopes() -> None:
    """_summary_
        Function in charge of testing the clear_scopes function.
    """
    VI.variables = {
        SCOPE: {
            "test": {"data": "1", "type": str},
            "test2": {"data": 1, "type": int},
            "test3": {"data": 1.0, "type": float}
        },
        "default_scope": {
            "test": {"data": "1", "type": str},
            "test2": {"data": 1, "type": int},
            "test3": {"data": 1.0, "type": float}
        }
    }
    assert VI.clear_scopes() == SUCCESS
    assert not VI.variables
    assert "default_scope" not in VI.variables
    assert SCOPE not in VI.variables


def test_clear_scope_contents() -> None:
    """_summary_
        Function in charge of testing the clear_scope_contents function.
    """
    VI.variables = {
        SCOPE: {
            "test": {"data": "1", "type": str},
            "test2": {"data": 1, "type": int},
            "test3": {"data": 1.0, "type": float}
        },
        "default_scope": {
            "test": {"data": "1", "type": str},
            "test2": {"data": 1, "type": int},
            "test3": {"data": 1.0, "type": float}
        }
    }
    assert VI.clear_scope_contents() == SUCCESS
    assert "default_scope" in VI.variables
    assert SCOPE in VI.variables
    assert not VI.variables[SCOPE]
    assert not VI.variables["default_scope"]
