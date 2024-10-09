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


# Mail management
SENDER_ADDRESS = _get_environement_variable(ENV, "SENDER_ADDRESS")
SENDER_KEY = _get_environement_variable(ENV, "SENDER_KEY")
SENDER_HOST = _get_environement_variable(ENV, "SENDER_HOST")
SENDER_PORT = int(_get_environement_variable(ENV, "SENDER_PORT"))

# Server oath variables
REDIRECT_URI = _get_environement_variable(ENV, "REDIRECT_URI")

# |- Github
GITHUB_CLIENT_ID = _get_environement_variable(ENV, "GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = _get_environement_variable(ENV, "GITHUB_CLIENT_SECRET")

# |- Google
GOOGLE_CLIENT_ID = _get_environement_variable(ENV, "GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = _get_environement_variable(ENV, "GOOGLE_CLIENT_SECRET")

# Database management
DB_HOST = _get_environement_variable(ENV, "DB_HOST")
DB_PORT = int(_get_environement_variable(ENV, "DB_PORT"))
DB_USER = _get_environement_variable(ENV, "DB_USER")
DB_PASSWORD = _get_environement_variable(ENV, "DB_PASSWORD")
DB_DATABASE = _get_environement_variable(ENV, "DB_DATABASE")

# Minio management
MINIO_HOST = _get_environement_variable(ENV, "MINIO_HOST")
MINIO_PORT = int(_get_environement_variable(ENV, "MINIO_PORT"))
MINIO_ROOT_USER = _get_environement_variable(ENV, "MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD = _get_environement_variable(ENV, "MINIO_ROOT_PASSWORD")

# TOML variables
# |- Cron settings
CLEAN_TOKENS = _get_toml_variable(TOML_CONF, "Crons", "clean_tokens", True)
CLEAN_TOKENS_DELAY = int(_get_toml_variable(
    TOML_CONF, "Crons", "clean_tokens_interval", 1800
))
ENABLE_TEST_CRONS = _get_toml_variable(
    TOML_CONF, "Crons", "enable_test_crons", False
)
CHECK_ACTIONS_INTERVAL = int(_get_toml_variable(
    TOML_CONF, "Crons", "check_actions_interval", 300
))

# |- Verification
EMAIL_VERIFICATION_DELAY = int(_get_toml_variable(
    TOML_CONF, "Verification", "email_verification_delay", 120
))

# |- Status codes
SUCCESS = int(_get_toml_variable(TOML_CONF, "Status_codes", "success", 0))
ERROR = int(_get_toml_variable(TOML_CONF, "Status_codes", "error", 84))

# |- Debug
DEBUG = _get_toml_variable(TOML_CONF, "Debug_mode", "debug", False)

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

# Database table names
TAB_ACCOUNTS = "Users"
TAB_ACTIONS = "Actions"
TAB_SERVICES = "Services"
TAB_CONNECTIONS = "Connections"
TAB_VERIFICATION = "Verification"
TAB_USER_SERVICES = "User Services"

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

# E-mail token generation
RANDOM_MIN = 100000
RANDOM_MAX = 999999

# User sql data
UA_TOKEN_LIFESPAN: int = 7200
UA_EMAIL_KEY: str = "email"
UA_LIFESPAN_KEY: str = "lifespan"
