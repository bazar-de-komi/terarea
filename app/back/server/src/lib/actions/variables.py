"""_summary_
    File in charge of tracking the variables for the current action.
"""

from typing import Dict, Any, Type, Union
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME


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
        # -------------------------- Inherited values --------------------------
        self.success: int = success
        self.error: int = error
        self.debug: bool = debug
        self.variables: Dict[str, Any] = {}
        # ---------------------- The visual logger class  ----------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            SAVE_TO_FILE,
            FILE_NAME,
            FILE_DESCRIPTOR,
            debug=self.debug,
            logger=self.__class__.__name__
        )

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
        title = "add_variable"
        if name in self.variables:
            self.disp.log_error(f"Variable: {name} is already present.", title)
            return self.error
        if isinstance(variable_data, variable_type) is False:
            self.disp.log_error(f"Incorrect type for variable {name}.", title)
            return self.error
        self.variables[name] = {"data": variable_data, "type": variable_type}
        msg = f"Variable: {name} of type {variable_type}"
        msg += f"containing {variable_data} successfully added."
        self.disp.log_debug(msg, title)
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
        title = "update_variable"
        if name not in self.variables:
            self.disp.log_error(f"Variable: {name} is not present.", title)
            return self.error
        if isinstance(variable_data, variable_type) is False:
            self.disp.log_error(f"Incorrect type for variable {name}.", title)
            return self.error
        self.variables[name] = {"data": variable_data, "type": variable_type}
        msg = f"Variable: {name} of type {variable_type}"
        msg += f"containing {variable_data} successfully added."
        self.disp.log_debug(msg, title)
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
        title = "insert_or_update"
        if name in self.variables:
            self.disp.log_debug(
                "Variable is already present in the list, updating.", title
            )
            return self.update_variable(name, variable_data, variable_type)
        self.disp.log_debug(
            "Variable is not present in the list, adding.", title
        )
        return self.add_variable(name, variable_data, variable_type)

    def has_variable(self, name: str) -> bool:
        """_summary_
            Check if the variable exists in the current action.

        Args:
            name (str): _description_: The name of the variable

        Returns:
            bool: _description_: Returns True if the variable exists, False otherwise.
        """
        title = "has_variable"
        self.disp.log_debug(f"Checking if variable {name} exists.", title)
        if name not in self.variables:
            self.disp.log_debug(f"Variable {name} exists.", title)
            return False
        self.disp.log_debug(f"Variable {name} does not exist.", title)
        return True

    def get_variable(self, name: str) -> Any:
        """_summary_
            Get the variable from the current action.

        Args:
            name (str): _description_: The name of the variable

        Raises:
            ValueError: _description_: If the variable does not exist.

        Returns:
            Any: _description_: Returns the variable if it exists, self.error otherwise.
        """
        title = "get_variable"
        if name not in self.variables:
            msg = f"Variable {name} not found."
            self.disp.log_error(msg, title)
            raise ValueError(msg)
        self.disp.log_debug(f"Variable {name} found.", title)
        return self.variables[name]["data"]

    def get_variables(self) -> Dict[str, Any]:
        """_summary_
            Get all the variables from the current action.

        Returns:
            Dict[str, Any]: _description_: Returns all the variables.
        """
        self.disp.log_debug("Returning all the variables.", "get_variables")
        return self.variables

    def get_variable_type(self, name: str) -> Union[int, Type]:
        """_summary_
            Get the type of the variable from the current action.

        Args:
            name (str): _description_: The name of the variable

        Returns:
            Type: _description_: Returns the type of the variable if it exists, self.error otherwise.
        """
        title = "get_variable_type"
        if name not in self.variables:
            self.disp.log_error(f"Variable {name} does not exist.", title)
            return self.error
        self.disp.log_debug(f"Retrieving type for {name}", title)
        return self.variables[name]["type"]

    def remove_variable(self, name: str) -> int:
        """_summary_
            Remove the variable from the current action.

        Args:
            name (str): _description_: The name of the variable

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise.
        """
        title = "remove_variable"
        msg = f"Removing variable {name} from the list"
        msg += " if present."
        self.disp.log_debug(msg, title)
        if name not in self.variables:
            self.disp.log_error(f"Variable {name} is not present.", title)
            return self.error
        self.disp.log_debug(f"Removing variable {name} from the list.", title)
        del self.variables[name]
        return self.success

    def clear_variables(self) -> int:
        """_summary_
            Clear all the variables from the current action.

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise.
        """
        title = "clear_variables"
        self.disp.log_debug("Clearing all the variables.", title)
        self.variables = {}
        self.disp.log_debug("All the variables have been cleared.", title)
        return self.success
