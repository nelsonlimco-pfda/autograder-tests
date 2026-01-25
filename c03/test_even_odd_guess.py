from collections import namedtuple
import importlib
import sys
from check_pfda.utils import (assert_script_exists, build_user_friendly_err)
from check_pfda.core import REPO_PATH


MODULE_NAME = "even_odd_guess"
ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS, REPO_PATH)


def test_is_odd():
    Parameter = namedtuple(
        "Parameter",
        ["test_input", "expected_output"]
    )
    parameters = [Parameter(0, False),  # test base case 0
                  Parameter(1, True),  # test base case 1
                  Parameter(105, True),  # test arbitrary odd
                  Parameter(998, False)]  # test arbitrary even
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    for param in parameters:
        actual = mod.is_odd(param.test_input)
        expected = param.expected_output
        assert actual == expected, build_user_friendly_err(actual, expected)


def test_check_guess():
    Parameter = namedtuple(
        "Parameter",
        ["secret_number", "guess", "expected_output"]
    )
    parameters = [Parameter(1, "odd", True),  # 1 is odd
                  Parameter(0, "even", True),  # 0 is even
                  Parameter(7, "even", False),  # 7 is not even
                  Parameter(8, "odd", False)]  # 8 is not odd
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    for param in parameters:
        actual = mod.check_guess(param.secret_number, param.guess)
        expected = param.expected_output
        assert actual == expected, build_user_friendly_err(actual, expected)
