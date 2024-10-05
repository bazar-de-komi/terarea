##
# EPITECH PROJECT, 2024
# Desktop_pet
# File description:
# crons.py
##

"""
    File in charge of setting up the cron jobs for the server.
"""

from typing import Union, Any
from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerAlreadyRunningError, SchedulerNotRunningError
from display_tty import Disp, TOML_CONF, FILE_DESCRIPTOR, SAVE_TO_FILE, FILE_NAME


class BackgroundTasks:
    """_summary_
        This is the class that is in charge of scheduling background tasks that need to run on intervals
    """

    def __init__(self, success: int = 0, error: int = 84, debug: bool = False) -> None:
        # -------------------------- Inherited values --------------------------
        self.success: int = success
        self.error: int = error
        self.debug: bool = debug
        # ------------------------ The scheduler class  ------------------------
        self.scheduler = BackgroundScheduler()
        # ------------------------ The logging function ------------------------
        self.disp: Disp = Disp(
            TOML_CONF,
            FILE_DESCRIPTOR,
            SAVE_TO_FILE,
            FILE_NAME,
            debug=self.debug,
            logger=self.__class__.__name__
        )

    def safe_add_task(self, func: callable, args: Union[Any, None] = None, trigger: Union[str, Any] = "interval", seconds: int = 5) -> Union[int, Job]:
        """_summary_
            A non-crashing implementation of the add_task function.

        Args:
            func (callable): _description_: The function to be called when it is time to run the job
            args (Union[Any, None], optional): _description_. Defaults to None.: Arguments you wish to pass to the function when executed.
            trigger (Union[str, Any], optional): _description_. Defaults to "interval".
            seconds (int, optional): _description_. Defaults to 5. The amount of seconds to wait before executing the task again (I don't think it is effective for the cron option)

        Returns:
            Union[int, Job]: _description_: returns self.error if there was an error, otherwise, returns a Job instance.
        """
        try:
            return self.add_task(
                func=func,
                args=args,
                trigger=trigger,
                seconds=seconds
            )
        except ValueError as e:
            self.disp.log_error(
                f"Runtime Error for add_task. {e}",
                "safe_add_task"
            )
            return self.error

    def safe_start(self) -> int:
        """_summary_
            This function is in charge of starting the scheduler. In a non-breaking way.

        Returns:
            int: _description_: Will return self.success if it worked, otherwise self.error.
        """
        try:
            return self.start()
        except RuntimeError as e:
            self.disp.log_error(
                f"Runtime Error for start. {e}",
                "safe_start"
            )
            return self.error

    def safe_pause(self, pause: bool = True) -> int:
        """_summary_
            This function is in charge of pausing the scheduler. In a non-breaking way.

        Args:
            pause (bool, optional): _description_: This is the boolean that will determine if the scheduler should be paused or not. Defaults to True.

        Returns:
            int: _description_: Will return self.success if it worked, otherwise self.error
        """
        try:
            return self.pause(pause=pause)
        except RuntimeError as e:
            self.disp.log_error(
                f"Runtime Error for start. {e}",
                "safe_pause"
            )
            return self.error

    def safe_resume(self) -> int:
        """_summary_
            This function is in charge of resuming the scheduler. In a non-breaking way.

        Returns:
            int: _description_: Will return self.success if it worked, otherwise self.error.
        """
        try:
            return self.resume()
        except RuntimeError as e:
            self.disp.log_error(
                f"Runtime Error for start. {e}",
                "safe_resume"
            )
            return self.error

    def safe_stop(self, wait: bool = True) -> int:
        """_summary_
            This function is in charge of stopping the scheduler. In a non-breaking way.

        Args:
            wait (bool, optional): _description_: Wait for the running tasks to finish. Defaults to True.

        Returns:
            int: _description_: will return self.success if it succeeds, otherwise self.error
        """
        try:
            return self.stop(wait=wait)
        except RuntimeError as e:
            self.disp.log_error(
                f"Runtime Error for start. {e}",
                "safe_stop"
            )
            return self.error

    def add_task(self, func: callable, args: Union[Any, None] = None, trigger: Union[str, Any] = "interval",  seconds: int = 5) -> Union[Job, None]:
        """_summary_
            Function in charge of adding an automated call to functions that are meant to run in the background.
            They are meant to run on interval.

        Args:
            func (callable): _description_: The function to be called when it is time to run the job
            args (Union[Any, None], optional): _description_. Defaults to None.: Arguments you wish to pass to the function when executed.
            trigger (Union[str, Any], optional): _description_. Defaults to "interval".
            seconds (int, optional): _description_. Defaults to 5. The amount of seconds to wait before executing the task again (I don't think it is effective for the cron option)

        Returns:
            Union[int,Job]: _description_: will raise a ValueError when an error occurs, otherwise, returns an instance of Job. 
        """
        if callable(func) is False:
            self.disp.log_error(
                f"The provided function is not callable: {func}.",
                "add_task"
            )
            raise ValueError("The function must be callable.")
        if trigger is not None and isinstance(trigger, str) is False:
            self.disp.log_error(
                f"The provided trigger is not a string: {trigger}.",
                "add_task"
            )
            raise ValueError("The trigger must be a string.")
        return self.scheduler.add_job(
            func=func,
            trigger=trigger,
            seconds=seconds,
            args=args
        )

    def start(self) -> Union[int, None]:
        """_summary_
            The function in charge of starting the scheduler loop.

        Raises:
            RuntimeError: _description_: Will raise a runtile error if the underlying functions failled.

        Returns:
            Union[int, None]: _description_: Will return self.success if it worked, otherwise None because it will have raised an error.
        """
        try:
            self.scheduler.start()
            self.disp.log_info("Scheduler started...", "start")
            return self.success
        except SchedulerAlreadyRunningError:
            self.disp.log_info("Scheduler is already running...", "start")
            return self.success
        except RuntimeError as e:
            self.disp.log_error(
                f"An error occurred while starting the scheduler: {e}",
                "start"
            )
            raise RuntimeError(
                f"Error({self.__class__.__name__}): Failed to call the scheduler's start wrapper function."
            ) from e
        except Exception as e:
            self.disp.log_error(
                f"An error occurred while starting the scheduler: {e}", "start"
            )
            raise RuntimeError(
                f"Error({self.__class__.__name__}): Failed to call the scheduler's start wrapper function."
            ) from e

    def pause(self, pause: bool = True) -> Union[int, None]:
        """_summary_
            This function is in charge of pausing the scheduler if it was running.

        Args:
            pause (bool, optional): _description_: This is the boolean that will determine if the scheduler should be paused or not. Defaults to True.

        Returns:
            Union[int, None]: _description_: Will return self.success if it worked, otherwise None because it will have raised an error.
        """
        try:
            if pause is True:
                self.scheduler.pause()
                self.disp.log_info("Scheduler paused.", "pause")
            else:
                self.scheduler.resume()
                self.disp.log_info("Scheduler resumed.", "pause")
            return self.success
        except Exception as e:
            self.disp.log_error(
                f"An error occurred while pausing the scheduler: {e}",
                "pause"
            )
            raise RuntimeError(
                f"Error({self.__class__.__name__}): Failed to call the chron pause wrapper function."
            ) from e

    def resume(self) -> Union[int]:
        """_summary_
            This function is in charge of resuming the scheduler loop if it was paused.

        Returns:
            Union[int]: _description_: Will return self.success if it worked, otherwise None because it will have raised an error.
        """
        return self.pause(pause=False)

    def stop(self, wait: bool = True) -> Union[int, None]:
        """_summary_
            This function is responsible for shutting down the scheduler, terminating any running jobs, and optionally waiting for those jobs to complete before exiting.

        Args:
            wait (bool, optional): _description_. Defaults to True. Wait for the running tasks to finish.

        Raises:
            RuntimeError: _description_: The function failed to call the underlying processes that were required for it to run.

        Returns:
            Union[int, None]: _description_: will return self.success if it succeeds, or none if it raised an error.
        """
        try:
            self.scheduler.shutdown(wait=wait)
            self.disp.log_info("Scheduler stopped.", "stop")
            return self.success
        except SchedulerNotRunningError:
            self.disp.log_info("Scheduler is already stopped.", "stop")
            return self.success
        except Exception as e:
            self.disp.log_error(
                f"An error occurred while stopping the scheduler: {e}", "stop"
            )
            raise RuntimeError(
                f"Error({self.__class__.__name__}): Failed to call the chron stop wrapper function."
            ) from e


