"""Helper functions for working with RGB colors."""


def rgb_to_hex(rgb):
    """Convert an RGB tuple of three integers into a HEX color string."""
    if len(rgb) != 3:
        raise ValueError("RGB colors must have three values.")

    for value in rgb:
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 255:
            raise ValueError("RGB values must be integers between 0 and 255.")

    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
