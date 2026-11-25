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
    
