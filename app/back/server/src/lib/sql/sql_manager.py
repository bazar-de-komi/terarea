"""
    File in charge of containing the interfacing between an sql library and the program.
    This contains functions that simplify the process of interracting with databases as well as check for injection attempts.
"""
from typing import Union, List, Dict, Any

import mysql.connector
import mysql.connector.cursor
from display_tty import Disp, TOML_CONF, SAVE_TO_FILE, FILE_NAME
from .injection import Injection
from .time_manipulation import TimeManipulation
from .sql_connections import SQLManageConnections
from .sanitisation_functions import SanitiseFunctions
from .sql_query_boilerplates import SQLQueryBoilerplates


class SQL:
    """
    The class in charge of managing a SQL database
    """

    def __init__(self, url: str, port: int, username: str, password: str, db_name: str, success: int = 0, error: int = 84, debug: bool = False):
        """
        The constructor of the SQL class
        Args:
            url (str): _description_
            port (int): _description_
            username (str): _description_
            password (str): _description_
            db_name (str): _description_
            success (int, optional): _description_. Defaults to 0.
            error (int, optional): _description_. Defaults to 84.
            debug (bool, optional): _description_. Defaults to False.
        """
        self.debug: bool = debug
        self.success: int = success
        self.error: int = error
        self.url: str = url
        self.port: int = port
        self.username: str = username
        self.password: str = password
        self.db_name: str = db_name
        # --------------------------- logger section ---------------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            SAVE_TO_FILE,
            FILE_NAME,
            debug=self.debug,
            logger=self.__class__.__name__
        )
        # ------------- The class in charge of the sql connection  -------------
        self.sql_manage_connections: SQLManageConnections = SQLManageConnections(
            url=self.url,
            port=self.port,
            username=self.username,
            password=self.password,
            db_name=self.db_name,
            success=self.success,
            error=self.error,
            debug=self.debug
        )
        # ---------------------------- sql section  ----------------------------
        self.injection: Injection = Injection(
            self.error,
            self.success,
            self.debug
        )
        # ---------------------------- Time logger  ----------------------------
        self.time_manipulation: TimeManipulation = TimeManipulation(self.debug)
        self.datetime_to_string: TimeManipulation.datetime_to_string = self.time_manipulation.datetime_to_string
        self.string_to_datetime: TimeManipulation.string_to_datetime = self.time_manipulation.string_to_datetime
        self._get_correct_now_value: TimeManipulation.get_correct_now_value = self.time_manipulation.get_correct_now_value
        self._get_correct_current_date_value: TimeManipulation.get_correct_current_date_value = self.time_manipulation.get_correct_current_date_value
        # -------------------- Keyword sanitizing functions --------------------
        self.sanitize_functions: SanitiseFunctions = SanitiseFunctions(
            self.debug
        )
        self._protect_sql_cell: SanitiseFunctions.protect_sql_cell = self.sanitize_functions.protect_sql_cell
        self._escape_risky_column_names: SanitiseFunctions.escape_risky_column_names = self.sanitize_functions.escape_risky_column_names
        self._escape_risky_column_names_where_mode: SanitiseFunctions.escape_risky_column_names_where_mode = self.sanitize_functions.escape_risky_column_names_where_mode
        self._check_sql_cell: SanitiseFunctions.check_sql_cell = self.sanitize_functions.check_sql_cell
        # --------------------------- debug section  ---------------------------
        self.sql_manage_connections.show_connection_info("__init__")
        # --------------------------- initialise pool --------------------------
        if self.sql_manage_connections.initialise_pool() != self.success:
            msg = "Failed to initialise the connection pool."
            self.disp.log_critical(msg, "__init__")
            raise RuntimeError(f"Error: {msg}")
        # ----------------------- sql query boilerplates -----------------------
        self.sql_query_boilerplates: SQLQueryBoilerplates = SQLQueryBoilerplates(
            sql_pool=self.sql_manage_connections, success=self.success,
            error=self.error, debug=self.debug
        )

    def __del__(self) -> None:
        """
            Disconnect the database when the class is destroyed
        """
        if self.sql_manage_connections is not None:
            del self.sql_manage_connections
