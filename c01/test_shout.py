from check_pfda.utils import (assert_script_exists, build_user_friendly_err)
import io
import importlib
import sys


import pytest

from check_pfda.core import REPO_PATH
MODULE_NAME = "shout"
ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS, REPO_PATH)


def test_alphabets_only(monkeypatch, test_input='hey', expected='HEY\n'):
    # patches the standard output to catch the output of print()
    patch_stdout = io.StringIO()
    # Returns a new mock object which undoes any patching done inside
    # the with block on exit to avoid breaking pytest itself.
    with monkeypatch.context() as m:
        m.setattr('sys.stdout', patch_stdout)
        # patches the input()
        patch_input = lambda prompt="": test_input
        m.setattr('builtins.input', patch_input)
        sys.modules.pop(MODULE_NAME, None)
        importlib.import_module(name=MODULE_NAME)
    assert patch_stdout.getvalue() == expected, build_user_friendly_err(
        patch_stdout.getvalue(), expected)


def test_alphabets_numbers_and_special_chars(monkeypatch,
                                             test_input='pfda is #1!', expected='PFDA IS #1!\n'):
    # patches the standard output to catch the output of print()
    patch_stdout = io.StringIO()
    # Returns a new mock object which undoes any patching done inside
    # the with block on exit to avoid breaking pytest itself.
    with monkeypatch.context() as m:
        m.setattr('sys.stdout', patch_stdout)
        # patches the input()
        patch_input = lambda prompt="": test_input
        m.setattr('builtins.input', patch_input)
        sys.modules.pop(MODULE_NAME, None)
        importlib.import_module(name=MODULE_NAME)
    assert patch_stdout.getvalue() == expected, build_user_friendly_err(
        patch_stdout.getvalue(), expected)


def test_numbers_and_special_chars(monkeypatch,
                                   test_input='123!', expected='123!\n'):
    # patches the standard output to catch the output of print()
    patch_stdout = io.StringIO()
    # Returns a new mock object which undoes any patching done inside
    # the with block on exit to avoid breaking pytest itself.
    with monkeypatch.context() as m:
        m.setattr('sys.stdout', patch_stdout)
        # patches the input()
        patch_input = lambda prompt="": test_input
        m.setattr('builtins.input', patch_input)
        sys.modules.pop(MODULE_NAME, None)
        importlib.import_module(name=MODULE_NAME)
    assert patch_stdout.getvalue() == expected, build_user_friendly_err(
        patch_stdout.getvalue(), expected)
