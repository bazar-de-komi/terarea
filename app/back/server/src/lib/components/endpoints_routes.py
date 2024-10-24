"""_summary_
    This is the file in charge of storing the endpoints_initialised ready to be imported into the server class.
"""
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from .runtime_data import RuntimeData
from .password_handling import PasswordHandling
# , Github_check#, IFTTT_Manager
from .endpoints import Bonus, UserEndpoints, Services, OAuthAuthentication


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
        self.oauth: OAuthAuthentication = OAuthAuthentication(
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
            "", self.bonus.get_welcome, [
                "GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"
            ]
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/", self.bonus.get_welcome, [
                "GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"
            ]
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/", self.bonus.get_welcome, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/test", self.bonus.my_test_component, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/bucket_names", self.bonus.get_s3_bucket_names, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/get_table", self.bonus.get_table, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/stop", self.bonus.post_stop_server, "PUT"
        )

        # Services routes
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/services", self.services.get_services, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/service/{name}", self.services.get_service, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/services_by_tag/{tag}", self.services.get_services_by_tag, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/recent_services", self.services.get_recent_services, "GET"
        )

        # Authentication routes
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/login", self.user_endpoints.post_login, "POST"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/register", self.user_endpoints.post_register, "POST"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/send_email_verification", self.user_endpoints.post_send_email_verification, "POST"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/reset_password", self.user_endpoints.put_reset_password, "PATCH"
        )
        
        # Oauth routes
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/oauth/login", self.oauth.oauth_login, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/oauth/callback", self.oauth.oauth_callback, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/oauth/{provider}", self.oauth.add_oauth_provider, "POST"
        )

        # Users routes
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/user", self.user_endpoints.patch_user, "PATCH"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/user", self.user_endpoints.put_user, "PUT"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/user", self.user_endpoints.get_user, "GET"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/user", self.user_endpoints.delete_user, "DELETE"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/user_favicon", self.user_endpoints.put_user_favicon, "PUT"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/user_favicon", self.user_endpoints.delete_user_favicon, "DELETE"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/logout", self.user_endpoints.post_logout, "POST"
        )
        self.runtime_data_initialised.paths_initialised.add_path(
            "/api/v1/user_id", self.user_endpoints.get_user_id, "GET"
        )
