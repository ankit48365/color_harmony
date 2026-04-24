from __future__ import annotations

from scripts.update_quality_badges import (
    format_coverage_badge,
    format_pylint_badge,
    update_quality_badges,
)


def test_update_quality_badges_replaces_existing_badges() -> None:
    readme_text = """# color_harmony

![coverage](https://img.shields.io/badge/coverage-72.22%25-blue)
![pylint](https://img.shields.io/badge/pylint-10.00-green)
"""

    updated = update_quality_badges(readme_text, coverage_score=83.33, pylint_score=9.12)

    assert format_coverage_badge(83.33) in updated
    assert format_pylint_badge(9.12) in updated
    assert "72.22%25" not in updated
    assert "10.00-green" not in updated


def test_update_quality_badges_inserts_missing_badges_below_title() -> None:
    readme_text = """# color_harmony

Small Gradio app.
"""

    updated = update_quality_badges(readme_text, coverage_score=91.5, pylint_score=8.75)

    expected = """# color_harmony

![coverage](https://img.shields.io/badge/coverage-91.50%25-blue)
![pylint](https://img.shields.io/badge/pylint-8.75-green)

Small Gradio app.
"""
    assert updated == expected
