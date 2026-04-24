from __future__ import annotations

import argparse
import re
from pathlib import Path

PYLINT_BADGE_PATTERN = re.compile(
    r"!\[pylint\]\(https://img\.shields\.io/badge/pylint-[^)]+-green\)"
)
COVERAGE_BADGE_PATTERN = re.compile(
    r"!\[coverage\]\(https://img\.shields\.io/badge/coverage-[^)]+-blue\)"
)


def format_pylint_badge(score: float) -> str:
    return f"![pylint](https://img.shields.io/badge/pylint-{score:.2f}-green)"


def format_coverage_badge(score: float) -> str:
    return f"![coverage](https://img.shields.io/badge/coverage-{score:.2f}%25-blue)"


def insert_missing_badges(readme_text: str, missing_badges: list[str]) -> str:
    heading, separator, remainder = readme_text.partition("\n")
    if heading.startswith("# ") and separator:
        return f"{heading}\n\n" + "\n".join(missing_badges) + "\n\n" + remainder.lstrip("\n")
    return "\n".join(missing_badges) + "\n\n" + readme_text


def update_quality_badges(readme_text: str, coverage_score: float, pylint_score: float) -> str:
    coverage_badge = format_coverage_badge(coverage_score)
    pylint_badge = format_pylint_badge(pylint_score)

    updated = readme_text
    coverage_found = bool(COVERAGE_BADGE_PATTERN.search(updated))
    pylint_found = bool(PYLINT_BADGE_PATTERN.search(updated))

    if coverage_found:
        updated = COVERAGE_BADGE_PATTERN.sub(coverage_badge, updated, count=1)
    if pylint_found:
        updated = PYLINT_BADGE_PATTERN.sub(pylint_badge, updated, count=1)

    missing_badges: list[str] = []
    if not coverage_found:
        missing_badges.append(coverage_badge)
    if not pylint_found:
        missing_badges.append(pylint_badge)

    if missing_badges:
        updated = insert_missing_badges(updated, missing_badges)

    return updated


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update the README coverage and pylint badge values."
    )
    parser.add_argument("--readme", type=Path, required=True, help="Path to the README file.")
    parser.add_argument(
        "--coverage", type=float, required=True, help="Coverage percentage without the percent sign."
    )
    parser.add_argument(
        "--pylint", type=float, required=True, help="Pylint score on the 0-10 scale."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    original_text = args.readme.read_text(encoding="utf-8")
    updated_text = update_quality_badges(original_text, args.coverage, args.pylint)
    args.readme.write_text(updated_text, encoding="utf-8")


if __name__ == "__main__":
    main()
