"""Load images and use NumPy to inspect their pixel colors."""

from pathlib import Path
import numpy as np
from PIL import Image, UnidentifiedImageError


class ImageAnalyzer:
    """Load an image and provide its RGB pixel data for analysis."""

    def __init__(self, image_path):
        """Store the path to an image that will be analyzed."""
        self.image_path = Path(image_path)
        self.image = None

    def load_image(self):
        """Open the image and make sure all pixels use RGB colors."""
        try:
            with Image.open(self.image_path) as source:
                self.image = source.convert("RGB")
        except FileNotFoundError as error:
            raise FileNotFoundError(f"Image not found: {self.image_path}") from error
        except (UnidentifiedImageError, OSError) as error:
            raise ValueError(f"Cannot open this image: {self.image_path}") from error
        return self.image

    def get_pixels(self):
        """Return image pixels in a NumPy array with shape (height, width, 3)."""
        if self.image is None:
            self.load_image()
        return np.array(self.image)

    def get_image_size(self):
        """Return the image dimensions as (width, height)."""
        if self.image is None:
            self.load_image()
        return self.image.size

    def get_unique_colors(self):
        """Return a list of unique RGB tuples found in the image."""
        pixels = self.get_pixels()
        # Each row is one RGB pixel, which NumPy can compare for uniqueness
        pixel_rows = pixels.reshape(-1, 3)
        unique_pixels = np.unique(pixel_rows, axis=0)
        return [tuple(int(value) for value in row) for row in unique_pixels]

if __name__ == "__main__":
    print("Import ImageAnalyzer in main.ipynb to analyze an image.")
