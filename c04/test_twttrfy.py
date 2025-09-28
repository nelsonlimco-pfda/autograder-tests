import importlib
import os
import sys


from check_pfda.utils import (assert_script_exists, build_user_friendly_err,
                              get_module_in_src)

MODULE_NAME = get_module_in_src()
ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS)


def test_removed_vowels():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = ("Gd Mrnng")
    actual = mod.twitterfy("Good Morning")
    assert actual == expected_output, build_user_friendly_err(actual, expected_output)

def test_first_letter_vowel():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = ("Pythn is th bst")
    actual = mod.twitterfy("Python is the best")
    assert actual == expected_output, build_user_friendly_err(actual, expected_output)

def test_numbers_and_special_characters():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = ("1234567890!@#$%^&*()-=_+~`[]|;:',.<>?/")
    actual = mod.twitterfy("1234567890!@#$%^&*()-=_+~`[]|;:',.<>?/")
    assert actual == expected_output, build_user_friendly_err(actual, expected_output)

def test_empty_input():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = ("")
    actual = mod.twitterfy("")
    assert actual == expected_output, build_user_friendly_err(actual, expected_output)