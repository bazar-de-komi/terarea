"""_summary_
This is the file in charge of storing the variable constants

Raises:
    ValueError: _description_
    KeyError: _description_
    KeyError: _description_
    RuntimeError: _description_

Returns:
    _type_: _description_
"""
from os import getpid
from uuid import uuid4
from random import randint
from typing import Dict, Any
from string import ascii_letters, digits

import toml
import dotenv
from display_tty import IDISP
IDISP.logger.name = "Constants_tests"


DB_PORT = 3307
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = ""
DB_DATABASE = "terarea"

SERVER_HOST = "0.0.0.0"
QUERY_HOST = "http://127.0.0.1"
PORT = 6000

SUCCESS = 0
ERROR = 1

APP_NAME = "Survivor - Testing"

# DEBUG = False
DEBUG = True
IDISP.debug = DEBUG

SKIP_CACHE_GATHERING = True

QUERY_DELAY = 2

# Creating a string that is void of injection material
SAFE_STRING = ascii_letters+digits
SAFE_STRING_LENGTH = len(SAFE_STRING)


def get_cache_busting() -> str:
    """_summary_
        This function is in charge of generating a cache busting string.
        This is done in order to avoid creating already existing accounts

    Returns:
        str: _description_
    """
    cache: str = ""
    length: int = 20
    iterations: int = 0

    cache += "startCacheBusting"
    cache += str(getpid())
    cache += str(uuid4()).replace("-", "")
    while iterations < length:
        cache += SAFE_STRING[
            randint(
                0, SAFE_STRING_LENGTH - 1
            )
        ]
        iterations += 1
    cache += str(getpid())
    cache += "endCacheBusting"
    return cache


def _get_env_node(env: Dict[str, Any], key: str, default: str) -> Any:
    """_summary_
        Load the variable from the environement.
        Otherwise, use the default value provided.
    Args:
        key (_type_): _description_
        default (_type_): _description_

    Returns:
        Any: _description_
    """
    node = env.get(key)
    if node is None:
        return default
    return node


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

    except KeyError as err:
        IDISP.log_warning(f"{err}", "_get_toml_variable")
        return default


CACHE_BUSTER = get_cache_busting()

TEST_ENV = ".env"
try:
    dotenv.load_dotenv(TEST_ENV)
    ENV = dict(dotenv.dotenv_values())

    DB_PORT = int(_get_env_node(ENV, "DB_PORT", DB_PORT))
    DB_HOST = _get_env_node(ENV, "DB_HOST", DB_HOST)
    DB_USER = _get_env_node(ENV, "DB_USER", DB_USER)
    DB_PASSWORD = _get_environement_variable(ENV, "DB_PASSWORD")
    DB_DATABASE = _get_env_node(ENV, "DB_DATABASE", DB_DATABASE)
    MINIO_HOST = _get_env_node(ENV, "MINIO_HOST", "minio")
    MINIO_PORT = int(_get_env_node(ENV, "MINIO_PORT", 9000))
    MINIO_ROOT_USER = _get_env_node(ENV, "MINIO_ROOT_USER", "root")
    MINIO_ROOT_PASSWORD = _get_environement_variable(
        ENV, "MINIO_ROOT_PASSWORD"
    )


except Exception as e:
    raise RuntimeError(
        f"Environement {TEST_ENV} failed to load, aborting"
    ) from e

TOML_CONF = toml.load("config.toml")

# |- Toml status codes
SUCCESS = int(_get_toml_variable(
    TOML_CONF, "Status_codes", "success", SUCCESS
))
ERROR = int(_get_toml_variable(TOML_CONF, "Status_codes", "error", ERROR))
# |- Toml test configuration
SERVER_HOST = str(_get_toml_variable(
    TOML_CONF, "Test.host", "server", SERVER_HOST
))
QUERY_HOST = str(_get_toml_variable(
    TOML_CONF, "Test.host", "client", QUERY_HOST
))
PORT = int(_get_toml_variable(
    TOML_CONF, "Test.host", "port", PORT
))

# Endpoints to test the server
GET_HOME = "/"
PUT_REGISTER = "/register"
POST_LOGIN = "/login"

# Token key references
LAMBDA_USER_TOKEN_KEY: str = "lambda_user"
ADMIN_USER_TOKEN_KEY: str = "admin_user"
