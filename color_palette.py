"""
Stores the dominant colors extracted from an image.
"""

import csv
from pathlib import Path

from color_utils import rgb_to_hex

# Column names used for exported palette CSV files
CSV_HEADERS = ["RGB", "HEX", "Percentage"]

class ColorPalette:
  """
  Stores RGB values and their percentages in a dictionary.
  """
  def __init__(self, colors):
    """Initializes ColorPalette object with the extracted colors."""
    self.colors = colors

  def get_colors(self):
    """Returns the RGB colors in the palette"""
    return list(self.colors.keys())

  def get_proportions(self):
    """Returns the percentages of each color."""
    return list(self.colors.values())

  
  def __str__(self):
    """Returns a readable description of the palette."""
    result = "Color Palette:\n"

    for rgb, percentage in self.colors.items():
      result += f"RGB: {rgb}, Percentage: {percentage:.2f}%\n"

    return result


  def __getitem__(self,index):
    """Returns the RGB color and percentage at the given index."""
    return list(self.colors.items())[index]

  def __len__(self):
    """Returns the number of colors in the palette."""
    return len(self.colors)


  def format_colors(self):
    """Creates a list of RGB, HEX, and % values for visualization and export."""
    rgb_colors = self.get_colors()
    percentages = self.get_proportions()

    #Convert RGB values to HEX using map()
    hex_colors = list(map(rgb_to_hex, rgb_colors))

    #Combine RGB, HEX, and % values using list comprehension
    formatted_colors = [
      {"RGB": rgb, "HEX": hex_code, "Percentage": percentage}
      for rgb, hex_code, percentage in zip(rgb_colors, hex_colors, percentages)
    ]

    return formatted_colors

  def export_palette(self, output_path="output/palette.csv"):
    """
    Export the palette's RGB, HEX, and percentage values to a CSV file.

    The output folder is created if it does not exist yet.
    Returns the Path of the saved CSV file.

    Raises ValueError if the palette is empty, the path is not a .csv file,
    the path is an existing folder, or the file cannot be written.
    """
    if len(self) == 0:
      raise ValueError("Cannot export an empty palette.")

    output_path = Path(output_path)

    # Only allow CSV files so the output opens correctly in spreadsheet apps
    if output_path.suffix.lower() != ".csv":
      raise ValueError(f"Output file must end in .csv: {output_path}")

    if output_path.is_dir():
      raise ValueError(f"Output path is a folder, not a file: {output_path}")

    # Reuse the formatted records so the CSV matches the visualization
    records = self.format_colors()

    try:
      # Make sure the folder for the CSV file exists
      output_path.parent.mkdir(parents=True, exist_ok=True)

      with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        writer.writeheader()

        # Write one row per palette color
        for record in records:
          writer.writerow({
            "RGB": str(record["RGB"]),
            "HEX": record["HEX"],
            "Percentage": f"{record['Percentage']:.2f}",
          })
    except OSError as error:
      # Covers missing permissions or a file being used as a folder name
      raise ValueError(f"Cannot write palette to {output_path}: {error}") from error

    return output_path