if __name__ == "__main__":
    import sys
    from time import sleep

    def hello_world() -> None:
        print("Hello, World!")

    def pending_world() -> None:
        print("Pending, World!")

    def goodbye_world() -> None:
        print("Goodbye, World!")

    print("Testing declared functions.")
    hello_world()
    pending_world()
    goodbye_world()
    print("Declared functions tested.")

    SUCCES = 0
    ERROR = 84
    DEBUG = True
    KIND_KILL = True
    NB_REPEATS = 2
    TRIGGER = "interval"
    SECONDS = 5
    NB_FUNCTIONS = 3
    MAIN_THREAD_DELAY = int((SECONDS*NB_FUNCTIONS)*NB_REPEATS)

    print(f"Statuses:\nSUCCESS = {SUCCES}, ERROR = {ERROR}")
    print(
        f"DEBUG = {DEBUG}, KIND_KILL = {KIND_KILL}, NB_REPEATS = {NB_REPEATS}"
    )
    print(
        f"TRIGGER = {TRIGGER}, SECONDS = {SECONDS}, NB_FUNCTIONS = {NB_FUNCTIONS}"
    )
    print(f"MAIN_THREAD_DELAY = {MAIN_THREAD_DELAY}")

    print("Initialising class BackgroundTasks.")
    BTI = BackgroundTasks(
        success=SUCCES,
        error=ERROR,
        debug=DEBUG
    )
    print("Class BackgroundTasks initialised.")

    print("Adding tasks to the scheduler.")
    status = BTI.safe_add_task(
        hello_world,
        None,
        TRIGGER,
        SECONDS
    )
    print(f"status {status}")
    status = BTI.safe_add_task(
        pending_world,
        None,
        TRIGGER,
        SECONDS*2
    )
    print(f"status {status}")
    status = BTI.add_task(
        goodbye_world,
        None,
        TRIGGER,
        SECONDS*3
    )
    print(f"status {status}")
    print("Added tasks to the scheduler.")

    print("Startins scheduler.")
    print(f"Status: {BTI.safe_start()}")
    print("Scheduler started.")
    print(f"Waiting {MAIN_THREAD_DELAY} on the main thread.")
    sleep(MAIN_THREAD_DELAY)
    print(f"Waited {MAIN_THREAD_DELAY} on the main thread.")
    print("Stopping scheduler.")
    status = BTI.safe_stop(KIND_KILL)
    print(f"Status: {status}")
    sys.exit(status)
