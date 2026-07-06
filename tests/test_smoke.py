"""Smoke test: the package skeleton is importable and exposes a version."""

import hubspot_agent_kit


def test_package_importable() -> None:
    assert hubspot_agent_kit is not None


def test_version_exposed() -> None:
    assert isinstance(hubspot_agent_kit.__version__, str)
    assert hubspot_agent_kit.__version__
