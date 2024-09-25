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
    from src.lib.components.runtime_data import RuntimeData
    from src.lib.components.endpoints_routes import Endpoints
    from src.lib.boilerplates.non_web import BoilerplateNonHTTP
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
BNHTTPI = BoilerplateNonHTTP(
    runtime_data_initialised=RDI,
    success=SUCCESS,
    error=ERROR,
    debug=False
)


def test_pause(monkeypatch: pytest.MonkeyPatch) -> None:
    """_summary_
        Function in charge of testing the pause function.
    """
    test = "Charlie"
    monkeypatch.setattr('builtins.input', lambda _: test)
    data = BNHTTPI.pause()
    assert data == test


def test_set_lifespan() -> None:
    """_summary_
        Function in charge of testing the set lifespan function.
    """
    delay = 42
    src: datetime = datetime.now() + timedelta(seconds=delay)
    data: datetime = BNHTTPI.set_lifespan(delay)
    assert data.strftime(
        "%d/%m/%Y, %H:%M:%S") == src.strftime("%d/%m/%Y, %H:%M:%S")


def test_generate_token() -> None:
    """_summary_
        Function in charge of testing the generate token function.
    """
    token = BNHTTPI.generate_token()
    assert isinstance(token, str)
    assert len(token) == 36
    assert token.count("-") == 4


def test_check_date_correct() -> None:
    """_summary_
        Function in charge of testing the check date function with a correct date.
    """
    assert BNHTTPI.check_date("11/09/2001") is True


def test_check_date_incorrect_day() -> None:
    """_summary_
        Function in charge of testing the check date function with an incorrect date.
    """
    assert BNHTTPI.check_date("32/01/2021") is False


def test_check_date_incorrect_month() -> None:
    """_summary_
        Function in charge of testing the check date function with an incorrect date.
    """
    assert BNHTTPI.check_date("12/13/2021") is False


def test_check_date_incorrect_year() -> None:
    """_summary_
        Function in charge of testing the check date function with an incorrect date.
    """
    assert BNHTTPI.check_date("12/12/2O21") is False


def test_check_incorrect_format() -> None:
    """_summary_
        Function in charge of testing the check date function with an incorrect date.
    """
    assert BNHTTPI.check_date("12-12-2021") is False
