"""Provides functionalities to create new conventional commit messages through a simple CLI interface."""

from __future__ import annotations

from . import commits
from .config import Config, NewCommitType, NewGitmoji, parse_config
from .main import main

__all__ = ["Config", "NewCommitType", "NewGitmoji", "commits", "main", "parse_config"]
