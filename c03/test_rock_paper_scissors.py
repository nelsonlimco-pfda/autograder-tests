from collections import namedtuple
import io
import importlib
import os
import sys
from check_pfda.utils import (assert_script_exists, build_user_friendly_err)
from check_pfda.core import REPO_PATH


MODULE_NAME = "rps"
ACCEPTED_DIRS = ["src"]


def test_script_exists():
    assert_script_exists(MODULE_NAME, ACCEPTED_DIRS, REPO_PATH)


def test_play_round_p1_wins():
    """
    GIVEN: inputs for players one and two resulting in player one winning.
    WHEN: the inputs are compared.
    THEN: player one should win.
    NOTE: same GWT for all play_round tests.
    """
    Parameter = namedtuple(
        "Parameter",
        ["p1_pick", "p2_pick", "expected_output"]
    )
    parameters = [Parameter("rock", "scissors", 1),
                  Parameter("scissors", "paper", 1),
                  Parameter("paper", "rock", 1)]
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    for param in parameters:
        actual = mod.play_round(param.p1_pick, param.p2_pick)
        expected = param.expected_output
        assert actual == expected, build_user_friendly_err(actual, expected)


def test_play_round_p2_wins():
    Parameter = namedtuple(
        "Parameter",
        ["p1_pick", "p2_pick", "expected_output"]
    )
    parameters = [Parameter("rock", "paper", 2),
                  Parameter("scissors", "rock", 2),
                  Parameter("paper", "scissors", 2)]
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    for param in parameters:
        actual = mod.play_round(param.p1_pick, param.p2_pick)
        expected = param.expected_output
        assert actual == expected, build_user_friendly_err(actual, expected)


def test_play_round_ties():
    Parameter = namedtuple(
        "Parameter",
        ["p1_pick", "p2_pick", "expected_output"]
    )
    parameters = [Parameter("rock", "rock", 0),
                  Parameter("scissors", "scissors", 0),
                  Parameter("paper", "paper", 0)]
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    for param in parameters:
        actual = mod.play_round(param.p1_pick, param.p2_pick)
        expected = param.expected_output
        assert actual == expected, build_user_friendly_err(actual, expected)


def test_format_round_results_player_wins():
    """
    GIVEN: the input of a round win.
    WHEN: the function is called.
    THEN: we should expect a properly formatted string returned.
    """
    Parameter = namedtuple(
        "Parameter",
        ["winner_input", "expected_output"]
    )
    parameters = [Parameter(1, "Player 1 Wins!"),
                  Parameter(2, "Player 2 Wins!"),
                  Parameter(0, "Tie!")]
    sys.modules.pop(MODULE_NAME, None)
    mod = importlib.import_module(name=MODULE_NAME)
    for param in parameters:
        actual = mod.format_round_results(param.winner_input)
        expected = param.expected_output
        assert actual == expected, build_user_friendly_err(actual, expected)


def test_main_3_rounds_tie(monkeypatch):
    """
    GIVEN: a full three rounds played with correct user inputs.
    WHEN: the function returns.
    THEN: we should expect the full correct game output.
    NOTE: same logic for the other main test.
    """
    Parameter = namedtuple(
        "Parameter",
        ["test_inputs", "expected_output"]
    )
    parameters = [Parameter(["rock", "rock", "paper", "paper", "scissors", "scissors"],
                            "Round 1:\nTie!\n\nRound 2:\nTie!\n\nRound 3:\nTie!\n\n"
                            "This game is a Tie!\n"),
                  Parameter(["rock",
                             "scissors",
                             "scissors",
                             "scissors",
                             "paper",
                             "scissors"],
                            "Round 1:\nPlayer 1 Wins!\n\nRound 2:\nTie!\n\nRound "
                            "3:\nPlayer 2 Wins!\n\nThis game is a Tie!\n")]
    # TODO: refactor this into a function in autograder utils to simplify the way
    # standard io tests are written.
    for param in parameters:
        # Patches the standard output to catch the output of print()
        # Flush the output after each parameter test with a new StringIO object.
        patch_stdout = io.StringIO()
        # Returns a new mock object which undoes any patching done inside the block
        # on exit to avoid breaking pytest itself
        with monkeypatch.context() as m:
            # patches the input() and pops the first test input in params
            m.setattr('builtins.input',
                      lambda prompt='': param.test_inputs.pop(0))
            m.setattr('sys.stdout', patch_stdout)
            sys.modules.pop(MODULE_NAME, None)
            mod = importlib.import_module(name=MODULE_NAME)
            mod.main()
        actual = patch_stdout.getvalue()
        expected = param.expected_output
        assert actual == expected, build_user_friendly_err(actual, expected)


def test_main_3_rounds_win(monkeypatch):
    Parameter = namedtuple("Parameter", ["test_inputs", "expected_output"])
    parameters = [Parameter(["rock", "scissors", "paper", "rock", "scissors", "paper"],
                            "Round 1:\nPlayer 1 Wins!\n\nRound 2:\nPlayer 1 Wins!\n\n"
                            "Round 3:\nPlayer 1 Wins!\n\nPlayer 1 wins the game!\n"),
                  Parameter(["rock", "scissors", "paper", "rock", "scissors", "rock"],
                            "Round 1:\nPlayer 1 Wins!\n\nRound 2:\nPlayer 1 Wins!\n\n"
                            "Round 3:\nPlayer 2 Wins!\n\nPlayer 1 wins the game!\n"),
                  Parameter(["rock", "scissors", "paper", "rock", "rock", "rock"],
                            "Round 1:\nPlayer 1 Wins!\n\nRound 2:\nPlayer 1 Wins!\n\n"
                            "Round 3:\nTie!\n\nPlayer 1 wins the game!\n"),
                  Parameter(["scissors", "rock", "paper", "scissors", "rock", "paper"],
                            "Round 1:\nPlayer 2 Wins!\n\nRound 2:\nPlayer 2 Wins!\n\n"
                            "Round 3:\nPlayer 2 Wins!\n\nPlayer 2 wins the game!\n")]
    for param in parameters:
        # Patches the standard output to catch the output of print()
        # Flush the output after each parameter test with a new StringIO object.
        patch_stdout = io.StringIO()
        # Returns a new mock object which undoes any patching done inside the block
        # on exit to avoid breaking pytest itself
        with monkeypatch.context() as m:
            # patches the input() and pops the first test input in params
            m.setattr('builtins.input',
                      lambda prompt='': param.test_inputs.pop(0))
            m.setattr('sys.stdout', patch_stdout)
            sys.modules.pop(MODULE_NAME, None)
            mod = importlib.import_module(name=MODULE_NAME)
            mod.main()
        actual = patch_stdout.getvalue()
        expected = param.expected_output
        assert actual == expected, build_user_friendly_err(actual, expected)
