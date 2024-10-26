"""_summary_
    File in charge of tracking the variables for the current action.
"""

from typing import Dict, List, Any, Type


class Variables:
    """_summary_
    """

    def __init__(self, success: int = 0, error: int = 84, debug: bool = False):
        """_summary_
            Class in charge of storing and restoring variables.

        Args:
            success (int, optional): _description_. Defaults to 0.
            error (int, optional): _description_. Defaults to 84.
            debug (bool, optional): _description_. Defaults to False.
        """
        self.success: int = success
        self.error: int = error
        self.debug: bool = debug
        self.variables: Dict[str, Any] = {}

    def add_variable(self, name: str, variable_data: Any, variable_type: Type = str) -> int:
        """_summary_
            Add a variable to the current action.

        Args:
            name (str): _description_: The name of the variable
            variable_data (Any): _description_: The data of the given variable
            variable_type (Type): _description_: The type of the data

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise.
        """
        if name in self.variables:
            return self.error
        if isinstance(variable_data, variable_type) is False:
            return self.error
        self.variables[name] = {"data": variable_data, "type": variable_type}
        return self.success

    def update_variable(self, name: str, variable_data: Any, variable_type: Type = str) -> int:
        """_summary_
            Update the variable from the current action.

        Args:
            name (str): _description_: The name of the variable
            variable_data (Any): _description_: The data of the given variable
            variable_type (Type): _description_: The type of the data

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise.
        """
        if name not in self.variables:
            return self.error
        if isinstance(variable_data, variable_type) is False:
            return self.error
        self.variables[name] = {"data": variable_data, "type": variable_type}
        return self.success

    def insert_or_update(self, name: str, variable_data: Any, variable_type: Type = str) -> int:
        """_summary_
            Insert or update the variable from the current action.

        Args:
            name (str): _description_: The name of the variable
            variable_data (Any): _description_: The data of the given variable
            variable_type (Type): _description_: The type of the data

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise.
        """
        if name in self.variables:
            return self.update_variable(name, variable_data, variable_type)
        return self.add_variable(name, variable_data, variable_type)

    def has_variable(self, name: str) -> bool:
        """_summary_
            Check if the variable exists in the current action.

        Args:
            name (str): _description_: The name of the variable

        Returns:
            bool: _description_: Returns True if the variable exists, False otherwise.
        """
        return name in self.variables

    def get_variable(self, name: str) -> Any:
        """_summary_
            Get the variable from the current action.

        Args:
            name (str): _description_: The name of the variable

        Returns:
            Any: _description_: Returns the variable if it exists, self.error otherwise.
        """
        if name not in self.variables:
            return self.error
        return self.variables[name]["data"]

    def get_variables(self) -> Dict[str, Any]:
        """_summary_
            Get all the variables from the current action.

        Returns:
            Dict[str, Any]: _description_: Returns all the variables.
        """
        return self.variables

    def get_variable_type(self, name: str) -> Type:
        """_summary_
            Get the type of the variable from the current action.

        Args:
            name (str): _description_: The name of the variable

        Returns:
            Type: _description_: Returns the type of the variable if it exists, self.error otherwise.
        """
        if name not in self.variables:
            return self.error
        return self.variables[name]["type"]

    def remove_variable(self, name: str) -> int:
        """_summary_
            Remove the variable from the current action.

        Args:
            name (str): _description_: The name of the variable

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise.
        """
        if name not in self.variables:
            return self.error
        del self.variables[name]
        return self.success

    def clear_variables(self) -> int:
        """_summary_
            Clear all the variables from the current action.

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise.
        """
        self.variables = {}
        return self.success
