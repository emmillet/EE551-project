"""Tests for RGB color formatting."""

import pytest

from color_utils import rgb_to_hex


def test_rgb_to_hex():
    """Known RGB values should convert to correct HEX codes."""
    assert rgb_to_hex((255, 0, 0)) == "#FF0000"
    assert rgb_to_hex((0, 128, 255)) == "#0080FF"
    assert rgb_to_hex((0, 0, 0)) == "#000000"


def test_invalid_rgb():
    """Colors outside the valid RGB range should raise an error."""
    with pytest.raises(ValueError):
        rgb_to_hex((256, 0, 0))
    with pytest.raises(ValueError):
        rgb_to_hex((10, 20))
