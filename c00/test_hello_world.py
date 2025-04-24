import importlib
import sys
import io
import os
from pathlib import Path

from check_pfda.utils import (assert_script_exists, build_user_friendly_err,
                              get_module_in_src)


cwd_src = os.path.join(os.getcwd(), "src")
if cwd_src not in sys.path:
    sys.path.insert(0, cwd_src)

MODULE_NAME = get_module_in_src()

ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS)


def test_correct_output(monkeypatch):
    mocked_stdout = io.StringIO()
    with monkeypatch.context() as mock_context:
        mock_context.setattr(sys, "stdout", mocked_stdout)
        try:
            sys.modules.pop(MODULE_NAME, None)
            importlib.import_module(MODULE_NAME)
        finally:
            if cwd_src in sys.path:
                sys.path.remove(cwd_src)
    expected_result = ("Hello World!\n")
    assert mocked_stdout.getvalue() == expected_result, (build_user_friendly_err(mocked_stdout.getvalue(), expected_result))
