"""
Display an image next to its extracted color palette using Matplotlib.

Each swatch is labeled with its RGB value, HEX code, and percentage.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image

from color_palette import ColorPalette


def _to_image(image):
    """Return a PIL image from either a file path or an existing PIL image."""
    if isinstance(image, (str, Path)):
        with Image.open(image) as source:
            return source.convert("RGB")
    return image


def _text_color(rgb):
    """Pick black or white label text so it is readable on the swatch color."""
    red, green, blue = rgb
    # Perceived brightness formula: brighter colors get dark text
    brightness = 0.299 * red + 0.587 * green + 0.114 * blue
    if brightness > 150:
        return "black"
    return "white"


def show_palette(image, palette, title="Color Palette", show=True):
    """
    Display the original image above a row of labeled color swatches.

    image   -- an image file path or a PIL image
    palette -- a ColorPalette, or the dictionary from extract_dominant_colors()
    show    -- call plt.show() when True (set False for saving or testing)

    Returns the Matplotlib figure so it can also be saved with savefig().
    """
    # Accept the raw dictionary as well as a ColorPalette object
    if isinstance(palette, dict):
        palette = ColorPalette(palette)

    records = palette.format_colors()
    if not records:
        raise ValueError("The palette has no colors to display.")

    figure, (image_axis, swatch_axis) = plt.subplots(
        2, 1, figsize=(10, 8), gridspec_kw={"height_ratios": [3, 1]}
    )

    # Top: the original image
    image_axis.imshow(_to_image(image))
    image_axis.set_title(title)
    image_axis.axis("off")

    # Bottom: one rectangle per color, width based on its percentage
    left = 0.0
    for record in records:
        width = record["Percentage"] / 100
        rgb = record["RGB"]
        face_color = tuple(value / 255 for value in rgb)
        swatch_axis.barh(0, width, left=left, color=face_color, edgecolor="white")

        # Wide swatches get the full label, narrow ones only the percentage
        if width >= 0.12:
            label = f"{record['HEX']}\n{rgb}\n{record['Percentage']:.1f}%"
        elif width >= 0.04:
            label = f"{record['Percentage']:.0f}%"
        else:
            label = ""
        if label:
            swatch_axis.text(left + width / 2, 0, label, ha="center", va="center",
                             fontsize=8, color=_text_color(rgb))
        left += width

    swatch_axis.set_xlim(0, 1)
    swatch_axis.axis("off")

    # A legend lists every color, including ones too small to label
    legend_labels = [f"{r['HEX']}  {r['RGB']}  {r['Percentage']:.2f}%" for r in records]
    handles = [plt.Rectangle((0, 0), 1, 1, color=tuple(v / 255 for v in r["RGB"]))
               for r in records]
    swatch_axis.legend(handles, legend_labels, loc="upper center",
                       bbox_to_anchor=(0.5, -0.1), ncol=min(len(records), 3),
                       fontsize=8, frameon=False)

    figure.tight_layout()
    if show:
        plt.show()
    return figure


if __name__ == "__main__":
    # Quick demo with a sample image when run directly
    from image_analyzer import ImageAnalyzer

    sample = Path(__file__).parent / "images" / "Quebrada_de_las_Conchas_04.jpg"
    colors = ImageAnalyzer(sample).extract_dominant_colors(6)
    show_palette(sample, ColorPalette(colors), title=sample.name)
