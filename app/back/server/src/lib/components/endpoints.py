"""_summary_
    This is the file in charge of storing the endpoints_initialised ready to be imported into the server class.
"""
import signal
from fastapi import Response, Request
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from . import constants as CONST
from .runtime_data import RuntimeData
from .http_codes import HCI
from .password_handling import PasswordHandling


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
        self.password_handling_initialised: PasswordHandling = PasswordHandling(
            self.error,
            self.success,
            self.debug
        )
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
            f"header = {self.runtime_data_initialised.json_header}",
            "get_welcome"
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
        title = "Login"
        request_body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        self.disp.log_debug(f"Request body: {request_body}", title)
        email = request_body["email"]
        password = request_body["password"]
        table = "Users"
        user_info = self.runtime_data_initialised.database_link.get_data_from_table(table, "*", f"email='{email}'")
        self.disp.log_debug(f"Retrived data: {user_info}", title)
        if isinstance(user_info, int):
            return HCI.unauthorized({"error": "Access denied."})
        if self.password_handling_initialised.check_password(password, user_info[0]["password"]) is False:
            return HCI.unauthorized({"error": "Access denied."})
        data = self.runtime_data_initialised.boilerplate_incoming_initialised.log_user_in(email)
        if data["status"] == self.error:
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="Login failed.",
                resp="error",
                token=data["token"],
                error=True
            )
            return HCI.forbidden(content=body, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)
        name = user_info[0]["username"]
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=f"Welcome {name}",
            resp="success",
            token=data["token"],
            error=False
        )
        body["token"] = data["token"]
        return HCI.success(content=body, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)

    async def put_register(self, request: Request) -> Response:
        """_summary_

        Args:
            request (Request): _description_

        Returns:
            Response: _description_
        """
        title = "Register"
        body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        self.disp.log_debug(f"Register body: {body}", title)
        email: str = body["email"]
        password = body["password"]
        table = "Users"
        user_info = self.runtime_data_initialised.database_link.get_data_from_table(table, "*", f"email='{email}'")
        if isinstance(user_info, int) is False:
            return HCI.conflict({"error": "Email already exist."})
        hashed_password = self.password_handling_initialised.hash_password(password)
        username = email.split('@')[0]
        self.disp.log_debug(f"Username = {username}", title)
        data = [username, email, hashed_password, "local"]
        self.disp.log_debug(f"Data list = {data}", title)
        column = self.runtime_data_initialised.database_link.get_table_column_names(table)
        self.disp.log_debug(f"Column = {column}", title)
        if isinstance(column, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        column.pop(0)
        self.disp.log_debug(f"Column after id pop = {column}", title)
        if self.runtime_data_initialised.database_link.insert_data_into_table(table, data, column) == self.error:
            return HCI.internal_server_error({"error": "Internal server error."})
        return HCI.success({"msg": "Account created successfully."})

    def get_s3_bucket_names(self, request: Request) -> Response:
        """
            The endpoint to get every bucket data
        """
        title = "get_s3_bucket"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(request)
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
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(request)
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
