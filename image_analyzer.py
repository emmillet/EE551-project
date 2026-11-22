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

    def _calculate_proportions(self, palette):
        """Calculate the percentage of pixels represented by each palette color."""
        palette = np.array(palette, dtype=np.int32)
        pixels = self.get_pixels().reshape(-1, 3)
        counts = np.zeros(len(palette), dtype=np.int64)

        # Process pixels in batches to reduce memory usage on large images
        for start in range(0, len(pixels), 4096):
            batch = pixels[start:start + 4096].astype(np.int32)

            # Compare each pixel to every palette color and find the closest one
            differences = batch[:, None, :] - palette[None, :, :]
            distances = np.sum(differences ** 2, axis=2)
            closest = np.argmin(distances, axis=1)

            # Add the number of pixels assigned to each color
            counts += np.bincount(closest, minlength=len(palette))

        # Convert counts to percentages and sort from most to least dominant
        proportions = counts / len(pixels) * 100
        order = np.argsort(-counts, kind="stable")

        # Store RGB tuples and percentages in a dictionary
        return {tuple(int(value) for value in palette[i]): float(proportions[i])
                for i in order}
    
    def extract_dominant_colors(self, num_colors):
        """Return a dictionary of dominant RGB colors and percentages, sorted by dominance."""
        if isinstance(num_colors, bool) or not isinstance(num_colors, int):
            raise ValueError("Number of colors must be an integer.")

        if not 1 <= num_colors <= 256:
            raise ValueError("Number of colors must be between 1 and 256.")

        if self.image is None:
            self.load_image()

        # Extract extra candidate colors to allow for more palette diversity
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

        # Calculate proportions for the selected palette colors
        palette = colors[selected]
        return self._calculate_proportions(palette)

if __name__ == "__main__":
    print("Import ImageAnalyzer in main.ipynb to analyze an image.")
