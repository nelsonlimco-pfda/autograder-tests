import importlib
import sys
import io
import pytest

from check_pfda.utils.test_helpers import assert_equal, assert_script_exists


MODULE_NAME = "helloworld"
ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS)


def test_correct_output(monkeypatch):
    mocked_stdout = io.StringIO()
    with monkeypatch.context() as mock_context:
        mock_context.setattr(sys, "stdout", mocked_stdout)
        sys.modules.pop(MODULE_NAME, None)
        importlib.import_module(name=MODULE_NAME)
    expected_result = ("Hello World!\n")
    assert_equal (expected_result, mocked_stdout.getvalue())
