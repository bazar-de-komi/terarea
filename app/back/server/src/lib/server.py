##
# EPITECH PROJECT, 2023
# Desktop_pet
# File description:
# pet_server.py
##
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from .sql import SQL
from .bucket import Bucket
from .components import Endpoints, ServerPaths, RuntimeData, ServerManagement, CONST
from .boilerplates import BoilerplateIncoming, BoilerplateNonHTTP, BoilerplateResponses


class Server:
    """_summary_
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 5000, success: int = 0, error: int = 84, app_name: str = "Area", debug: bool = False) -> None:
        """_summary_
            This is the class Server, a class that contains the structures used to allow the uvicorn and fastapi combo to run successfully.
        Args:
            host (str, optional): _description_. Defaults to "0.0.0.0".
            port (int, optional): _description_. Defaults to 5000.
            character_folder (str, optional): _description_. Defaults to "".
            usr_db_path (str, optional): _description_. Defaults to "".
            success (int, optional): _description_. Defaults to 0.
            error (int, optional): _description_. Defaults to 84.
            app_name (str, optional): _description_. Defaults to "Desktop Pets".
            debug (bool, optional): _description_. Defaults to False.
        """
        # ---------------------   The inherited arguments  ---------------------
        self.host: str = host
        self.port: int = port
        self.success: int = success
        self.error: int = error
        self.debug: bool = debug
        self.continue_running: bool = False
        # ------------------------ The logging function ------------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            FILE_DESCRIPTOR,
            SAVE_TO_FILE,
            FILE_NAME,
            debug=self.debug,
            logger=self.__class__.__name__
        )
        # ------------------------ Shared Runtime data  ------------------------
        self.rdi: RuntimeData = RuntimeData(
            host=self.host,
            port=self.port,
            app_name=app_name
        )
        # ----- The classes that need to be tracked for the server to run  -----
        self.rdi.smi = ServerManagement(
            self.rdi,
            error=self.error,
            success=self.success,
            debug=self.debug
        )
        self.rdi.bri = BoilerplateResponses(
            self.rdi,
            debug=self.debug
        )
        self.rdi.bii = BoilerplateIncoming(
            self.rdi,
            error=self.error,
            success=self.success,
            debug=self.debug
        )
        self.rdi.bnhttpi = BoilerplateNonHTTP(
            self.rdi,
            error=self.error,
            success=self.success,
            debug=self.debug
        )
        self.rdi.paths = ServerPaths(
            self.rdi,
            error=self.error,
            success=self.success,
            debug=self.debug
        )
        self.rdi.database_link = SQL(
            url=CONST.DB_HOST,
            port=CONST.DB_PORT,
            username=CONST.DB_USER,
            password=CONST.DB_PASSWORD,
            db_name=CONST.DB_DATABASE,
            debug=self.debug
        )
        self.rdi.bucket_link = Bucket(
            error=self.error,
            success=self.success
        )
        self.rdi.endpoints = Endpoints(
            self.rdi,
            error=self.error,
            success=self.success,
            debug=self.debug
        )

    def main(self) -> int:
        """_summary_
            The main function of the server.
            This is the one in charge of starting the server.

        Returns:
            int: _description_
        """
        self.rdi.smi.initialise_classes()
        self.rdi.paths.load_default_paths()
        self.rdi.paths.inject_routes()
        try:
            self.rdi.server.run()
        except Exception as e:
            self.disp.log_error(f"Error: {e}", "main")
            return self.error
        return self.success

    def is_running(self) -> bool:
        """_summary_
            The function in charge of checking if the server is running.

        Returns:
            bool: _description_: Returns True if the server is running.
        """
        return self.rdi.smi.is_server_running()
