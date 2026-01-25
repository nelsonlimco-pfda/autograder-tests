from check_pfda.utils import (assert_script_exists, build_user_friendly_err)
import io
import importlib
import sys


import pytest


MODULE_NAME = "timelapse_calc"
ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS)


def test_integer_input(monkeypatch):
    # patches the standard output to catch the output of print()
    test_inputs = ["24", "3", "4"]
    patch_stdout = io.StringIO()
    expected = "4min 48.0s (288.0s)\n"
    # Returns a new mock object which undoes any patching done inside
    # the with block on exit to avoid breaking pytest itself.
    with monkeypatch.context() as m:
        # patches the input()
        m.setattr('builtins.input', lambda prompt='': test_inputs.pop(0))
        m.setattr('sys.stdout', patch_stdout)
        sys.modules.pop(MODULE_NAME, None)
        importlib.import_module(name=MODULE_NAME)
    assert patch_stdout.getvalue() == expected, build_user_friendly_err(
        patch_stdout.getvalue(), expected)


def test_float_input(monkeypatch):
    # patches the standard output to catch the output of print()
    test_inputs = ["29.97", "3.5", "4.6"]
    patch_stdout = io.StringIO()
    expected = "8min 2.5s (482.5s)\n"
    # Returns a new mock object which undoes any patching done inside
    # the with block on exit to avoid breaking pytest itself.
    with monkeypatch.context() as m:
        # patches the input()
        m.setattr('builtins.input', lambda prompt='': test_inputs.pop(0))
        m.setattr('sys.stdout', patch_stdout)
        sys.modules.pop(MODULE_NAME, None)
        importlib.import_module(name=MODULE_NAME)
    assert patch_stdout.getvalue() == expected, build_user_friendly_err(
        patch_stdout.getvalue(), expected)


def test_zeroes_input(monkeypatch):
    # patches the standard output to catch the output of print()
    test_inputs = ["0", "0", "0"]
    patch_stdout = io.StringIO()
    expected = "0min 0.0s (0.0s)\n"
    # Returns a new mock object which undoes any patching done inside
    # the with block on exit to avoid breaking pytest itself.
    with monkeypatch.context() as m:
        # patches the input()
        m.setattr('builtins.input', lambda prompt='': test_inputs.pop(0))
        m.setattr('sys.stdout', patch_stdout)
        sys.modules.pop(MODULE_NAME, None)
        importlib.import_module(name=MODULE_NAME)
    assert patch_stdout.getvalue() == expected, build_user_friendly_err(
        patch_stdout.getvalue(), expected)
