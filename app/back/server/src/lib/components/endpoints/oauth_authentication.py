"""
The file that contains all the methods for the OAuth authentication
"""

import requests
from typing import Union
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

    # def _generate_oauth_authorization_url(self, provider: str) -> Union[int, str]:
    #     """_summary_
    #     """
    #     title = "generate_oauth_authorization_url"
    #     if provider == "google":
    #         base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    #         client_id = CONST.GOOGLE_CLIENT_ID
    #         scope = "email"
    #     elif provider == "github":
    #         base_url = "https://github.com/login/oauth/authorize"
    #         client_id = CONST.GITHUB_CLIENT_ID
    #         scope = "user:email"
    #     else:
    #         self.disp.log_error("Unknown or Unsupported Oauth provider", title)
    #         return self.error
    #     redirect_uri = CONST.REDIRECT_URI
    #     url = base_url
    #     url += f"?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
    #     self.disp.log_debug(f"url = {url}", title)
    #     return url

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
        url = url.replace(" ", "%20")
        url = url.replace(":", "%3A")
        url = url.replace("/", "%2F")
        url = url.replace("?", "%3F")
        url = url.replace("&", "%26")
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
                return {"error": token_response["error"]}
            return token_response
        except requests.RequestException as e:
            self.disp.log_error(f"RequestException: {str(e)}", title)
            return {"error": "HTTP request failed", "details": str(e)}
        except ValueError:
            self.disp.log_error("Failed to parse response JSON.", title)
            return {"error": "Invalid JSON response from provider."}

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
            return {"error": f"Failed to fetch user info. Status code: {response.status_code}"}
        return response.json()

    def oauth_callback(self, provider: str, code: str) -> Response:
        """
        Callback of the OAuth login
        """
        token_response = self._exchange_code_for_token(provider, code)
        if "error" in token_response:
            return HCI.bad_request({"error": token_response["error"]})
        access_token = token_response.get("access_token")
        if not access_token:
            return HCI.bad_request({"error": "Access token not found."})
        user_info = self._get_user_info(provider, access_token)
        if "error" in user_info:
            return HCI.internal_server_error({"error": user_info["error"]})
        return HCI.accepted({"user_info": user_info})

    async def oauth_login(self, request: Request) -> Response:
        """
        Get the authorization url for the OAuth login depending on the provider
        """
        title = "oauth_login"
        request_body = await self.runtime_data_initialised.boilerplate_incoming_initialised.get_body(request)
        self.disp.log_debug(f"Request body: {request_body}", title)
        if not request_body or not all(key in request_body for key in ("provider")):
            return HCI.bad_request({"error": "Bad request."})
        provider = request_body["provider"]
        authorization_url = self._generate_oauth_authorization_url(provider)
        if isinstance(authorization_url, int):
            return HCI.internal_server_error({"error": "Internal server error."})
        return HCI.success({"authorization_url": authorization_url})
