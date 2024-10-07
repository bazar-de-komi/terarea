##
# EPITECH PROJECT, 2023
# Desktop_pet
# File description:
# pet_server.py
##

from typing import Any
from datetime import datetime
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from .sql import SQL
from .bucket import Bucket
from .components import Endpoints, ServerPaths, RuntimeData, ServerManagement, CONST, BackgroundTasks
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
        self.runtime_data_initialised: RuntimeData = RuntimeData(
            host=self.host,
            port=self.port,
            app_name=app_name
        )
        # ----- The classes that need to be tracked for the server to run  -----
        self.runtime_data_initialised.background_tasks_initialised = BackgroundTasks(
            error=self.error,
            success=self.success,
            debug=self.debug
        )
        self.runtime_data_initialised.server_management_initialised = ServerManagement(
            self.runtime_data_initialised,
            error=self.error,
            success=self.success,
            debug=self.debug
        )
        self.runtime_data_initialised.boilerplate_responses_initialised = BoilerplateResponses(
            self.runtime_data_initialised,
            debug=self.debug
        )
        self.runtime_data_initialised.boilerplate_incoming_initialised = BoilerplateIncoming(
            self.runtime_data_initialised,
            error=self.error,
            success=self.success,
            debug=self.debug
        )
        self.runtime_data_initialised.boilerplate_non_http_initialised = BoilerplateNonHTTP(
            self.runtime_data_initialised,
            error=self.error,
            success=self.success,
            debug=self.debug
        )
        self.runtime_data_initialised.paths_initialised = ServerPaths(
            self.runtime_data_initialised,
            error=self.error,
            success=self.success,
            debug=self.debug
        )
        self.runtime_data_initialised.database_link = SQL(
            url=CONST.DB_HOST,
            port=CONST.DB_PORT,
            username=CONST.DB_USER,
            password=CONST.DB_PASSWORD,
            db_name=CONST.DB_DATABASE,
            debug=self.debug
        )
        self.runtime_data_initialised.bucket_link = Bucket(
            error=self.error,
            success=self.success
        )
        self.runtime_data_initialised.endpoints_initialised = Endpoints(
            self.runtime_data_initialised,
            error=self.error,
            success=self.success,
            debug=self.debug
        )
        # --------------------------- The test crons ---------------------------
        self._inject_test_cron()

    def _test_hello_world(self) -> None:
        """_summary_
            This is a test function that will print "Hello World".
        """
        self.disp.log_info("Hello World", "_test_hello_world")

    def _test_current_date(self, *args: Any) -> None:
        """_summary_
            This is a test function that will print the current date.
        Args:
            date (datetime): _description_
        """
        if len(args) >= 1:
            date = args[0]
        else:
            date = datetime.now()
        if callable(date) is True:
            self.disp.log_info(
                f"(Called) Current date: {date()}",
                "_test_current_date"
            )
        else:
            self.disp.log_info(
                f"(Not called) Current date: {date}",
                "_test_current_date"
            )

    def _inject_test_cron(self) -> None:
        test_delay = 20
        self.runtime_data_initialised.background_tasks_initialised.add_task(
            func=self._test_hello_world,
            args=None,
            trigger='interval',
            seconds=test_delay
        )
        self.runtime_data_initialised.background_tasks_initialised.safe_add_task(
            func=self._test_current_date,
            args=datetime.now,
            trigger='interval',
            seconds=test_delay
        )

    def main(self) -> int:
        """_summary_
            The main function of the server.
            This is the one in charge of starting the server.

        Returns:
            int: _description_
        """
        self.runtime_data_initialised.server_management_initialised.initialise_classes()
        self.runtime_data_initialised.paths_initialised.load_default_paths_initialised()
        self.runtime_data_initialised.paths_initialised.inject_routes()
        status = self.runtime_data_initialised.background_tasks_initialised.safe_start()
        if status != self.success:
            self.disp.log_error(
                "Error: background tasks failed to start.",
                "main"
            )
            return status
        try:
            self.runtime_data_initialised.server.run()
            print("ffd")
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
        return self.runtime_data_initialised.server_management_initialised.is_server_running()
