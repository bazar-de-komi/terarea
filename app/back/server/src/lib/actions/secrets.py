"""_summary_
    File in charge of tracking secrets for a given check
"""

from typing import Dict, Any
from datetime import datetime, timezone
from .variables import Variables


class Secrets:
    """_summary_
    This class is in charge of storing the secrets for the server.
    """

    def __init__(self, success: int = 0, error: int = 84, debug: bool = False) -> None:
        """_summary_
            Class in charge of managing the secrets for the server runtime trigger and consequences.

        Args:
            success (int, optional): _description_. Defaults to 0.
            error (int, optional): _description_. Defaults to 84.
            debug (bool, optional): _description_. Defaults to False.
        """
        self.debug: bool = debug
        self.success: int = success
        self.error: int = error

        self.vars: Variables = Variables(
            success=self.success,
            error=self.error,
            debug=self.debug
        )

    def get_secret(self, secret_name: str) -> Dict[str, Any]:
        """_summary_
            Get the secret from the server.

        Args:
            secret_name (str): _description_

        Returns:
            Dict[str, Any]: _description_
        """
        return self.vars.get_variable(secret_name)

    def set_token(self, token: str) -> None:
        """_summary_
            Set the token for the server.

        Args:
            token (str): _description_
        """
        self.vars.insert_or_update("token", token)
        self.vars.insert_or_update("bearer", f"Bearer {token}")

    def get_token(self) -> str:
        """_summary_
            Get the token for the server.

        Returns:
            str: _description_
        """
        return self.vars.get_variable("token")

    def get_bearer(self) -> str:
        """_summary_
            Get the bearer for the server.

        Returns:
            str: _description_
        """
        return self.vars.get_variable("bearer")

    def now(self):
        """_summary_
        Get the current time.
        """
        return datetime.now().isoformat()

    def current_date(self):
        """_summary_
            $ref{secrets.current_date}: Returns the current date without the time in the server's local timezone

        Returns:
            _type_: _description_
        """
        return datetime.now().date().isoformat()

    def current_time(self):
        """_summary_
            $ref{secrets.current_time}: Returns the current time (hours:minutes:seconds) in the server's local timezone

        Returns:
            _type_: _description_
        """
        return datetime.now().time().replace(microsecond=0).isoformat()

    def now_utc(self):
        """_summary_
            $ref{secrets.now_utc}: Returns the current datetime in UTC with timezone info

        Returns:
            _type_: _description_
        """
        return datetime.now(timezone.utc).isoformat()

    def current_date_utc(self):
        """_summary_
            $ref{secrets.current_date_utc}: Returns the current date without the time in UTC

        Returns:
            _type_: _description_
        """
        return datetime.now(timezone.utc).date().isoformat()

    def current_time_utc(self):
        """_summary_
            $ref{secrets.current_time_utc}: Returns the current time (hours:minutes:seconds) in UTC

        Returns:
            _type_: _description_
        """
        return datetime.now(timezone.utc).time().replace(microsecond=0).isoformat()

    def now_server(self):
        """_summary_
            $ref{secrets.now_server}: Returns the current datetime with timezone info in the server's local timezone

        Returns:
            _type_: _description_
        """
        return datetime.now().astimezone().isoformat()

    def current_date_server(self):
        """_summary_
            $ref{secrets.current_date_server}: Returns the current date without the time in the server's local timezone

        Returns:
            _type_: _description_
        """
        return datetime.now().astimezone().date().isoformat()

    def current_time_server(self):
        """_summary_
            $ref{secrets.current_time_server}: Returns the current time (hours:minutes:seconds) in the server's local timezone

        Returns:
            _type_: _description_
        """
        return datetime.now().astimezone().time().replace(microsecond=0).isoformat()
