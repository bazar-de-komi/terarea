from typing import Union, List, Dict, Any
from datetime import datetime

import mariadb
from display_tty import Disp, TOML_CONF, SAVE_TO_FILE, FILE_NAME
from .injection import Injection


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
        self.connection = None
        self.cursor = None
        self.injection: Injection = Injection(
            self.error,
            self.success,
            self.debug
        )
        # --------------------------- logger section ---------------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            SAVE_TO_FILE,
            FILE_NAME,
            debug=self.debug,
            logger=self.__class__.__name__
        )
        # ----------------- Database risky keyword sanitising  -----------------
        self.risky_keywords: List[str] = [
            "ADD", "ALL", "ALTER", "ANALYZE", "AND", "AS", "ASC", "ASENSITIVE", "BEFORE", "BETWEEN",
            "BIGINT", "BINARY", "BLOB", "BOTH", "BY", "CALL", "CASCADE", "CASE", "CHANGE", "CHAR",
            "CHARACTER", "CHECK", "COLLATE", "COLUMN", "CONDITION", "CONSTRAINT", "CONTINUE",
            "CONVERT", "CREATE", "CROSS", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP",
            "CURSOR", "DATABASE", "DATABASES", "DAY_HOUR", "DAY_MICROSECOND", "DAY_MINUTE",
            "DAY_SECOND", "DEC", "DECIMAL", "DECLARE", "DEFAULT", "DELAYED", "DELETE", "DESC",
            "DESCRIBE", "DETERMINISTIC", "DISTINCT", "DISTINCTROW", "DIV", "DOUBLE", "DROP",
            "DUAL", "EACH", "ELSE", "ELSEIF", "ENCLOSED", "ESCAPED", "EXISTS", "EXIT", "EXPLAIN",
            "FALSE", "FETCH", "FLOAT", "FOR", "FORCE", "FOREIGN", "FROM", "FULLTEXT", "GENERAL",
            "GRANT", "GROUP", "HAVING", "HIGH_PRIORITY", "HOUR_MICROSECOND", "HOUR_MINUTE",
            "HOUR_SECOND", "IF", "IGNORE", "IN", "INDEX", "INFILE", "INNER", "INOUT",
            "INSENSITIVE", "INSERT", "INT", "INTEGER", "INTERVAL", "INTO", "IS", "ITERATE", "JOIN",
            "KEY", "KEYS", "KILL", "LEADING", "LEAVE", "LEFT", "LIKE", "LIMIT", "LINEAR", "LINES",
            "LOAD", "LOCALTIME", "LOCALTIMESTAMP", "LOCK", "LONG", "LONGBLOB", "LONGTEXT", "LOOP",
            "LOW_PRIORITY", "MASTER_SSL_VERIFY_SERVER_CERT", "MATCH", "MAXVALUE", "MEDIUMBLOB",
            "MEDIUMINT", "MEDIUMTEXT", "MIDDLEINT", "MINUTE_MICROSECOND", "MINUTE_SECOND", "MOD",
            "MODIFIES", "NATURAL", "NOT", "NO_WRITE_TO_BINLOG", "NULL", "NUMERIC", "ON", "OPTIMIZE",
            "OPTION", "OPTIONALLY", "OR", "ORDER", "OUT", "OUTER", "OUTFILE", "PRECISION", "PRIMARY",
            "PROCEDURE", "PURGE", "RANGE", "READ", "READS", "READ_WRITE", "REAL", "REFERENCES",
            "REGEXP", "RELEASE", "RENAME", "REPEAT", "REPLACE", "REQUIRE", "RESIGNAL", "RESTRICT",
            "RETURN", "REVOKE", "RIGHT", "RLIKE", "SCHEMA", "SCHEMAS", "SECOND_MICROSECOND",
            "SELECT", "SENSITIVE", "SEPARATOR", "SET", "SHOW", "SIGNAL", "SMALLINT", "SPATIAL",
            "SPECIFIC", "SQL", "SQLEXCEPTION", "SQLSTATE", "SQLWARNING", "SQL_BIG_RESULT",
            "SQL_CALC_FOUND_ROWS", "SQL_SMALL_RESULT", "SSL", "STARTING", "STORED", "STRAIGHT_JOIN",
            "TABLE", "TERMINATED", "THEN", "TINYBLOB", "TINYINT", "TINYTEXT", "TO", "TRAILING",
            "TRIGGER", "TRUE", "UNDO", "UNION", "UNIQUE", "UNLOCK", "UNSIGNED", "UPDATE", "USAGE",
            "USE", "USING", "UTC_DATE", "UTC_TIME", "UTC_TIMESTAMP", "VALUES", "VARBINARY",
            "VARCHAR", "VARCHARACTER", "VARYING", "VIRTUAL", "WHEN", "WHERE", "WHILE", "WITH",
            "WRITE", "XOR", "YEAR_MONTH", "ZEROFILL"
        ]
        # -------------------------- datetime parsing --------------------------
        self.date_only: str = '%Y-%m-%d'
        self.date_and_time: str = '%Y-%m-%d %H:%M:%S'
        # --------------------------- debug section  ---------------------------
        if self.debug is True:
            msg = f"self.debug = '{self.debug}'\n"
            msg += f"self.success = '{self.success}'\n"
            msg += f"self.error = '{self.error}'\n"
            msg += f"self.url = '{self.url}'\n"
            msg += f"self.port = '{self.port}'\n"
            msg += f"self.username = '{self.username}'\n"
            msg += f"self.password = '{self.password}'\n"
            msg += f"self.db_name = '{self.db_name}'\n"
            msg += f"self.connection = '{self.connection}'\n"
            msg += f"self.cursor = '{self.cursor}'\n"
            msg += f"self.injection = '{self.injection}'\n"
            self.disp.log_debug(msg, "__init__")

    def __del__(self) -> None:
        """
            Disconnect the database when the class is destroyed
        """
        self.disconnect_db()

    def _protect_sql_cell(self, cell: str) -> str:
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

    def datetime_to_string(self, datetime_instance: datetime, date_only: bool = False, sql_mode: bool = False) -> str:
        """_summary_
            Convert a datetime instance to a string.

        Args:
            datetime_instance (datetime): _description_: The datetime item
            date_only (bool, optional): _description_. Defaults to False.: if True will only return the date section, otherwise will return the date and time section.
            sql_mode (bool, optional): _description_. Defaults to False.: if True, will add the microseconds to the response so that it can be directly inserted into an sql command.

        Raises:
            ValueError: _description_: If the datetime instance is not a datetime, a valueerror is raised.

        Returns:
            str: _description_: A string instance of the datetime.
        """

        if isinstance(datetime_instance, datetime) is False:
            self.disp.log_error(
                "The input is not a datetime instance.",
                "datetime_to_string"
            )
            raise ValueError("Error: Expected a datetime instance.")
        if date_only is True:
            return datetime_instance.strftime(self.date_only)
        microsecond = ""
        if sql_mode is True:
            microsecond = datetime_instance.strftime("%f")[:3]
        converted_time = datetime_instance.strftime(self.date_and_time)
        return f"{converted_time}.{microsecond}"

    def string_to_datetime(self, datetime_string_instance: str, date_only: bool = False) -> str:
        """_summary_
            Convert a datetime instance to a string.

        Args:
            datetime_string_instance (str): _description_: The string datetime item
            date_only (bool, optional): _description_. Defaults to False.: if True will only return the date section, otherwise will return the date and time section.

        Raises:
            ValueError: _description_: If the datetime instance is not a datetime, a valueerror is raised.

        Returns:
            str: _description_: A string instance of the datetime.
        """

        if isinstance(datetime_string_instance, str) is False:
            self.disp.log_error(
                "The input is not a string instance.",
                "string_to_datetime"
            )
            raise ValueError("Error: Expected a string instance.")
        if date_only is True:
            return datetime.strptime(datetime_string_instance, self.date_only)
        return datetime.strptime(datetime_string_instance, self.date_and_time)

    def _get_correct_now_value(self) -> str:
        """_summary_
            Get the current date and time in the correct format for the database.

        Returns:
            str: _description_
        """
        current_time = datetime.now()
        return current_time.strftime(self.date_and_time)

    def _get_correct_current_date_value(self) -> str:
        """_summary_
            Get the current date and time in the correct format for the database.

        Returns:
            str: _description_
        """
        current_time = datetime.now()
        return current_time.strftime(self.date_only)

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

    def _escape_risky_column_names(self, columns: Union[List[str], str]) -> Union[List[str], str]:
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
                if key.upper() in self.risky_keywords:
                    self.disp.log_warning(
                        f"Escaping risky column name '{key}'.",
                        "_escape_risky_column_names"
                    )
                    data[index] = f"`{key}`={value}"
            elif item.upper() in self.risky_keywords:
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

    def _check_sql_cell(self, cell: str) -> str:
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
        cell = self._protect_sql_cell(cell)
        tmp = cell.lower()
        if tmp in ("now", "now()"):
            tmp = self._get_correct_now_value()
        elif tmp in ("current_date", "current_date()"):
            tmp = self._get_correct_current_date_value()
        else:
            tmp = str(cell)
        if ";base" not in tmp:
            self.disp.log_debug(f"result = {tmp}", "_check_sql_cell")
        return f"\"{str(tmp)}\""

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
            self.connect_to_db()

    def _save(self) -> int:
        """_summary_
            Save the changes to the database.

        Returns:
            int: _description_
        """
        self.disp.log_debug("Saving changes to the database.", "_save")
        try:
            self.connection.commit()
            self.disp.log_debug("Changes saved.", "_save")
            return self.success
        except mariadb.Error as e:
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
        self._reconnect()
        self.disp.log_debug(
            f"running command {sql_query}",
            "_run_editing_command"
        )
        try:
            self.cursor.execute(sql_query)
            self.disp.log_debug(
                "command ran successfully.",
                "_run_editing_command"
            )
        except mariadb.Error as e:
            self.disp.log_error(
                f"Failed to {action_type} data in '{table}': {str(e)}",
                "_run_editing_command"
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
        self.disp.log_debug("Getting table names.", "get_table_names")
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        data = []
        for i in tables:
            data.append(i[0])
        self.disp.log_debug("Tables fetched", "get_table_names")
        return data

    def connect_to_db(self, username: str = "", password: str = "", db_name: str = "") -> None:
        """
            The function to connect to the database

        Args:
            username (str, optional): Username of the account. Defaults to "".
            password (str, optional): Password of the account. Defaults to "".
            db_name (str, optional): Name of the database. Defaults to "".
        """
        self.disp.log_debug("Connecting to database", "connect_to_db")
        if username != "":
            self.username = username
        if password != "":
            self.password = password
        if db_name != "":
            self.db_name = db_name
        try:
            self.connection = mariadb.connect(
                user=self.username,
                password=self.password,
                host=self.url,
                port=self.port,
                database=self.db_name
            )
            self.disp.log_info(
                f"Connected to {self.db_name}",
                "connect_to_db"
            )
        except mariadb.Error as e:
            self.disp.log_critical(
                f"Failed to connect to {self.db_name}",
                "connect_to_db"
            )
            self.connection = None
            self.cursor = None
            raise RuntimeError(
                "Error: Failed to connect to the database."
            ) from e
        self.cursor = self.connection.cursor()

    def is_connected(self) -> bool:
        """_summary_
            Check if the connection to the database is still active.

        Returns:
            bool: _description_
        """
        self.disp.log_debug(
            "Checking if we are still connected to the database.",
            "is_connected"
        )
        if self.connection is None:
            self.disp.log_error(
                "No active connection found.",
                "is_connected"
            )
            return False
        try:
            self.connection.ping()
            self.disp.log_info("Connection is alive.", "is_connected")
            return True
        except mariadb.Error as e:
            self.disp.log_error(
                f"Connection lost: {str(e)}",
                "is_connected"
            )
            return False

    def describe_table(self, table: str) -> List[Any]:
        """_summary_
            This is the function in charge of fetching the headers of a table.

        Args:
            table (str): _description_

        Raises:
            RuntimeError: _description_

        Returns:
            List[Any]: _description_
        """
        self.disp.log_debug(
            f"describing table {table}",
            "describe_table"
        )
        if self.injection.check_if_sql_injection(table) is True:
            self.disp.log_error("Injection detected.", "sql")
            return self.error
        try:
            self._reconnect()
            self.cursor.execute(f"DESCRIBE {table}")
        except mariadb.Error as e:
            self.disp.log_critical(
                f" The table '{table}' does not exist.",
                "describe_table"
            )
            raise RuntimeError(
                f"Error: The table '{table}' does not exist."
            ) from e
        return self.cursor.fetchall()

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
            List[Dict[str, Any]]: _description_
        """
        self.disp.log_debug(
            f"fetching data from the table {table}",
            "get_data_from_table"
        )
        if self.injection.check_if_injections_in_strings([table, column]) is True or self.injection.check_if_symbol_and_command_injection(where) is True:
            self.disp.log_error("Injection detected.", "sql")
            return self.error
        if isinstance(column, list) is True:
            column = ", ".join(column)
        sql_command = f"SELECT {column} FROM {table}"
        if isinstance(where, List) is True:
            where = " AND ".join(where)
        if where != "":
            sql_command += f" WHERE {where}"
        data = self.describe_table(table)
        self._reconnect()
        self.disp.log_debug(
            f"sql_query = '{sql_command}'",
            "get_data_from_table"
        )
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
            int: _description_: Return the size of the table, -1 if an error occured.
        """
        self.disp.log_debug(
            f"fetching data from the table {table}",
            "get_table_size"
        )
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
        self.disp.log_debug(
            f"sql_query = '{sql_command}'",
            "get_table_size"
        )
        self.cursor.execute(sql_command)
        table_data = self.cursor.fetchall()
        if len(table_data) == 0:
            self.disp.log_error(
                "There was no data returned by the query.", "get_table_size"
            )
            return (-1)
        if isinstance(table_data[0], tuple) is False:
            self.disp.log_error(
                "The data returned is not a tuple.", "get_table_size"
            )
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
        msg = f"Updating the data contained in the table: {table}"
        self.disp.log_debug(msg, "update_data_in_table")
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

        self.disp.log_debug(
            f"sql_query = '{sql_query}'",
            "update_data_in_table"
        )

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
        self.disp.log_debug(
            "Inserting or updating data into the table.",
            "insertor_update_data_into_table"
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
                "insert_or_update_data_into_table"
            )
            return self.error

        if len(table_content) == 0:
            return self.insert_data_into_table(table, data, column)

        if isinstance(data, List) is True and (len(data) > 0 and isinstance(data[0], List) is True):
            self.disp.log_debug(
                "Processing double data list",
                "insert_or_update_data_into_table"
            )
            for line in data:
                node_found = False
                if len(line) == 0:
                    self.disp.log_warning(
                        "The line is empty, skipping.",
                        "insert_or_update_data_into_table"
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
            self.disp.log_debug(
                "Processing single data list",
                "insert_or_update_data_into_table"
            )
            if len(data) == 0:
                self.disp.log_warning(
                    "The data list is empty, skipping.",
                    "insert_or_update_data_into_table"
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
                "insert_or_update_data_into_table"
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
