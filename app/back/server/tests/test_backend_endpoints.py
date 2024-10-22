##
# EPITECH PROJECT, 2024
# Desktop_pet (Workspace)
# File description:
# test_character_server.py
##

"""_summary_
This file is in charge of testing the endpoints of the character server.
"""

import os
import sys
import time
import json
import asyncio
from random import randint
from typing import Dict
from threading import Thread

import pytest

from status_check import QueryStatus
from query_boilerplate import QueryEndpoint
import constants as TCONST

sys.path.append(os.getcwd())


try:
    from src import Server
    from src import CONST
except ImportError as e:
    raise ImportError("Failed to import the src module") from e


def pytest_configure(config: pytest.Config):
    """_summary_
        This function is called when the pytest configuration is being set up.
    Args:
        config (pytest.Config): _description_
    """
    config.addinivalue_line(
        "markers",
        "critical: mark test as critical to determine final server stop"
    )
    config.addinivalue_line(
        "markers",
        "last: mark test to run after all other tests"
    )


@pytest.fixture(scope="module")
def setup_environment(request: pytest.FixtureRequest):
    """Fixture for setting up the environment once per module."""

    query: QueryEndpoint = QueryEndpoint(
        host=TCONST.QUERY_HOST,
        port=TCONST.PORT,
        delay=TCONST.QUERY_DELAY
    )

    status: QueryStatus = QueryStatus()

    server: Server = Server(
        host=TCONST.SERVER_HOST,
        port=TCONST.PORT,
        success=TCONST.SUCCESS,
        error=TCONST.ERROR,
        app_name="Area",
        debug=TCONST.DEBUG
    )

    active_thread: Thread = Thread(
        target=server.main,
        daemon=True, name=f"{TCONST.APP_NAME}_server_thread"
    )
    active_thread.start()

    # Let the server start
    print("Waiting for server to start (5 seconds delay)...")
    time.sleep(5)
    if active_thread.is_alive() is not True:
        pytest.skip("(test_server) thread failed to start")
    if server.is_running() is not True:
        pytest.skip("(test_server) Server is not running")
    call = server.runtime_data_initialised.database_link.get_table_names()
    if isinstance(call, int) and call == server.error:
        pytest.skip(
            "(test_server) Server failed to connect to the database"
        )
    print("Server started.")

    async def teardown():
        if server is not None:
            print("Shutting down server...")
            server.stop_server()
            print("Server stopped")
        if active_thread.is_alive() is True:
            print("Stopping thread (5 seconds grace) ...")
            active_thread.join(timeout=5)
            print("Thread stopped.")
        else:
            print("Thread already stopped.")
        return TCONST.SUCCESS

    def teardown_sync():
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(teardown())

    request.addfinalizer(teardown_sync)

    return {
        "query": query,
        "status": status,
        "server": server,
        "success": TCONST.SUCCESS,
        "error": TCONST.ERROR,
        "thread": active_thread,
        "tokens": {
            TCONST.LAMBDA_USER_TOKEN_KEY: "",
            TCONST.ADMIN_USER_TOKEN_KEY: ""
        },
        "accounts": {
            "lambda_user": {
                "normal": {
                    "email": f"endpoint_{TCONST.USER_DATA_EMAIL}",
                    "password": f"endpoint_{TCONST.USER_DATA_PASSWORD}",
                    "username": f"endpoint_{TCONST.USER_DATA_USERNAME}",
                    "method": f"{TCONST.USER_DATA_METHOD}",
                    "favicon": f"{TCONST.USER_DATA_FAVICON}",
                    "admin": f"{TCONST.USER_DATA_ADMIN}"
                },
                "put": {
                    "email": f"endpoint_{TCONST.USER_DATA_EMAIL_REBIND}",
                    "password": f"endpoint_{TCONST.USER_DATA_PASSWORD_REBIND}",
                    "username": f"endpoint_{TCONST.USER_DATA_USERNAME_REBIND}",
                    "method": f"{TCONST.USER_DATA_METHOD}",
                    "favicon": f"{TCONST.USER_DATA_FAVICON}",
                    "admin": f"{TCONST.USER_DATA_ADMIN}"
                },
                "patch": {
                    "email": f"endpoint_{TCONST.USER_DATA_EMAIL_PATCH}",
                    "password": f"endpoint_{TCONST.USER_DATA_PASSWORD_PATCH}",
                    "username": f"endpoint_{TCONST.USER_DATA_USERNAME_PATCH}",
                    "method": f"{TCONST.USER_DATA_METHOD}",
                    "favicon": f"{TCONST.USER_DATA_FAVICON}",
                    "admin": f"{TCONST.USER_DATA_ADMIN}"
                }
            },
            "admin_user": {
                "normal": {
                    "email": f"endpoint_{TCONST.ADMIN_DATA_EMAIL}",
                    "password": f"endpoint_{TCONST.ADMIN_DATA_PASSWORD}",
                    "username": f"endpoint_{TCONST.ADMIN_DATA_USERNAME}",
                    "method": f"{TCONST.USER_DATA_METHOD}",
                    "favicon": f"{TCONST.USER_DATA_FAVICON}",
                    "admin": f"{TCONST.USER_DATA_ADMIN}"
                },
                "put": {
                    "email": f"endpoint_{TCONST.ADMIN_DATA_EMAIL_REBIND}",
                    "password": f"endpoint_{TCONST.ADMIN_DATA_PASSWORD_REBIND}",
                    "username": f"endpoint_{TCONST.ADMIN_DATA_USERNAME_REBIND}",
                    "method": f"{TCONST.USER_DATA_METHOD}",
                    "favicon": f"{TCONST.USER_DATA_FAVICON}",
                    "admin": f"{TCONST.USER_DATA_ADMIN}"
                },
                "patch": {
                    "email": f"endpoint_{TCONST.ADMIN_DATA_EMAIL_PATCH}",
                    "password": f"endpoint_{TCONST.ADMIN_DATA_PASSWORD_PATCH}",
                    "username": f"endpoint_{TCONST.ADMIN_DATA_USERNAME_PATCH}",
                    "method": f"{TCONST.USER_DATA_METHOD}",
                    "favicon": f"{TCONST.USER_DATA_FAVICON}",
                    "admin": f"{TCONST.USER_DATA_ADMIN}"
                }
            }
        },
        "critical_failed": False,
        "teardown_func": teardown_sync
    }


