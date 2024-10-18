"""
    File in charge of containing the interfacing between an sql library and the program.
    This contains functions that simplify the process of interracting with databases as well as check for injection attempts.
"""
from typing import Union, List, Dict, Any

import mysql.connector
import mysql.connector.cursor
from display_tty import Disp, TOML_CONF, SAVE_TO_FILE, FILE_NAME
from . import sql_constants as SCONST
from .injection import Injection
from .time_manipulation import TimeManipulation
from .sanitisation_functions import SanitiseFunctions
from ..components import constants as CONST


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
        # ----------------------------- sql section -----------------------------
        self.pool: mysql.connector.pooling.MySQLConnectionPool = None
        self.connection: mysql.connector.pooling.PooledMySQLConnection = None
        self.cursor: mysql.connector.cursor.MySQLCursor = None
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
        # --------------------------- logger section ---------------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            SAVE_TO_FILE,
            FILE_NAME,
            debug=self.debug,
            logger=self.__class__.__name__
        )
        # -------------------- Keyword sanitizing functions --------------------
        self.sanitize_functions: SanitiseFunctions = SanitiseFunctions(
            self.debug
        )
        self._protect_sql_cell: SanitiseFunctions.protect_sql_cell = self.sanitize_functions.protect_sql_cell
        self._escape_risky_column_names: SanitiseFunctions.escape_risky_column_names = self.sanitize_functions.escape_risky_column_names
        self._escape_risky_column_names_where_mode: SanitiseFunctions.escape_risky_column_names_where_mode = self.sanitize_functions.escape_risky_column_names_where_mode
        self._check_sql_cell: SanitiseFunctions.check_sql_cell = self.sanitize_functions.check_sql_cell
        # -------------------------- datetime parsing --------------------------
        self.date_only: str = SCONST.DATE_ONLY
        self.date_and_time: str = SCONST.DATE_AND_TIME
        # --------------------------- debug section  ---------------------------
        self.show_connection_info("__init__")
        # --------------------------- initialise pool --------------------------
        self._recreate_pool()

    def __del__(self) -> None:
        """
            Disconnect the database when the class is destroyed
        """
        self.disconnect_db()

    def show_connection_info(self, func_name: str = "show_connection_info") -> None:
        """
            Show the connection information
        """
        msg = "\n"
        msg += f"pool_name = '{CONST.DATABASE_POOL_NAME}': "
        msg += f"{type(CONST.DATABASE_POOL_NAME)}\n"
        msg += "max_pool_connections = "
        msg += f"'{CONST.DATABASE_MAX_POOL_CONNECTIONS}': "
        msg += f"{type(CONST.DATABASE_MAX_POOL_CONNECTIONS)}\n"
        msg += "reset_pool_node_connection = "
        msg += f"'{CONST.DATABASE_RESET_POOL_NODE_CONNECTION}': "
        msg += f"{type(CONST.DATABASE_RESET_POOL_NODE_CONNECTION)}\n"
        msg += f"self.debug = '{self.debug}': {type(self.debug)}\n"
        msg += f"self.success = '{self.success}': {type(self.success)}\n"
        msg += f"self.error = '{self.error}': {type(self.error)}\n"
        msg += f"self.url = '{self.url}': {type(self.url)}\n"
        msg += f"self.port = '{self.port}': {type(self.port)}\n"
        msg += f"self.username = '{self.username}': {type(self.username)}\n"
        msg += f"self.password = '{self.password}': {type(self.password)}\n"
        msg += f"self.db_name = '{self.db_name}': {type(self.db_name)}\n"
        msg += f"self.connection = '{self.connection}':"
        msg += f" {type(self.connection)}\n"
        msg += f"self.cursor = '{self.cursor}': {type(self.cursor)}\n"
        msg += f"self.injection = '{self.injection}': {type(self.injection)}\n"
        # msg += f"connection_timeout='{CONST.DATABASE_CONNECTION_TIMEOUT}':"
        # msg += f"{type(CONST.DATABASE_CONNECTION_TIMEOUT)}\n"
        # msg += f"read_timeout='{CONST.DATABASE_READ_TIMEOUT}':"
        # msg += f" {type(CONST.DATABASE_READ_TIMEOUT)}\n"
        # msg += f"write_timeout='{CONST.DATABASE_WRITE_TIMEOUT}':"
        # msg += f" {type(CONST.DATABASE_WRITE_TIMEOUT)}\n"
        # msg += f"local_infile='{CONST.DATABASE_LOCAL_INFILE}':"
        # msg += f" {type(CONST.DATABASE_LOCAL_INFILE)}\n"
        # msg += f"compress='{CONST.DATABASE_COMPRESS}':"
        # msg += f" {type(CONST.DATABASE_COMPRESS)}\n"
        # msg += f"init_command='{CONST.DATABASE_INIT_COMMAND}':"
        # msg += f" {type(CONST.DATABASE_INIT_COMMAND)}\n"
        # msg += f"default_file='{CONST.DATABASE_DEFAULT_FILE}':"
        # msg += f" {type(CONST.DATABASE_DEFAULT_FILE)}\n"
        # msg += f"default_group='{CONST.DATABASE_DEFAULT_GROUP}':"
        # msg += f" {type(CONST.DATABASE_DEFAULT_GROUP)}\n"
        # msg += f"plugin_dir='{CONST.DATABASE_PLUGIN_DIR}':"
        # msg += f" {type(CONST.DATABASE_PLUGIN_DIR)}\n"
        # msg += f"reconnect='{CONST.DATABASE_RECONNECT}':"
        # msg += f" {type(CONST.DATABASE_RECONNECT)}\n"
        # msg += f"ssl_key='{CONST.DATABASE_SSL_KEY}':"
        # msg += f" {type(CONST.DATABASE_SSL_KEY)}\n"
        # msg += f"ssl_cert='{CONST.DATABASE_SSL_CERT}':"
        # msg += f" {type(CONST.DATABASE_SSL_CERT)}\n"
        # msg += f"ssl_ca='{CONST.DATABASE_SSL_CA}':"
        # msg += f" {type(CONST.DATABASE_SSL_CA)}\n"
        # msg += f"ssl_capath='{CONST.DATABASE_SSL_CAPATH}':"
        # msg += f" {type(CONST.DATABASE_SSL_CAPATH)}\n"
        # msg += f"ssl_cipher='{CONST.DATABASE_SSL_CIPHER}':"
        # msg += f" {type(CONST.DATABASE_SSL_CIPHER)}\n"
        # msg += f"ssl_crlpath='{CONST.DATABASE_SSL_CRLPATH}':"
        # msg += f" {type(CONST.DATABASE_SSL_CRLPATH)}\n"
        # msg += f"ssl_verify_cert='{CONST.DATABASE_SSL_VERIFY_CERT}':"
        # msg += f" {type(CONST.DATABASE_SSL_VERIFY_CERT)}\n"
        # msg += f"ssl='{CONST.DATABASE_SSL}':"
        # msg += f" {type(CONST.DATABASE_SSL)}\n"
        # msg += f"tls_version='{CONST.DATABASE_TLS_VERSION}':"
        # msg += f" {type(CONST.DATABASE_TLS_VERSION)}\n"
        # msg += f"autocommit='{CONST.DATABASE_AUTOCOMMIT}':"
        # msg += f" {type(CONST.DATABASE_AUTOCOMMIT)}\n"
        # msg += f"converter='{CONST.DATABASE_CONVERTER}':"
        # msg += f" {type(CONST.DATABASE_CONVERTER)}\n"
        self.disp.log_debug(msg, func_name)

    def _beautify_table(self, column_names: List[str], table_content: List[List[Any]]) -> Union[List[Dict[str, Any]], int]:
        """_summary_
            Convert the table to an easier version for navigating.

        Args:
            column_names (List[str]): _description_
            table_content (List[List[Any]]): _description_

        Returns:
            Union[List[Dict[str, Any]], int]: _description_: the formated content or self.error if an error occured.
        """
        data: List[Dict[str, Any]] = []
        v_index: int = 0
        if len(column_names) == 0:
            self.disp.log_error(
                "There are not provided table column names.",
                "_beautify_table"
            )
            return table_content
        if len(table_content) == 0:
            self.disp.log_error(
                "There is no table content.",
                "_beautify_table"
            )
            return self.error
        column_length = len(column_names)
        for i in table_content:
            cell_length = len(i)
            if cell_length != column_length:
                self.disp.log_warning(
                    "Table content and column lengths do not correspond.",
                    "_beautify_table"
                )
            data.append({})
            for index, items in enumerate(column_names):
                if index == cell_length:
                    self.disp.log_warning(
                        "Skipping the rest of the tuple because it is shorter than the column names.",
                        "_beautify_table"
                    )
                    break
                data[v_index][items[0]] = i[index]
            v_index += 1
        self.disp.log_debug(f"beautified_table = {data}", "_beautify_table")
        return data

    def get_table_column_names(self, table_name: str) -> Union[List[str], int]:
        """_summary_
            Get the names of the columns in a table.

        Args:
            table_name (str): _description_

        Returns:
            List[str]: _description_
        """
        try:
            columns = self.describe_table(table_name)
            data = []
            for i in columns:
                data.append(i[0])
            return data
        except RuntimeError as e:
            msg = "Error: Failed to get column names of the tables.\n"
            msg += f"\"{str(e)}\""
            self.disp.log_error(msg, "get_table_column_names")
            return self.error

    def _compile_update_line(self, line: List, column: List, column_length) -> str:
        """_summary_
            Compile the line required for an sql update to work.

        Args:
            line (List): _description_
            column (List): _description_
            column_length (_type_): _description_

        Returns:
            str: _description_
        """
        final_line = ""
        for i in range(0, column_length):
            cell_content = self._check_sql_cell(line[i])
            final_line += f"{column[i]} = {cell_content}"
            if i < column_length - 1:
                final_line += ", "
            if i == column_length:
                break
        self.disp.log_debug(f"line = {final_line}", "_compile_update_line")
        return final_line

    def _reconnect(self) -> None:
        """_summary_
            Reconnect to the database.
        """
        if self.is_connected() is False:
            self.disconnect_db()
            self.connect_to_db()

    def _save(self) -> int:
        """_summary_
            Save the changes to the database.

        Returns:
            int: _description_
        """
        title = "_save"
        self.disp.log_debug("Saving changes to the database.", "_save")
        self._reconnect()
        if self.is_connected() is False:
            self.disp.log_critical(
                "Connection to the database is non-existant, aborting command.",
                title
            )
            return self.error
        try:
            self.connection.commit()
            self.disp.log_debug("Changes saved.", "_save")
            return self.success
        except mysql.connector.Error as e:
            self.disp.log_error(
                f"Failed to save changes: {str(e)}",
                "_save"
            )
            return self.error

    def _run_editing_command(self, sql_query: str, table: str, action_type: str = "update") -> int:
        """_summary_
            Function in charge of running the execute and making sure that the connection to the database is still valid.

        Args:
            command (str): _description_

        Returns:
            int: _description_
        """
        title = "_run_editing_command"
        self._reconnect()
        if self.is_connected() is False:
            self.disp.log_critical(
                "Connection to the database is non-existant, aborting command.",
                title
            )
            return self.error
        self.disp.log_debug(
            f"running command {sql_query}",
            title
        )
        try:
            self.cursor.execute(sql_query)
            self.disp.log_debug(
                "command ran successfully.",
                title
            )
        except mysql.connector.Error as e:
            self.disp.log_error(
                f"Failed to {action_type} data in '{table}': {str(e)}",
                title
            )
            return self.error
        return self._save()

    def _process_sql_line(self, line: List[str], column: List[str], column_length: int = (-1)) -> str:
        """_summary_
            Convert a List of strings to an sql line so that it can be inserted into a table.

        Args:
            line (List[str]): _description_

        Returns:
            str: _description_
        """
        if column_length == -1:
            column_length = len(column)
        line_length = len(line)

        line_final = "("
        if self.debug is True and ";base" not in str(line):
            msg = f"line = {line}"
            self.disp.log_debug(msg, "_process_sql_line")
        for i in range(0, column_length):
            line_final += self._check_sql_cell(line[i])
            if i < column_length - 1:
                line_final += ", "
            if i == column_length:
                if i < line_length:
                    msg = "The line is longer than the number of columns, truncating."
                    self.disp.log_warning(msg, "_process_sql_line")
                break
        line_final += ")"
        if ";base" not in str(line_final):
            msg = f"line_final = '{line_final}'"
            msg += f", type(line_final) = '{type(line_final)}'"
            self.disp.log_debug(msg, "_process_sql_line")
        return line_final

    def get_table_names(self) -> List[str]:
        """_summary_
            Get the names of the tables in the database.

        Returns:
            List[str]: _description_
        """
        title = "get_table_names"
        self.disp.log_debug("Getting table names.", title)
        self._reconnect()
        if self.is_connected() is False:
            self.disp.log_critical(
                "Connection to the database is non-existant, aborting command.",
                title
            )
            return self.error
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        data = []
        for i in tables:
            data.append(i[0])
        self.disp.log_debug("Tables fetched", title)
        return data

    def _recreate_pool(self) -> None:
        """_summary_
            Recreate the connection pool.
        """
        title = "_recreate_pool"
        self.disp.log_debug("Recreating the connection pool.", title)
        if self.pool is not None:
            del self.pool
            self.pool = None
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=CONST.DATABASE_POOL_NAME,
            pool_size=CONST.DATABASE_MAX_POOL_CONNECTIONS,
            pool_reset_session=CONST.DATABASE_RESET_POOL_NODE_CONNECTION,
            user=self.username,
            password=self.password,
            host=self.url,
            port=self.port,
            database=self.db_name,
            collation="utf8mb4_unicode_ci"
        )

    def _abort_attempt(self) -> None:
        """_summary_
        """
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def connect_to_db(self, username: str = "", password: str = "", db_name: str = "") -> None:
        """
            The function to connect to the database

        Args:
            username (str, optional): Username of the account. Defaults to "".
            password (str, optional): Password of the account. Defaults to "".
            db_name (str, optional): Name of the database. Defaults to "".
        """
        title = "connect_to_db"
        self.disp.log_debug("Connecting to database", title)
        reset_pool = False
        if username != "":
            self.username = username
            reset_pool = True
        if password != "":
            self.password = password
            reset_pool = True
        if db_name != "":
            reset_pool = True
            self.db_name = db_name
        if reset_pool is True:
            self._recreate_pool()
        try:
            self.connection = self.pool.get_connection()
            self.disp.log_info(f"Connected to {self.db_name}", title)
        except mysql.connector.Error as e:
            msg = f"Failed to connect to {self.db_name}"
            self.disp.log_critical(msg, title)
            self._abort_attempt()
            raise RuntimeError(f"Error: {msg}") from e
        try:
            self.cursor = self.connection.cursor()
        except Exception as e:
            msg = "Failed to create a cursor."
            self.disp.log_error(msg, title)
            self._abort_attempt()
            raise RuntimeError(msg) from e

    def is_connected(self) -> bool:
        """_summary_
            Check if the connection to the database is still active.

        Returns:
            bool: _description_: True if the connection is active, False otherwise.
        """
        title = "is_connected"
        self.disp.log_debug(
            "Checking if we are still connected to the database.", title
        )
        if self.connection is None:
            self.disp.log_error("No active connection object found.", title)
            return False
        try:
            self.connection.ping(reconnect=False)
            self.disp.log_info("Connection is alive.", title)
            return True
        except mysql.connector.errors.InterfaceError as ie:
            self.disp.log_error(
                f"InterfaceError: Connection is no longer active: {str(ie)}",
                title
            )
            return False
        except mysql.connector.errors.OperationalError as oe:
            msg = "OperationalError: Lost connection or server "
            msg += f"issue: {str(oe)}"
            self.disp.log_error(msg, title)
            return False
        except mysql.connector.Error as e:
            self.disp.log_error(
                f"MySQL Error: Connection lost: {str(e)}", title
            )
            return False
        except Exception as e:
            self.disp.log_error(
                f"Unexpected error while checking connection: {str(e)}", title
            )
            return False

    def describe_table(self, table: str) -> Union[int, List[Any]]:
        """_summary_
            Fetch the headers (description) of a table from the database.

        Args:
            table (str): _description_: The name of the table to describe.

        Raises:
            RuntimeError: _description_: If there is a critical issue with the table or the database connection.

        Returns:
            Union[int, List[Any]]: _description_: A list containing the description of the table, or self.error if an error occurs.
        """
        title = "describe_table"
        self.disp.log_debug(f"Describing table {table}", title)
        if self.injection.check_if_sql_injection(table) is True:
            self.disp.log_error("Injection detected.", "sql")
            return self.error
        self._reconnect()
        if self.is_connected() is False:
            self.disp.log_critical(
                "Connection to the database is non-existant, aborting command.",
                title
            )
            return self.error
        try:
            self.cursor.execute(f"DESCRIBE {table}")
            if self.cursor is not None and self.cursor.description is not None:
                result = self.cursor.fetchall()
                self.disp.log_debug(
                    f"Description for table '{table}': {result}",
                    title
                )
                return result
            return self.error
        except mysql.connector.errors.ProgrammingError as pe:
            msg = f"ProgrammingError: The table '{table}'"
            msg += "does not exist or the query failed."
            self.disp.log_critical(msg, title)
            raise RuntimeError(msg) from pe
        except mysql.connector.errors.IntegrityError as ie:
            msg = "IntegrityError: There was an integrity constraint "
            msg += f"issue while describing the table '{table}'."
            self.disp.log_critical(msg, title)
            raise RuntimeError(msg) from ie
        except mysql.connector.errors.OperationalError as oe:
            msg = "OperationalError: There was an operational error "
            msg += f"while describing the table '{table}'."
            self.disp.log_critical(msg, title)
            raise RuntimeError(msg) from oe
        except mysql.connector.Error as e:
            msg = "MySQL Error: An unexpected error occurred while "
            msg += f"describing the table '{table}'."
            self.disp.log_critical(msg, title)
            raise RuntimeError(msg) from e
        except RuntimeError as e:
            msg = "A runtime error occurred during the table description process."
            self.disp.log_critical(msg, title)
            raise RuntimeError(msg) from e

    def insert_data_into_table(self, table: str, data: Union[List[List[str]], List[str]], column: Union[List[str], None] = None) -> int:
        """_summary_
            Insert data into a table.

        Args:
            table (str): _description_
            data (List[List[str]]): _description_
            column (List[str]): _description_

        Returns:
            int: _description_
        """
        self.disp.log_debug(
            "Inserting data into the table.",
            "insert_data_into_table"
        )
        if column is None:
            column = ""
        if self.injection.check_if_injections_in_strings([table, data, column]) is True:
            self.disp.log_error("Injection detected.", "sql")
            return self.error

        if column == "":
            column = self.get_table_column_names(table)

        column = self._escape_risky_column_names(column)

        column_str = ", ".join(column)
        column_length = len(column)

        if isinstance(data, List) is True and (len(data) > 0 and isinstance(data[0], List) is True):
            self.disp.log_debug(
                "processing double array",
                "insert_data_into_table"
            )
            values = ""
            max_lengths = len(data)
            for index, line in enumerate(data):
                values += self._process_sql_line(line, column, column_length)
                if index < max_lengths - 1:
                    values += ", "
                if index == max_lengths - 1:
                    break

        elif isinstance(data, List) is True:
            self.disp.log_debug(
                "processing single array",
                "insert_data_into_table"
            )
            values = self._process_sql_line(data, column, column_length)
        else:
            self.disp.log_error(
                "data is expected to be, either of type: List[str] or List[List[str]]",
                "insert_data_into_table"
            )
            return self.error
        sql_query = f"INSERT INTO {table} ({column_str}) VALUES {values}"
        self.disp.log_debug(
            f"sql_query = '{sql_query}'",
            "insert_data_into_table"
        )
        return self._run_editing_command(sql_query, table, "insert")

    def get_data_from_table(self, table: str, column: Union[str, List[str]], where: Union[str, List[str]] = "", beautify: bool = True) -> Union[int, List[Dict[str, Any]]]:
        """_summary_

        Args:
            table (str): _description_
            column (Union[str, List[str]]): _description_
            where (Union[str, List[str]]): _description_

        Returns:
            Union[int, List[Dict[str, Any]]]: _description_: Will return the data you requested, self.error otherwise
        """
        title = "get_data_from_table"
        self.disp.log_debug(f"fetching data from the table {table}", title)
        if self.injection.check_if_injections_in_strings([table, column]) is True or self.injection.check_if_symbol_and_command_injection(where) is True:
            self.disp.log_error("Injection detected.", "sql")
            return self.error
        if isinstance(column, list) is True:
            column = ", ".join(column)
        sql_command = f"SELECT {column} FROM {table}"
        if isinstance(where, str) is True:
            where = self._escape_risky_column_names_where_mode(where)
        if isinstance(where, List) is True:
            where = self._escape_risky_column_names_where_mode(where)
            where = " AND ".join(where)
        if where != "":
            sql_command += f" WHERE {where}"
        data = self.describe_table(table)
        self.disp.log_debug(f"sql_query = '{sql_command}'", title)
        self._reconnect()
        if self.is_connected() is False:
            self.disp.log_critical(
                "Connection to the database is non-existant, aborting command.",
                title
            )
            return self.error
        self.cursor.execute(sql_command)
        table_data = self.cursor.fetchall()
        if beautify is False:
            return table_data
        return self._beautify_table(data, table_data)

    def get_table_size(self, table: str, column: Union[str, List[str]], where: Union[str, List[str]] = "") -> Union[int]:
        """_summary_
            Get the size of a table.

        Args:
            table (str): _description_
            column (Union[str, List[str]]): _description_
            where (Union[str, List[str]]): _description_

        Returns:
            int: _description_: Return the size of the table, -1 if an error occurred.
        """
        title = "get_table_size"
        self.disp.log_debug(f"fetching data from the table {table}", title)
        if self.injection.check_if_injections_in_strings([table, column]) is True or self.injection.check_if_symbol_and_command_injection(where) is True:
            self.disp.log_error("Injection detected.", "sql")
            return (-1)
        if isinstance(column, list) is True:
            column = ", ".join(column)
        sql_command = f"SELECT COUNT({column}) FROM {table}"
        if isinstance(where, List) is True:
            where = " AND ".join(where)
        if where != "":
            sql_command += f" WHERE {where}"
        self._reconnect()
        if self.is_connected() is False:
            self.disp.log_critical(
                "Connection to the database is non-existant, aborting command.",
                title
            )
            return (-1)
        self.disp.log_debug(f"sql_query = '{sql_command}'", title)
        self.cursor.execute(sql_command)
        table_data = self.cursor.fetchall()
        if len(table_data) == 0:
            self.disp.log_error(
                "There was no data returned by the query.", title
            )
            return (-1)
        if isinstance(table_data[0], tuple) is False:
            self.disp.log_error("The data returned is not a tuple.", title)
            return (-1)
        return table_data[0][0]

    def update_data_in_table(self, table: str, data: List[str], column: List, where: Union[str, List[str]] = "") -> int:
        """_summary_
            Update the data contained in a table.

        Args:
            table (str): _description_
            data (Union[List[List[str]], List[str]]): _description_
            column (List): _description_

        Returns:
            int: _description_
        """
        title = "update_data_in_table"
        msg = f"Updating the data contained in the table: {table}"
        self.disp.log_debug(msg, title)
        if column is None:
            column = ""

        if self.injection.check_if_injections_in_strings([table, column, data]) is True or self.injection.check_if_symbol_and_command_injection(where) is True:
            self.disp.log_error("Injection detected.", "sql")
            return self.error

        if column == "":
            column = self.get_table_column_names(table)

        column = self._escape_risky_column_names(column)

        column_length = len(column)

        if isinstance(where, List) is True:
            where = " AND ".join(where)

        update_line = self._compile_update_line(data, column, column_length)

        sql_query = f"UPDATE {table} SET {update_line}"

        if where != "":
            sql_query += f" WHERE {where}"

        self.disp.log_debug(f"sql_query = '{sql_query}'", title)

        return self._run_editing_command(sql_query, table, "update")

    def insert_or_update_data_into_table(self, table: str, data: Union[List[List[str]], List[str]], column: Union[List[str], None] = None) -> int:
        """_summary_
            Insert or update data into a given table.

        Args:
            table (str): _description_
            data (Union[List[List[str]], List[str]]): _description_
            column (Union[List[str], None], optional): _description_. Defaults to None.

        Returns:
            int: _description_
        """
        title = "insert_or_update_data_into_table"
        self.disp.log_debug(
            "Inserting or updating data into the table.", title
        )

        if column is None:
            column = ""
        if self.injection.check_if_injections_in_strings([table, data, column]) is True:
            self.disp.log_error("Injection detected.", "sql")
            return self.error

        if column == "":
            column = self.get_table_column_names(table)

        table_content = self.get_data_from_table(
            table=table,
            column=column,
            where="",
            beautify=False
        )
        if isinstance(table_content, int) is True and table_content != self.success:
            self.disp.log_critical(
                f"Failed to retrieve data from table {table}",
                title
            )
            return self.error

        if len(table_content) == 0:
            return self.insert_data_into_table(table, data, column)

        if isinstance(data, List) is True and (len(data) > 0 and isinstance(data[0], List) is True):
            self.disp.log_debug(
                "Processing double data list",                title)
            for line in data:
                node_found = False
                if len(line) == 0:
                    self.disp.log_warning(
                        "The line is empty, skipping.", title
                    )
                    continue
                node0 = str(line[0])
                for table_line in table_content:
                    if str(table_line[0]) == node0:
                        self.update_data_in_table(
                            table,
                            line,
                            column,
                            f"{column[0]} = {node0}"
                        )
                        node_found = True
                        break
                if node_found is False:
                    self.insert_data_into_table(table, line, column)

        elif isinstance(data, List) is True:
            self.disp.log_debug("Processing single data list", title)
            if len(data) == 0:
                self.disp.log_warning(
                    "The data list is empty, skipping.",
                    title
                )
                return self.success
            node0 = str(data[0])
            for line in table_content:
                if str(line[0]) == node0:
                    return self.update_data_in_table(table, data, column, [f"{column[0]} = {node0}"])
            return self.insert_data_into_table(table, data, column)
        else:
            self.disp.log_error(
                "data is expected to be, either of type: List[str] or List[List[str]]",
                title
            )
            return self.error

    def remove_data_from_table(self, table: str, where: Union[str, List[str]] = "") -> int:
        """_summary_
            Remove the data from a table.
        Args:
            table (str): _description_
            data (List): _description_
            column (List): _description_

        Returns:
            int: _description_
        """
        self.disp.log_debug(
            f"Removing data from table {table}",
            "remove_data_from_table"
        )
        if self.injection.check_if_sql_injection(table) is True or self.injection.check_if_symbol_and_command_injection(where) is True:
            self.disp.log_error("Injection detected.", "sql")
            return self.error

        if isinstance(where, List) is True:
            where = " AND ".join(where)

        sql_query = f"DELETE FROM {table}"

        if where != "":
            sql_query += f" WHERE {where}"

        self.disp.log_debug(
            f"sql_query = '{sql_query}'",
            "remove_data_from_table"
        )

        return self._run_editing_command(sql_query, table, "delete")

    def disconnect_db(self) -> int:
        """_summary_
            Close the connection to the database.

        Returns:
            int: _description_
        """
        self.disp.log_debug(
            "Disconnecting the database",
            "disconnect_db"
        )
        if self.connection is None:
            self.disp.log_error(
                "There are not active connections to the database",
                "disconnect_db"
            )
            return self.error
        self.connection.close()
        self.cursor = None
        self.connection = None
        self.disp.log_info(
            f"Disconnected from {self.db_name}",
            "disconnect_db"
        )
        return self.success
