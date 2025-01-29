"""Provides functionalities to create new conventional commit messages through a simple CLI interface."""

from __future__ import annotations

from . import commits
from .main import main

__all__ = ["commits", "main"]
