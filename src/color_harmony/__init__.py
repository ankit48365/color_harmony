from __future__ import annotations

from .app import SECTION_CSS, create_demo

__all__ = ["create_demo", "main"]


def main() -> None:
    create_demo().launch(css=SECTION_CSS)
