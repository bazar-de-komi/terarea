"""_summary_
    File in charge of logging events into the logging database
"""
from typing import List, Union

from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME

from ..components.runtime_data import RuntimeData
from ..components import constants as CONST

from . import constants as ACONST


class ActionLogger:
    """_summary_
        Class in charge of logging events into the logging database
    """

    def __init__(self, runtime_data: RuntimeData, success: int = 0, error: int = 84, debug: bool = False) -> None:
        """_summary_
            Class in charge of logging events into the logging database

        Args:
            runtime_data (RuntimeData): _description_
            success (int, optional): _description_. Defaults to 0.
            error (int, optional): _description_. Defaults to 84.
            debug (bool, optional): _description_. Defaults to False.
        """
        # -------------------------- Inherited values --------------------------
        self.error = error
        self.debug = debug
        self.success = success
        self.runtime_data = runtime_data
        # ---------------------- The visual logger class  ----------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            SAVE_TO_FILE,
            FILE_NAME,
            FILE_DESCRIPTOR,
            debug=self.debug,
            logger=self.__class__.__name__
        )

    def log_event(self, log_type: str, action_id: int = 0, code: int = ACONST.CODE_ERROR, message: Union[str, None] = None, resolved: bool = False) -> int:
        """_summary_
            Log an event into the logging database

        Args:
            log_type (str): _description_: The type of the event
            action_id (int, optional): _description_: The id of the action that triggered the event, defaults to 0
            code (int, optional): _description_: The code of the event, defaults to ACONST.CODE_ERROR
            message (Union[str, None], optional): _description_: The message of the event, defaults to None
            resolved (bool, optional): _description_: The status of the event, defaults to False

        Returns:
            int: _description_: Returns 0 if it succeeds, 84 otherwise
        """
        title = "log_event"

        columns: List[str] = self.runtime_data.database_link.get_table_column_names(
            CONST.TAB_ACTION_LOGGING
        )
        if columns != self.success:
            self.disp.log_error("Failed to get the table columns.", title)
            return self.error
        columns.pop(0)

        if log_type not in ACONST.LIST_TYPE:
            msg = f"Type: {type} is not in the list of types."
            msg += f" Setting type to {ACONST.TYPE_UNKNOWN}."
            self.disp.log_warning(msg, title)
            log_type = ACONST.TYPE_UNKNOWN

        if self._check_if_action_id_in_table(action_id) is False:
            msg = f"The action_id, {action_id},"
            msg += " is not in the Actions table."
            self.disp.log_error(msg, title)
            return self.error

        if code in ACONST.LOG_EQUIVALENCE:
            code_level = ACONST.LOG_EQUIVALENCE[code]
        else:
            code_level = ACONST.LOG_EQUIVALENCE[ACONST.CODE_UNKNOWN]

        if message is None:
            self.disp.log_warning(
                "The message is None, defaulting to the code message equivalence.", title
            )
            message = ACONST.LOG_MESSAGE_EQUIVALENCE[code_level]

        if isinstance(resolved, bool) is False:
            self.disp.log_warning(
                "The resolved status is not a boolean, defaulting to False.", title
            )
            resolved = False

        data = [
            "now",  # time
            f"{log_type}",  # type
            f"{action_id}",  # action_id
            f"{message}",  # message
            f"{code}",  # error_code
            f"{code_level}",  # error_level
            f"{int(resolved)}"  # resolved
        ]
        status = self.runtime_data.database_link.insert_data_into_table(
            table=CONST.TAB_ACTION_LOGGING,
            data=data,
            column=columns
        )
        if status != self.success:
            self.disp.log_error("Failed to log the event.", title)
            return self.error
        return self.success

    def _check_if_action_id_in_table(self, action_id: int = 0) -> bool:
        """_summary_
            Check if the action_id is in the Actions table

        Args:
            action_id (int, optional): _description_. Defaults to 0.: The id of the concerned action.

        Returns:
            bool: _description_: Returns True if it is present, False otherwise.
        """
        data = self.runtime_data.database_link.get_data_from_table(
            table=CONST.TAB_ACTIONS,
            column="id",
            where=f"id={action_id}",
            beautify=False
        )
        if data != self.success:
            return False
        if len(data) == 1:
            return True
        return False

    def log_info(self, log_type: str, action_id: int = 0, message: Union[str, None] = None, resolved: bool = False) -> int:
        """_summary_
            Log an info event into the logging database

        Args:
            log_type (str): _description_: The type of the event
            action_id (int, optional): _description_: The id of the action that triggered the event, defaults to 0
            message (Union[str, None], optional): _description_: The message of the event, defaults to None
            resolved (bool, optional): _description_: The status of the event, defaults to False

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise
        """
        return self.log_event(
            log_type=log_type,
            action_id=action_id,
            code=ACONST.CODE_INFO,
            message=message,
            resolved=resolved
        )

    def log_success(self, log_type: str, action_id: int = 0, message: Union[str, None] = None, resolved: bool = False) -> int:
        """_summary_
            Log an success event into the logging database

        Args:
            log_type (str): _description_: The type of the event
            action_id (int, optional): _description_: The id of the action that triggered the event, defaults to 0
            message (Union[str, None], optional): _description_: The message of the event, defaults to None
            resolved (bool, optional): _description_: The status of the event, defaults to False

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise
        """
        return self.log_event(
            log_type=log_type,
            action_id=action_id,
            code=ACONST.CODE_SUCCESS,
            message=message,
            resolved=resolved
        )

    def log_debug(self, log_type: str, action_id: int = 0, message: Union[str, None] = None, resolved: bool = False) -> int:
        """_summary_
            Log an debug event into the logging database

        Args:
            log_type (str): _description_: The type of the event
            action_id (int, optional): _description_: The id of the action that triggered the event, defaults to 0
            message (Union[str, None], optional): _description_: The message of the event, defaults to None
            resolved (bool, optional): _description_: The status of the event, defaults to False

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise
        """
        return self.log_event(
            log_type=log_type,
            action_id=action_id,
            code=ACONST.CODE_DEBUG,
            message=message,
            resolved=resolved
        )

    def log_warning(self, log_type: str, action_id: int = 0, message: Union[str, None] = None, resolved: bool = False) -> int:
        """_summary_
            Log an warning event into the logging database

        Args:
            log_type (str): _description_: The type of the event
            action_id (int, optional): _description_: The id of the action that triggered the event, defaults to 0
            message (Union[str, None], optional): _description_: The message of the event, defaults to None
            resolved (bool, optional): _description_: The status of the event, defaults to False

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise
        """
        return self.log_event(
            log_type=log_type,
            action_id=action_id,
            code=ACONST.CODE_WARNING,
            message=message,
            resolved=resolved
        )

    def log_error(self, log_type: str, action_id: int = 0, message: Union[str, None] = None, resolved: bool = False) -> int:
        """_summary_
            Log an error event into the logging database

        Args:
            log_type (str): _description_: The type of the event
            action_id (int, optional): _description_: The id of the action that triggered the event, defaults to 0
            message (Union[str, None], optional): _description_: The message of the event, defaults to None
            resolved (bool, optional): _description_: The status of the event, defaults to False

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise
        """
        return self.log_event(
            log_type=log_type,
            action_id=action_id,
            code=ACONST.CODE_ERROR,
            message=message,
            resolved=resolved
        )

    def log_critical(self, log_type: str, action_id: int = 0, message: Union[str, None] = None, resolved: bool = False) -> int:
        """_summary_
            Log an critical event into the logging database

        Args:
            log_type (str): _description_: The type of the event
            action_id (int, optional): _description_: The id of the action that triggered the event, defaults to 0
            message (Union[str, None], optional): _description_: The message of the event, defaults to None
            resolved (bool, optional): _description_: The status of the event, defaults to False

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise
        """
        return self.log_event(
            log_type=log_type,
            action_id=action_id,
            code=ACONST.CODE_CRITICAL,
            message=message,
            resolved=resolved
        )

    def log_fatal(self, log_type: str, action_id: int = 0, message: Union[str, None] = None, resolved: bool = False) -> int:
        """_summary_
            Log an fatal event into the logging database

        Args:
            log_type (str): _description_: The type of the event
            action_id (int, optional): _description_: The id of the action that triggered the event, defaults to 0
            message (Union[str, None], optional): _description_: The message of the event, defaults to None
            resolved (bool, optional): _description_: The status of the event, defaults to False

        Returns:
            int: _description_: Returns self.success if it succeeds, self.error otherwise
        """
        return self.log_event(
            log_type=log_type,
            action_id=action_id,
            code=ACONST.CODE_FATAL,
            message=message,
            resolved=resolved
        )
