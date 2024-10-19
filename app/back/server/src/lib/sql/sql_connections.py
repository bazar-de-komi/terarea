"""
    File in charge of containing the class that will manage the sql connections.
"""

from typing import Union, Any

import mysql
import mysql.connector
import mysql.connector.cursor
from display_tty import Disp, TOML_CONF, SAVE_TO_FILE, FILE_NAME

from . import sql_constants as SCONST
from ..components import constants as CONST


class SQLManageConnections:
    """_summary_
    """

    def __init__(self, url: str, port: int, username: str, password: str, db_name: str, success: int = 0, error: int = 84, debug: bool = False) -> None:
        """_summary_
            This class is in charge of managing the connections to the sql database

        Args:
            url (str): _description_
            port (int): _description_
            username (str): _description_
            password (str): _description_
            db_name (str): _description_
            succes (int, optional): _description_. Defaults to 0.
            error (int, optional): _description_. Defaults to 84.
            debug (bool, optional): _description_. Defaults to False.
        """
        # -------------------------- Inherited values --------------------------
        self.error: int = error
        self.debug: bool = debug
        self.success: int = success
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

        # ---------------- variables containing the connection  ----------------
        self.pool: Union[
            None,
            mysql.connector.pooling.MySQLConnectionPool
        ] = None

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
        self.disp.log_debug(msg, func_name)

    def initialise_pool(self) -> int:
        """_summary_
            Initialise a connection to the database (but within a pool)

        Raises:
            RuntimeError: _description_: A runtime error is raised if it fails.

        Returns:
            int: _description_: Returns self.success if the function succeeds.
        """
        title = "initialise_pool"
        self.disp.log_debug("Initialising the connection pool.", title)
        try:
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
            return self.success
        except mysql.connector.errors.ProgrammingError as pe:
            msg = "ProgrammingError: The pool could not be initialized."
            msg += f"Original error: {str(pe)}"
            self.disp.log_critical(msg, title)
            raise RuntimeError(msg) from pe
        except mysql.connector.errors.IntegrityError as ie:
            msg = "IntegrityError: Integrity issue while initializing the pool."
            msg += f" Original error: {str(ie)}"
            self.disp.log_critical(msg, title)
            raise RuntimeError(msg) from ie
        except mysql.connector.errors.OperationalError as oe:
            msg = "OperationalError: Operational error occurred during pool initialization."
            msg += f" Original error: {str(oe)}"
            self.disp.log_critical(msg, title)
            raise RuntimeError(msg) from oe
        except mysql.connector.Error as e:
            msg = "MySQL Error: An unexpected error occurred during pool initialization."
            msg += f"Original error: {str(e)}"
            self.disp.log_critical(msg, title)
            raise RuntimeError(msg) from e

    def get_connection(self) -> mysql.connector.pooling.PooledMySQLConnection:
        """_summary_
            Retrieves a connection from the pool.

        Returns:
            mysql.connector.pooling.PooledMySQLConnection: _description_: A pooled connection
        """
        title = "get_connection"
        if self.pool is None:
            raise RuntimeError("Connection pool is not initialized.")
        try:
            self.disp.log_debug("Getting an sql connection", title)
            return self.pool.get_connection()
        except mysql.connector.errors.OperationalError as oe:
            msg = "OperationalError: Could not retrieve a connection from the pool."
            msg += f" Original error: {str(oe)}"
            self.disp.log_critical(msg, title)
            raise RuntimeError(msg) from oe
        except mysql.connector.Error as e:
            msg = "MySQL Error: An unexpected error occurred while getting the connection."
            msg += f" Original error: {str(e)}"
            self.disp.log_critical(msg, title)
            raise RuntimeError(msg) from e

    def get_cursor(self, connection: mysql.connector.pooling.PooledMySQLConnection) -> mysql.connector.cursor.MySQLCursor:
        """
        Retrieves a cursor from the given connection.

        Args:
            connection (mysql.connector.pooling.PooledMySQLConnection): The active connection.

        Returns:
            mysql.connector.cursor.MySQLCursor: The cursor object.
        """
        if not self.is_connection_active(connection):
            raise RuntimeError("Cannot get cursor, connection is not active.")
        return connection.cursor()

    def close_cursor(self, cursor: mysql.connector.cursor.MySQLCursor) -> int:
        """
        Closes the given cursor.

        Args:
            cursor (mysql.connector.cursor.MySQLCursor): The cursor to close.
        """
        title = "close_cursor"
        self.disp.log_debug("Closing cursor, if it is open.", title)
        if self.is_cursor_active(cursor):
            self.disp.log_debug("Closing cursor", title)
            cursor.close()
            return self.success
        self.disp.log_error(
            "The cursor did not have an active connection.", title
        )
        return self.error

    def return_connection(self, connection: mysql.connector.pooling.PooledMySQLConnection) -> int:
        """
        Returns a connection to the pool by closing it.

        Args:
            connection (mysql.connector.pooling.PooledMySQLConnection): The connection to close.
        """
        title = "return_connection"
        self.disp.log_debug("Closing a database connection.", title)
        if self.is_connection_active(connection):
            self.disp.log_debug("Connection has been closed.", title)
            connection.close()
            return self.success
        self.disp.log_error(
            "Connection was not open in the first place.", title
        )
        return self.error

    def destroy_pool(self) -> int:
        """_summary_
            Destroy the connection pool.

        Returns:
            int: _description_
        """
        title = "destroy_pool"
        self.disp.log_debug("Destroying pool, if it exists.", title)
        if self.pool is not None:
            self.disp.log_debug("Destroying pool.", title)
            del self.pool
            self.pool = None
        self.disp.log_warning("There was no pool to be destroyed.", title)
        return self.success

    def release_connection_and_cursor(self, connection: Union[mysql.connector.pooling.PooledMySQLConnection, None], cursor: Union[mysql.connector.pooling.PooledMySQLConnection, None] = None) -> None:
        """_summary_

        Args:
            connection (Union[None]): _description_
            cursor (Union[None]): _description_
        """
        title = "release_connection_and_cursor"
        msg = "Connections have ended with status: "
        self.disp.log_debug("Closing cursor.", title)
        status = self.close_cursor(cursor)
        msg += f"cursor = {status}, "
        self.disp.log_debug("Closing connection.", title)
        status = self.return_connection(connection)
        msg += f"connection = {status}"
        self.disp.log_debug(msg, title)

    def run_and_commit(self, query: str, cursor: Union[mysql.connector.cursor.MySQLCursor, None] = None) -> int:
        """
        Executes a query and commits changes.

        Args:
            cursor (mysql.connector.cursor.MySQLCursor): The active cursor.
            query (str): The query to execute.
        """
        title = "run_and_commit"
        self.disp.log_debug("Running and committing sql query.", title)
        if cursor is None:
            self.disp.log_debug("No cursor found, generating one.", title)
            connection = self.get_connection()
            if connection is None:
                self.disp.log_critical(SCONST.CONNECTION_FAILED, title)
                return self.error
            internal_cursor = self.get_cursor(connection)
            if internal_cursor is None:
                self.disp.log_critical(SCONST.CURSOR_FAILED, title)
                return self.error
        else:
            self.disp.log_debug("Cursor found, using it.", title)
            internal_cursor = cursor
        try:
            self.disp.log_debug(f"Executing query: {query}.", title)
            internal_cursor.execute(query)
            self.disp.log_debug("Committing content.", title)
            internal_cursor.connection.commit()
            if cursor is None:
                self.disp.log_debug(
                    "The cursor was generated by us, releasing.", title
                )
                self.release_connection_and_cursor(connection, internal_cursor)
            else:
                self.disp.log_debug(
                    "The cursor was provided, not releasing.", title
                )
            return self.success
        except mysql.connector.errors.ProgrammingError as pe:
            msg = "ProgrammingError: Failed to execute the query."
            msg += f" Original error: {str(pe)}"
            self.disp.log_error(msg, title)
            if cursor is None:
                self.disp.log_debug(
                    "The cursor was generated by us, releasing.", title
                )
                self.release_connection_and_cursor(connection, internal_cursor)
            else:
                self.disp.log_debug(
                    "The cursor was provided, not releasing.", title
                )
            raise RuntimeError(msg) from pe
        except mysql.connector.errors.IntegrityError as ie:
            msg = "IntegrityError: Integrity constraint issue occurred during query execution."
            msg += f" Original error: {str(ie)}"
            self.disp.log_error(msg, title)
            if cursor is None:
                self.disp.log_debug(
                    "The cursor was generated by us, releasing.", title
                )
                self.release_connection_and_cursor(connection, internal_cursor)
            else:
                self.disp.log_debug(
                    "The cursor was provided, not releasing.", title
                )
            raise RuntimeError(msg) from ie
        except mysql.connector.errors.OperationalError as oe:
            msg = "OperationalError: Operational error occurred during query execution."
            msg += f" Original error: {str(oe)}"
            self.disp.log_error(msg, title)
            if cursor is None:
                self.disp.log_debug(
                    "The cursor was generated by us, releasing.", title
                )
                self.release_connection_and_cursor(connection, internal_cursor)
            else:
                self.disp.log_debug(
                    "The cursor was provided, not releasing.", title
                )
            raise RuntimeError(msg) from oe
        except mysql.connector.Error as e:
            msg = "MySQL Error: An unexpected error occurred during query execution."
            msg += f" Original error: {str(e)}"
            self.disp.log_error(msg, title)
            if cursor is None:
                self.disp.log_debug(
                    "The cursor was generated by us, releasing.", title
                )
                self.release_connection_and_cursor(connection, internal_cursor)
            else:
                self.disp.log_debug(
                    "The cursor was provided, not releasing.", title
                )
            raise RuntimeError(msg) from e

    def run_and_fetch_all(self, query: str, cursor: Union[mysql.connector.cursor.MySQLCursor, None] = None) -> Union[int, Any]:
        """
        Executes a query and fetches all results.

        Args:
            cursor (mysql.connector.cursor.MySQLCursor): The active cursor.
            query (str): The query to execute.
        """
        title = "run_and_fetchall"
        if cursor is None:
            connection = self.get_connection()
            if connection is None:
                self.disp.log_critical(SCONST.CONNECTION_FAILED, title)
                return self.error
            internal_cursor = self.get_cursor(connection)
            if internal_cursor is None:
                self.disp.log_critical(SCONST.CURSOR_FAILED, title)
                return self.error
        else:
            internal_cursor = cursor
        try:
            self.disp.log_debug(f"Executing query: {query}.", title)
            internal_cursor.execute(query)
            if internal_cursor is None or internal_cursor.description is None:
                self.disp.log_error(
                    "Failed to gather data from the table, cursor is invalid.", title
                )
                if cursor is None:
                    self.disp.log_debug(
                        "The cursor was generated by us, releasing.", title
                    )
                    self.release_connection_and_cursor(
                        connection, internal_cursor
                    )
                else:
                    self.disp.log_debug(
                        "The cursor was provided, not releasing.", title
                    )
                return self.error
            self.disp.log_debug(
                "Storing a copy of the content of the cursor.", title
            )
            data = internal_cursor.fetchall().copy()
            self.disp.log_debug(f"Data gathered: {data}.", title)
            if cursor is None:
                self.disp.log_debug(
                    "The cursor was generated by us, releasing.", title
                )
                self.release_connection_and_cursor(connection, internal_cursor)
            else:
                self.disp.log_debug(
                    "The cursor was provided, not releasing.", title
                )
            return data
        except mysql.connector.errors.ProgrammingError as pe:
            msg = "ProgrammingError: Failed to execute the query."
            msg += f" Original error: {str(pe)}"
            self.disp.log_error(msg, title)
            if cursor is None:
                self.disp.log_debug(
                    "The cursor was generated by us, releasing.", title
                )
                self.release_connection_and_cursor(connection, internal_cursor)
            else:
                self.disp.log_debug(
                    "The cursor was provided, not releasing.", title
                )
            raise RuntimeError(msg) from pe
        except mysql.connector.errors.IntegrityError as ie:
            msg = "IntegrityError: Integrity constraint issue occurred during query execution."
            msg += f" Original error: {str(ie)}"
            self.disp.log_error(msg, title)
            if cursor is None:
                self.disp.log_debug(
                    "The cursor was generated by us, releasing.", title
                )
                self.release_connection_and_cursor(connection, internal_cursor)
            else:
                self.disp.log_debug(
                    "The cursor was provided, not releasing.", title
                )
            raise RuntimeError(msg) from ie
        except mysql.connector.errors.OperationalError as oe:
            msg = "OperationalError: Operational error occurred during query execution."
            msg += f" Original error: {str(oe)}"
            self.disp.log_error(msg, title)
            if cursor is None:
                self.disp.log_debug(
                    "The cursor was generated by us, releasing.", title
                )
                self.release_connection_and_cursor(connection, internal_cursor)
            else:
                self.disp.log_debug(
                    "The cursor was provided, not releasing.", title
                )
            raise RuntimeError(msg) from oe
        except mysql.connector.Error as e:
            msg = "MySQL Error: An unexpected error occurred during query execution."
            msg += f" Original error: {str(e)}"
            self.disp.log_error(msg, title)
            if cursor is None:
                self.disp.log_debug(
                    "The cursor was generated by us, releasing.", title
                )
                self.release_connection_and_cursor(connection, internal_cursor)
            else:
                self.disp.log_debug(
                    "The cursor was provided, not releasing.", title
                )
            raise RuntimeError(msg) from e

    def run_editing_command(self, sql_query: str, table: str, action_type: str = "update") -> int:
        """_summary_
            Function in charge of running the execute and making sure that the connection to the database is still valid.

        Args:
            command (str): _description_

        Returns:
            int: _description_
        """
        title = "_run_editing_command"
        try:
            resp = self.run_and_commit(query=sql_query)
            if resp != self.success:
                self.disp.log_error(
                    f"Failed to {action_type} data in '{table}'.", title
                )
                return self.error
            self.disp.log_debug("command ran successfully.", title)
            return self.success
        except mysql.connector.Error as e:
            self.disp.log_error(
                f"Failed to {action_type} data in '{table}': {str(e)}", title
            )
            return self.error

    def __del__(self) -> None:
        """_summary_
            Destructor
        """
        self.destroy_pool()

    def is_pool_active(self) -> bool:
        """_summary_
            Check if the connection pool is active.

        Returns:
            bool: _description_
        """
        title = "is_pool_active"
        self.disp.log_debug("Checking if the connection is active.", title)
        resp = self.pool is not None
        if resp:
            self.disp.log_debug("The connection is active.", title)
            return True
        self.disp.log_error("The connection is not active.", title)
        return False

    def is_connection_active(self, connection: mysql.connector.pooling.PooledMySQLConnection) -> bool:
        """
        Checks if the connection is active.

        Args:
            connection (mysql.connector.pooling.PooledMySQLConnection): The connection to check.

        Returns:
            bool: True if the connection is active, False otherwise.
        """
        title = "is_connection_active"
        self.disp.log_debug(
            "Checking if the connection is active.", title
        )
        try:
            if connection:
                connection.ping(reconnect=False)
                self.disp.log_debug("The connection is active.", title)
                return True
        except (mysql.connector.Error, mysql.connector.errors.Error):
            self.disp.log_error("The connection is not active.", title)
            return False
        self.disp.log_error("The connection is not active.", title)
        return False

    def is_cursor_active(self, cursor: mysql.connector.cursor.MySQLCursor) -> bool:
        """
        Checks if the cursor is active.

        Args:
            cursor (mysql.connector.cursor.MySQLCursor): The cursor to check.

        Returns:
            bool: True if the cursor is active, False otherwise.
        """
        title = "is_cursor_active"
        self.disp.log_debug(
            "Checking if the provided cursor is active.", title
        )
        resp = cursor is not None and cursor._connection is not None
        if resp:
            self.disp.log_debug("The cursor is active.", title)
            return True
        self.disp.log_error("The cursor is not active.", title)
        return False
