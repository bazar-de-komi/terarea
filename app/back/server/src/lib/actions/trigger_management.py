"""_summary_
    File in charge of checking the trigger rules.
"""

import os
import json
from typing import Any, Dict, List

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

    def get_api(self, api_name: str, action_id: int) -> Dict[str, Any]:
        """_summary_
            Get the API data from the database.

        Args:
            api_name (str): _description_
            action_id (int): _description_

        Returns:
            Dict[str, Any]: _description_
        """
        title = "get_api"
        if api_name is None:
            self._log_fatal(
                title=title,
                action_id=action_id,
                msg="No api_name found.",
                raise_item=True
            )
        service = self.runtime_data.database_link.get_data_from_table(
            table=CONST.TAB_SERVICES,
            column="*",
            where=f"name='{api_name}'",
            beautify=True
        )
        if isinstance(service, int) is True:
            self._log_fatal(
                title=title,
                action_id=action_id,
                msg=f"Service '{api_name}' not found.",
                raise_item=True
            )
        data: Dict[str, Any] = service[0]
        if data.get("url") is None:
            self._log_fatal(
                title=title,
                action_id=action_id,
                msg="No url found in the service.",
                raise_item=True
            )
        if data.get("api_key") is None:
            self._log_fatal(
                title=title,
                action_id=action_id,
                msg="No api_key found in the service.",
                raise_item=True
            )
        if data.get("oauth") is None:
            self._log_fatal(
                title=title,
                action_id=action_id,
                msg="No oauth found in the service.",
                raise_item=True
            )
        return data

    def process_url_params(self, url_params: List[str]) -> str:
        """_summary_
        Args:
        url_params (List[str]): _description_
        Returns:
        str: _description_
        """
        title = "process_url_params"
        params = ""
        self.disp.log_debug(f"Processing URL params: {url_params}", title)
        param_length = len(url_params)
        for index, item in enumerate(url_params):
            if index == param_length - 1:
                params += f"{item}"
            else:
                params += f"{item}&"
        self.disp.log_debug(f"Processed URL params: {params}", title)
        return params

    def get_oauth_token(self, user_id: int) -> str:
        """_summary_
            Get the OAuth token for the user.

        Args:
            user_id (int): _description_: The user ID to get the token for.

        Returns:
            str: _description_: The OAuth token for the user.
        """
        title = "get_oauth_token"
        token = self.runtime_data.database_link.get_data_from_table(
            table=CONST.TAB_ACTIVE_OAUTHS,
            column="token",
            where=f"user_id={user_id}",
            beautify=False
        )
        if token is None:
            msg = "No token found for user."
            self._log_fatal(title, msg, 0, raise_item=True)
        return token

    def get_correct_token(self, token: str, oauth: bool, location: Dict[str, Any]) -> str:
        """_summary_
            Get the correct token to use.

        Returns:
            str: _description_: The correct token to use.
        """
        title = "get_correct_token"
        if oauth is True:
            data = self.get_oauth_token(location.get("user_id"))
        return token

    def get_api_response(self, action_id: int, service: Dict[str, Any]) -> Response:
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
        url = ""
        header = {}
        body = {}
        if service.get("name") is None:
            msg = "No name found in the service."
            return self._log_fatal(title, msg, action_id, raise_item=False)
        api_node = self.get_api(service.get("name"), action_id)
        url += api_node.get("url")
        url_extra = service.get("url_extra")
        if url_extra is not None:
            if url_extra[0] != "/" and url[-1] != "/":
                url += "/" + url_extra
            elif url_extra[0] == "/" and url[-1] == "/":
                url += url_extra[1:]
            else:
                url += url_extra
        url_params = service.get("url_params")
        if url_params is not None:
            url_params += self.process_url_params(url_params)
            if url_params[0] != "?" and url[-1] != "?":
                url += "?" + url_params
            else:
                url += url_params
        self.disp.log_debug(f"URL: {url}", title)
        body = service.get("body")
        if body is not None:
            self.disp.log_debug(f"Body: {body}", title)
        token_location = service.get("token_location")
        key = self.get_correct_token(
            api_node.get("api_key"),
            api_node.get("oauth"),
            token_location
        )
        usr_header = service.get("header")
        if usr_header is not None:
            header.update(usr_header)
        query_endpoint = QueryEndpoint(
            host=url,
            delay=self.delay
        )
        query_endpoint.get_endpoint()

    def process_single_trigger(self, node: Dict[str, Any]) -> int:
        """_summary_
            Process a single node.

        Args:
            node (Dict[str, Any]): _description_: The node to process.

        Returns:
            int: _description_: Returns self.success if the program succeeded, self.error otherwise.
        """
        pass

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
        if isinstance(trigger, List) is True:
            if len(trigger) == 0:
                self._log_fatal(
                    title,
                    "Empty trigger data.",
                    0, raise_item=True,
                    raise_func=ValueError
                )
            for i in trigger:
                self.process_single_trigger(i)
        elif isinstance(trigger, Dict) is True:
            self.process_single_trigger(trigger)
        else:
            self._log_fatal(
                title, "Incorrect type for variable 'trigger'.",
                0, raise_item=True, raise_func=ValueError
            )

        action_id = trigger.get('id')

        if action_id is None:
            msg = "No action ID found in trigger data."
            self._log_fatal(
                title, msg, 0, raise_item=True,
                raise_func=ValueError
            )

        response = self.get_api_response(action_id, trigger)
        return self.success
