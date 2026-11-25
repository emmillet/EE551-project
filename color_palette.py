"""
Stores the dominant colors extracted from an image.
"""

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
