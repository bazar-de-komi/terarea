"""_summary_
    File in charge of checking the trigger rules.
"""

from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME

from .variables import Variables
from ..components.runtime_data import RuntimeData


class TriggerManagement:
    """_summary_
    """

    def __init__(self, variable: Variables, runtime_data: RuntimeData, error: int = 84, success: int = 0, debug: bool = False):
        """_summary_
            This is the class in charge of checking the triggers and storing variables if required.

        Args:
            variable (Variables): _description_: The class variable in charge of tracking the variables for the runtime.
            runtime_data (RuntimeData): _description_: The class runtime data in charge of containing important connections.
            error (int, optional): _description_. Defaults to 84.: The error value
            success (int, optional): _description_. Defaults to 0.: The success value
            debug (bool, optional): _description_. Defaults to False.: Set to True if you wish to activate debug mode.
        """
        # -------------------------- Inherited values --------------------------
        self.variable: Variables = variable
        self.error: int = error
        self.debug: bool = debug
        self.success: int = success
        self.runtime_data: RuntimeData = runtime_data
        # ---------------------- The visual logger class  ----------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            SAVE_TO_FILE,
            FILE_NAME,
            FILE_DESCRIPTOR,
            debug=self.debug,
            logger=self.__class__.__name__
        )