@pytest.mark.usefixtures("setup_environment")
class TestServer:
    """Class for running tests on the character server endpoint."""

    def check_server(self, setup_environment, critical: bool = False):
        """Helper function to check if the server is still running."""
        server: Server = setup_environment["server"]
        if server is None or setup_environment["critical_failed"] is True:
            if critical is True:
                setup_environment["critical_failed"] = True
            pytest.skip(
                "(test_server) Server is not running, skipping the test."
            )

    def test_home(self, setup_environment):
        """ Test the / endpoint of the server. """
        self.check_server(setup_environment)

        query: QueryEndpoint = setup_environment["query"]
        status: QueryStatus = setup_environment["status"]
        response = query.get_endpoint(TCONST.GET_HOME)
        assert status.success(response) is True
        assert TCONST.are_json_responses_identical(
            response.json(),
            TCONST.GET_HOME_RESPONSE_NOT_LOGGED_IN,
            "test_home"
        ) is True

    @pytest.mark.critical
    def test_post_register_lambda(self, setup_environment):
        """_summary_
            Test the /register endpoint of the server.
        Args:
            setup_environment (_type_): _description_
        """
        self.check_server(setup_environment, True)
        path = TCONST.PUT_REGISTER
        query: QueryEndpoint = setup_environment["query"]
        status: QueryStatus = setup_environment["status"]
        accounts: Dict[
            str, any
        ] = setup_environment["accounts"]["lambda_user"]["normal"]
        body = {
            "email": accounts["email"],
            "password": accounts["password"]
        }
        TCONST.IDISP.log_info(f"body = {body}")
        response = query.post_endpoint(path, content=body)
        TCONST.IDISP.log_info(f"response.json() = {response.json()}")
        assert status.success(response) is True
        assert TCONST.are_json_responses_identical(
            response.json(),
            TCONST.POST_REGISTER,
            "test_post_register_lambda"
        ) is True

    @pytest.mark.critical
    def test_post_login_lambda(self, setup_environment):
        """_summary_
            Test the /login endpoint of the server.
        Args:
            setup_environment (_type_): _description_
        """
        self.check_server(setup_environment, True)
        path = TCONST.POST_LOGIN
        token: Dict[str, Dict[str, str]] = setup_environment["tokens"]
        query: QueryEndpoint = setup_environment["query"]
        status: QueryStatus = setup_environment["status"]
        accounts: Dict[
            str, any
        ] = setup_environment["accounts"]["lambda_user"]["normal"]
        body = {
            "email": accounts["email"],
            "password": accounts["password"]
        }
        TCONST.IDISP.log_info(f"body = {body}")
        response = query.post_endpoint(path, content=body)
        TCONST.IDISP.log_info(f"response.json() = {response.json()}")
        if status.success(response) is True:
            msg = f"Bearer {response.json()['token']}"
            token[TCONST.LAMBDA_USER_TOKEN_KEY] = msg
        else:
            setup_environment["critical_failed"] = True
        correct_node = TCONST.POST_LOGIN
        correct_node['msg'] = f"Welcome {accounts['username']}"
        correct_node["token"] = token[TCONST.LAMBDA_USER_TOKEN_KEY]
        assert status.success(response) is True
        assert TCONST.are_json_responses_identical(
            response.json(),
            correct_node,
            "test_post_login_lambda"
        ) is True

    @pytest.mark.critical
    def test_post_register_admin(self, setup_environment):
        """_summary_
            Test the /register endpoint of the server.
        Args:
            setup_environment (_type_): _description_
        """
        self.check_server(setup_environment, True)
        server: Server = setup_environment["server"]
        path = TCONST.PUT_REGISTER
        query: QueryEndpoint = setup_environment["query"]
        status: QueryStatus = setup_environment["status"]
        accounts: Dict[
            str, any
        ] = setup_environment["accounts"]["admin_user"]["normal"]
        body = {
            "email": accounts["email"],
            "password": accounts["password"]
        }
        TCONST.IDISP.log_info(f"body = {body}")
        response = query.post_endpoint(path, content=body)
        TCONST.IDISP.log_info(f"response.json() = {response.json()}")
        if status.success(response) is True:
            column = server.runtime_data_initialised.database_link.get_table_column_names(
                CONST.TAB_ACCOUNTS
            )
            if column == server.error or len(column) == 0:
                setup_environment["critical_failed"] = True
                assert column == server.success
            user_node = server.runtime_data_initialised.database_link.get_data_from_table(
                CONST.TAB_ACCOUNTS,
                column,
                f"email='{accounts['email']}'"
            )
            if user_node == server.error:
                setup_environment["critical_failed"] = True
                assert user_node == server.success
            column.pop(0)
            user_node[0].pop("id")
            user_node[0]['admin'] = str(TCONST.ADMIN_DATA_ADMIN)
            user_node_list = list(user_node[0].values())
            msg = f"user_node_list = {user_node_list}\n"
            msg += f"user_node = {user_node}"
            server.disp.log_debug(msg, "test_post_register_admin")
            command_status = server.runtime_data_initialised.database_link.update_data_in_table(
                CONST.TAB_ACCOUNTS,
                user_node_list,
                column,
                f"email='{accounts['email']}'"
            )
            assert command_status == server.success
        assert status.success(response) is True
        assert TCONST.are_json_responses_identical(
            response.json(),
            TCONST.POST_REGISTER,
            "test_post_register_admin"
        ) is True

    @pytest.mark.critical
    def test_post_login_admin(self, setup_environment):
        """_summary_
            Test the /login endpoint of the server.
        Args:
            setup_environment (_type_): _description_
        """
        self.check_server(setup_environment, True)
        path = TCONST.POST_LOGIN
        token: Dict[str, Dict[str, str]] = setup_environment["tokens"]
        query: QueryEndpoint = setup_environment["query"]
        status: QueryStatus = setup_environment["status"]
        accounts: Dict[
            str, any
        ] = setup_environment["accounts"]["admin_user"]["normal"]
        body = {
            "email": accounts["email"],
            "password": accounts["password"]
        }
        TCONST.IDISP.log_info(f"body = {body}")
        response = query.post_endpoint(path, content=body)
        TCONST.IDISP.log_info(f"response.json() = {response.json()}")
        if status.success(response) is True:
            msg = f"Bearer {response.json()['token']}"
            token[TCONST.ADMIN_USER_TOKEN_KEY] = msg
        else:
            setup_environment["critical_failed"] = True
        correct_node = TCONST.POST_LOGIN
        correct_node['msg'] = f"Welcome {accounts['username']}"
        correct_node["token"] = token[TCONST.ADMIN_USER_TOKEN_KEY]
        assert status.success(response) is True
        assert TCONST.are_json_responses_identical(
            response.json(),
            correct_node,
            "test_post_login_admin"
        ) is True

    def test_put_user_lambda(self, setup_environment):
        """_summary_
            Test the /user endpoint of the server.
        Args:
            setup_environment (_type_): _description_
        """
        self.check_server(setup_environment)
        path = TCONST.PUT_USER
        query: QueryEndpoint = setup_environment["query"]
        status: QueryStatus = setup_environment["status"]
        token: Dict[str, Dict[str, str]] = setup_environment["tokens"]
        accounts: Dict[
            str, any
        ] = setup_environment["accounts"]["lambda_user"]["put"]
        body = {
            "username": accounts["username"],
            "email": accounts["email"],
            "password": accounts["password"]
        }
        response = query.put_endpoint(
            path, content=body, token=token[TCONST.LAMBDA_USER_TOKEN_KEY]
        )
        assert status.success(response) is True
        assert TCONST.are_json_responses_identical(
            response.json(),
            TCONST.PUT_USER_RESPONSE,
            "test_put_user_lambda"
        ) is True

    def test_put_user_admin(self, setup_environment):
        """_summary_
            Test the /user endpoint of the server.
        Args:
            setup_environment (_type_): _description_
        """
        self.check_server(setup_environment)
        path = TCONST.PUT_USER
        query: QueryEndpoint = setup_environment["query"]
        status: QueryStatus = setup_environment["status"]
        token: Dict[str, Dict[str, str]] = setup_environment["tokens"]
        accounts: Dict[
            str, any
        ] = setup_environment["accounts"]["admin_user"]["put"]
        body = {
            "username": accounts["username"],
            "email": accounts["email"],
            "password": accounts["password"]
        }
        response = query.put_endpoint(
            path, content=body, token=token[TCONST.LAMBDA_USER_TOKEN_KEY]
        )
        assert status.success(response) is True
        assert TCONST.are_json_responses_identical(
            response.json(),
            TCONST.PUT_USER_RESPONSE,
            "test_put_user_admin"
        ) is True

    # @pytest.mark.last
    # def test_post_stop_server(self, setup_environment):
    #     """ Test the /stop endpoint of the server. """
    #     self.check_server(setup_environment)
    #     teardown_func: callable = setup_environment["teardown_func"]
    #     success: int = setup_environment["success"]
    #     status = teardown_func()
    #     assert status == success
