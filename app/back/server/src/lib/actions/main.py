"""_summary_
    The main file of this section, in charge of the action processing
"""
from typing import Dict
from time import sleep
from random import uniform
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME

from ..components.runtime_data import RuntimeData

from .variables import Variables
from .logger import ActionLogger
from .action_management import ActionManagement
from .trigger_management import TriggerManagement


class ActionsMain:
    """_summary_
    """

    def __init__(self, runtime_data: RuntimeData, error: int = 84, success: int = 0, debug: bool = False):
        """_summary_
            Class in charge of processing the actions.

        Args:
            runtime_data (RuntimeData): _description_
            error (int, optional): _description_. Defaults to 84.
            success (int, optional): _description_. Defaults to 0.
            debug (bool, optional): _description_. Defaults to False.
        """
        # -------------------------- Inherited values --------------------------
        self.error = error
        self.debug = debug
        self.success = success
        self.runtime_data = runtime_data
        # ---------------------- The visual logger class  ----------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            SAVE_TO_FILE,
            FILE_NAME,
            FILE_DESCRIPTOR,
            debug=self.debug,
            logger=self.__class__.__name__
        )
        # -------------------------- Internal classes --------------------------
        self.variables: Variables = Variables(
            success=self.success,
            error=self.error,
            debug=self.debug
        )
        self.logger: ActionLogger = ActionLogger(
            runtime_data=self.runtime_data,
            success=self.success,
            error=self.error,
            debug=self.debug
        )

    def random_delay(self, max_value: float = 1) -> float:
        """_summary_
            Function in charge of generating a random delay.
        """
        delay = uniform(0, max_value)
        delay = int(delay * 100) / 100
        return delay

    def execute_actions(self) -> Dict[str, int]:
        """_summary_
            The function in charge of processing actions.

        Returns:
            int: _description_: The statuses of all the runs.
        """
        delay = self.random_delay(1)
        sleep(delay)
