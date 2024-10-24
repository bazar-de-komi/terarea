#!/usr/bin/env python3
"""_summary_
    This file contains functions for the applet endpoint
"""

from fastapi import FastAPI, Request, Response
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from .. import constants as CONST
from ..runtime_data import RuntimeData
from ..http_codes import HCI

class Applets:
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

    def get_applet_name(self, request: Request) -> Response:
        """
        The method to get every applets contained in the db
        """
        title = "get_applets"
        token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request)
        self.disp.log_debug(f"Token = {token}", title)
        if token is None:
            return HCI.unauthorized({"error": "Authorisation required."})

        applets_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACTIONS,
            "*"
        )
        if applets_data is None or isinstance(applets_data, int):
            return HCI.not_found({"error": "Services not found."}, content_type=CONST.CONTENT_TYPE, headers=self.runtime_data_initialised.json_header)
        self.disp.log_debug(f"received in {title}", applets_data)
        return HCI.success({"services": applets_data})
