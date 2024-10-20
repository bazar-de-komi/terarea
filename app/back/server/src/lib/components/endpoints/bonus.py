"""_summary_
"""

import signal
from fastapi import Response, Request
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from .. import constants as CONST
from ..runtime_data import RuntimeData
from ..http_codes import HCI


class Bonus:
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

    def my_test_component(self) -> Response:
        """_summary_
        This is a test component that will return a response with the message "Hello World".
        Returns:
            Response: _description_
        """
        return HCI.success({"msg": "Hello World"})

    def get_welcome(self, request: Request) -> Response:
        """_summary_
            The endpoint corresponding to '/'.

        Returns:
            Response: _description_: The data to send back to the user as a response.
        """
        title = "get_welcome"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request)
        self.disp.log_debug(f'(get_welcome) token = {token}', title)
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title="Home",
            message="Welcome to the control server.",
            resp="",
            token=token,
            error=False
        )
        self.disp.log_debug(f"sent body : {body}", title)
        self.disp.log_debug(
            f"header = {self.runtime_data_initialised.json_header}", title
        )
        outgoing = HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )
        self.disp.log_debug(f"ready_to_go: {outgoing}", title)
        return outgoing

    def get_s3_bucket_names(self, request: Request) -> Response:
        """
            The endpoint to get every bucket data
        """
        title = "get_s3_bucket"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request)
        self.disp.log_debug(f"Token = {token}", title)
        if token is None:
            return HCI.unauthorized({"error": "Authorisation required."})
        bucket_names = self.runtime_data_initialised.bucket_link.get_bucket_names()
        self.disp.log_debug(f"Bucket names: {bucket_names}", title)
        if isinstance(bucket_names, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        return HCI.success({"msg": bucket_names})

    def get_table(self, request: Request) -> Response:
        """
            table
        """
        title = "get_table"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request)
        self.disp.log_debug(f"Token = {token}", title)
        if token is None:
            return HCI.unauthorized({"error": "Authorisation required."})
        table = self.runtime_data_initialised.database_link.get_table_names()
        self.disp.log_debug(f"received in {title}", table)
        return HCI.success({"msg": table})

    async def post_stop_server(self, request: Request) -> Response:
        """_summary_
            The endpoint allowing a user to stop the server.

        Returns:
            Response: _description_: The data to send back to the user as a response.
        """
        title = "Stop server"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_admin(token) is False:
            self.disp.log_error(
                "Non-admin user tried to stop the server.", title
            )
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="You do not have enough privileges to run this endpoint.",
                resp="privilege to low",
                token=token,
                error=True
            )
            return HCI.unauthorized(content=body, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)
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
        status = self.runtime_data_initialised.background_tasks_initialised.safe_stop()
        if status != self.success:
            msg = "The server is stopping with errors, cron exited "
            msg += f"with {status}."
            self.disp.log_error(
                msg,
                "post_stop_server"
            )
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message=msg,
                resp="error",
                token=token,
                error=True
            )
            del self.runtime_data_initialised.background_tasks_initialised
            self.runtime_data_initialised.background_tasks_initialised = None
            return HCI.internal_server_error(content=body, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)
        return HCI.success(content=body, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)
