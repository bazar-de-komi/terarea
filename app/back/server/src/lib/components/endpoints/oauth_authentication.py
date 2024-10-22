"""
The file that contains all the methods for the OAuth authentication
"""

import requests
from typing import Union, Dict
from fastapi import Response, Request
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME
from .. import constants as CONST
from ..runtime_data import RuntimeData
from ..http_codes import HCI


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

        # Dictionnaire pour gérer les informations des providers
        provider_info = {
            "google": {
                "base_url": "https://accounts.google.com/o/oauth2/v2/auth",
                "client_id": CONST.GOOGLE_CLIENT_ID,
                "scope": "email"
            },
            "github": {
                "base_url": "https://github.com/login/oauth/authorize",
                "client_id": CONST.GITHUB_CLIENT_ID,
                "scope": "user:email"
            }
        }

        if provider not in provider_info:
            self.disp.log_error("Unknown or Unsupported OAuth provider", title)
            return self.error

        base_url = provider_info[provider]["base_url"]
        client_id = provider_info[provider]["client_id"]
        scope = provider_info[provider]["scope"]
        redirect_uri = CONST.REDIRECT_URI

        url = f"{base_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
        self.disp.log_debug(f"url = {url}", title)
        return url

    def _exchange_code_for_token(self, provider: str, code: str):
        """
        Exchange the OAuth authorization code for an access token
        """
        title = "exchange_code_for_token"

        if provider == "google":
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "client_id": CONST.GOOGLE_CLIENT_ID,
                "client_secret": CONST.GOOGLE_CLIENT_SECRET,
                "code": code,
                "redirect_uri": CONST.REDIRECT_URI,
                "grant_type": "authorization_code"
            }
        elif provider == "github":
            token_url = "https://github.com/login/oauth/access_token"
            data = {
                "client_id": CONST.GITHUB_CLIENT_ID,
                "client_secret": CONST.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": CONST.REDIRECT_URI
            }
        else:
            self.disp.log_error("Unknown or Unsupported Oauth provider", title)
            return {"error": "Unsupported OAuth provider."}
        self.disp.log_debug(f"data = {data}", title)
        headers = {"Accept": "application/json"}
        try:
            response = requests.post(token_url, data=data, headers=headers, timeout=10)
            self.disp.log_debug(f"Response = {response}", title)
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
        if provider == "google":
            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        elif provider == "github":
            user_info_url = "https://api.github.com/user"
        else:
            return self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                "get_user_info",
                "The provider you chose is not supported.",
                "Unsupported provider.",
                None,
                True
            )
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(user_info_url, headers=headers)
        if response.status_code != 200:
            return self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
                "get_user_info",
                "Failed to fetch user info.",
                "Fetching user info error.",
                None,
                True
            )
        return response.json()

    def _insert_if_user_not_exist_in_database(self, user_info: Dict, provider: str) -> int:
        """
        The function to insert or update the user information in the database
        """
        title: str = "insert_if_user_not_exist_in_database"
        email: str = user_info["email"]
        table: str = "Users"
        retrieved_user = self.runtime_data_initialised.database_link.get_data_from_table(table, "email", f"email='{email}'")
        self.disp.log_debug(f"Retrieved user: {retrieved_user}", title)
        if isinstance(retrieved_user, int) or retrieved_user[0]["method"] == provider:
            data = self.runtime_data_initialised.boilerplate_incoming_initialised.log_user_in(email)
            if data["status"] == self.error:
                return self.error
            return self.success
        columns = self.runtime_data_initialised.database_link.get_table_column_names(table)
        if isinstance(columns, int):
            return self.error
        columns.pop(0)
        self.disp.log_debug(f"Columns list = {columns}", title)
        username: str = email.split('@')[0]
        data: list = []
        data.append(username)
        data.append(email)
        data.append(provider)
        data.append(provider)
        data.append("NULL")
        data.append(str(int(False)))
        self.disp.log_debug(f"Data list = {data}", title)
        if self.runtime_data_initialised.database_link.insert_data_into_table(table, data, columns) == self.error:
            return self.error
        return self.success

    def oauth_callback(self, provider: str, code: str) -> Response:
        """
        Callback of the OAuth login
        """
        title = "oauth_callback"
        token_response = self._exchange_code_for_token(provider, code)
        self.disp.log_debug(f"Token response: {token_response}", title)
        if "error" in token_response:
            return HCI.bad_request({"error": token_response["error"]})
        access_token = token_response.get("access_token")
        if not access_token:
            return HCI.bad_request({"error": "Access token not found."})
        user_info = self._get_user_info(provider, access_token)
        self.disp.log_debug(f"User info: {user_info}", title)
        if "error" in user_info:
            return HCI.internal_server_error({"error": user_info["error"]})
        if self._insert_if_user_not_exist_in_database(user_info, provider) == self.error:
            return HCI.internal_server_error({"error": "Internal server error."})
        return HCI.accepted({"user_info": user_info})

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
        authorization_url = self._generate_oauth_authorization_url(provider)
        self.disp.log_debug(f"Authorization url: {authorization_url}", title)
        if isinstance(authorization_url, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        return HCI.success({"authorization_url": authorization_url})
