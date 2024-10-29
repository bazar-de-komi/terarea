"""_summary_
    File in charge of checking the trigger rules.
"""

import json
from typing import Any

from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME

from .variables import Variables
from . import constants as ACONST
from .logger import ActionLogger
from ..components.runtime_data import RuntimeData
from ..components import constants as CONST


class TriggerManagement:
    """_summary_
    """

    def __init__(self, variable: Variables, logger: ActionLogger, runtime_data: RuntimeData, scope: Any = "default_scope", error: int = 84, success: int = 0, debug: bool = False):
        """_summary_
            This is the class in charge of checking the triggers and storing variables if required.

        Args:
            variable (Variables): _description_: The class variable in charge of tracking the variables for the runtime.
            runtime_data (RuntimeData): _description_: The class runtime data in charge of containing important connections.
            scope (Any, optional): _description_: The scope of the trigger. Defaults to "default_scope".
            error (int, optional): _description_. Defaults to 84.: The error value
            success (int, optional): _description_. Defaults to 0.: The success value
            debug (bool, optional): _description_. Defaults to False.: Set to True if you wish to activate debug mode.
        """
        # -------------------------- Inherited values --------------------------
        self.error: int = error
        self.scope: Any = scope
        self.debug: bool = debug
        self.success: int = success
        self.logger: ActionLogger = logger
        self.variable: Variables = variable
        self.runtime_data: RuntimeData = runtime_data
        # ---------------------- The visual logger class  ----------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            SAVE_TO_FILE,
            FILE_NAME,
            FILE_DESCRIPTOR,
            debug=self.debug,
            logger=self.__class__.__name__
        )

# variable = scope: {"test1": node1, "test2": node2, "test3": node3 }
# example 1 : node = {"data": 1, "type": int}
# example 2 : node = {"data": "1", "type": str}
    def run(self) -> int:
        """_summary_
            Run the trigger checking.

        Returns:
            int: _description_: Returns self.success if the program succeeded, self.error otherwise.
        """
        title = "run"
        if self.variable.has_variable("node_data", self.scope) is False:
            return self.error

        trigger = json.loads(self.variable.get_variable(name="node_data", scope=self.scope))
        action_id = trigger[0]['id']

        if ACONST.OPERATOR_EXCHANGE.get(trigger.verification_operator) is None:
            msg = f"Incorrect type for variable {trigger}."
            self.disp.log_error(msg, title)
            self.logger.log_fatal(
                ACONST.TYPE_SERVICE_TRIGGER,
                action_id=action_id,
                message=msg,
                resolved=False
            )
            raise ValueError(f"Operator does not exist.")
        comparison_func = ACONST.OPERATOR_EXCHANGE.get(trigger.verification_operator)

        if comparison_func:
            res = comparison_func(trigger.url_params, trigger.verification_value)
        else:
            raise ValueError(f"Operator '{trigger.verification_operator}' is not supported.")
        if res is False:
            msg = "Condition was not met."
            self.logger.log_warning(
                ACONST.TYPE_SERVICE_TRIGGER,
                action_id=action_id,
                message=msg,
                resolved=True
            )
        oauth_token = self.runtime_data.database_link.get_data_from_table(
            table=CONST.TAB_ACTIVE_OAUTHS,
            column="token_expiration",
            where=f"user_id={trigger[0]['user_id']}",
            beautify=False
        )
        if ACONST.check_if_oauth_is_valid(oauth_token) is False:
            msg = f"Oauth token has expired."
            self.disp.log_error(msg, title)
            self.logger.log_fatal(
                ACONST.TYPE_SERVICE_TRIGGER,
                action_id=action_id,
                message=msg,
                resolved=True
            )
            return self.error
        return self.success
