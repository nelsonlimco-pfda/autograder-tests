import importlib
import sys
import io

from check_pfda.utils import (assert_script_exists, build_user_friendly_err,
                              get_module_in_src)


MODULE_NAME = get_module_in_src()
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
    assert mocked_stdout.getvalue() == expected_result, (build_user_friendly_err(mocked_stdout.getvalue(), expected_result))
