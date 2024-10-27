"""_summary_
    File in charge of testing the logger class for the actions
"""

import os
import sys
from typing import List, Dict, Any

sys.path.append(os.path.join("..", os.getcwd()))
sys.path.append(os.getcwd())

try:
    import constants as TCONST
except ImportError as e:
    raise ImportError("Failed to import the unit test constants module") from e

try:
    from src.lib.actions import constants as ACONST
    from src.lib.actions.logger import ActionLogger
    from src.lib.sql.sql_manager import SQL
    from src.lib.components import constants as CONST
    from src.lib.components.runtime_data import RuntimeData
    from src.lib.boilerplates.non_web import BoilerplateNonHTTP
    from src.lib.boilerplates.responses import BoilerplateResponses
    from src.lib.components.password_handling import PasswordHandling
except ImportError as e:
    raise ImportError("Failed to import the src module") from e

ERROR = TCONST.ERROR
SUCCESS = TCONST.SUCCESS
DEBUG = TCONST.DEBUG


RDI = RuntimeData(TCONST.SERVER_HOST, TCONST.PORT, "Area", ERROR, SUCCESS)
BRI = BoilerplateResponses(
    runtime_data=RDI,
    debug=DEBUG
)
RDI.boilerplate_responses_initialised = BRI
RDI.boilerplate_non_http_initialised = BoilerplateNonHTTP(
    runtime_data_initialised=RDI,
    success=SUCCESS,
    error=ERROR,
    debug=DEBUG
)

SQLI = SQL(
    url=CONST.DB_HOST,
    port=CONST.DB_PORT,
    username=CONST.DB_USER,
    password=CONST.DB_PASSWORD,
    db_name=CONST.DB_DATABASE,
    debug=DEBUG
)
RDI.database_link = SQLI

RDI.boilerplate_responses_initialised = BRI

ACLI = ActionLogger(
    runtime_data=RDI,
    success=SUCCESS,
    error=ERROR,
    debug=DEBUG
)

PHI = PasswordHandling(
    error=ERROR,
    success=SUCCESS,
    debug=DEBUG
)

TEST_INFO = {
    "user_id": 0,
    "action_id": 0,
    "cache_busting": TCONST.CACHE_BUSTER_ADMIN
}


def _add_dummy_user() -> None:
    """_summary_
        Function in charge of adding a dummy user to the database.
    """
    columns: List[str] = SQLI.get_table_column_names(CONST.TAB_ACCOUNTS)
    if columns == ERROR:
        msg = f"Failed get data from table: {CONST.TAB_ACCOUNTS}"
        raise RuntimeError(msg)
    columns.pop(0)
    username = f"test_user_{TEST_INFO['cache_busting']}"
    email = f"test_email_{TEST_INFO['cache_busting']}@combobox.ttk"
    password = PHI.hash_password(f"test_password_{TEST_INFO['cache_busting']}")
    method = "local"
    favicon = "NULL"
    admin = "1"
    data = [
        username,
        email,
        password,
        method,
        favicon,
        admin
    ]
    status = SQLI.insert_data_into_table(
        table=CONST.TAB_ACCOUNTS,
        data=data,
        column=columns
    )
    if status == ERROR:
        msg = f"Failed to add user {username}"
        msg += f"to the database {CONST.TAB_ACCOUNTS}"
        raise RuntimeError(msg)
    usr_id = SQLI.get_data_from_table(
        table=CONST.TAB_ACCOUNTS,
        column="id",
        where=f"email='{email}'"
    )
    if usr_id == ERROR:
        msg = f"Failed to get user id for {username}"
        raise RuntimeError(msg)
    TEST_INFO["user_id"] = usr_id[0][0]


def _add_dummy_action() -> None:
    """_summary_
        Function in charge of adding a dummy action to the database.
    """
    _add_dummy_user()
    columns: List[str] = SQLI.get_table_column_names(CONST.TAB_ACTIONS)
    if columns == ERROR:
        msg = f"Failed get data from table: {CONST.TAB_ACTIONS}"
        raise RuntimeError(msg)
    columns.pop(0)
    name = f"test_action_name_{TEST_INFO['cache_busting']}"
    trigger = f"test_trigger_{TEST_INFO['cache_busting']}"
    consequences = f"test_consequences_{TEST_INFO['cache_busting']}"
    user_id = TEST_INFO["user_id"]
    tags = "test_actions,will_not_run"
    running = f"{int(False)}"
    description = "This is an action that was generated during unit tests, it is thus not an action that can run."
    colour = "#00D9FFFF"
    favicon = "NULL"
    frequency = "0"
    data = [
        name,
        trigger,
        consequences,
        user_id,
        tags,
        running,
        description,
        colour,
        favicon,
        frequency
    ]
    status = SQLI.insert_data_into_table(
        table=CONST.TAB_ACTIONS,
        data=data,
        column=columns
    )
    if status == ERROR:
        msg = f"Failed to add action {name}"
        msg += f"to the database {CONST.TAB_ACTIONS}"
        raise RuntimeError(msg)
    action_id = SQLI.get_data_from_table(
        table=CONST.TAB_ACTIONS,
        column="id",
        where=f"name='{name}'"
    )
    if action_id == ERROR:
        msg = f"Failed to get action id for {name}"
        raise RuntimeError(msg)
    TEST_INFO["action_id"] = action_id[0][0]


def _remove_dummy_user() -> None:
    """_summary_
        Function in charge of removing the dummy user from the database.
    """
    _remove_dummy_action()
    SQLI.remove_data_from_table(
        CONST.TAB_ACCOUNTS,
        where=f"id={TEST_INFO['user_id']}"
    )


def _remove_dummy_action() -> None:
    """_summary_
        Function in charge of removing the dummy action from the database.
    """
    SQLI.remove_data_from_table(
        CONST.TAB_ACTIONS,
        where=f"id={TEST_INFO['user_id']}"
    )


def _remove_log_line(log_id: int) -> None:
    """_summary_
        Function in charge of removing the log line from the database.

    Args:
        log_id (int): _description_
    """
    SQLI.remove_data_from_table(
        CONST.TAB_ACTION_LOGGING,
        where=f"id={log_id}"
    )


def _get_log_lines(action_id: str = "") -> Dict[str, Any]:
    """_summary_
        Function in charge of getting the log line from the database.
    """
    node = action_id
    log_line = SQLI.get_data_from_table(
        table=CONST.TAB_ACTION_LOGGING,
        column="*",
        where=f"action_id='{node}'"
    )
    if log_line == ERROR:
        msg = f"Failed to get log line for {TEST_INFO['log_id']}"
        raise RuntimeError(msg)
    return log_line


def test_log_event() -> None:
    """_summary_
        Function in charge of testing the log_event function.
    """
    _add_dummy_action()
    action_id = TEST_INFO["action_id"]
    log_id = ACLI.log_event(
        log_type=ACONST.TYPE_ACTION,
        action_id=action_id,
        code=ACONST.CODE_INFO,
        message="This is a test message",
        resolved=False,
    )
    if log_id == ERROR:
        msg = "Failed to log the event."
        raise RuntimeError(msg)
    data = _get_log_lines(action_id)
    print(f"Gathered data: {data}")
    _remove_log_line(data[0]["id"])
    _remove_dummy_user()
