"""Tests for ColorPalette CSV export."""

import csv

import pytest
from PIL import Image

from color_palette import ColorPalette, CSV_HEADERS
from image_analyzer import ImageAnalyzer


def read_csv(path):
    """Return the rows of a CSV file as a list of dictionaries."""
    with open(path, newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def test_export_palette_values(tmp_path):
    """Exported rows should contain the correct RGB, HEX, and percentages in order."""
    palette = ColorPalette({(255, 0, 0): 70.0, (0, 0, 255): 30.0})
    output = palette.export_palette(tmp_path / "palette.csv")

    assert output.exists()
    rows = read_csv(output)

    # Header and one row per color, most dominant first
    assert list(rows[0].keys()) == CSV_HEADERS
    assert rows == [
        {"RGB": "(255, 0, 0)", "HEX": "#FF0000", "Percentage": "70.00"},
        {"RGB": "(0, 0, 255)", "HEX": "#0000FF", "Percentage": "30.00"},
    ]


def test_export_creates_missing_folder(tmp_path):
    """Exporting into a folder that does not exist yet should create it."""
    output_path = tmp_path / "new_folder" / "nested" / "palette.csv"
    ColorPalette({(10, 20, 30): 100.0}).export_palette(output_path)
    assert output_path.exists()


def test_export_from_image(tmp_path):
    """A palette extracted from a known image should export accurate percentages."""
    # Create an image with 70% red and 30% blue pixels
    image_path = tmp_path / "two_colors.png"
    image = Image.new("RGB", (10, 10), (255, 0, 0))
    image.paste((0, 0, 255), (0, 0, 10, 3))
    image.save(image_path)

    colors = ImageAnalyzer(image_path).extract_dominant_colors(2)
    rows = read_csv(ColorPalette(colors).export_palette(tmp_path / "out.csv"))

    assert [row["HEX"] for row in rows] == ["#FF0000", "#0000FF"]
    assert [float(row["Percentage"]) for row in rows] == pytest.approx([70, 30])
    # Percentages in the file should still add up to 100
    assert sum(float(row["Percentage"]) for row in rows) == pytest.approx(100)


def test_export_overwrites_existing_file(tmp_path):
    """Exporting twice to the same path should replace the old contents."""
    output_path = tmp_path / "palette.csv"
    ColorPalette({(1, 2, 3): 50.0, (4, 5, 6): 50.0}).export_palette(output_path)
    ColorPalette({(7, 8, 9): 100.0}).export_palette(output_path)

    rows = read_csv(output_path)
    assert len(rows) == 1
    assert rows[0]["HEX"] == "#070809"


# Run the same test with different file types that are not CSV
@pytest.mark.parametrize("filename", ["palette.txt", "palette", "palette.csv.png"])
def test_export_rejects_non_csv(tmp_path, filename):
    """Only .csv output paths should be accepted."""
    with pytest.raises(ValueError):
        ColorPalette({(1, 2, 3): 100.0}).export_palette(tmp_path / filename)


def test_export_rejects_folder_path(tmp_path):
    """An existing folder cannot be used as the output file."""
    folder = tmp_path / "looks_like.csv"
    folder.mkdir()
    with pytest.raises(ValueError):
        ColorPalette({(1, 2, 3): 100.0}).export_palette(folder)


def test_export_unwritable_location(tmp_path):
    """A path whose parent is a file (not a folder) should give a clear error."""
    blocker = tmp_path / "not_a_folder"
    blocker.write_text("this is a file")
    with pytest.raises(ValueError):
        ColorPalette({(1, 2, 3): 100.0}).export_palette(blocker / "palette.csv")


def test_export_empty_palette(tmp_path):
    """An empty palette should not create a CSV file."""
    output_path = tmp_path / "empty.csv"
    with pytest.raises(ValueError):
        ColorPalette({}).export_palette(output_path)
    assert not output_path.exists()
