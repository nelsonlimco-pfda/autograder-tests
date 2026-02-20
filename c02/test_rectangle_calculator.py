from collections import namedtuple
import io
import importlib
import os
import sys

import pytest

from check_pfda.utils import (assert_script_exists, build_user_friendly_err)
from check_pfda.core import REPO_PATH
MODULE_NAME = "rectangle_calc"
ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS, REPO_PATH)


def test_input_output(monkeypatch):
    # patches the standard output to catch the output of print()
    test_inputs = ["12", "6"]
    expected = "Perimeter: 36.00 m\nArea: 72.00 m²\n"
    patch_stdout = io.StringIO()
    # Returns a new mock object which undoes any patching done inside
    # the with block on exit to avoid breaking pytest itself.
    with monkeypatch.context() as m:
        # patches the input()
        m.setattr('builtins.input', lambda prompt='': test_inputs.pop(0))
        m.setattr('sys.stdout', patch_stdout)
        sys.modules.pop(MODULE_NAME, None)
        mod = importlib.import_module(name=MODULE_NAME)
        mod.main()
    assert patch_stdout.getvalue() == expected, build_user_friendly_err(
        patch_stdout.getvalue(), expected)


def test_calculate_perimeter():
    # Manual parametrization as GitHub's python autograder does not support
    # pytest parameterization syntax.
    Parameter = namedtuple("Parameter", ["length", "width", "expected_output"])
    parameters = [Parameter(12, 6, 36.0),  # whole number test
                  Parameter(3.6, 13.7, 34.6),  # float number test
                  Parameter(0, 0, 0.0)]  # zero test
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    for param in parameters:
        actual = mod.calculate_perimeter(param.length, param.width)
        expected = param.expected_output
        assert actual == expected, build_user_friendly_err(actual, expected)


def test_calculate_area():
    # Manual parametrization as GitHub's python autograder does not support
    # pytest parameterization syntax.
    Parameter = namedtuple("Parameter", ["length", "width", "expected_output"])
    parameters = [Parameter(12, 6, 72.0),  # whole number test
                  Parameter(3.6, 13.7, 49.32),  # float number test
                  Parameter(0, 0, 0.0)]  # zero test
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    for param in parameters:
        actual = mod.calculate_area(param.length, param.width)
        expected = param.expected_output
        assert actual == expected, build_user_friendly_err(actual, expected)
