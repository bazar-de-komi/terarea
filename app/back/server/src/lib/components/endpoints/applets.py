"""
The file that contains every endpoints for applets
"""

from typing import Union, List, Dict, Any
import json
from fastapi import Response, Request
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from .. import constants as CONST
from ..runtime_data import RuntimeData
from ..http_codes import HCI

class Applets:
    """
    The class that contains every methods for applets
    """
    def __init__(self, runtime_data: RuntimeData, success: int = 0, error: int = 84, debug: bool = False) -> None:
        """
        The constructor of the Applets class
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

    # Endpoints for my applets page

    async def get_applet_by_id(self, request: Request, applet_id: str) -> Response:
        """
        Get applet by id
        """
        title = "Get applet by id"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        self.disp.log_debug(f"Token = {token}", title)
        user_id: Union[str, Response] = self.runtime_data_initialised.boilerplate_non_http_initialised.get_user_id_from_token(
            title=title,
            token=token
        )
        if isinstance(user_id, Response):
            return user_id
        applet_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTIONS,
            "*",
            [f"id='{applet_id}'", f"user_id='{user_id}'"]
        )
        if not applet_data or isinstance(applet_data, int):
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="Your applet was not found.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )
        applet_data[0]["trigger"] = json.loads(applet_data[0]["trigger"])
        applet_data[0]["consequences"] = json.loads(applet_data[0]["consequences"])
        self.disp.log_debug(f"Applet found: {applet_data}", title)
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=applet_data[0],
            resp="success",
            token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_my_applets(self, request: Request) -> Response:
        """
        Get my applets
        """
        title = "Get my applets"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        self.disp.log_debug(f"Token = {token}", title)
        user_id = self.runtime_data_initialised.boilerplate_non_http_initialised.get_user_id_from_token(
            title,
            token
        )
        if isinstance(user_id, Response):
            return user_id
        applets_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTIONS,
            "*",
            f"user_id='{user_id}'"
        )
        if not applets_data or isinstance(applets_data, int):
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="Your applets were not found.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )
        for _, applet in enumerate(applets_data):
            applet["trigger"] = json.loads(applet["trigger"])
            applet["consequences"] = json.loads(applet["consequences"])
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=applets_data,
            resp="success",
            token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_my_applets_by_tags(self, request: Request, tags: str) -> Response:
        """
        Get my applets by tags
        """
        title = "Get my applets by tags"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        self.disp.log_debug(f"Token = {token}", title)
        user_id = self.runtime_data_initialised.boilerplate_non_http_initialised.get_user_id_from_token(
            title,
            token
        )
        if isinstance(user_id, Response):
            return user_id
        if not tags or tags == "":
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title,
                token
            )
        tags_list = tags.split("+")
        applets_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTIONS,
            "*",
            f"user_id='{user_id}'"
        )
        if not applets_data or isinstance(applets_data, int):
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="Applets not found.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )
        self.disp.log_debug(f"Applet found: {applets_data}", title)
        filtered_applets: list[dict] = []
        for _, applet in enumerate(applets_data):
            for _, element in enumerate(tags_list):
                if element in applet["tags"]:
                    filtered_applets.append(applet)
        self.disp.log_debug(f"Applet found with tags: {filtered_applets}", title)
        for _, applet in enumerate(filtered_applets):
            applet["trigger"] = json.loads(applet["trigger"])
            applet["consequences"] = json.loads(applet["consequences"])
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=filtered_applets,
            resp="success",
            token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    # Endpoints for Create/Modify applets page

    async def create_applet(self, request: Request) -> Response:
        """
        Create applet
        """
        title = "Create applet"

        # Token getter
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        self.disp.log_debug(f"Token = {token}", title)

        # Request Body getter
        request_body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        if not request_body or not all(key in request_body for key in ("name", "trigger", "consequences", "tags", "description", "colour")):
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(title)
        if request_body["name"] == "" or request_body["description"] == "" or request_body["colour"] == "" or len(request_body["trigger"]) == 0 or len(request_body["consequences"]) == 0:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(title)
        self.disp.log_debug(f"Request body: {request_body}", title)

        # User id getter
        user_id: Union[str, Response] = self.runtime_data_initialised.boilerplate_non_http_initialised.get_user_id_from_token(
            title,
            token
        )
        if isinstance(user_id, Response):
            return user_id

        # Get Actions table columns names
        columns: Union[List[str], int] = self.runtime_data_initialised.database_link.get_table_column_names(
            table_name=CONST.TAB_ACTIONS
        )
        if isinstance(columns, int):
            return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(
                title=title,
                token=token
            )
        columns.pop(0)

        if (isinstance(request_body["trigger"], str) is False):
            request_body["trigger"] = json.dumps(request_body["trigger"], ensure_ascii=False)
        if (isinstance(request_body["consequences"], str) is False):
            request_body["consequences"] = json.dumps(request_body["consequences"], ensure_ascii=False)

        self.disp.log_debug(f"Before inserting in database: {request_body}", title)

        # Insert new applet into database
        status: int = self.runtime_data_initialised.database_link.insert_data_into_table(
            table=CONST.TAB_ACTIONS,
            data=[
                request_body["name"],
                request_body["trigger"],
                request_body["consequences"],
                user_id,
                request_body["tags"],
                "0",
                request_body["description"],
                request_body["colour"]
            ],
            column=columns
        )
        self.disp.log_debug(f"Insert status: {status}", title)
        if status == self.error:
            return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(
                title=title,
                token=token
            )
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="The applet was created successfully.",
            resp="success",
            token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def put_applet_by_id(self, request: Request, applet_id: str) -> Response:
        """
        Modify applet by id
        """
        title = "Put applet by id"

        # Token getter
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        self.disp.log_debug(f"Token = {token}", title)

        # Request Body getter
        request_body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        self.disp.log_debug(f"Request body: {request_body}", title)
        if not request_body or not all(key in request_body for key in ("name", "trigger", "consequences", "tags", "description", "colour")):
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(title)
        if request_body["name"] == "" or request_body["description"] == "" or request_body["colour"] == "" or len(request_body["trigger"]) == 0 or len(request_body["consequences"]) == 0:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(title)

        # User id getter
        user_id: Union[str, Response] = self.runtime_data_initialised.boilerplate_non_http_initialised.get_user_id_from_token(
            title,
            token
        )
        if isinstance(user_id, Response):
            return user_id

        # Verify if the applet is found
        applet_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTIONS,
            "*",
            [f"id='{applet_id}'", f"user_id='{user_id}'"]
        )
        if not applet_data or isinstance(applet_data, int):
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="Your applet was not found.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )

        # Get Actions table columns names
        columns: Union[List[str], int] = self.runtime_data_initialised.database_link.get_table_column_names(
            table_name=CONST.TAB_ACTIONS
        )
        if isinstance(columns, int):
            return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(
                title=title,
                token=token
            )
        columns.pop(0)

        if (isinstance(request_body["trigger"], str) is False):
            request_body["trigger"] = json.dumps(request_body["trigger"], ensure_ascii=False)
        if (isinstance(request_body["consequences"], str) is False):
            request_body["consequences"] = json.dumps(request_body["consequences"], ensure_ascii=False)

        # Update applet into database
        status: int = self.runtime_data_initialised.database_link.update_data_in_table(
            table=CONST.TAB_ACTIONS,
            data=[
                request_body["name"],
                request_body["trigger"],
                request_body["consequences"],
                user_id,
                request_body["tags"],
                "0",
                request_body["description"],
                request_body["colour"]
            ],
            column=columns,
            where=f"id='{applet_id}'"
        )
        if status == self.error:
            return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(
                title=title,
                token=token
            )
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="The applet was updated successfully.",
            resp="success",
            token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def patch_applet_by_id(self, request: Request, applet_id: str) -> Response:
        """
        Modify some applet by id
        """
        title = "Modify some applet by id"

        # Token getter
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        self.disp.log_debug(f"Token = {token}", title)

        # Request Body getter
        request_body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        self.disp.log_debug(f"Request body: {request_body}", title)

        # User id getter
        user_id: Union[str, Response] = self.runtime_data_initialised.boilerplate_non_http_initialised.get_user_id_from_token(
            title,
            token
        )
        if isinstance(user_id, Response):
            return user_id

        # Verify if the applet is found
        applet_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTIONS,
            "*",
            [f"id='{applet_id}'", f"user_id='{user_id}'"]
        )
        if not applet_data or isinstance(applet_data, int):
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="Your applet was not found.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )

        # Get Actions table columns names
        columns: Union[List[str], int] = self.runtime_data_initialised.database_link.get_table_column_names(
            table_name=CONST.TAB_ACTIONS
        )
        if isinstance(columns, int):
            return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(
                title=title,
                token=token
            )
        columns.pop(0)

        # Update applet into database
        if "name" in request_body:
            if request_body["name"] == "":
                return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(title)
            if self.runtime_data_initialised.boilerplate_non_http_initialised.update_single_data(
                CONST.TAB_ACTIONS,
                "id",
                "name",
                applet_id,
                request_body
            ) == self.error:
                return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(title, token)
        if "trigger" in request_body:
            if len(request_body["trigger"]) == 0:
                return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(title)
            if (isinstance(request_body["trigger"], str) is False):
                request_body["trigger"] = json.dumps(request_body["trigger"], ensure_ascii=False)
            if self.runtime_data_initialised.boilerplate_non_http_initialised.update_single_data(
                CONST.TAB_ACTIONS,
                "id",
                "trigger",
                applet_id,
                request_body
            ) == self.error:
                return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(title, token)
        if "consequences" in request_body:
            if len(request_body["consequences"]) == 0:
                return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(title)
            if (isinstance(request_body["consequences"], str) is False):
                request_body["consequences"] = json.dumps(request_body["consequences"], ensure_ascii=False)
            if self.runtime_data_initialised.boilerplate_non_http_initialised.update_single_data(
                CONST.TAB_ACTIONS,
                "id",
                "consequences",
                applet_id,
                request_body
            ) == self.error:
                return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(title, token)
        if "tags" in request_body:
            if self.runtime_data_initialised.boilerplate_non_http_initialised.update_single_data(
                CONST.TAB_ACTIONS,
                "id",
                "tags",
                applet_id,
                request_body
            ) == self.error:
                return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(title, token)
        if "colour" in request_body:
            if request_body["colour"] == "":
                return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(title)
            if self.runtime_data_initialised.boilerplate_non_http_initialised.update_single_data(
                CONST.TAB_ACTIONS,
                "id",
                "colour",
                applet_id,
                request_body
            ) == self.error:
                return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(title, token)
        if "description" in request_body:
            if request_body["description"] == "":
                return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(title)
            if self.runtime_data_initialised.boilerplate_non_http_initialised.update_single_data(
                CONST.TAB_ACTIONS,
                "id",
                "description",
                applet_id,
                request_body
            ) == self.error:
                return self.runtime_data_initialised.boilerplate_responses_initialised.internal_server_error(title, token)
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="The applet was updated successfully.",
            resp="success",
            token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    def _search_services(self, type_to_search: str, title: str, token: str) -> Union[List[Dict[str, Any]], Response]:
        """
        Search for the services depending on if the type is trigger or action
        """
        # Get the data of ActionTemplates table by the triggers type
        templates_data: Union[List[Dict[str, Any]], int] = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTION_TEMPLATE,
            "*",
            f"type='{type_to_search}'"
        )
        if not templates_data or isinstance(templates_data, int):
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="The actions templates were not found.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )

        # Loop inside the actions templates list
        already_retrieved_services: List[int] = []
        services: List[Dict[str, Any]] = []
        for _, template in enumerate(templates_data):
            if template["service_id"] in already_retrieved_services:
                continue
            key: str = "service_id"
            service: Union[List[Dict[str, Any]], int] = self.runtime_data_initialised.database_link.get_data_from_table(
                CONST.TAB_SERVICES,
                "*",
                f"id='{template[key]}'"
            )
            if not service or isinstance(service, int):
                continue
            services.append({
                "id": service[0]["id"],
                "name": service[0]["name"],
                "colour": service[0]["colour"],
                "description": service[0]["description"]
            })
            already_retrieved_services.append(service[0]["id"])
        return services

    async def get_triggers_services(self, request: Request) -> Response:
        """
        Get triggers services
        """
        title = "Get triggers services"

        # Token getter
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        self.disp.log_debug(f"Token = {token}", title)

        # Get triggers services
        services: Union[List[Dict[str, Any]], Response] = self._search_services("trigger", title, token)
        if (isinstance(services, Response)):
            return services

        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=services,
            resp="success",
            token=None,
            error= True
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_reactions_services(self, request: Request) -> Response:
        """
        Get reactions services
        """
        title = "Get reactions services"

        # Token getter
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        self.disp.log_debug(f"Token = {token}", title)

        # Get actions services
        services: Union[List[Dict[str, Any]], Response] = self._search_services("action", title, token)
        if (isinstance(services, Response)):
            return services

        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=services,
            resp="success",
            token=None,
            error= True
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    # def _search_templates_by_query(self, type_to_search: str, query_list: List[str], title: str, token: str) -> Union[List[Dict[str, Any]], Response]:
    #     """
    #     Search the actions templates by a query set by the user and depending on the template type
    #     """
    #     templates_data: Union[List[Dict[str, Any]], int] = self.runtime_data_initialised.database_link.get_data_from_table(
    #         CONST.TAB_ACTION_TEMPLATE,
    #         "*",
    #         f"type='{type_to_search}'"
    #     )
    #     if not templates_data or isinstance(templates_data, int):
    #         body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
    #             title=title,
    #             message="The templates were not found.",
    #             resp="not found",
    #             token=token,
    #             error=True
    #         )
    #         return HCI.not_found(
    #             content=body,
    #             content_type=CONST.CONTENT_TYPE,
    #             headers=self.runtime_data_initialised.json_header
    #         )
    #     self.disp.log_debug(f"Triggers found: {templates_data}", title)
    #     filtered_templates: List[Dict[str, Any]] = []
    #     for _, template in enumerate(templates_data):
    #         action_info: Dict[str, Any] = json.load(template["json"])
    #         self.disp.log_debug(f"Action info: {action_info}", title)
    #         for _, query in enumerate(query_list):
    #             if query in action_info["name"]:
    #                 filtered_templates.append(template)
    #                 break
    #             if query in action_info["description"]:
    #                 filtered_templates.append(template)
    #                 break
    #     self.disp.log_debug(f"Template found with query: {filtered_templates}", title)
    #     return filtered_templates

    # async def get_triggers_by_research(self, request: Request, query: str) -> Response:
    #     """
    #     Get triggers by research
    #     """
    #     title = "Get triggers by research"

    #     # Token getter
    #     token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
    #         request
    #     )
    #     if not token:
    #         return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
    #             title
    #         )
    #     if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
    #         token
    #     ) is False:
    #         return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
    #             title
    #         )
    #     self.disp.log_debug(f"Token = {token}", title)

    #     # Get the triggers by the research query
    #     query_list: List[str] = query.split("+")
    #     triggers_data: Union[List[Dict[str, Any]], Response] = self._search_templates_by_query("trigger", query_list, title, token)
    #     if isinstance(triggers_data, Response):
    #         return triggers_data

    #     for _, trigger in enumerate(triggers_data):
    #         trigger["json"] = json.load(trigger["json"])
    #     body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
    #         title=title,
    #         message=triggers_data,
    #         resp="success",
    #         token=token
    #     )
    #     return HCI.success(
    #         content=body,
    #         content_type=CONST.CONTENT_TYPE,
    #         headers=self.runtime_data_initialised.json_header
    #     )

    # async def get_reactions_by_research(self, request: Request, query: str) -> Response:
    #     """
    #     Get reactions by research
    #     """
    #     title = "Get reactions by research"

    #     # Token getter
    #     token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
    #         request
    #     )
    #     if not token:
    #         return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
    #             title
    #         )
    #     if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
    #         token
    #     ) is False:
    #         return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
    #             title
    #         )
    #     self.disp.log_debug(f"Token = {token}", title)

    #     # Get the reactions by the research query
    #     query_list: List[str] = query.split("+")
    #     reactions_data: Union[List[Dict[str, Any]], Response] = self._search_templates_by_query("action", query_list, title, token)
    #     if isinstance(reactions_data, Response):
    #         return reactions_data

    #     for _, reaction in enumerate(reactions_data):
    #         reaction["json"] = json.load(reaction["json"])
    #     body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
    #         title=title,
    #         message=reactions_data,
    #         resp="success",
    #         token=token
    #     )
    #     return HCI.success(
    #         content=body,
    #         content_type=CONST.CONTENT_TYPE,
    #         headers=self.runtime_data_initialised.json_header
    #     )

    async def get_triggers(self, request: Request) -> Response:
        """
        Get triggers by research
        """
        title = "Get triggers by research"

        # Token getter
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        self.disp.log_debug(f"Token = {token}", title)

        # Get the triggers
        templates_data: Union[List[Dict[str, Any]], int] = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTION_TEMPLATE,
            "*",
            "type='trigger'"
        )
        if not templates_data or isinstance(templates_data, int):
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="The templates were not found.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )

        for _, template in enumerate(templates_data):
            template["json"] = json.loads(template["json"])
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=templates_data,
            resp="success",
            token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_reactions(self, request: Request) -> Response:
        """
        Get triggers by research
        """
        title = "Get triggers by research"

        # Token getter
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        self.disp.log_debug(f"Token = {token}", title)

        # Get the reactions
        templates_data: Union[List[Dict[str, Any]], int] = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTION_TEMPLATE,
            "*",
            "type='action'"
        )
        if not templates_data or isinstance(templates_data, int):
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="The templates were not found.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )

        for _, template in enumerate(templates_data):
            template["json"] = json.loads(template["json"])
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=templates_data,
            resp="success",
            token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_triggers_by_service_id(self, request: Request, service_id: str) -> Response:
        """
        Get triggers by service name
        """
        title = "Get triggers by service name"

        # Token getter
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        self.disp.log_debug(f"Token = {token}", title)

        # Get the triggers list by service id from the ActionTemplate table
        triggers_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTION_TEMPLATE,
            "*",
            ["type='trigger'", f"service_id='{service_id}'"]
        )
        if not triggers_data or isinstance(triggers_data, int):
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="The triggers were not found.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )

        for _, trigger in enumerate(triggers_data):
            trigger["json"] = json.loads(trigger["json"])
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=triggers_data,
            resp="success",
            token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_reactions_by_service_id(self, request: Request, service_id: str) -> Response:
        """
        Get reactions by service name
        """
        title = "Get reactions by service name"

        # Token getter
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        self.disp.log_debug(f"Token = {token}", title)

        # Get the reactions list by service id from the ActionTemplate table
        reactions_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTION_TEMPLATE,
            "*",
            ["type='action'", f"service_id='{service_id}'"]
        )
        if not reactions_data or isinstance(reactions_data, int):
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="The reactions were not found.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )
        for _, reaction in enumerate(reactions_data):
            reaction["json"] = json.loads(reaction["json"])
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=reactions_data,
            resp="success",
            token=token
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def delete_my_applet_by_id(self, request: Request, applet_id: str) -> Response:
        """
        Get reactions by service name
        """
        title = "Delete service by id"

        # Token getter
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if not token:
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title
            )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
            token
        ) is False:
            return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
                title
            )
        self.disp.log_debug(f"Token = {token}", title)

        # User id getter
        user_id: Union[str, Response] = self.runtime_data_initialised.boilerplate_non_http_initialised.get_user_id_from_token(
            title,
            token
        )
        if isinstance(user_id, Response):
            return user_id

        # Verify if the applet exist or if the user has the right to delete it
        applet_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTIONS,
            "*",
            [f"id='{applet_id}'", f"user_id='{user_id}'"]
        )
        if not applet_data or isinstance(applet_data, int):
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="Your applet was not found or it's not your applet.",
                resp="not found",
                token=token,
                error=True
            )
            return HCI.not_found(
                content=body,
                content_type=CONST.CONTENT_TYPE,
                headers=self.runtime_data_initialised.json_header
            )
        self.disp.log_debug(f"Applet found: {applet_data}", title)
        self.runtime_data_initialised.database_link.remove_data_from_table(
            table=CONST.TAB_ACTIONS,
            where=f"id='{applet_id}'"
        )
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="Your applet has been deleted successfully.",
            resp="success",
            token=None,
        )
        return HCI.success(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )
