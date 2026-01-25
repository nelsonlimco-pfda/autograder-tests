import io
import importlib
import os
import sys


from check_pfda.utils import (assert_script_exists,
                              build_user_friendly_err)

MODULE_NAME = "magic_sorting_hat"
ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS)


def test_sort_to_house_uses_random():
    # GIVEN that sort_to_house() is random
    # WHEN sort_to_house() is called 10 times
    # THEN we can reasonably expect the order of the first 5 houses to be different from the order of the next 5 houses
    # WHEN we seed the random module with random.seed()
    # THEN we expect sort_to_house() to give us the same result when called repeatedly.
    # BOTH conditions should be True to assure randomness and the use of the random module.
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    first_five = [mod.sort_to_house() for n in range(5)]
    next_five = [mod.sort_to_house() for n in range(5)]
    if first_five == next_five:
        assert False, f"Function repeats itself. {first_five}:{next_five}"
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
        initial_result.append(mod.sort_to_house())
    # reseed random to get the same result
    repeat_result = []
    for n in range(10):
        mod.random.seed(n)
        repeat_result.append(mod.sort_to_house())
    # restore the random generator state just before we exit the test.
    mod.random.setstate(original_state)
    if initial_result != repeat_result:
        assert False, random_not_found_msg
        return


def test_sort_to_house_has_no_missing_houses():
    # GIVEN that sort_to_house() randomly returns the 4 harry porter houses
    # WHEN called 100x
    # THEN we expect each of the 4 houses to be generated at least once
    sys.modules.pop(MODULE_NAME, None)
    expected = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
    mod = importlib.import_module(name=MODULE_NAME)
    houses = []
    for n in range(100):
        houses.append(mod.sort_to_house())
    # set() removes duplicate houses, so we know if each house was generated once.
    uniq_houses = list(set(houses))
    uniq_houses.sort()
    if uniq_houses != expected:
        assert False, f"{uniq_houses} != {expected}"
        return
    assert True
