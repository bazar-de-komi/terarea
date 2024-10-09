"""_summary_
    This is the file in charge of storing the endpoints_initialised ready to be imported into the server class.
"""
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from .runtime_data import RuntimeData
from .password_handling import PasswordHandling
# , Github_check#, IFTTT_Manager
from .endpoints import Bonus, UserEndpoints, Services


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
        # ------------------- Initialize endpoints sub-classes ------------------
        self.bonus: Bonus = Bonus(
            runtime_data=runtime_data,
            success=success,
            error=error,
            debug=debug
        )
        self.services: Services = Services(
            runtime_data=self.runtime_data_initialised,
            success=self.success,
            error=self.error,
            debug=self.debug
        )
        self.user_endpoints: UserEndpoints = UserEndpoints(
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
            "/api/v1/", self.bonus.get_welcome, "GET"
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
        self.runtime_data_initialised.paths_initialised.add_path(
            "/get_services", self.services.get_services, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/get_service/{name}", self.services.get_service, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/get_services_by_tag/{tag}", self.services.get_services_by_tag, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/get_recent_services", self.services.get_recent_services, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/stop", self.bonus.post_stop_server, "PUT"
        )

        # Authentication routes
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/login", self.user_endpoints.post_login, "PUT"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/register", self.user_endpoints.put_register, "POST"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/send_email_verification", self.user_endpoints.post_email_reset_password, "PUT"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/reset_password", self.user_endpoints.put_reset_password, "PATCH"
        )
