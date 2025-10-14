import io
import importlib
import os
import sys
import csv


import pytest


from check_pfda.utils import (assert_script_exists, build_user_friendly_err,
                              get_module_in_src)

MODULE_NAME = get_module_in_src()
ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS)


@pytest.fixture
def tmp_inventory_csv(tmpdir):
    """Generates a temporary csv file in a temporary directory for testing."""
    file_contents = "Crossbow,50\nSword,20\nIron Helmet,25\n"
    filename = os.path.join(tmpdir, "inventory.csv")
    with open(filename, 'w') as inventory_file:
        inventory_file.write(file_contents)
    return filename


def test_display_inventory_output(monkeypatch, tmp_inventory_csv):
    # GIVEN a temporary inventory CSV file that we generate.
    # patches the standard output to catch the output of print()
    patch_stdout = io.StringIO()
    # Returns a new mock object which undoes any patching done inside
    # the with block on exit to avoid breaking pytest itself.
    with monkeypatch.context() as m:
        # patches the input()
        m.setattr('sys.stdout', patch_stdout)
        sys.modules.pop(MODULE_NAME, None)
        mod = importlib.import_module(name=MODULE_NAME)
        # WHEN display_inventory is called using the file path to our temp csv file
        mod.display_inventory(tmp_inventory_csv)
    # THEN we test if it prints the correctly formatted text to our terminal/standard out.
    expected = "Crossbow - 50 Points\nSword - 20 Points\nIron Helmet - 25 Points\n"
    actual = patch_stdout.getvalue()
    assert actual == expected, build_user_friendly_err(actual, expected)


def test_add_item_creates_new_line(monkeypatch, tmp_inventory_csv):
    # GIVEN a temporary inventory CSV file that we generate.
    # Returns a new mock object which undoes any patching done inside
    # the with block on exit to avoid breaking pytest itself.
    mod = importlib.import_module(name=MODULE_NAME)
    # WHEN add_inventory is called using the file path to our temp csv file
    mod.add_item(tmp_inventory_csv, "Shield", 15)
    # THEN we test if the new line in the file matches the expected new line.

    # Reading the last line in the file
    with open(tmp_inventory_csv) as file:
        csv_reader = csv.reader(file)
        file_output = ""
        for row in csv_reader:
            file_output += (f"{row[0]},{row[1]}\n")

    expected = "Crossbow,50\nSword,20\nIron Helmet,25\nShield,15\n"
    assert file_output == expected, build_user_friendly_err(file_output, expected)
    