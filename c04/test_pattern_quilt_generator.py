import importlib
import os
import sys

from check_pfda.utils import (assert_script_exists, build_user_friendly_err)

MODULE_NAME = "pattern_quilt_generator"
ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS)


def test_odd_quilt():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = ("🔵🔴🔵\n"
                       "🔴🔵🔴\n"
                       "🔵🔴🔵\n"
                       "🔴🔵🔴\n"
                       "🔵🔴🔵\n")
    actual = mod.create_checkered_quilt_pattern("🔵", "🔴", 3, 5)
    assert actual == expected_output, build_user_friendly_err(
        actual, expected_output)


def test_even_quilt():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = ("🔵🔴🔵🔴\n"
                       "🔴🔵🔴🔵\n"
                       "🔵🔴🔵🔴\n"
                       "🔴🔵🔴🔵\n")
    actual = mod.create_checkered_quilt_pattern("🔵", "🔴", 4, 4)
    assert actual == expected_output, build_user_friendly_err(
        actual, expected_output)


def test_zero_width_height():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = ""
    actual = mod.create_checkered_quilt_pattern("🔵", "🔴", 0, 0)
    assert actual == expected_output, build_user_friendly_err(
        actual, expected_output)


def test_single_tile():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = "🔵\n"
    actual = mod.create_checkered_quilt_pattern("🔵", "🔴", 1, 1)
    assert actual == expected_output, build_user_friendly_err(
        actual, expected_output)


def test_single_row():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = "🔵🔴🔵🔴🔵🔴\n"
    actual = mod.create_checkered_quilt_pattern("🔵", "🔴", 6, 1)
    assert actual == expected_output, build_user_friendly_err(
        actual, expected_output)


def test_single_column():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = ("🔵\n"
                       "🔴\n"
                       "🔵\n"
                       "🔴\n"
                       "🔵\n"
                       "🔴\n")
    actual = mod.create_checkered_quilt_pattern("🔵", "🔴", 1, 6)
    assert actual == expected_output, build_user_friendly_err(
        actual, expected_output)


def test_no_emojis_given_as_args():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = ""
    actual = mod.create_checkered_quilt_pattern("", "", 8, 8)
    assert actual == expected_output, build_user_friendly_err(
        actual, expected_output)


def test_one_emoji_given_as_arg():
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    expected_output = ("🔵🔵🔵🔵🔵\n"
                       "🔵🔵🔵🔵🔵\n"
                       "🔵🔵🔵🔵🔵\n")
    actual = mod.create_checkered_quilt_pattern("🔵", "", 10, 3)
    assert actual == expected_output, build_user_friendly_err(
        actual, expected_output)
