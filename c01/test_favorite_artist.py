import io
import importlib
import sys

from check_pfda.utils import (assert_script_exists, build_user_friendly_err)
from check_pfda.core import REPO_PATH

MODULE_NAME = "favorite_artist"
ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS, REPO_PATH)


def test_string_input(monkeypatch):
    # patches the standard output to catch the output of print()
    test_inputs = ["Pablo Picasso", "painter",
                   "Girl Before A Mirror", "complex", "colorful"]
    patch_stdout = io.StringIO()
    expected = "Pablo Picasso is my favorite painter!\nMy favorite work from Pablo Picasso is Girl Before A Mirror.\nI love it, because it is so complex and colorful!\n"
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


def test_converts_to_appropriate_case(monkeypatch):
    # patches the standard output to catch the output of print()
    test_inputs = ["christoPHer noLAN", "Director",
                   "Interstellar", "gRaNd", "inteRestiNg"]
    patch_stdout = io.StringIO()
    expected = "Christopher Nolan is my favorite director!\nMy favorite work from Christopher Nolan is Interstellar.\nI love it, because it is so grand and interesting!\n"
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


def test_special_char_numbers_input(monkeypatch):
    # patches the standard output to catch the output of print()
    test_inputs = ["haya0 miyazak!", "An1ma+0r",
                   "princes5 monok3", "Thou&ht-pr0voking", "M3an’ngful"]
    patch_stdout = io.StringIO()
    expected = "Haya0 Miyazak! is my favorite an1ma+0r!\nMy favorite work from Haya0 Miyazak! is Princes5 Monok3.\nI love it, because it is so thou&ht-pr0voking and m3an’ngful!\n"
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


def test_blank_input(monkeypatch):
    # patches the standard output to catch the output of print()
    test_inputs = ["", "", "", "", ""]
    patch_stdout = io.StringIO()
    expected = " is my favorite !\nMy favorite work from  is .\nI love it, because it is so  and !\n"
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
