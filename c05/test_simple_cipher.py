import io
import importlib
import sys


from check_pfda.utils import (assert_script_exists, build_user_friendly_err)

MODULE_NAME = "simple_cipher"
ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS)


def test_main_empty_input_produces_correct_output(monkeypatch):
    """GIVEN: A correct implementation of encrypt.
       WHEN: Main receives an empty user input.
       THEN: Main should output exclusively the hardcoded part of
       encrypt's output."""
    # patches the standard output to catch the output of print()
    test_inputs = [""]  # test basic input and output
    expected = "Encrypted Message: \n"
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
    actual = patch_stdout.getvalue()
    assert actual == expected, build_user_friendly_err(actual, expected)


def test_encrypt_upper_case_alphabets():
    """GIVEN: A correct implementation of encrypt.
       WHEN: Encrypt is passed a string containing all uppercase alphabetical
       characters.
       THEN: We can expect a string of in which each alphabetical character
       has been offset by four to be returned."""
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = "CBAZYXWVUTSRQPONMLKJIHGFED"  # upper case alphabets
    actual = mod.encrypt("ZYXWVUTSRQPONMLKJIHGFEDCBA")
    assert actual == expected_output, build_user_friendly_err(
        actual, expected_output)


def test_encrypt_lower_case_alphabets():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = "CBAZYXWVUTSRQPONMLKJIHGFED"  # lower case alphabets
    actual = mod.encrypt("zyxwvutsrqponmlkjihgfedcba")
    assert actual == expected_output, build_user_friendly_err(
        actual, expected_output)


def test_encrypt_ignores_numbers():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = "1234567890"  # number
    actual = mod.encrypt("1234567890")
    assert actual == expected_output, build_user_friendly_err(
        actual, expected_output)


def test_encrypt_ignores_special_characters():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = "~`!@#$%^&*()-_+={}[]|\\/:;\"'<>,.?"  # special chracters
    actual = mod.encrypt("~`!@#$%^&*()-_+={}[]|\\/:;\"'<>,.?")
    assert actual == expected_output, build_user_friendly_err(
        actual, expected_output)


def test_encrypt_all_chars():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = ("CBAZYXWVUTSRQPONMLKJIHGFEDCBA"
                       "ZYXWVUTSRQPONMLKJIHGFED"
                       "1234567890"
                       "~`!@#$%^&*()-_+={}[]|\\/:;\"'<>,.?")  # all characters
    actual = mod.encrypt("zyxwvutsrqponmlkjihgfedcba"
                         "ZYXWVUTSRQPONMLKJIHGFEDCBA"
                         "1234567890"
                         "~`!@#$%^&*()-_+={}[]|\\/:;\"'<>,.?")
    assert actual == expected_output, build_user_friendly_err(
        actual, expected_output)
