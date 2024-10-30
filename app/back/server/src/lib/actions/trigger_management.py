"""_summary_
    File in charge of checking the trigger rules.
"""

import os
import json
from typing import Any, Dict

from fastapi import Response
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME

from .variables import Variables
from .logger import ActionLogger
from .query_boilerplate import QueryEndpoint
from . import constants as ACONST
from ..components.runtime_data import RuntimeData
from ..components import constants as CONST


class TriggerManagement:
    """_summary_
    """

    def __init__(self, variable: Variables, logger: ActionLogger, runtime_data: RuntimeData, scope: Any = "default_scope", error: int = 84, success: int = 0, debug: bool = False, delay: int = 10):
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
        self.delay: int = delay
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

    def compile_final_url(self, url: str, url_extra: str, url_params: str) -> str:
        """_summary_
            This function will compile the final URL to be used.

        Args:
            url (str): _description_: The URL to be used.
            url_extra (str): _description_: The extra URL to be used.
            url_params (str): _description_: The URL parameters to be used.

        Returns:
            str: _description_: The final URL to be used.
        """
        if url_extra is not None:
            url += url_extra
        if url_params is not None:
            if url_params[0] != "?":
                url += "?"
            url += url_params
        return url

    def get_api_response(self, action_id: int, trigger_node: Dict[str, Any]) -> Response:
        """_summary_
            Get the response from the API.

        Args:
            action_id (int): _description_: The action ID to log.
            service_name (str): _description_: The name of the service to call.
            url_extra (str): _description_: The extra URL to call.
            url_params (str): _description_: The URL parameters to pass.
            body (Dict[str, Any]): _description_: The body to pass.

        Returns:
            Response: _description_: The response from the API.
        """
        title = "get_api_response"
        if "service_name" not in trigger_node or trigger_node.get("service_name") is None:
            msg = "No service name provided."
            return self._log_fatal(title, msg, action_id, raise_item=True, raise_func=ValueError)
        if url_extra is None:
            msg = "No URL extra provided."
            return self._log_fatal(title, msg, action_id, raise_item=True, raise_func=ValueError)
        if url_params is None:
            msg = "No URL parameters provided."
            return self._log_fatal(title, msg, action_id, raise_item=True, raise_func=ValueError)
        if body is None:
            msg = "No body provided."
            return self._log_fatal(title, msg, action_id, raise_item=True, raise_func=ValueError)
        query_endpoint = QueryEndpoint(
            host=self.compile_final_url(url, ),
            delay=self.delay
        )
        query_endpoint.get_endpoint()

    def run(self) -> int:
        """_summary_
            Run the trigger checking.

        Returns:
            int: _description_: Returns self.success if the program succeeded, self.error otherwise.
        """
        title = "run"
        if self.variable.has_variable("node_data", self.scope) is False:
            msg = f"No applet data found for scope {self.scope}"
            msg += f" in pid {os.getpid()}."
            self._log_fatal(
                title, msg, 0, raise_item=True,
                raise_func=ValueError
            )

        try:
            trigger = json.loads(
                self.variable.get_variable(
                    name="node_data", scope=self.scope
                )
            )
        except json.JSONDecodeError as e:
            msg = f"Error while decoding trigger data: {e}"
            self._log_fatal(
                title, msg, 0, raise_item=True,
                raise_func=ValueError
            )
        action_id = trigger[0].get('id')

        if action_id is None:
            msg = "No action ID found in trigger data."
            self._log_fatal(
                title, msg, 0, raise_item=True,
                raise_func=ValueError
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

        trigger = json.loads(
            self.variable.get_variable(
                name="node_data", scope=self.scope
            )
        )
        action_id = trigger[0]['id']

        if ACONST.OPERATOR_EXCHANGE.get(trigger.verification_operator) is None:
            msg = f"Incorrect type for variable {trigger}."
            self._log_fatal(
                title, msg, action_id,
                raise_item=True, raise_func=ValueError
            )
        comparison_func = ACONST.OPERATOR_EXCHANGE.get(
            trigger["verification_operator"]
        )

        if comparison_func is not None:
            res = comparison_func(
                trigger["url_params"],
                trigger["verification_value"]
            )
        else:
            msg = f"Operator '{trigger['verification_operator']}'"
            msg += "is not supported."
            self._log_fatal(
                title, msg, action_id, raise_item=True, raise_func=ValueError
            )
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
            msg = "Oauth token has expired."
            self.disp.log_error(msg, title)
            self.logger.log_fatal(
                ACONST.TYPE_SERVICE_TRIGGER,
                action_id=action_id,
                message=msg,
                resolved=True
            )
            return self.error
        return self.success
