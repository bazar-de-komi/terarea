"""_summary_
    File containing boilerplate functions that could be used by the server in it's endpoints_initialised for checking incoming data.
"""

from fastapi import FastAPI, Response, Request
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from ..runtime_data import RuntimeData
from ..http_codes import HCI

app = FastAPI()

class Services:
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
        self.services = []

    @app.get("get_services")
    async def get_services(self, request: Request) -> Response:
        title = "get_services"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request)
        self.disp.log_debug(f"Token = {token}", title)
        if token is None:
            return HCI.unauthorized({"error": "Authorisation required."})
        table = self.runtime_data_initialised.database_link.get_data_from_table()
        self.disp.log_debug(f"received in {title}", table["Services"])
        self.services = table["Services"]
        return HCI.success({"msg": table["Services"]})

    @app.get("get_service/{name}")
    async def get_service(self, name):
        return

    @app.get("get_services_by_tag/{tag}")
    async def get_services_by_tag(self, tag):
        return

    @app.get("get_recent_services")
    async def get_recent_services(self):
        return
