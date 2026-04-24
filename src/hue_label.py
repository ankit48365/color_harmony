from __future__ import annotations


def hue_label(center_deg: float) -> str:
    """Map a hue angle to a human-friendly color-family label.

    Args:
        center_deg: Hue center in degrees on the 0-360 color wheel.

    Returns:
        The display label for the closest named hue family.
    """

    names = [
        "Red",
        "Orange",
        "Yellow",
        "Chartreuse",
        "Green",
        "Spring",
        "Cyan",
        "Azure",
        "Blue",
        "Violet",
        "Magenta",
        "Rose",
    ]
    index = int(((center_deg % 360.0) / 360.0) * len(names)) % len(names)
    return names[index]
