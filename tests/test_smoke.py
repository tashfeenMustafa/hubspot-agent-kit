"""Smoke test: the package skeleton is importable and exposes a version."""

import importlib.metadata

import hubspot_agent_kit


def test_version_exposed() -> None:
    assert isinstance(hubspot_agent_kit.__version__, str)
    assert hubspot_agent_kit.__version__


def test_version_matches_package_metadata() -> None:
    """The single-sourced __version__ is what the installed distribution reports."""
    assert hubspot_agent_kit.__version__ == importlib.metadata.version("hubspot-agent-kit")
