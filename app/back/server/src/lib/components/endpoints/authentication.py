"""_summary_
"""

import random
from fastapi import Response, Request
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from .. import constants as CONST
from ..runtime_data import RuntimeData
from ..http_codes import HCI
from ..password_handling import PasswordHandling
from ..mail_management import MailManagement


class Authentication:
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
        self.mail_management_initialised: MailManagement = MailManagement(
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
        self.code_for_forgot_password: list[dict] = []

    async def post_login(self, request: Request) -> Response:
        """_summary_
            The endpoint allowing a user to log into the server.

        Returns:
            Response: _description_: The data to send back to the user as a response.
        """
        title = "Login"
        request_body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        self.disp.log_debug(f"Request body: {request_body}", title)
        if not request_body or not all(key in request_body for key in ("email", "password")):
            return HCI.bad_request({"error": "Bad request."})
        email = request_body["email"]
        password = request_body["password"]
        table = "Users"
        user_info = self.runtime_data_initialised.database_link.get_data_from_table(
            table, "*", f"email='{email}'")
        self.disp.log_debug(f"Retrived data: {user_info}", title)
        if isinstance(user_info, int):
            return HCI.unauthorized({"error": "Access denied."})
        if self.password_handling_initialised.check_password(password, user_info[0]["password"]) is False:
            return HCI.unauthorized({"error": "Access denied."})
        data = self.runtime_data_initialised.boilerplate_incoming_initialised.log_user_in(
            email
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
        request_body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        self.disp.log_debug(f"Request body: {request_body}", title)
        if not request_body or not all(key in request_body for key in ("email", "password")):
            return HCI.bad_request({"error": "Bad request."})
        email: str = request_body["email"]
        password = request_body["password"]
        table = "Users"
        user_info = self.runtime_data_initialised.database_link.get_data_from_table(
            table, "*", f"email='{email}'")
        if isinstance(user_info, int) is False:
            return HCI.conflict({"error": "Email already exist."})
        hashed_password = self.password_handling_initialised.hash_password(
            password)
        username = email.split('@')[0]
        self.disp.log_debug(f"Username = {username}", title)
        admin = str(int(False))
        favicon = "NULL"
        data = [username, email, hashed_password, "local", favicon, admin]
        self.disp.log_debug(f"Data list = {data}", title)
        column = self.runtime_data_initialised.database_link.get_table_column_names(
            table
        )
        self.disp.log_debug(f"Column = {column}", title)
        if isinstance(column, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        column.pop(0)
        self.disp.log_debug(f"Column after id pop = {column}", title)
        if self.runtime_data_initialised.database_link.insert_data_into_table(table, data, column) == self.error:
            return HCI.internal_server_error({"error": "Internal server error."})
        return HCI.success({"msg": "Account created successfully."})

    async def post_email_reset_password(self, request: Request) -> Response:
        """_summary_
        """
        title = "Email reset password"
        request_body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        self.disp.log_debug(f"Request body: {request_body}", title)
        if not request_body or ("email") not in request_body:
            return HCI.bad_request({"error": "Bad request."})
        email: str = request_body["email"]
        table = "Users"
        data = self.runtime_data_initialised.database_link.get_data_from_table(
            table, "email", f"email='{email}'")
        if data == self.error:
            return HCI.bad_request({"error": "Bad request."})
        email_subject = "[AREA] Verification code"
        code = random.randint(100000, 999999)
        code_str = str(code)
        new_node = {}
        new_node['email'] = email
        new_node['code'] = code_str
        self.code_for_forgot_password.append(new_node)
        body = "The code is "
        body += code_str
        status = self.mail_management_initialised.send_email(
            email, email_subject, body)
        if status == self.error:
            return HCI.internal_server_error({"error": "Internal server error."})
        return HCI.success({"msg": "Email send successfully."})

    async def put_reset_password(self, request: Request) -> Response:
        """_summary_
        """
        title = "Reset password"
        request_body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        self.disp.log_debug(f"Request body: {request_body}", title)
        if not request_body or not all(key in request_body for key in ("email", "code", "password")):
            return HCI.bad_request({"error": "Bad request."})
        body_email: str = request_body["email"]
        body_code: str = request_body["code"]
        body_password: str = request_body["password"]
        verified_user: dict = {}
        for user in self.code_for_forgot_password:
            if user.get("email") == body_email and user.get("code") == body_code:
                verified_user = user
        if not verified_user:
            return HCI.bad_request({"error": "Invalid verification code."})
        table = "Users"
        data: list = []
        column: list = []
        hashed_password = self.password_handling_initialised.hash_password(
            body_password)
        data.append(hashed_password)
        column.append("password")
        status = self.runtime_data_initialised.database_link.update_data_in_table(
            table, data, column, f"email='{body_email}'")
        if status == self.error:
            return HCI.internal_server_error({"error": "Internal server error."})
        for user in self.code_for_forgot_password:
            if user.get("email") == body_email and user.get("code") == body_code:
                self.code_for_forgot_password.remove(user)
                break
        return HCI.success({"msg": "Password changed successfully."})
