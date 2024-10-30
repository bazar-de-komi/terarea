"""_summary_
    The file that contains mandatory endpoints
"""


import time
from fastapi import Response, Request
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from .. import constants as CONST
from ..runtime_data import RuntimeData
from ..http_codes import HCI


class Mandatory:
    """
        The class that contains mandatory endpoints
    """

    def __init__(self, runtime_data: RuntimeData, success: int = 0, error: int = 84, debug: bool = False) -> None:
        """_summary_
            The class in charge of the mandatory endpoints

        Args:
            runtime_data (RuntimeData): _description_
            success (int, optional): _description_. Defaults to 0.
            error (int, optional): _description_. Defaults to 84.
            debug (bool, optional): _description_. Defaults to False.
        """
        # ------------------------ Inherited variables  ------------------------
        self.debug: bool = debug
        self.success: int = success
        self.error: int = error
        self.runtime_data_initialised: RuntimeData = runtime_data
        # ------------------------- The visual logger  -------------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            SAVE_TO_FILE,
            FILE_NAME,
            FILE_DESCRIPTOR,
            debug=self.debug,
            logger=self.__class__.__name__
        )

    def get_about(self, request: Request) -> Response:
        """_summary_
            The endpoint corresponding to '/about'.

        Returns:
            Response: _description_: The data to send back to the user as a response.
        """
        title = "get_about"
        host = request.client.host
        current_time = int(time.time())
        json_body = {
            " client ": {
                " host ": host
            },
            " server ": {
                " current_time ": current_time,
                " services ": self.runtime_data_initialised.boilerplate_non_http_initialised.get__services()
                # [
                #     {
                #         " name ": " facebook ",
                #         " actions ": [
                #             {
                #                 " name ": " new_message_in_group ",
                #                 " description ": " A new message is posted in the group "
                #             }, {
                #                 " name ": " new_message_inbox ",
                #                 " description ": " A new private message is received by the user "
                #             }, {
                #                 " name ": " new_like ",
                #                 " description ": " The user gains a like from one of their messages "
                #             }
                #         ],
                #         " reactions ": [
                #             {
                #                 " name ": " like_message ",
                #                 " description ": " The user likes a message "
                #             }
                #         ]
                #     }
                # ]
            }
        }
        outgoing = HCI.success(
            json_body,
            headers=self.runtime_data_initialised.json_header
        )
        return outgoing
