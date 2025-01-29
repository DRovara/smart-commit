"""Tests specific to the commits sub-module."""

from __future__ import annotations

import commit.commits as c


def test_check_incorrect_capitalisation() -> None:
    """Test check_commit_message with incorrect capitalisation."""
    msg = "This is a test message"
    assert c.check_commit_message(msg) == (False, msg)


def test_check_incorrect_punctuation() -> None:
    """Test check_commit_message with incorrect punctuation."""
    msg = "This is a test message."
    assert c.check_commit_message(msg) == (False, msg)


def test_check_correct() -> None:
    """Test check_commit_message with a correct input."""
    msg = " this is a test message"
    assert c.check_commit_message(msg) == (True, msg.strip())
