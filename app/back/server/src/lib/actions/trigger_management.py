"""_summary_
    File in charge of checking the trigger rules.
"""

import os
import json
from typing import Any, Dict, List

from requests import Response
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME

from .secrets import Secrets
from .variables import Variables
from .logger import ActionLogger
from . import constants as ACONST
from .api_querier import APIQuerier
from ..components import constants as CONST
from ..components.runtime_data import RuntimeData


class TriggerManagement:
    """_summary_
    """

    def __init__(self, variable: Variables, logger: ActionLogger, runtime_data: RuntimeData, scope: Any = "default_scope", action_id: int = 0, error: int = 84, success: int = 0, debug: bool = False, delay: int = 10):
        """_summary_
            This is the class in charge of checking the triggers and storing variables if required.

        Args:
            variable (Variables): _description_: The class variable in charge of tracking the variables for the runtime.
            logger (ActionLogger): _description_: The class logger in charge of logging the actions.
            runtime_data (RuntimeData): _description_: The class runtime data in charge of containing important connections.
            action_id (int): _description_: The action ID to log.
            scope (Any, optional): _description_: The scope of the trigger. Defaults to "default_scope".
            error (int, optional): _description_. Defaults to 84.: The error value
            success (int, optional): _description_. Defaults to 0.: The success value
            debug (bool, optional): _description_. Defaults to False.: Set to True if you wish to activate debug mode.
        """
        # -------------------------- Inherited values --------------------------
        self.error: int = error
        self.scope: Any = scope
        self.delay: int = delay
        self.debug: bool = debug
        self.success: int = success
        self.action_id: str = str(action_id)
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
        # ------------------ The class containing the secrets ------------------
        self.secrets: Secrets = Secrets(
            success=self.success,
            error=self.error,
            debug=self.debug
        )

    def _log_fatal(self, title: str, msg, action_id: int, raise_item: bool = False, raise_func: object = ValueError) -> int:
        """_summary_
            A function that will log a provided fatal error.

        Args:
            title (str): _description_: the title of the function
            msg (str): _description_: The message to log
            raise_item (bool, optional): _description_. Inform if the logger should raise or just return an error. Defaults to False.
            raise_func (object, optional): _description_. The function to raise if required. Defaults to ValueError.

        Raises:
            ValueError: _description_: One of the possible errors to raise.

        Returns:
            int: _description_: Will return self.error if raise_item is False
        """
        self.disp.log_error(msg, title)
        self.logger.log_fatal(
            ACONST.TYPE_SERVICE_TRIGGER,
            action_id=action_id,
            message=msg,
            resolved=False
        )
        if raise_item is True:
            raise_func(msg)
        else:
            return self.error

    def run(self) -> int:
        """_summary_
            Run the trigger checking.

        Returns:
            int: _description_: Returns self.success if the program succeeded, self.error otherwise.
        """
        title = "run"
        self.disp.log_debug("Running trigger management.", title)
        data = self.variable.get_scope(self.scope)
        self.disp.log_debug(
            f"Scope: {self.scope}, scope_content = {data}", title
        )
        if self.variable.has_variable("node_data", self.scope) is False:
            msg = f"No applet data found for scope {self.scope}"
            msg += f" in pid {os.getpid()}."
            self._log_fatal(
                title, msg, self.action_id, raise_item=True,
                raise_func=ValueError
            )

        action_node = self.variable.get_variable(
            name="node_data", scope=self.scope
        )
        if "trigger" not in action_node:
            self._log_fatal(
                title=title,
                msg="No trigger data found in applet data.",
                action_id=self.action_id,
                raise_item=True,
                raise_func=ValueError
            )
        trigger_node = action_node["trigger"]
        self.disp.log_debug(f"Trigger node: {trigger_node}", title)
        if isinstance(trigger_node, Dict) is False:
            try:
                trigger = json.loads(trigger_node)
            except json.JSONDecodeError as e:
                msg = f"Error while decoding trigger data: {e}"
                self._log_fatal(
                    title, msg, self.action_id, raise_item=True,
                    raise_func=ValueError
                )
        else:
            trigger: Dict[str, Any] = trigger_node
        self.disp.log_debug(f"Trigger data: {trigger}", title)
        node_of_interest = "service"
        if node_of_interest not in trigger:
            self._log_fatal(
                title=title,
                msg="No service data found in trigger data.",
                action_id=self.action_id,
                raise_item=True,
                raise_func=ValueError
            )
        node = trigger.get(node_of_interest)
        apiqi = APIQuerier(
            service=node,
            variable=self.variable,
            scope=self.scope,
            runtime_data=self.runtime_data,
            logger=self.logger,
            action_id=self.action_id,
            error=self.error,
            success=self.success,
            debug=self.debug
        )
        self.disp.log_debug("apiqi initialised", title)
        response: Response = apiqi.query()
        if response is None:
            self._log_fatal(
                title=title,
                msg="No response found from API query.",
                action_id=self.action_id,
                raise_item=True,
                raise_func=ValueError
            )
        self.disp.log_debug(f"Response: {response}", title)
        self.disp.log_debug(
            f"Response status_code: {response.status_code}", title
        )
        self.disp.log_debug(
            f"Response headers: {response.headers}", title
        )
        self.disp.log_debug(
            f"Response content: {response.content}", title
        )
        self.disp.log_debug(
            f"Response json: {response.json()}", title
        )
        if response.json() is None:
            self._log_fatal(
                title=title,
                msg="No JSON data found in response.",
                action_id=self.action_id,
                raise_item=True,
                raise_func=ValueError
            )

        return self.success
