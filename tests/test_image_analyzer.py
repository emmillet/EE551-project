"""Tests for image loading and RGB pixel inspection."""

import numpy as np
import pytest
from PIL import Image
from image_analyzer import ImageAnalyzer


def test_load_image_and_pixels(tmp_path):
    """A saved image should load with the expected size and pixels."""
    image_path = tmp_path / "red.png"
    Image.new("RGB", (4, 3), (255, 0, 0)).save(image_path)

    analyzer = ImageAnalyzer(image_path)
    assert analyzer.get_image_size() == (4, 3)
    pixels = analyzer.get_pixels()
    assert pixels.shape == (3, 4, 3)
    assert np.all(pixels == np.array([255, 0, 0]))
    assert analyzer.get_unique_colors() == [(255, 0, 0)]


def test_missing_image(tmp_path):
    """Trying to load a nonexistent file should give a clear error."""
    analyzer = ImageAnalyzer(tmp_path / "missing.png")
    with pytest.raises(FileNotFoundError):
        analyzer.load_image()


def test_invalid_image(tmp_path):
    """A text file should not be accepted as an image."""
    image_path = tmp_path / "not_an_image.png"
    image_path.write_text("This is not a picture.")
    with pytest.raises(ValueError):
        ImageAnalyzer(image_path).load_image()
