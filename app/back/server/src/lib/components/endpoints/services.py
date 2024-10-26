"""
This file contains every method about services
"""

from fastapi import Response, Request
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from .. import constants as CONST
from ..runtime_data import RuntimeData
from ..http_codes import HCI


class Services:
    """
    The class that contains every method about services
    """

    def __init__(self, runtime_data: RuntimeData, success: int = 0, error: int = 84, debug: bool = False) -> None:
        """_summary_
        The constructor of the services class
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

    async def get_services(self, request: Request) -> Response:
        """
        The method to get every services contained in the db
        """
        title = "get_services"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        self.disp.log_debug(f"Token = {token}", title)
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.unauthorized(
                title,
                token
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        services_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_SERVICES,
            "*"
        )
        if not services_data or isinstance(services_data, int):
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="services not found.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )
        self.disp.log_debug(f"Retrieved data {services_data}", title)
        for i, service in enumerate(services_data):
            services_data[i]["created_at"] = self.runtime_data_initialised.database_link.datetime_to_string(service["created_at"])
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message=services_data,
                resp="success",
                token=token
            )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_service(self, request: Request, name: str) -> Response:
        """
        The method to get a service by his name
        """
        title = "get_service"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        self.disp.log_debug(f"Token = {token}", title)
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.unauthorized(
                title,
                token
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        service_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_SERVICES,
            "*",
            f"name='{name}'"
        )
        if isinstance(service_data, int):
            return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(
                title,
                token
            )
        for i, service in enumerate(service_data):
            service_data[i]["created_at"] = self.runtime_data_initialised.database_link.datetime_to_string(service["created_at"])
        self.disp.log_debug(f"Service found: {service_data}", title)
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message=service_data,
                resp="success",
                token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_services_by_tag(self, tag, request: Request) -> Response:
        """
        The function to get and filter every services by specifics tag
        """
        title = "get_services_by_tag"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        self.disp.log_debug(f"Token = {token}", title)
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.unauthorized(
                title,
                token
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        service_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_SERVICES,
            "*"
        )
        filtered_services = [
            srv for srv in service_data if tag in srv.get("tags", [])
        ]
        if not filtered_services:
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message=f"No services found for tag '{tag}'.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )
        for i, service in enumerate(filtered_services):
            filtered_services[i]["created_at"] = self.runtime_data_initialised.database_link.datetime_to_string(service["created_at"])
        msg = f"Services with tag '{tag}': "
        msg += f"{filtered_services}"
        self.disp.log_debug(msg, title)
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=filtered_services,
            resp="success",
            token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_recent_services(self, request: Request) -> Response:
        """
        The function to get and filter every services by the most recent to the oldest
        """
        title = "get_recent_services"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        self.disp.log_debug(f"Token = {token}", title)
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.unauthorized(
                title,
                token
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        service_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_SERVICES,
            "*"
        )
        recent_services = sorted(
            service_data, key=lambda x: x["created_at"], reverse=True
        )[:10]
        if not recent_services:
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="No recent services found.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )
        for i, service in enumerate(recent_services):
            recent_services[i]["created_at"] = self.runtime_data_initialised.database_link.datetime_to_string(service["created_at"])
        self.disp.log_debug(f"Recent services: {recent_services}", title)
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=recent_services,
            resp="success",
            token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def create_service(self, request: Request, name: str) -> Response:
        """
        Create a new service (Only for admin account)
        """
        title: str = "create_service"
        token: str = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.unauthorized(
                title,
                token
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_admin(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.unauthorized(title, token)
        if not name:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title,
                token
            )
        self.disp.log_debug(f"Service name: {name}", title)
        user_id = self.runtime_data_initialised.boilerplate_non_http_initialised.get_user_id_from_token(
            title, token
        )
        if isinstance(user_id, Response):
            return user_id
        user_profile = self.runtime_data_initialised.database_link.get_data_from_table(
            table=CONST.TAB_ACCOUNTS,
            column="*",
            where=f"id='{user_id}'",
        )
        self.disp.log_debug(f"User profile: {user_profile}", title)
        if isinstance(self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_SERVICES,
            "*",
            f"name='{name}'"), int) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(
                title,
                token
            )
        request_body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        if not request_body or not all(key in request_body for key in ("url", "api_key", "category", "type", "tags")):
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title,
                token
            )
        self.disp.log_debug(f"Request body: {request_body}", title)
        data: list = [
            name,
            request_body["url"],
            request_body["api_key"],
            request_body["category"],
            str(0),
            request_body["type"],
            request_body["tags"],
            "NOW()",
            str(int(False))
        ]
        self.disp.log_debug(f"Generated data: {data}", title)
        columns = self.runtime_data_initialised.database_link.get_table_column_names(CONST.TAB_SERVICES)
        if isinstance(columns, int):
            return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(
                title,
                token
            )
        columns.pop(0)
        self.disp.log_debug(f"Columns: {columns}", title)
        if self.runtime_data_initialised.database_link.insert_data_into_table(CONST.TAB_SERVICES, data, columns) == self.error:
            return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(
                title,
                token
            )
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="The new service is created successfully.",
            resp="success",
            token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )
