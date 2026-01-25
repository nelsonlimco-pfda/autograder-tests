from collections import namedtuple

import io
import importlib
import sys

from check_pfda.utils import (assert_script_exists, build_user_friendly_err)
import pytest


MODULE_NAME = "render_calc"
ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS)


def test_input_output(monkeypatch):
    # patches the standard output to catch the output of print()
    test_inputs = ["4", "24", "30"]
    expected = "48min 0.0s (2880.0s)\n"
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


def test_calc_render_time():
    Parameter = namedtuple("Parameter",
                           ["duration", "fps", "ave_render_time", "expected_output"])
    parameters = [Parameter(4, 24, 30, 2880.0),  # whole num
                  Parameter(1.5, 60.0, 10.5, 945.0),  # float num
                  # round up frames & single decimal
                  Parameter(1.55, 29.97, 10.84, 509.5),
                  Parameter(0, 0, 0, 0.0)]  # zero
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    for param in parameters:
        actual = mod.calc_render_time(param.duration,
                                      param.fps,
                                      param.ave_render_time)
        expected = param.expected_output
        assert actual == expected, build_user_friendly_err(actual, expected)


def test_sec_to_min_sec():
    Parameter = namedtuple("Parameter", ["duration",
                                         "expected_output"])
    parameters = [Parameter(2880, "48min 0.0s"),  # whole num
                  Parameter(945.0, "15min 45.0s"),  # float num
                  # round up frames & single decimal
                  Parameter(509.5, "8min 29.5s"),
                  Parameter(0.0, "0min 0.0s")]  # zero
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    for param in parameters:
        actual = mod.sec_to_min_sec(param.duration)
        expected = param.expected_output
        assert actual == expected, build_user_friendly_err(actual, expected)
