import io
import importlib
import os
import sys


import pytest

from check_pfda.utils import (assert_script_exists, build_user_friendly_err)
from check_pfda.core import REPO_PATH
MODULE_NAME = "art_prompts"
ACCEPTED_DIRS = ["src"]

nouns_list = ["Percentage", "Storage", "Reflection", "Physics", "Village"]
adjectives_list = ["Pointless", "Halting", "Free", "Stimulating", "Clever"]
adjectives_filename = "adjectives.txt"
nouns_filename = "nouns.txt"


@pytest.fixture
def tmp_noun_list(tmpdir):
    """Generates a temporary .txt file in a temporary directory for testing."""
    file_contents = "Percentage\nStorage\nReflection\nPhysics\nVillage\n"
    filename = os.path.join(tmpdir, "tmp_nouns.txt")
    with open(filename, 'w') as inventory_file:
        inventory_file.write(file_contents)
    return filename


@pytest.fixture
def tmp_adj_list(tmpdir):
    """Generates a temporary .txt file in a temporary directory for testing."""
    file_contents = "Pointless\nHalting\nFree\nStimulating\nClever\n"
    filename = os.path.join(tmpdir, "tmp_adjs.txt")
    with open(filename, 'w') as inventory_file:
        inventory_file.write(file_contents)
    return filename


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS, REPO_PATH)


def test_get_prompts_from_file_returns_list_of_words(tmp_noun_list):
    # GIVEN a text file with known contents and a list of known results
    # WHEN get_prompts_from_file is called
    # THEN we can compare the output of get_prompts_from_file using the text file with known contents and the list of known results
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)

    result_get_prompts_from_file = mod.get_prompts_from_file(tmp_noun_list)

    for word in range(0, len(nouns_list)):
        assert result_get_prompts_from_file[word] == nouns_list[word], (
            "get_prompts_from_file did not read the text file correctly.")


def test_pick_random_prompt_generates_random_prompt():
    # GIVEN that pick_random_prompt() is random
    # WHEN pick_random_prompt() is called 10 times
    # THEN we can reasonably expect the order of the first 5 combinations to be different from the order of the next 5 combinations
    # WHEN we seed the random module with random.seed()
    # THEN we expect pick_random_prompt() to give us the same result when called repeatedly.
    # BOTH conditions should be True to assure randomness and the use of the random module.
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    curr_dir = os.getcwd()
    subfolder = "src"
    filename_nouns = os.path.join(curr_dir, subfolder, nouns_filename)
    filename_adjectives = os.path.join(
        curr_dir, subfolder, adjectives_filename)
    prompt_nouns = mod.get_prompts_from_file(filename_nouns)
    prompt_adjectives = mod.get_prompts_from_file(filename_adjectives)
    first_five_combinations = [
        f"{mod.pick_random_prompt(prompt_nouns)} {mod.pick_random_prompt(prompt_adjectives)}" for n in range(5)]
    next_five_combinations = [
        f"{mod.pick_random_prompt(prompt_nouns)} {mod.pick_random_prompt(prompt_adjectives)}" for n in range(5)]
    if first_five_combinations == next_five_combinations:
        assert False, f"Function repeats itself. {first_five_combinations}:{next_five_combinations}"
        return
    random_not_found_msg = f"Not able to find the standard library's random module. If you did use it, check that you used 'import random' only to import the module."
    # store the original random generator state, so we can restore it after messing around with the seed.
    try:
        original_state = mod.random.getstate()
    except AttributeError as err:
        assert False, random_not_found_msg
    initial_result = []
    for n in range(10):
        mod.random.seed(n)
        initial_result.append(
            f"{mod.pick_random_prompt(prompt_nouns)} {mod.pick_random_prompt(prompt_adjectives)}")
    # reseed random to get the same result
    repeat_result = []
    for n in range(10):
        mod.random.seed(n)
        repeat_result.append(
            f"{mod.pick_random_prompt(prompt_nouns)} {mod.pick_random_prompt(prompt_adjectives)}")
    # restore the random generator state just before we exit the test.
    mod.random.setstate(original_state)
    if initial_result != repeat_result:
        assert False, random_not_found_msg
        return
