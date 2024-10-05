"""_summary_
    This is the file in charge of storing the endpoints_initialised ready to be imported into the server class.
"""
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from .runtime_data import RuntimeData
from .password_handling import PasswordHandling
from .endpoints import Bonus, Authentication#, IFTTT_Manager


class Endpoints:
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
        self.password_handling_initialised: PasswordHandling = PasswordHandling(
            self.error,
            self.success,
            self.debug
        )
        self.disp: Disp = Disp(
            TOML_CONF,
            SAVE_TO_FILE,
            FILE_NAME,
            FILE_DESCRIPTOR,
            debug=self.debug,
            logger=self.__class__.__name__
        )
        #------------------- Initialize endpoints sub-classes ------------------
        self.bonus: Bonus = Bonus(
            runtime_data=runtime_data,
            success=success,
            error=error,
            debug=debug
        )
        self.authentication: Authentication = Authentication(
            runtime_data=runtime_data,
            success=success,
            error=error,
            debug=debug
        )

    def inject_routes(self) -> None:
        """_summary_
        """
        # Bonus routes
        self.runtime_data_initialised.paths_initialised.add_path(
            "/", self.bonus.get_welcome, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/stop", self.bonus.post_stop_server, "POST"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/test", self.bonus.my_test_component, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/bucket_names", self.bonus.get_s3_bucket_names, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/get_table", self.bonus.get_table, "GET"
        )

        # Authentication routes
        self.runtime_data_initialised.paths_initialised.add_path(
            "/login", self.authentication.post_login, "POST"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/register", self.authentication.put_register, "PUT"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/ask_email_forgot_password", self.authentication.post_email_reset_password, "POST"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/reset_password", self.authentication.put_reset_password, "PUT"
        )
