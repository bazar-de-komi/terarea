"""
The file that contains all the methods for the OAuth authentication
"""

import uuid
from datetime import datetime, timedelta
from typing import Union, Dict
import requests
from fastapi import Response, Request
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from . import constants as CONST
from . import RuntimeData, HCI

class OAuthAuthentication:
    """
    The class that handle the oauth authentication
    """

    def __init__(self, runtime_data: RuntimeData, success: int = 0, error: int = 84, debug: bool = False) -> None:
        """
        The constructor of the OAuth authentication class
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

    def _generate_oauth_authorization_url(self, provider: str) -> Union[int, str]:
        """
        Generate an OAuth authorization url depends on the given provider
        """
        title = "generate_oauth_authorization_url"
        retrived_provider = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_USER_OAUTH_CONNECTION,
            "*",
            f"provider_name='{provider}'"
        )
        self.disp.log_debug(f"Retrived provider: {retrived_provider}", title)
        if isinstance(retrived_provider, int):
            self.disp.log_error("Unknown or Unsupported OAuth provider", title)
            return self.error
        base_url = retrived_provider[0]["authorisation_base_url"]
        client_id = retrived_provider[0]["client_id"]
        scope = retrived_provider[0]["provider_scope"]
        redirect_uri = CONST.REDIRECT_URI
        state = str(uuid.uuid4())
        columns = self.runtime_data_initialised.database_link.get_table_column_names(CONST.TAB_VERIFICATION)
        self.disp.log_debug(f"Columns list: {columns}", title)
        if isinstance(columns, int):
            return self.error
        columns.pop(0)
        expiration_time = self.runtime_data_initialised.boilerplate_non_http_initialised.set_lifespan(CONST.EMAIL_VERIFICATION_DELAY)
        et_str = self.runtime_data_initialised.database_link.datetime_to_string(expiration_time, False)
        self.disp.log_debug(f"Expiration time: {et_str}", et_str)
        data: list = []
        data.append("state")
        data.append(state)
        data.append(et_str)
        if self.runtime_data_initialised.database_link.insert_data_into_table(CONST.TAB_VERIFICATION, data, columns) == self.error:
            return self.error
        state += ":"
        state += provider
        url = f"{base_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&state={state}"
        # url = url.replace(" ", "%20")
        # url = url.replace(":", "%3A")
        # url = url.replace("/", "%2F")
        # url = url.replace("?", "%3F")
        # url = url.replace("&", "%26")
        self.disp.log_debug(f"url = {url}", title)
        return url

    def _exchange_code_for_token(self, provider: str, code: str):
        """
        Exchange the OAuth authorization code for an access token
        """
        title = "exchange_code_for_token"

        retrieved_provider = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_USER_OAUTH_CONNECTION,
            "*",
            f"provider_name='{provider}'"
        )
        if isinstance(retrieved_provider, int):
            return self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                "exchange_code_for_token",
                "Internal server error.",
                "Internal server error.",
                None,
                True
            )
        headers = {"Accept": "application/json"}
        token_url = retrieved_provider[0]["token_grabber_base_url"]
        
        data: dict = {}
        data["client_id"] = retrieved_provider[0]["client_id"]
        data["client_secret"] = retrieved_provider[0]["client_secret"]
        data["code"] = code
        data["redirect_uri"] = CONST.REDIRECT_URI
        if provider == "google":
            data["grant_type"] = "authorization_code"
        try:
            response = requests.post(token_url, data=data, headers=headers, timeout=10)
            self.disp.log_debug(f"Exchange response = {response}", title)
            response.raise_for_status()
            token_response = response.json()
            if "error" in token_response:
                self.disp.log_error(f"OAuth error: {token_response['error_description']}", title)
                return self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                    "exchange_code_for_token",
                    "Failed to get the token",
                    f"{token_response['error']}",
                    None,
                    True
                )
            return token_response
        except requests.RequestException as e:
            self.disp.log_error(f"RequestException: {str(e)}", title)
            return self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                "exchange_code_for_token",
                "HTTP request failed.",
                f"{str(e)}",
                None,
                True
            )
        except ValueError:
            self.disp.log_error("Failed to parse response JSON.", title)
            return self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                "exchange_code_for_token",
                "Invalid JSON response from provider.",
                "Invalid JSON",
                None,
                True
            )

    def _get_user_info(self, provider: str, access_token: str):
        """
        Get a user information depending
        """
        title: str = "get_user_info"
        retrieved_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_USER_OAUTH_CONNECTION,
            "*",
            f"provider_name='{provider}'"
        )
        self.disp.log_debug(f"Retrieved data: {retrieved_data}", title)
        if isinstance(retrieved_data, int):
            return self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                "get_user_info",
                "Failed to fetch the oauth provider information.",
                "Failed to fetch the oauth provider information.",
                None,
                True
            )
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        user_info_url = retrieved_data[0]["user_info_base_url"]
        response = requests.get(user_info_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                "get_user_info",
                "Failed to fetch user info.",
                "Fetching user info error.",
                None,
                True
            )
        user_info = response.json()
        self.disp.log_debug(f"User info: {user_info}", title)
        if provider == "github":
            for _, info in enumerate(user_info):
                if info["primary"]:
                    email: dict = {}
                    email["email"] = info["email"]
                    return email
        return user_info

    def _oauth_user_logger(self, user_info: Dict, provider: str, connection_data: list) -> Response:
        """
        The function to insert or update the user information in the database
        """
        title: str = "oauth_user_logger"
        email: str = user_info["email"]
        retrieved_user = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACCOUNTS,
            "*",
            f"email='{email}'"
        )
        self.disp.log_debug(f"Retrieved user: {retrieved_user}", title)
        if isinstance(retrieved_user, int) is False:
            retrieved_provider = self.runtime_data_initialised.database_link.get_data_from_table(
                CONST.TAB_SERVICES,
                "*",
                f"name='{provider}'"
            )
            self.disp.log_debug(f"Retrieved provider: {retrieved_provider}", title)
            if isinstance(retrieved_user, int):
                return HCI.internal_server_error({"error": "Internal server error."})
            connection_data.append(str(retrieved_provider[0]["id"]))
            connection_data.append(str(retrieved_user[0]["id"]))
            self.disp.log_debug(f"Connection data: {connection_data}", title)
            columns = self.runtime_data_initialised.database_link.get_table_column_names(CONST.TAB_ACTIVE_OAUTHS)
            if isinstance(columns, int):
                return HCI.internal_server_error({"error": "Internal server error."})
            columns.pop(0)
            self.disp.log_debug(f"Columns list = {columns}", title)
            if self.runtime_data_initialised.database_link.insert_data_into_table(
                CONST.TAB_ACTIVE_OAUTHS,
                connection_data,
                columns
            ) == self.error:
                return HCI.internal_server_error({"error": "Internal server error."})
            user_data = self.runtime_data_initialised.boilerplate_incoming_initialised.log_user_in(email)
            if user_data["status"] == self.error:
                return HCI.internal_server_error({"error": "Internal server error."})
            return HCI.accepted({"token": user_data["token"]})
        columns = self.runtime_data_initialised.database_link.get_table_column_names(CONST.TAB_ACCOUNTS)
        if isinstance(columns, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        columns.pop(0)
        self.disp.log_debug(f"Columns list = {columns}", title)
        username: str = email.split('@')[0]
        user_data: list = []
        user_data.append(username)
        user_data.append(email)
        user_data.append(provider)
        user_data.append(provider)
        user_data.append("NULL")
        user_data.append(str(int(False)))
        self.disp.log_debug(f"Data list = {user_data}", title)
        if self.runtime_data_initialised.database_link.insert_data_into_table(CONST.TAB_ACCOUNTS, user_data, columns) == self.error:
            return HCI.internal_server_error({"error": "Internal server error."})
        retrieved_user = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_ACCOUNTS,
            "*",
            f"email='{email}'"
        )
        self.disp.log_debug(f"Retrieved user: {retrieved_user}", title)
        if isinstance(retrieved_user, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        retrieved_provider = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_SERVICES,
            "*",
            f"name='{provider}'"
        )
        self.disp.log_debug(f"Retrieved provider: {retrieved_provider}", title)
        if isinstance(retrieved_user, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        connection_data.append(str(retrieved_provider[0]["id"]))
        connection_data.append(str(retrieved_user[0]["id"]))
        self.disp.log_debug(f"Connection data: {connection_data}", title)
        columns = self.runtime_data_initialised.database_link.get_table_column_names(CONST.TAB_ACTIVE_OAUTHS)
        if isinstance(columns, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        columns.pop(0)
        self.disp.log_debug(f"Columns list = {columns}", title)
        if self.runtime_data_initialised.database_link.insert_data_into_table(
            CONST.TAB_ACTIVE_OAUTHS,
            connection_data,
            columns
        ) == self.error:
            return HCI.internal_server_error({"error": "Internal server error."})
        user_data = self.runtime_data_initialised.boilerplate_incoming_initialised.log_user_in(email)
        if user_data["status"] == self.error:
            return HCI.internal_server_error({"error": "Internal server error."})
        return HCI.accepted({"token": user_data["token"]})

    def _handle_token_response(self, token_response: Dict, provider: str) -> Response:
        title: str = "handle_token_response"
        data: list = []
        access_token: str = token_response["access_token"]
        if not access_token:
            return HCI.bad_request({"error": "Access token not found."})
        data.append(access_token)
        if provider == "google":
            expires: int = token_response["expires_in"]
            if not expires:
                return HCI.bad_request({"error": "Expiration time not found."})
            current_time = datetime.now()
            new_time = current_time + timedelta(seconds=expires)
            expiration_date = self.runtime_data_initialised.database_link.datetime_to_string(new_time)
            data.append(expiration_date)
            data.append(str(expires))
            refresh_link = token_response["refresh_token"]
            if not refresh_link:
                return HCI.bad_request({"error": "Refresh link not found."})
            data.append(refresh_link)
        if provider == "github":
            data.append(self.runtime_data_initialised.database_link.datetime_to_string(datetime.now()))
            data.append("0")
            data.append("NULL")
        user_info = self._get_user_info(provider, access_token)
        if "error" in user_info:
            return HCI.internal_server_error({"error": user_info["error"]})
        return self._oauth_user_logger(user_info, provider, data)

    def refresh_token(self, provider_name: str, refresh_link: str) -> Union[str, None]:
        """
        The function that use the given provider name and refresh link to generate a new token for oauth authentication
        """
        title: str = "refresh_token"
        if provider_name == "google":
            retrieved_data = self.runtime_data_initialised.database_link.get_data_from_table(
                CONST.TAB_USER_OAUTH_CONNECTION,
                "*",
                f"provider_name='{provider_name}'"
            )
            self.disp.log_debug(f"Retrieved provider data: {retrieved_data}", title)
            if isinstance(retrieved_data, int):
                self.disp.log_error("An error has been dectected when retrieving the provider data", title)
                return None
            token_url: str = retrieved_data[0]["token_grabber_base_url"]
            generated_data: dict = {}
            generated_data["client_id"] = retrieved_data[0]["token_grabber_base_url"]
            generated_data["client_secret"] = retrieved_data[0]["client_secret"]
            generated_data["refresh_token"] = refresh_link
            generated_data["grant_type"] = "refresh_token"
            self.disp.log_debug(f"Generated data: {generated_data}", title)
            google_response: Response = requests.post(token_url, data=generated_data, timeout=10)
            self.disp.log_debug(f"Google response: {google_response}", title)
            if google_response.status_code == 200:
                token_response = google_response.json()
                self.disp.log_debug(f"Google response to json: {token_response}", title)
                if "access_token" in token_response:
                    return token_response["access_token"]
        self.disp.log_error("The provider is not recognised", title)
        return None

    async def oauth_callback(self, request: Request) -> Response:
        """
        Callback of the OAuth login
        """
        title = "oauth_callback"
        query_params = request.query_params
        if not query_params:
            return HCI.bad_request({"error": "Query parameters not provided."})
        self.disp.log_debug(f"Query params: {query_params}", title)
        code = query_params.get("code")
        self.disp.log_debug(f"Code: {code}", title)
        state = query_params.get("state")
        self.disp.log_debug(f"State: {state}", title)
        if not code or not state:
            return HCI.bad_request({"error": "Authorization code or state not provided."})
        uuid_gotten, provider = state.split(":")
        if not uuid_gotten or not provider:
            return HCI.bad_request({"error": "The state is in bad format."})
        self.disp.log_debug(f"Uuid gotten: {uuid_gotten}", title)
        self.disp.log_debug(f"Provider: {provider}", title)
        data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_VERIFICATION,
            "*",
            f"definition='{uuid_gotten}'"
        )
        self.disp.log_debug(f"Data gotten: {data}", title)
        if isinstance(data, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        if isinstance(self.runtime_data_initialised.database_link.drop_data_from_table(
            CONST.TAB_VERIFICATION,
            f"definition='{uuid_gotten}'"
        ), int) is False:
            return HCI.internal_server_error({"error": "Internal server error."})
        token_response = self._exchange_code_for_token(provider, code)
        self.disp.log_debug(f"Token response: {token_response}", title)
        if "error" in token_response:
            return HCI.bad_request({"error": token_response["error"]})
        return self._handle_token_response(token_response, provider)

    async def oauth_login(self, request: Request) -> Response:
        """
        Get the authorization url for the OAuth login depending on the provider
        """
        title = "oauth_login"
        request_body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        self.disp.log_debug(f"Request body: {request_body}", title)
        if not request_body or "provider" not in request_body:
            return HCI.bad_request({"error": "Bad request."})
        provider = request_body["provider"]
        self.disp.log_debug(f"Oauth login provider: {provider}", title)
        authorization_url = self._generate_oauth_authorization_url(provider)
        self.disp.log_debug(f"Authorization url: {authorization_url}", title)
        if isinstance(authorization_url, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        return HCI.success({"authorization_url": authorization_url})

    async def add_oauth_provider(self, request: Request, provider: str) -> Response:
        """
        Add a new oauth provider to the database (only for admin)
        """
        title: str = "add_oauth_provider"
        if not provider:
            return HCI.bad_request({"error": "The provider is not provided."})
        self.disp.log_debug(f"Provider: {provider}", title)
        token: str = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_admin(token) is False:
            self.disp.log_error("You're not admin.", title)
            return HCI.unauthorized({"error": "This ressource cannot be accessed."})
        retrived_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_USER_OAUTH_CONNECTION,
            "*",
            f"provider_name='{provider}'")
        if isinstance(retrived_data, int) is False:
            return HCI.conflict({"error": "The provider already exist in the database."})
        request_body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        if not request_body or not all(key in request_body for key in ("client_id", "client_secret", "provider_scope", "authorisation_base_url", "token_grabber_base_url", "user_info_base_url")):
            return HCI.bad_request({"error": "A variable is missing in the body."})
        self.disp.log_debug(f"Request body: {request_body}", title)
        client_id = request_body["client_id"]
        client_secret = request_body["client_secret"]
        provider_scope = request_body["provider_scope"]
        authorisation_base_url = request_body["authorisation_base_url"]
        token_grabber_base_url = request_body["token_grabber_base_url"]
        user_info_base_url = request_body["user_info_base_url"]
        data: list = [
            provider,
            client_id,
            client_secret,
            provider_scope,
            authorisation_base_url,
            token_grabber_base_url,
            user_info_base_url
        ]
        columns = self.runtime_data_initialised.database_link.get_table_column_names(CONST.TAB_USER_OAUTH_CONNECTION)
        if isinstance(columns, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        columns.pop(0)
        self.disp.log_debug(f"Columns: {columns}", title)
        if self.runtime_data_initialised.database_link.insert_data_into_table(CONST.TAB_USER_OAUTH_CONNECTION, data, columns) == self.error:
            return HCI.internal_server_error({"error": "Internal server error."})
        oauth: list = ["1"]
        column: list = ["oauth"]
        if self.runtime_data_initialised.database_link.update_data_in_table(
            CONST.TAB_SERVICES,
            oauth,
            column,
            f"name='{provider}'"
        ) == self.error:
            return HCI.internal_server_error({"error": "Internal server error."})
        return HCI.success({"msg": "The provider is successfully added."})

    async def update_oauth_provider_data(self, request: Request, provider: str) -> Response:
        """
        The function that modify every value of an oauth provider
        """
        title: str = "update_oauth_provider_data"
        if not provider:
            return HCI.bad_request({"error": "The provider is not provided."})
        self.disp.log_debug(f"Provider: {provider}", title)
        token: str = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
            request
        )
        self.disp.log_debug(f"Token gotten: {token}", title)
        if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_admin(token) is False:
            self.disp.log_error("You're not admin.", title)
            return HCI.unauthorized({"error": "This ressource cannot be accessed."})
        retrived_data = self.runtime_data_initialised.database_link.get_data_from_table(
            CONST.TAB_USER_OAUTH_CONNECTION,
            "*",
            f"provider_name='{provider}'")
        if isinstance(retrived_data, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        request_body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        if not request_body or not all(key in request_body for key in ("client_id", "client_secret", "provider_scope", "authorisation_base_url", "token_grabber_base_url", "user_info_base_url")):
            return HCI.bad_request({"error": "A variable is missing in the body."})
        self.disp.log_debug(f"Request body: {request_body}", title)
        client_id = request_body["client_id"]
        client_secret = request_body["client_secret"]
        provider_scope = request_body["provider_scope"]
        authorisation_base_url = request_body["authorisation_base_url"]
        token_grabber_base_url = request_body["token_grabber_base_url"]
        user_info_base_url = request_body["user_info_base_url"]
        data: list = [
            client_id,
            client_secret,
            provider_scope,
            authorisation_base_url,
            token_grabber_base_url,
            user_info_base_url
        ]
        self.disp.log_debug(f"Generated data: {data}", title)
        columns: list = self.runtime_data_initialised.database_link.get_table_column_names(
            CONST.TAB_USER_OAUTH_CONNECTION
        )
        if isinstance(columns, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        columns.pop(0)
        columns.pop(0)
        self.disp.log_debug(f"Columns: {columns}", title)
        if self.runtime_data_initialised.database_link.update_data_in_table(
            CONST.TAB_USER_OAUTH_CONNECTION,
            data,
            columns,
            f"provider_name='{provider}'"
        ) == self.error:
            return HCI.internal_server_error({"error": "Internal server error."})
        return HCI.success({"msg": "The provider is successfully updated."})
