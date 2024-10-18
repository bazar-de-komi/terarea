"""
    File in charge of cleaning and sanitising sql queries before they are submitted to the database.
"""

from typing import List, Union
from display_tty import Disp, TOML_CONF, SAVE_TO_FILE, FILE_NAME

from . import sql_constants as SCONST
from .time_manipulation import TimeManipulation


class SanitiseFunctions:
    """_summary_
    """

    def __init__(self, debug: bool = False) -> None:
        """_summary_
            This is the class that contains functions in charge of sanitising sql queries.

        Args:
            debug (bool, optional): _description_. Defaults to False.: enable debug mode
        """
        self.debug: bool = debug
        # --------------------------- logger section ---------------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            SAVE_TO_FILE,
            FILE_NAME,
            debug=self.debug,
            logger=self.__class__.__name__
        )
        # ----------------- Database risky keyword sanitising  -----------------
        self.risky_keywords: List[str] = SCONST.RISKY_KEYWORDS
        self.keyword_logic_gates: List[str] = SCONST.KEYWORD_LOGIC_GATES
        # ---------------------- Time manipulation class  ----------------------
        self.time_manipulation: TimeManipulation = TimeManipulation(self.debug)

    def protect_sql_cell(self, cell: str) -> str:
        """_summary_
            This is a function in charge of cleaning by nullifying (escaping) characters that could cause the sql command to break.

        Args:
            cells (str): _description_: The cell to be checked

        Returns:
            str: _description_: A (hopfully) clean string.
        """
        result = ""
        for char in cell:
            if char in ("'", '"', "\\", '\0', "\r"):
                self.disp.log_info(
                    f"Escaped character '{char}' in '{cell}'.",
                    "_protect_sql_cell"
                )
                result += "\\"+char
            else:
                result += char
        return result

    def escape_risky_column_names(self, columns: Union[List[str], str]) -> Union[List[str], str]:
        """_summary_
            Escape the risky column names.

        Args:
            columns (List[str]): _description_

        Returns:
            List[str]: _description_
        """
        title = "_escape_risky_column_names"
        self.disp.log_debug("Escaping risky column names.", title)
        if isinstance(columns, str):
            data = [columns]
        else:
            data = columns
        for index, item in enumerate(data):
            if "=" in item:
                key, value = item.split("=", maxsplit=1)
                self.disp.log_debug(f"key = {key}, value = {value}", title)
                if key.lower() in self.risky_keywords:
                    self.disp.log_warning(
                        f"Escaping risky column name '{key}'.",
                        "_escape_risky_column_names"
                    )
                    data[index] = f"`{key}`={value}"
            elif item.lower() in self.risky_keywords:
                self.disp.log_warning(
                    f"Escaping risky column name '{item}'.",
                    "_escape_risky_column_names"
                )
                data[index] = f"`{item}`"
            else:
                continue
        self.disp.log_debug("Escaped risky column names.", title)
        if isinstance(columns, str):
            return data[0]
        return columns

    def escape_risky_column_names_where_mode(self, columns: Union[List[str], str]) -> Union[List[str], str]:
        """
        Escape the risky column names in where mode, except for those in keyword_logic_gates.

        Args:
            columns (Union[str, List[str]]): Column names to be processed.

        Returns:
            Union[List[str], str]: Processed column names with risky ones escaped.
        """
        title = "_escape_risky_column_names_where_mode"
        self.disp.log_debug(
            "Escaping risky column names in where mode.",
            title
        )

        if isinstance(columns, str):
            data = [columns]
        else:
            data = columns

        for index, item in enumerate(data):
            if "=" in item:
                key, value = item.split("=", maxsplit=1)
                self.disp.log_debug(f"key = {key}, value = {value}", title)

                if key.lower() not in self.keyword_logic_gates and key.lower() in self.risky_keywords:
                    self.disp.log_warning(
                        f"Escaping risky column name '{key}'.",
                        title
                    )
                    data[index] = f"\'{key}\'={value}"

            elif item.lower() not in self.keyword_logic_gates and item.lower() in self.risky_keywords:
                self.disp.log_warning(
                    f"Escaping risky column name '{item}'.",
                    title
                )
                data[index] = f"\'{item}\'"

        self.disp.log_debug("Escaped risky column names in where mode.", title)

        if isinstance(columns, str):
            return data[0]
        return data

    def check_sql_cell(self, cell: str) -> str:
        """_summary_
            Check if the cell is a string or a number.

        Args:
            cell (str): _description_

        Returns:
            str: _description_
        """
        if isinstance(cell, (str, float)) is True:
            cell = str(cell)
        if isinstance(cell, str) is False:
            msg = "The expected type of the input is a string,"
            msg += f"but got {type(cell)}"
            self.disp.log_error(msg, "_check_sql_cell")
            return cell
        cell = self.protect_sql_cell(cell)
        tmp = cell.lower()
        if tmp in ("now", "now()"):
            tmp = self.time_manipulation.get_correct_now_value()
        elif tmp in ("current_date", "current_date()"):
            tmp = self.time_manipulation.get_correct_current_date_value()
        else:
            tmp = str(cell)
        if ";base" not in tmp:
            self.disp.log_debug(f"result = {tmp}", "_check_sql_cell")
        return f"\"{str(tmp)}\""
