"""_summary_
    File containing boilerplate functions that could be used by the server in it's endpoints_initialised for checking incoming data.
"""

from typing import Union, Dict, Any
from time import sleep
from fastapi import Request
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME

from ..components import RuntimeData, CONST


class BoilerplateIncoming:
    """_summary_
    """

    def __init__(self, runtime_data: RuntimeData, error: int = 84, success: int = 0, debug: bool = False) -> None:
        self.debug: bool = debug
        self.success: int = success
        self.error: int = error
        self.runtime_data_initialised: RuntimeData = runtime_data
        # ------------------------ The logging function ------------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            FILE_DESCRIPTOR,
            SAVE_TO_FILE,
            FILE_NAME,
            debug=self.debug,
            logger=self.__class__.__name__
        )

    def token_correct(self, request: Request) -> bool:
        """_summary_
            This is a function that will check if the token is correct or not.
        Args:
            request (Request): _description_: The request object

        Returns:
            bool: _description_: True if the token is correct, False otherwise
        """
        self.disp.log_debug(
            f"request = {request}", "token_correct"
        )
        token = self.get_token_if_present(request)
        self.disp.log_debug(
            f"token = {token}", "token_correct"
        )
        if token is None:
            return False
        if token not in self.runtime_data_initialised.user_data:
            return False
        return True

    def logged_in(self, request: Request) -> bool:
        """_summary_
            This is a function that will check if the user is logged in or not.
        Args:
            request (Request): _description_: The request object

        Returns:
            bool: _description_: True if the user is logged in, False otherwise
        """
        self.disp.log_debug(
            f"request = {request}", "logged_in"
        )
        token = self.get_token_if_present(request)
        self.disp.log_debug(
            f"token = {token}", "logged_in"
        )
        if token is None:
            return False
        if self.token_correct(request) is False:
            return False
        if token in self.runtime_data_initialised.user_data:
            return True
        return False

    def log_user_in(self, username: str = '', password: str = '') -> Dict[str, Any]:
        """_summary_
            Attempt to log the user in based on the provided credentials and the database.

        Args:
            username (str): _description_: The username of the account
            password (str): _description_: The password for the account

        Returns:
            Dict[str, Any]: _description_: The response status
            {'status':Union[success, error], 'token':Union['some_token', '']}
        """
        data = {'status': self.error, 'token': ''}
        token = self.runtime_data_initialised.boilerplate_non_http_initialised.generate_token()
        self.runtime_data_initialised.user_data[token] = {
            CONST.UA_EMAIL_KEY: "Some email",
            CONST.UA_LIFESPAN_KEY: self.runtime_data_initialised.boilerplate_non_http_initialised.set_lifespan(
                CONST.UA_TOKEN_LIFESPAN
            )
        }
        self.disp.log_critical(
            "Please review this login function for the server",
            "log_user_in"
        )
        data['status'] = self.success
        data['token'] = token
        return data

    def get_token_if_present(self, request: Request) -> Union[str, None]:
        """_summary_
            Return the token if it is present.

        Args:
            request (Request): _description_: the request header created by the endpoint caller.

        Returns:
            Union[str, None]: _description_: If the token is present, a string is returned, otherwise, it is None.
        """
        mtoken: Union[str, None] = request.get(CONST.REQUEST_TOKEN_KEY)
        mbearer: Union[str, None] = request.get(CONST.REQUEST_BEARER_KEY)
        token: Union[str, None] = request.headers.get(CONST.REQUEST_TOKEN_KEY)
        bearer: Union[str, None] = request.headers.get(
            CONST.REQUEST_BEARER_KEY
        )
        msg = f"mtoken = {mtoken}, mbearer = {mbearer}"
        msg += f", token = {token}, bearer = {bearer}"
        self.disp.log_debug(msg, "get_token_if_present")
        if token is None and bearer is None and token is None and bearer is None:
            return None
        if mbearer is not None and mbearer.startswith('Bearer '):
            return mbearer.split(" ")[1]
        if bearer is not None and bearer.startswith('Bearer '):
            return bearer.split(" ")[1]
        if token is not None:
            return token
        return mtoken

    def log_user_out(self, token: str = "") -> Dict[str, Any]:
        """_summary_
            Attempt to log the user out based on the provided token.

        Args:
            token (str): _description_: The token of the account

        Returns:
            Dict[str, Any]: _description_: The response status
            {'status':Union[success, error], 'msg':'message'}
        """
        data = {'status': self.error, 'msg': "You are not logged in !"}
        if token == "":
            data["msg"] = "No token provided !"
            return data

        if token in self.runtime_data_initialised.user_data:
            self.runtime_data_initialised.user_data.pop(token)
            data["status"] = self.success
            data["msg"] = "You have successfully logged out."
        return data
