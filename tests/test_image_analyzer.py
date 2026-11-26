"""Tests for image loading, color extraction, and proportions."""

import numpy as np
import pytest
from PIL import Image
from image_analyzer import ImageAnalyzer
from color_palette import ColorPalette

def test_load_image_and_pixels(tmp_path):
    """A saved image should load with the expected size and pixels."""
    # Create a small red image for testing
    image_path = tmp_path / "red.png"
    Image.new("RGB", (4, 3), (255, 0, 0)).save(image_path)

    # Verify image dimensions and pixel array shape
    analyzer = ImageAnalyzer(image_path)
    assert analyzer.get_image_size() == (4, 3)
    pixels = analyzer.get_pixels()
    assert pixels.shape == (3, 4, 3)

    # Check that every pixel is red and only one unique color exists
    assert np.all(pixels == np.array([255, 0, 0]))
    assert analyzer.get_unique_colors() == [(255, 0, 0)]


def test_missing_image(tmp_path):
    """Trying to load a nonexistent file should give a clear error."""
    # Attempt to load an image that does not exist
    analyzer = ImageAnalyzer(tmp_path / "missing.png")
    with pytest.raises(FileNotFoundError):
        analyzer.load_image()


def test_invalid_image(tmp_path):
    """A text file should not be accepted as an image."""
    # Create a text file with an image extension
    image_path = tmp_path / "not_an_image.png"
    image_path.write_text("This is not a picture.")

    # Check that the invalid image is rejected
    with pytest.raises(ValueError):
        ImageAnalyzer(image_path).load_image()

def test_dominant_color_proportions(tmp_path):
    """Known color counts should produce the expected percentages."""
    # Create an image with 70% red and 30% blue pixels
    image_path = tmp_path / "two_colors.png"
    image = Image.new("RGB", (10, 10), (255, 0, 0))
    image.paste((0, 0, 255), (0, 0, 10, 3))
    image.save(image_path)

    palette = ImageAnalyzer(image_path).extract_dominant_colors(2)

    # Check that colors are ordered from most to least dominant
    assert list(palette.colors) == [(255, 0, 0), (0, 0, 255)]

    # Verify individual percentages and total proportion
    assert palette.colors[(255, 0, 0)] == pytest.approx(70)
    assert palette.colors[(0, 0, 255)] == pytest.approx(30)
    assert sum(palette.colors.values()) == pytest.approx(100)


def test_single_color_palette(tmp_path):
    """Requesting extra colors should not create new colors in a solid image."""
    # Create an image containing only one color
    image_path = tmp_path / "solid.png"
    Image.new("RGB", (4, 4), (20, 40, 60)).save(image_path)

    # Request more colors than the image contains
    palette = ImageAnalyzer(image_path).extract_dominant_colors(8)

    # Check that only the original color is returned
    assert palette.colors == {(20, 40, 60): 100.0}


# Run the same test with different invalid color counts
@pytest.mark.parametrize("num_colors", [0, -1, 257, 2.5, "5", True])
def test_invalid_color_count(tmp_path, num_colors):
    """Invalid palette sizes should raise a ValueError."""
    image_path = tmp_path / "sample.png"
    Image.new("RGB", (2, 2), (255, 0, 0)).save(image_path)

    # Check that each invalid input raises a ValueError
    with pytest.raises(ValueError):
        ImageAnalyzer(image_path).extract_dominant_colors(num_colors)


def test_reduced_palette_proportions(tmp_path):
    """Pixels from discarded colors should still count toward the final palette."""
    # Create an image with two shades of red and one shade of blue
    image_path = tmp_path / "three_colors.png"
    image = Image.new("RGB", (10, 10), (255, 0, 0))
    image.paste((240, 0, 0), (0, 0, 10, 3))
    image.paste((0, 0, 255), (0, 0, 10, 2))
    image.save(image_path)

    # Reduce the three original colors to a two-color palette
    palette = ImageAnalyzer(image_path).extract_dominant_colors(2)

    # Verify that both shades of red contribute to the red proportion
    assert list(palette.colors) == [(255, 0, 0), (0, 0, 255)]
    assert palette.colors[(255, 0, 0)] == pytest.approx(80)
    assert palette.colors[(0, 0, 255)] == pytest.approx(20)

def test_palette_composition(tmp_path):
    """ImageAnalyzer should create and store a ColorPalette object."""
    image_path = tmp_path / "solid.png"
    Image.new("RGB", (4, 4), (255, 0, 0)).save(image_path)

    analyzer = ImageAnalyzer(image_path)
    palette = analyzer.extract_dominant_colors(1)

    # Check that the analyzer stores the generated palette
    assert isinstance(palette, ColorPalette)
    assert analyzer.palette is palette
    assert palette.colors == {(255, 0, 0): 100.0}