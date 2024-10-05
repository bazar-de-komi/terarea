"""_summary_
    File in charge of testing the boilerplate Boilerplate non http class.
"""
import os
import sys
from datetime import datetime, timedelta

import pytest
from fastapi import FastAPI

sys.path.append(os.getcwd())

try:
    from src.lib.components.http_codes import HCI
    from src.lib.components import constants as CONST
    from src.lib.components.runtime_data import RuntimeData
    from src.lib.components.endpoints_routes import Endpoints
    from src.lib.boilerplates.responses import BoilerplateResponses
except ImportError as e:
    raise ImportError("Failed to import the src module") from e

ERROR = 84
SUCCESS = 0
RDI = RuntimeData("0.0.0.0", 5000, "Area", ERROR, SUCCESS)
RDI.app = FastAPI()
RDI.endpoints_initialised = Endpoints(
    runtime_data=RDI,
    success=SUCCESS,
    error=ERROR,
    debug=False
)
BRI = BoilerplateResponses(
    runtime_data=RDI,
    debug=False
)

RDI.boilerplate_responses_initialised = BRI


def test_build_response_body_no_error() -> None:
    """_summary_
        Function in charge of testing the build response body function.
    """
    title = "Hello World"
    message = "Some hello world !"
    response = "hw"
    token = None
    error = False
    data = BRI.build_response_body(
        title=title,
        message=message,
        resp=response,
        token=token,
        error=error
    )
    resp = {}
    resp[CONST.JSON_TITLE] = title
    resp[CONST.JSON_MESSAGE] = message
    resp[CONST.JSON_RESP] = response
    resp[CONST.JSON_LOGGED_IN] = False
    assert data == resp


def test_build_response_body_error() -> None:
    """_summary_
        Function in charge of testing the build response body function.
    """
    title = "Hello World"
    message = "Some hello world !"
    response = "hw"
    token = None
    error = True
    data = BRI.build_response_body(
        title=title,
        message=message,
        resp=response,
        token=token,
        error=error
    )
    resp = {}
    resp[CONST.JSON_TITLE] = title
    resp[CONST.JSON_MESSAGE] = message
    resp[CONST.JSON_ERROR] = response
    resp[CONST.JSON_LOGGED_IN] = False
    assert data == resp


def test_build_response_body_no_error_logged_in() -> None:
    """_summary_
        Function in charge of testing the build response body function.
    """
    token = "some_token"
    RDI.user_data = {token: ""}
    title = "Hello World"
    message = "Some hello world !"
    response = "hw"
    error = False
    data = BRI.build_response_body(
        title=title,
        message=message,
        resp=response,
        token=token,
        error=error
    )
    resp = {}
    resp[CONST.JSON_TITLE] = title
    resp[CONST.JSON_MESSAGE] = message
    resp[CONST.JSON_RESP] = response
    resp[CONST.JSON_LOGGED_IN] = True
    RDI.user_data = {}
    assert data == resp


def test_build_response_body_error_logged_in() -> None:
    """_summary_
        Function in charge of testing the build response body function.
    """
    token = "some_token"
    RDI.user_data = {token: ""}
    title = "Hello World"
    message = "Some hello world !"
    response = "hw"
    error = True
    data = BRI.build_response_body(
        title=title,
        message=message,
        resp=response,
        token=token,
        error=error
    )
    resp = {}
    resp[CONST.JSON_TITLE] = title
    resp[CONST.JSON_MESSAGE] = message
    resp[CONST.JSON_ERROR] = response
    resp[CONST.JSON_LOGGED_IN] = True
    RDI.user_data = {}
    assert data == resp


def test_invalid_token() -> None:
    """_summary_
        Function in charge of testing the invalid token function.
    """
    title = "Hello World"
    data = BRI.invalid_token(title)
    resp = {}
    resp[CONST.JSON_TITLE] = title
    resp[CONST.JSON_MESSAGE] = "The token you entered is invalid."
    resp[CONST.JSON_ERROR] = "Invalid token"
    resp[CONST.JSON_LOGGED_IN] = False
    compiled_response = HCI.invalid_token(
        content=resp,
        content_type=CONST.CONTENT_TYPE,
        headers=RDI.json_header
    )
    assert data.status_code == compiled_response.status_code
    assert data.headers == compiled_response.headers
    assert data.body == compiled_response.body


def test_not_logged_in() -> None:
    """_summary_
        Function in charge of testing the not logged in function.
    """
    title = "Hello World"
    data = BRI.not_logged_in(title)
    resp = {}
    resp[CONST.JSON_TITLE] = title
    resp[CONST.JSON_MESSAGE] = "You need to be logged in to be able to run this endpoint."
    resp[CONST.JSON_ERROR] = "User not logged in"
    resp[CONST.JSON_LOGGED_IN] = False
    compiled_response = HCI.unauthorized(
        content=resp,
        content_type=CONST.CONTENT_TYPE,
        headers=RDI.json_header
    )
    assert data.status_code == compiled_response.status_code
    assert data.headers == compiled_response.headers
    assert data.body == compiled_response.body


def test_login_failed() -> None:
    """_summary_
        Function in charge of testing the login failed function.
    """
    title = "Hello World"
    data = BRI.login_failed(title)
    resp = {}
    resp[CONST.JSON_TITLE] = title
    resp[CONST.JSON_MESSAGE] = "Login failed, invalid credentials or username."
    resp[CONST.JSON_ERROR] = "Invalid credentials or username."
    resp[CONST.JSON_LOGGED_IN] = False
    compiled_response = HCI.unauthorized(
        content=resp,
        content_type=CONST.CONTENT_TYPE,
        headers=RDI.json_header
    )
    assert data.status_code == compiled_response.status_code
    assert data.headers == compiled_response.headers
    assert data.body == compiled_response.body


def test_insuffisant_rights_invalid_token() -> None:
    """_summary_
        Function in charge of testing the insuffisant rights function.
    """
    title = "Hello World"
    data = BRI.insuffisant_rights(title, "not_a_token")
    resp = {}
    resp[CONST.JSON_TITLE] = title
    resp[CONST.JSON_MESSAGE] = "You do not have enough permissions to execute this endpoint."
    resp[CONST.JSON_ERROR] = "Insufficient rights for given account."
    resp[CONST.JSON_LOGGED_IN] = False
    compiled_response = HCI.forbidden(
        content=resp,
        content_type=CONST.CONTENT_TYPE,
        headers=RDI.json_header
    )
    assert data.status_code == compiled_response.status_code
    assert data.headers == compiled_response.headers
    assert data.body == compiled_response.body


def test_insuffisant_rights_valid_token() -> None:
    """_summary_
        Function in charge of testing the insuffisant rights function.
    """
    token = "some_token"
    RDI.user_data = {token: ""}
    title = "Hello World"
    data = BRI.insuffisant_rights(title, token)
    resp = {}
    resp[CONST.JSON_TITLE] = title
    resp[CONST.JSON_MESSAGE] = "You do not have enough permissions to execute this endpoint."
    resp[CONST.JSON_ERROR] = "Insufficient rights for given account."
    resp[CONST.JSON_LOGGED_IN] = True
    compiled_response = HCI.forbidden(
        content=resp,
        content_type=CONST.CONTENT_TYPE,
        headers=RDI.json_header
    )
    RDI.user_data = {}
    assert data.status_code == compiled_response.status_code
    assert data.headers == compiled_response.headers
    assert data.body == compiled_response.body
