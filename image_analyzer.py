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

    def extract_dominant_colors(self, num_colors):
        """Extract dominant RGB colors based on frequency and color diversity."""
        if isinstance(num_colors, bool) or not isinstance(num_colors, int):
            raise ValueError("Number of colors must be an integer.")

        if not 1 <= num_colors <= 256:
            raise ValueError("Number of colors must be between 1 and 256.")

        if self.image is None:
            self.load_image()

        # Extract more colors than requested so there are enough candidates to choose from when building the final palette
        candidate_count = min(num_colors * 8, 256)
        quantized = self.image.quantize(colors=candidate_count, kmeans=5).convert("RGB")

        pixels = np.array(quantized).reshape(-1, 3)

        # Count how many pixels belong to each candidate color
        colors, counts = np.unique(pixels, axis=0, return_counts=True)

        # Sort by frequency so the most common color is first
        order = np.argsort(-counts, kind="stable")
        colors = colors[order].astype(int)
        counts = counts[order]

        # Account for images with fewer colors than requested
        target = min(num_colors, len(colors))

        # Start the palette with the most frequent candidate color
        selected = [0]

        while len(selected) < target:
            scores = np.zeros(len(colors))

            for i, color in enumerate(colors):
                if i in selected:
                    continue
                # Find the distance to the closest color already selected
                # This helps avoid adding colors that look too similar
                distance = min(
                    np.linalg.norm(color - colors[j])
                    for j in selected
                )

                # Balance color frequency with distance from the existing palette
                # Use the square root so common colors don't outweigh diversity
                scores[i] = np.sqrt(counts[i]) * distance

            # Add the color with the best balance of frequency and distance
            selected.append(int(np.argmax(scores)))

        # Return regular Python RGB tuples for use with rgb_to_hex()
        return [tuple(int(value) for value in colors[i])
                for i in selected]

if __name__ == "__main__":
    print("Import ImageAnalyzer in main.ipynb to analyze an image.")
