"""_summary_
    File containing boilerplate functions that could be used by the server in it's endpoints_initialised for checking incoming data.
"""

from fastapi import Response, Request
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from .. import constants as CONST
from ..runtime_data import RuntimeData
from ..http_codes import HCI


class Services:
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

    def get_services(self, request: Request) -> Response:
        """_summary_

        Args:
            request (Request): _description_

        Returns:
            Response: _description_
        """
        title = "get_services"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request)
        self.disp.log_debug(f"Token = {token}", title)
        if token is None:
            return HCI.unauthorized({"error": "Authorisation required."})

        services_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_SERVICES)
        if services_data is None:
            return HCI.not_found({"error": "Services not found."}, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)
        self.disp.log_debug(f"received in {title}", services_data)
        return HCI.success({"msg": services_data})

    def get_service(self, name, request: Request) -> Response:
        """_summary_

        Args:
            name (_type_): _description_
            request (Request): _description_

        Returns:
            Response: _description_
        """
        title = "get_service"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request)
        self.disp.log_debug(f"Token = {token}", title)
        if token is None:
            return HCI.unauthorized({"error": "Authorization required."}, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)

        service_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_SERVICES)
        service = next(
            (srv for srv in service_data if srv["name"] == name), None)
        if service is None:
            return HCI.not_found({"error": f"Service '{name}' not found."}, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)
        self.disp.log_debug(f"Service found: {service}", title)
        return HCI.success({"msg": service})

    def get_services_by_tag(self, tag, request: Request) -> Response:
        """_summary_

        Args:
            tag (_type_): _description_
            request (Request): _description_

        Returns:
            Response: _description_
        """
        title = "get_services_by_tag"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request)
        self.disp.log_debug(f"Token = {token}", title)
        if token is None:
            return HCI.unauthorized({"error": "Authorization required."})

        service_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_SERVICES)
        filtered_services = [
            srv for srv in service_data if tag in srv.get("tags", [])]
        if not filtered_services:
            return HCI.not_found({"error": f"No services found for tag '{tag}'."}, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)
        msg = f"Services with tag '{tag}': "
        msg += f"{filtered_services}"
        self.disp.log_debug(msg, title)
        return HCI.success({"msg": filtered_services})

    def get_recent_services(self, request: Request) -> Response:
        """_summary_

        Args:
            request (Request): _description_

        Returns:
            Response: _description_
        """
        title = "get_recent_services"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request)
        self.disp.log_debug(f"Token = {token}", title)
        if token is None:
            return HCI.unauthorized({"error": "Authorization required."})

        service_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_SERVICES)
        recent_services = sorted(
            service_data, key=lambda x: x["created_at"], reverse=True)[:10]
        if not recent_services:
            return HCI.not_found({"error": "No recent services found."}, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)
        self.disp.log_debug(f"Recent services: {recent_services}", title)
        return HCI.success({"msg": recent_services})
