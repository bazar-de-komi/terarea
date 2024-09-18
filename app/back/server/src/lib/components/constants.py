"""_summary_
    This is the file in charge of containing the constants that run the server.
"""

from typing import List, Dict

import toml
import dotenv
from display_tty import IDISP
IDISP.logger.name = "Constants"

# Environement initialisation
dotenv.load_dotenv(".env")
ENV = dict(dotenv.dotenv_values())

# toml config file
TOML_CONF = toml.load("config.toml")


def _get_environement_variable(environement: dotenv, variable_name: str) -> str:
    """_summary_
        Get the content of an environement variable.

    Args:
        variable_name (str): _description_

    Returns:
        str: _description_: the value of that variable, otherwise an exception is raised.
    """
    data = environement.get(variable_name)
    if data is None:
        raise ValueError(
            f"Variable {variable_name} not found in the environement"
        )
    return data


def _get_toml_variable(toml_conf: dict, section: str, key: str, default=None) -> str:
    """
    Get the value of a configuration variable from the TOML file.

    Args:
        toml_conf (dict): The loaded TOML configuration as a dictionary.
        section (str): The section of the TOML file to search in.
        key (str): The key within the section to fetch.
        default: The default value to return if the key is not found. Defaults to None.

    Returns:
        str: The value of the configuration variable, or the default value if the key is not found.

    Raises:
        KeyError: If the section is not found in the TOML configuration.
    """
    try:
        keys = section.split('.')
        current_section = toml_conf

        for k in keys:
            if k in current_section:
                current_section = current_section[k]
            else:
                raise KeyError(
                    f"Section '{section}' not found in TOML configuration."
                )

        if key in current_section:
            return current_section[key]
        if default is None:
            msg = f"Key '{key}' not found in section '{section}' "
            msg += "of TOML configuration."
            raise KeyError(msg)
        return default

    except KeyError as e:
        IDISP.log_warning(f"{e}", "_get_toml_variable")
        return default


# Database management
DB_HOST = _get_environement_variable(ENV, "DB_HOST")
DB_PORT = _get_environement_variable(ENV, "DB_PORT")
DB_USER = _get_environement_variable(ENV, "DB_USER")
DB_PASSWORD = _get_environement_variable(ENV, "DB_PASSWORD")
DB_DATABASE = _get_environement_variable(ENV, "DB_DATABASE")

# Minio management
MINIO_HOST = _get_environement_variable(ENV, "MINIO_HOST")
MINIO_PORT = _get_environement_variable(ENV, "MINIO_PORT")
MINIO_ROOT_USER = _get_environement_variable(ENV, "MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD = _get_environement_variable(ENV, "MINIO_ROOT_PASSWORD")


# Getting data from the toml file
# |- Cache updater
STARTUP_DELAY = int(_get_toml_variable(
    TOML_CONF, "Cache_updater", "startup_delay", 20
))
# |- Toml status codes
SUCCESS = int(_get_toml_variable(
    TOML_CONF, "Status_codes", "success", 0
))
ERROR = int(_get_toml_variable(TOML_CONF, "Status_codes", "error", 84))
# |- Toml Debug mode
DEBUG = bool(_get_toml_variable(TOML_CONF, "Debug_mode", "debug", False))


# endpints help
HELP_COMMANDS: Dict[str, str] = {
    "/": "The home endpoint"
}

# Json response default keys
JSON_TITLE: str = "title"
JSON_MESSAGE: str = "msg"
JSON_ERROR: str = "error"
JSON_RESP: str = "resp"
JSON_LOGGED_IN: str = "logged in"
JSON_UID: str = "user_uid"
# JSON Header keys
JSON_HEADER_APP_NAME: str = "app_sender"
JSON_HEADER_HOST: str = "serving_host"
JSON_HEADER_PORT: str = "serving_port"
JSON_HEADER_CHARACTER_NAME: str = "character_name"
CONTENT_TYPE: str = "JSON"


# Character info config
CHAR_NODE_KEY: str = "node"
CHAR_ACTIVE_KEY: str = "active"
CHAR_NAME_KEY: str = "name"
CHAR_UID_KEY: str = "uid"
CHAR_ID_DEFAULT_INDEX: int = 0


# User info database table
USERNAME_INDEX_DB: int = 1
PASSWORD_INDEX_DB: int = 2
FIRSTNAME_INDEX_DB: int = 3
LASTNAME_INDEX_DB: int = 4
BIRTHDAY_INDEX_DB: int = 5
GENDER_INDEX_DB: int = 7
ROLE_INDEX_DB: int = 10
UD_USERNAME_KEY: str = "username"
UD_FIRSTNAME_KEY: str = "firstname"
UD_LASTNAME_KEY: str = "lastname"
UD_BIRTHDAY_KEY: str = "birthday"
UD_GENDER_KEY: str = "gender"
UD_ROLE_KEY: str = "role"
UD_ADMIN_KEY: str = "admin"
UD_LOGIN_TIME_KEY: str = "login_time"
UD_LOGGED_IN_KEY: str = "logged_in"

# For Path creation variables
PATH_KEY: str = "path"
ENDPOINT_KEY: str = "endpoint"
METHOD_KEY: str = "method"
ALLOWED_METHODS: List[str] = [
    "GET", "POST",
    "PUT", "PATCH",
    "DELETE", "HEAD",
    "OPTIONS"
]

# Incoming header variables
REQUEST_TOKEN_KEY = "token"
REQUEST_BEARER_KEY = "authorization"

# Cache loop
THREAD_CACHE_REFRESH_DELAY = 10

# User sql data
UA_TOKEN_LIFESPAN: int = 7200
UA_EMAIL_KEY: str = "email"
UA_LIFESPAN_KEY: str = "lifespan"
