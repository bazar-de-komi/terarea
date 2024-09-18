"""_summary_
    File containing boilerplate responses that could be used by the server in it's endpoints_initialised.
"""
from typing import Union, Dict, Any
from fastapi import Response
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from ..components import HCI, RuntimeData, CONST


class BoilerplateResponses:
    """_summary_
    """

    def __init__(self, runtime_data: RuntimeData, debug: bool = False) -> None:
        """_summary_

        Args:
            debug (bool, optional): _description_. Defaults to False.
        """
        self.debug: bool = debug
        self.runtime_data_initialised: RuntimeData = runtime_data
        self.disp: Disp = Disp(
            TOML_CONF,
            SAVE_TO_FILE,
            FILE_NAME,
            FILE_DESCRIPTOR,
            debug=self.debug,
            logger=self.__class__.__name__
        )

    def build_response_body(self, title: str, message: str, resp: Any, token: Union[str, None], error: bool = False) -> Dict[str, Any]:
        """_summary_
            This is a function that will create a response body for the queries of the server.
        Args:
            title (str): _description_: The title of the message in the body
            message (any): _description_: The actual message you wish to send (this is so that it is human friendly [i.e. "You have successfully logged in"])
            resp (any): _description_: The section where you can put more coder side data.
            token Union[str, None]: _description_: The user token or None if not present
            error (bool, optional): _description_: If this is an error message or not. Defaults to False.

        Returns:
            Dict[str, any]: _description_: the final version of the body message
        """
        json_body = {}
        msg = f"title={title}, message={message}, resp={resp},"
        msg += f"token={token}, error={error}"
        self.disp.log_debug(msg, "build_response_body")

        json_body[CONST.JSON_TITLE] = title
        json_body[CONST.JSON_MESSAGE] = message
        if error is False:
            json_body[CONST.JSON_RESP] = resp
        else:
            json_body[CONST.JSON_ERROR] = resp
        msg = f"token = {token}, self.user_data = {
            self.runtime_data_initialised.user_data}"
        msg += f", token in self.user_data = {
            token in self.runtime_data_initialised.user_data}"
        self.disp.log_debug(msg, "build_response_body")
        if token is not None and token in self.runtime_data_initialised.user_data:
            json_body[CONST.JSON_LOGGED_IN] = True
        else:
            json_body[CONST.JSON_LOGGED_IN] = False
        return json_body

    def invalid_token(self, title: str) -> Response:
        """_summary_
            This is a function that will return an invalid token response.

        Args:
            title (str): _description_: The title of the called endpoint

        Returns:
            Response: _description_: The response ready to be sent back to the user
        """
        body = self.build_response_body(
            title=title,
            message="The token you entered is invalid.",
            resp="Invalid token",
            token="",
            error=True
        )
        return HCI.invalid_token(content=body, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)

    def not_logged_in(self, title: str) -> Response:
        """_summary_
            This is a function that will return a not logged in response.

        Args:
            title (str): _description_: The title of the called endpoint

        Returns:
            Response: _description_: The response ready to be sent back to the user
        """
        body = self.build_response_body(
            title=title,
            message="You need to be logged in to be able to run this endpoint.",
            resp="User not logged in",
            token="",
            error=True
        )
        return HCI.unauthorized(content=body, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)

    def login_failed(self, title: str) -> Response:
        """_summary_
            This is a function that will return a failed login response.

        Args:
            title (str): _description_: The title of the called endpoint

        Returns:
            Response: _description_: The response ready to be sent back to the user
        """
        body = self.build_response_body(
            title=title,
            message="Login failed, invalid credentials or username.",
            resp="Invalid credentials or username.",
            token="",
            error=True
        )
        return HCI.unauthorized(content=body, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)

    def insuffisant_rights(self, title: str, token: str) -> Response:
        """_summary_
            This is a function that will return an insuffisant rights response.

        Args:
            title (str): _description_: The title of the called endpoint
            token (str): _description_: The token provided by the user of the called endpoint

        Returns:
            Response: _description_: The response ready to be sent back to the user
        """
        body = self.build_response_body(
            title=title,
            message="You do not have enough permissions to execute this endpoint.",
            resp="Insufficient rights for given account.",
            token=token,
            error=True
        )
        return HCI.forbidden(content=body, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)
