"""
The file that contains every endpoints for applets
"""

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

    async def get_applet_by_id(self, request: Request, applet_id: int) -> Response:
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
        id_str = str(id)
        applet_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTIONS,
            "*",
            f"id='{id_str}'"
        )
        if not applet_data or isinstance(applet_data, int):
            body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                title=title,
                message="Applet not found.",
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
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=applet_data,
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
            CONST.TAB_USER_SERVICES,
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
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message=applets_data,
            resp="success",
            token=token
        )
        return HCI.not_implemented(
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
        if not tags or tags == "":
            return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
                title,
                token
            )
        tags_list = tags.split(":")
        applets_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTIONS,
            "*"
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
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="Not implemented yet",
            resp="not implemented",
            token=None,
            error= True
        )
        return HCI.not_implemented(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def put_applet_by_id(self, request: Request, applet_id: str) -> Response:
        """
        Modify applet by id
        """
        title = "Put applet by id"
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="Not implemented yet",
            resp="not implemented",
            token=None,
            error= True
        )
        return HCI.not_implemented(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def patch_applet_by_id(self, request: Request, applet_id: str) -> Response:
        """
        Modify some applet by id
        """
        title = "Patch applet by id"
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="Not implemented yet",
            resp="not implemented",
            token=None,
            error= True
        )
        return HCI.not_implemented(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_triggers_services(self, request: Request) -> Response:
        """
        Get triggers services
        """
        title = "Get triggers services"
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="Not implemented yet",
            resp="not implemented",
            token=None,
            error= True
        )
        return HCI.not_implemented(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_triggers_by_research(self, request: Request, query: str) -> Response:
        """
        Get triggers by research
        """
        title = "Get triggers by research"
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="Not implemented yet",
            resp="not implemented",
            token=None,
            error= True
        )
        return HCI.not_implemented(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_reactions_by_research(self, request: Request, query: str) -> Response:
        """
        Get reactions by research
        """
        title = "Get reactions by research"
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="Not implemented yet",
            resp="not implemented",
            token=None,
            error= True
        )
        return HCI.not_implemented(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_reactions_services(self, request: Request) -> Response:
        """
        Get reactions services
        """
        title = "Get reactions services"
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="Not implemented yet",
            resp="not implemented",
            token=None,
            error= True
        )
        return HCI.not_implemented(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_triggers_by_service_id(self, request: Request, service_id: str) -> Response:
        """
        Get triggers by service name
        """
        title = "Get triggers by service name"
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title="create_applet",
            message="Not implemented yet",
            resp="not implemented",
            token=None,
            error= True
        )
        return HCI.not_implemented(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def get_reactions_by_service_id(self, request: Request, service_id: str) -> Response:
        """
        Get reactions by service name
        """
        title = "Get reactions by service name"
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title="create_applet",
            message="Not implemented yet",
            resp="not implemented",
            token=None,
            error= True
        )
        return HCI.not_implemented(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )

    async def delete_my_applet_by_id(self, request: Request, applet_id: str) -> Response:
        """
        Get reactions by service name
        """
        title = "Delete service by id"
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title="create_applet",
            message="Not implemented yet",
            resp="not implemented",
            token=None,
            error= True
        )
        return HCI.not_implemented(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )
