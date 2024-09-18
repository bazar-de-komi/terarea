"""_summary_
    This is the file in charge of storing the endpoints_initialised ready to be imported into the server class.
"""
import signal
from fastapi import Response, Request
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from . import constants as CONST
from .runtime_data import RuntimeData
from .http_codes import HCI


class Endpoints:
    """_summary_
    """

    def __init__(self, runtime_data: RuntimeData, success: int = 0, error: int = 84, debug: bool = False) -> None:
        """_summary_

        Args:
            runtime_data (RuntimeData): _description_
            success (int, optional): _description_. Defaults to 0.
            error (int, optional): _description_. Defaults to 84.
            debug (bool, optional): _description_. Defaults to False.
        """
        self.debug: bool = debug
        self.success: int = success
        self.error: int = error
        self.runtime_data_initialised: RuntimeData = runtime_data
        self.disp: Disp = Disp(
            TOML_CONF,
            SAVE_TO_FILE,
            FILE_NAME,
            FILE_DESCRIPTOR,
            debug=self.debug,
            logger=self.__class__.__name__
        )

    async def my_test_component(self) -> Response:
        """_summary_
        This is a test component that will return a response with the message "Hello World".
        Returns:
            Response: _description_
        """
        return HCI.success({"msg": "Hello World"})

    async def get_welcome(self, request: Request) -> Response:
        """_summary_
            The endpoint corresponding to '/'.

        Returns:
            Response: _description_: The data to send back to the user as a response.
        """
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request)
        self.disp.log_debug(f'(get_welcome) token = {token}')
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title="Home",
            message="Welcome to the control server.",
            resp="",
            token=token,
            error=False
        )
        self.disp.log_debug(f"sent body : {body}", "get_welcome")
        self.disp.log_debug(
            f"header = {
                self.runtime_data_initialised.json_header}", "get_welcome"
        )
        outgoing = HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )
        self.disp.log_debug(f"ready_to_go: {outgoing}", "get_welcome")
        return outgoing

    async def post_login(self, request: Request) -> Response:
        """_summary_
            The endpoint allowing a user to log into the server.

        Returns:
            Response: _description_: The data to send back to the user as a response.
        """
        title = "Stop server"
        self.disp.log_critical("Implement proper login.", "post_login")
        username = "some_username_body"
        data = self.runtime_data_initialised.boilerplate_incoming_initialised.log_user_in(
            username,
            "some_password_body"
        )
        if data["status"] == self.error:
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="Login failed.",
                resp="error",
                token=data["token"],
                error=True
            )
            return HCI.forbidden(content=body, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=f"Welcome {username}",
            resp="success",
            token=data["token"],
            error=False
        )
        return HCI.success(content=body, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)

    async def post_stop_server(self, request: Request) -> Response:
        """_summary_
            The endpoint allowing a user to stop the server.

        Returns:
            Response: _description_: The data to send back to the user as a response.
        """
        title = "Stop server"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request)
        self.disp.log_critical(
            "Please add admin verification in order to stop the server.",
            "post_stop_server"
        )
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="The server is stopping",
            resp="success",
            token=token,
            error=False
        )
        self.disp.log_debug("Server shutting down...", f"{title}")
        self.runtime_data_initialised.server_running = False
        self.runtime_data_initialised.continue_running = False
        self.runtime_data_initialised.server.handle_exit(signal.SIGTERM, None)
        return HCI.success(content=body, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)
