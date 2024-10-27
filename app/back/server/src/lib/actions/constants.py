"""_summary_
    This file contains the constants for the actions program.
    These are used to standardise error logging and other sections of the program.
"""

import operator

# ---------------------------------- log type ----------------------------------

TYPE_API = "API"
TYPE_SERVICE = "SERVICE"
TYPE_ACTION = "ACTION"
TYPE_UNDEFINED = "UNDEFINED"
TYPE_MISMATCH = "MISMATCH"
TYPE_BEFORE_ASSIGNEMENT = "REFERENCED BEFORE ASSIGNEMENT"
TYPE_DIV_ZERO = "DIVISION BY ZERO"
TYPE_SYNTAX_ERROR = "SYNTAX ERROR"
TYPE_RUNTIME_ERROR = "RUNTIME ERROR"
TYPE_INCOMPARABLE = "INCOMPARABLE TYPES"
TYPE_OVERFLOW = "VALUE OVERFLOW"
TYPE_UNDERFLOW = "VALUE UNDERFLOW"

# -------------------------------- Error codes  --------------------------------

CODE_INFO = 0
CODE_SUCCESS = 1
CODE_DEBUG = 2
CODE_WARNING = 3
CODE_ERROR = 4
CODE_CRITICAL = 5
CODE_FATAL = 6

# -------------------------------- Error level  --------------------------------

LEVEL_INFO = "INFO"
LEVEL_SUCCESS = "SUCCESS"
LEVEL_DEBUG = "DEBUG"
LEVEL_WARNING = "WARNING"
LEVEL_ERROR = "ERROR"
LEVEL_CRITICAL = "CRITICAL"
LEVEL_FATAL = "FATAL"

# ------------------------------- Error messages -------------------------------

MSG_INFO = "Information: Operation executed without any issues."
MSG_SUCCESS = "Success: Operation completed successfully."
MSG_DEBUG = "Debug: Tracking detailed operational data for diagnostics."
MSG_WARNING = "Warning: Potential issue detected. Review is recommended."
MSG_ERROR = "Error: Operation could not be completed successfully."
MSG_CRITICAL = "Critical: Immediate attention required to prevent severe impact."
MSG_FATAL = "Fatal: System failure imminent. Immediate intervention necessary."

# ----------------------------- Error equivalence  -----------------------------

LOG_EQUIVALENCE = {
    CODE_INFO: LEVEL_INFO,
    CODE_SUCCESS: LEVEL_SUCCESS,
    CODE_DEBUG: LEVEL_DEBUG,
    CODE_WARNING: LEVEL_WARNING,
    CODE_ERROR: LEVEL_ERROR,
    CODE_CRITICAL: LEVEL_CRITICAL,
    CODE_FATAL: LEVEL_FATAL,
}

LOG_MESSAGE_EQUIVALENCE = {
    CODE_INFO: MSG_INFO,
    CODE_SUCCESS: MSG_SUCCESS,
    CODE_DEBUG: MSG_DEBUG,
    CODE_WARNING: MSG_WARNING,
    CODE_ERROR: MSG_ERROR,
    CODE_CRITICAL: MSG_CRITICAL,
    CODE_FATAL: MSG_FATAL,
}

# -------------------------------- List checks  --------------------------------

LIST_TYPE = [
    TYPE_API,
    TYPE_SERVICE,
    TYPE_ACTION,
    TYPE_UNDEFINED,
    TYPE_MISMATCH,
    TYPE_BEFORE_ASSIGNEMENT,
    TYPE_DIV_ZERO,
    TYPE_SYNTAX_ERROR,
    TYPE_RUNTIME_ERROR,
    TYPE_INCOMPARABLE,
    TYPE_OVERFLOW,
    TYPE_UNDERFLOW
]

LIST_CODE = [
    CODE_INFO,
    CODE_SUCCESS,
    CODE_DEBUG,
    CODE_WARNING,
    CODE_ERROR,
    CODE_CRITICAL,
    CODE_FATAL
]

LIST_LEVEL_INFO = [
    LEVEL_INFO,
    LEVEL_SUCCESS,
    LEVEL_DEBUG,
    LEVEL_WARNING,
    LEVEL_ERROR,
    LEVEL_CRITICAL,
    LEVEL_FATAL
]

LIST_MSG = [
    MSG_INFO,
    MSG_SUCCESS,
    MSG_DEBUG,
    MSG_WARNING,
    MSG_ERROR,
    MSG_CRITICAL,
    MSG_FATAL
]

# ---------------------------- Operator equivalence ----------------------------


def _spaceship(a, b) -> int:
    """Compares two values and returns:
        -1 if a < b
         0 if a == b
         1 if a > b

    Args:
        a: The first value to compare.
        b: The second value to compare.

    Returns:
        int: -1, 0, or 1 based on the comparison.
    """
    if a < b:
        return -1
    if a == b:
        return 0
    return 1


OPERATOR_EXCHANGE = {
    "==": operator.eq,
    "===": operator.eq,
    "=": operator.eq,  # Bash string equality
    "eq": operator.eq,
    "-eq": operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,  # Not equal in SQL-like contexts
    "ne": operator.ne,
    "-ne": operator.ne,
    "<": operator.lt,
    "lt": operator.lt,
    "-lt": operator.lt,
    ">": operator.gt,
    "gt": operator.gt,
    "-gt": operator.gt,
    "<=": operator.le,
    "le": operator.le,
    "-le": operator.le,
    ">=": operator.ge,
    "ge": operator.ge,
    "-ge": operator.ge,
    "<=>": _spaceship,  # Custom spaceship operator
    "equal to": operator.eq,
    "less than": operator.lt,
    "not equal to": operator.ne,
    "greater than": operator.gt,
    "less than or equal to": operator.le,
    "greater than or equal to": operator.ge,
}
