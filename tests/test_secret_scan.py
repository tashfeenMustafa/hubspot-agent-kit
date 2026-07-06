"""Behavior tests for the CI PII/secret scanner.

Synthetic secrets below carry an inline ``pii-allow`` marker so the scanner does
not flag this test file when CI scans the tree. The strings are fabricated.
"""

from pathlib import Path

from hubspot_agent_kit.ci import secret_scan


def test_clean_text_has_no_findings() -> None:
    text = "def add(a: int, b: int) -> int:\n    return a + b\n"
    assert secret_scan.scan_text(text) == []


def test_detects_email_with_line_number() -> None:
    text = "owner = 'jane.doe@example.com'\n"  # pii-allow
    findings = secret_scan.scan_text(text)
    assert len(findings) == 1
    assert findings[0].kind == "email"
    assert findings[0].line == 1
    assert "jane.doe@example.com" in findings[0].match  # pii-allow


def test_detects_uuid() -> None:
    text = "api_key = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'\n"  # pii-allow
    findings = secret_scan.scan_text(text)
    assert [f.kind for f in findings] == ["uuid"]


def test_detects_hubspot_pat_token() -> None:
    text = "TOKEN=pat-na1-00000000-1111-2222-3333-444444444444\n"  # pii-allow
    kinds = {f.kind for f in secret_scan.scan_text(text)}
    assert "hubspot_token" in kinds


def test_detects_labeled_portal_id_but_not_bare_number() -> None:
    flagged = secret_scan.scan_text("portalId = 24857321\n")  # pii-allow
    assert [f.kind for f in flagged] == ["portal_id"]
    # A bare integer is not PII — avoid false positives on ordinary code.
    assert secret_scan.scan_text("retries = 24857321\n") == []


def test_allow_marker_suppresses_line() -> None:
    email = "real@" + "corp.example"  # split so no full email literal in source
    text = f"contact = '{email}'  # pii-allow\n"
    assert secret_scan.scan_text(text) == []


def test_main_returns_zero_for_clean_tree(tmp_path: Path) -> None:
    (tmp_path / "ok.py").write_text("x = 1\n", encoding="utf-8")
    assert secret_scan.main([str(tmp_path)]) == 0


def test_main_returns_one_when_secret_found(tmp_path: Path) -> None:
    email = "leak@" + "corp.example"
    (tmp_path / "bad.py").write_text(f"owner = '{email}'\n", encoding="utf-8")
    assert secret_scan.main([str(tmp_path)]) == 1


def test_detects_secret_in_utf16_file(tmp_path: Path) -> None:
    """UTF-16 (PowerShell's default) must not slip past the gate as undecodable."""
    email = "leak@" + "corp.example"
    (tmp_path / "u16.txt").write_text(f"owner = '{email}'\n", encoding="utf-16")
    assert secret_scan.main([str(tmp_path)]) == 1


def test_main_errors_on_missing_path(tmp_path: Path) -> None:
    """A mistyped/absent path must fail loudly, not silently pass the gate."""
    missing = tmp_path / "does-not-exist"
    assert secret_scan.main([str(missing)]) != 0


def test_skip_dir_only_below_root_not_ancestor(tmp_path: Path) -> None:
    """A skip-dir name in an ancestor of the scan root must not disable scanning."""
    root = tmp_path / "build" / "repo"  # 'build' is a skip-dir name, as an ancestor
    root.mkdir(parents=True)
    email = "leak@" + "corp.example"
    (root / "code.py").write_text(f"owner = '{email}'\n", encoding="utf-8")
    assert secret_scan.main([str(root)]) == 1
