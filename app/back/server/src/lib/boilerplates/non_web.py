"""_summary_
    This is the the class in charge of containing the non-http boilerplates.
"""

import re
import uuid
from random import randint
from datetime import datetime, timedelta
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME

from ..components import RuntimeData, CONST
from ..sql.sql_manager import SQL


class BoilerplateNonHTTP:
    """_summary_
    """

    def __init__(self, runtime_data_initialised: RuntimeData, success: int = 0, error: int = 84, debug: bool = False) -> None:
        """_summary_
        """
        self.debug: bool = debug
        self.error: int = error
        self.success: int = success
        self.runtime_data_initialised: RuntimeData = runtime_data_initialised
        # ------------------------ The logging function ------------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            FILE_DESCRIPTOR,
            SAVE_TO_FILE,
            FILE_NAME,
            debug=self.debug,
            logger=self.__class__.__name__
        )

    def pause(self) -> str:
        """_summary_
            This is a pause function that works in the same wat as the batch pause command.
            It pauses the program execution until the user presses the enter key.

        Returns:
            str: _description_: The input from the user
        """
        return input("Press enter to continue...")

    def set_lifespan(self, seconds: int) -> datetime:
        """
                The function to set the lifespan of the user token
            Args:
                seconds (int): Seconds

            Returns:
                datetime: The datetime of the lifespan of the token
            """
        current_time = datetime.now()
        offset_time = current_time + timedelta(seconds=seconds)
        return offset_time

    def generate_token(self) -> str:
        """_summary_
            This is a function that will generate a token for the user.
        Returns:
            str: _description_: The token generated
        """
        title = "generate_token"
        token = str(uuid.uuid4())
        user_token = self.runtime_data_initialised.database_link.get_data_from_table(
            table=CONST.TAB_CONNECTIONS,
            column="token",
            where=f"token='{token}'",
            beautify=False
        )
        self.disp.log_debug(f"user_token = {user_token}", title)
        while len(user_token) > 0:
            token = str(uuid.uuid4())
            user_token = self.runtime_data_initialised.database_link.get_data_from_table(
                table=CONST.TAB_CONNECTIONS,
                column="token",
                where=f"token='{token}'",
                beautify=False
            )
            self.disp.log_debug(f"user_token = {user_token}", title)
            if isinstance(user_token, int) is True and user_token == self.error:
                return token
            if len(user_token) == 0:
                return token
        return token

    def server_show_item_content(self, function_name: str = "show_item_content", item_name: str = "", item: object = None, show: bool = True) -> None:
        """_summary_
            This is a function that will display the content of an item.
            The purpose of this function is more for debugging purposes.
        Args:
            function_name (str, optional): _description_. Defaults to "show_item_content".
            item (object, optional): _description_. Defaults to None.
        """
        if show is False:
            return
        self.disp.log_debug(
            f"({function_name}) dir({item_name}) = {dir(item)}",
            "pet_server_show_item_content"
        )
        for i in dir(item):
            if i in ("auth", "session", "user"):
                self.disp.log_debug(
                    f"({function_name}) skipping {item_name}.{i}"
                )
                continue
            self.disp.log_debug(
                f"({function_name}) {item_name}.{i} = {getattr(item, i)}"
            )

    def check_date(self, date: str = "DD/MM/YYYY") -> bool:
        """_summary_
            This is a function that will check if the date is correct or not.
        Args:
            date (str, optional): _description_: The date to check. Defaults to "DD/MM/YYYY".

        Returns:
            bool: _description_: True if the date is correct, False otherwise
        """
        pattern = re.compile(
            r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
        )
        match = pattern.match(date)
        return bool(match)

    def check_database_health(self) -> None:
        """_summary_
            This function will reconnect to the database in case it has been disconnected.
        """
        if self.runtime_data_initialised.database_link is None:
            try:
                self.disp.log_debug(
                    "database_link is none, initialising sql.",
                    "check_database_health"
                )
                self.runtime_data_initialised.database_link = SQL(
                    url=CONST.DB_HOST,
                    port=CONST.DB_PORT,
                    username=CONST.DB_USER,
                    password=CONST.DB_PASSWORD,
                    db_name=CONST.DB_DATABASE,
                    success=self.success,
                    error=self.error,
                    debug=self.debug
                )
            except RuntimeError as e:
                msg = "Could not connect to the database."
                raise RuntimeError(msg) from e

        if self.runtime_data_initialised.database_link.is_connected() is False:
            if self.runtime_data_initialised.database_link.connect_to_db() is False:
                try:
                    self.disp.log_debug(
                        "database_link is none, initialising sql.",
                        "check_database_health"
                    )
                    self.runtime_data_initialised.database_link = SQL(
                        url=CONST.DB_HOST,
                        port=CONST.DB_PORT,
                        username=CONST.DB_USER,
                        password=CONST.DB_PASSWORD,
                        db_name=CONST.DB_DATABASE,
                        success=self.success,
                        error=self.error,
                        debug=self.debug
                    )
                except RuntimeError as e:
                    msg = "(check_database_health) Could not connect to the database."
                    raise RuntimeError(msg) from e

    def is_token_admin(self, token: str) -> bool:
        """_summary_
            Check if the user's token has admin privileges.
        Args:
            token (str): _description_

        Returns:
            bool: _description_
        """
        title = "is_token_admin"
        user_id = self.runtime_data_initialised.database_link.get_data_from_table(
            table=CONST.TAB_CONNECTIONS,
            column="user_id",
            where=f"token='{token}'",
            beautify=False
        )
        if isinstance(user_id, int) is True and user_id == self.error:
            self.disp.log_error(
                f"Failed to find token {token} in the database.", title
            )
            return False
        self.disp.log_debug(f"usr_id = {user_id}", title)
        user_info = self.runtime_data_initialised.database_link.get_data_from_table(
            table=CONST.TAB_ACCOUNTS,
            column="admin",
            where=f"id={user_id[0][0]}",
            beautify=False
        )
        if isinstance(user_info, int) is True and user_info == self.error:
            self.disp.log_error(
                f"Failed to find user {user_id[0][0]} in the database.", title
            )
            return False
        self.disp.log_debug(f"usr_info = {user_info}", title)
        return user_info[0][0] == 1

    def generate_check_token(self, token_size: int = 4) -> str:
        """_summary_
            Create a token that can be used for e-mail verification.

        Returns:
            str: _description_
        """
        if isinstance(token_size, (int, float)) is False:
            token_size = 4
        token_size = int(token_size)
        token_size = max(token_size, 0)
        code = f"{randint(CONST.RANDOM_MIN, CONST.RANDOM_MAX)}"
        for i in range(token_size):
            code += f"-{randint(CONST.RANDOM_MIN, CONST.RANDOM_MAX)}"
        return code
