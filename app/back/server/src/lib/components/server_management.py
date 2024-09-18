"""_summary_
    This is the file in charge of containing the functions that will manage the server run status.
"""

import signal
import uvicorn
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from . import CONST
from .http_codes import HCI
from .runtime_data import RuntimeData


class ServerManagement:
    """_summary_
    """

    def __init__(self, runtime_data: RuntimeData, error: int = 84, success: int = 0, debug: bool = False) -> None:
        """_summary_
        """
        # -------------------------- Inherited values --------------------------
        self.rdi: RuntimeData = runtime_data
        self.error: int = error
        self.success: int = success
        self.debug: bool = debug
        # ------------------------ The logging function ------------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            FILE_DESCRIPTOR,
            SAVE_TO_FILE,
            FILE_NAME,
            debug=self.debug,
            logger=self.__class__.__name__
        )

    def __del__(self) -> None:
        """_summary_
            The destructor of the class
        """
        if self.is_server_alive() is True:
            del self.rdi.database_link
            del self.rdi.bucket_link
            self.rdi.continue_running = False
            if self.rdi.server is not None:
                self.rdi.server.handle_exit(signal.SIGTERM, None)

    def is_server_alive(self) -> bool:
        """
            Check if the server is still running.
        Returns:
            bool: Returns True if it is running.
        """
        return self.rdi.continue_running

    def is_server_running(self) -> bool:
        """
            Check if the server is still running.
        Returns:
            bool: Returns True if it is running.
        """
        return self.is_server_alive()

    async def shutdown(self) -> Response:
        """
            The function to shutdown the server
        Returns:
            Response: Return the shutdown server message
        """
        if self.rdi.database_link.is_connected() is True:
            self.rdi.database_link.disconnect_db()
        if self.rdi.bucket_link.is_connected() is True:
            self.rdi.bucket_link.disconnect()
        self.rdi.continue_running = False
        self.rdi.server.handle_exit(signal.SIGTERM, None)
        body = self.rdi.bri.build_response_body(
            title="Shutdown",
            message="The server is shutting down.",
            resp="Shutdown",
            token="",
            error=False
        )
        return HCI.success(body, content_type=CONST.CONTENT_TYPE, headers=self.rdi.json_header)

    # -------------------Initialisation-----------------------

    def initialise_classes(self) -> None:
        """
            The function to initialise the server classes
        """

        self.rdi.app = FastAPI()
        self.rdi.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.rdi.config = uvicorn.Config(
            self.rdi.app,
            host=self.rdi.host,
            port=self.rdi.port
        )
        self.rdi.server = uvicorn.Server(self.rdi.config)
        self.rdi.continue_running = True
