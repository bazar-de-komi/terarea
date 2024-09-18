"""_summary_
    This file is the one in charge of containing data that will change during the server runtime.
"""
from typing import Dict, Any, TYPE_CHECKING
from fastapi import FastAPI
import uvicorn
from . import constants as CONST
from ..sql.sql_manager import SQL
from ..bucket import Bucket
if TYPE_CHECKING:
    from .paths_initialised import ServerPaths
    from .endpoints_initialised import Endpoints
    from .server_management import ServerManagement
    from ..boilerplates import BoilerplateIncoming, BoilerplateNonHTTP, BoilerplateResponses


class RuntimeData:
    """_summary_
    This class is the one in charge of containing data that will change during the server runtime.
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 5000, app_name: str = "Area", error: int = 84, success: int = 0) -> None:
        self.const: CONST = CONST
        self.host: str = host
        self.port: int = port
        self.error: int = error
        self.success: int = success
        self.app_name: str = app_name
        # -------------------------- Active sessions  --------------------------
        # <token>: {
        #     "user": <user>,
        #     "email": <email>,
        #     "lifespan": <datetime>
        # }
        self.user_data: Dict[Dict[str, Any]] = {}
        # --------------------- The rest api boiling class ---------------------
        self.app: FastAPI = None
        # ------------------------ The active database  ------------------------
        self.database_link: SQL = None
        # --------------------------- Active bucket  ---------------------------
        self.bucket_link: Bucket = None
        # ----------------------- Http response building -----------------------
        if isinstance(app_name, str) is False:
            app_name = f"{app_name}"
        if isinstance(host, str) is False:
            host = f"{host}"
        if isinstance(port, str) is False:
            port = f"{port}"
        self.json_header: Dict[str, Any] = {
            CONST.JSON_HEADER_APP_NAME: app_name,
            CONST.JSON_HEADER_HOST: host,
            CONST.JSON_HEADER_PORT: port
        }
        # ---------------------     The server classes     ---------------------
        self.config: uvicorn.Config = None
        self.server: uvicorn.Server = None
        self.server_running: bool = True
        self.continue_running: bool = True
        # -------------------------- The cache thread --------------------------
        self.thread_cache_continue: bool = True
        # ------------------------- Classes reference  -------------------------
        self.server_management_initialised: 'ServerManagement' = None
        self.boilerplate_responses_initialised: 'BoilerplateResponses' = None
        self.boilerplate_incoming_initialised: 'BoilerplateIncoming' = None
        self.boilerplate_non_http_initialised: 'BoilerplateNonHTTP' = None
        self.paths_initialised: 'ServerPaths' = None
        self.endpoints_initialised: 'Endpoints' = None
