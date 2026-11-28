# Image Color Palette Generator

Description to be written here 

## Dependencies

Python 3.12–3.14 is required. All libraries are listed in `requirements.txt`:

| Library | Purpose |
|---|---|
| `numpy` | Pixel arrays, color distances, and proportions |
| `Pillow` | Loading JPG/PNG images and color quantization |
| `matplotlib` | Displaying the image and color swatches |
| `ipywidgets` | Interactive controls in the notebook |
| `pyperclip` | Copying HEX codes to the clipboard |
| `notebook`, `ipykernel` | Running `main.ipynb` in Jupyter |
| `pytest` | Running the automated tests |

Built-in modules used: `pathlib` (file paths) and `csv` (palette export).

## Set up

### Windows (PowerShell)

1. Install Python 3.12–3.14 from [python.org](https://www.python.org/downloads/) and check "Add Python to PATH".
2. Open PowerShell and go to the project folder:
   ```powershell
   git clone https://github.com/emmillet/EE551-project.git
   cd EE551-project
   ```
3. Create and activate a virtual environment, then install the libraries:
   ```powershell
   py -3.14 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```
   If PowerShell blocks the activate script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.
4. Register the environment as a Jupyter kernel:
   ```powershell
   python -m ipykernel install --user --name ee551-palette --display-name "Python (EE551 Palette)"
   ```

### macOS (Terminal)

1. Install Python 3.12–3.14 from [python.org](https://www.python.org/downloads/) or with Homebrew (`brew install python@3.13`).
2. Open Terminal and go to the project folder:
   ```bash
   git clone https://github.com/emmillet/EE551-project.git
   cd EE551-project
   ```
3. Create and activate a virtual environment, then install the libraries:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```
4. Register the environment as a Jupyter kernel:
   ```bash
   python -m ipykernel install --user --name ee551-palette --display-name "Python (EE551 Palette)"
   ```

Activate the environment again (step 3's activate command) each time you open a new terminal.

## Test

With the environment activated, from the project folder:

```bash
python -m pytest -v
```

## Project Structure

```text
│
├── main.ipynb
│
├── image_analyzer.py
├── color_palette.py
├── color_utils.py
├── visualization.py
│
├── images/
│   ├── sample.png, etc. 
│
├── output/
│   └── (generated palette CSV files)
│
├── tests/
│   ├── test_image_analyzer.py
│   ├── test_color_palette.py
│   └── test_color_utils.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## File Descriptions

### Main Program
- `main.ipynb` — Interactive notebook for selecting images, generating and viewing color palettes, copying HEX codes, and exporting results to CSV.

### Python Modules
- `image_analyzer.py` — Loads images, analyzes RGB pixel data, extracts diverse dominant colors, and calculates color proportions using Pillow and NumPy.
- `color_palette.py` — Stores extracted colors and percentages, supports `str()`, indexing, and `len()`, formats RGB/HEX/percentage records, and exports palettes to CSV with `export_palette()`.
- `color_utils.py` — Converts RGB values to HEX and validates inputs.
- `visualization.py` — `show_palette()` displays the original image above color swatches labeled with RGB, HEX, and percentages using Matplotlib.

### Data and Output
- `images/` — Sample images for testing and demonstration.
- `output/` — Generated palette CSV files.

### Testing
- `tests/test_image_analyzer.py` — Tests image loading, pixel analysis, color extraction, proportions, and error handling.
- `tests/test_color_utils.py` — Tests RGB-to-HEX conversion and input validation.
- `tests/test_color_palette.py` — Tests CSV export values, folder creation, overwriting, and error handling for invalid output paths.

### Other Files
- `requirements.txt` — Required Python libraries.
- `README.md` — Project documentation and setup instructions.
- `.gitignore` — Excludes temporary and environment files from Git.

## Run the program

### Notebook (Windows or macOS)

1. Activate the environment (see Set up, step 3).
2. From the project folder, run `jupyter notebook`. A browser tab opens.
3. Open `main.ipynb`.
4. Choose **Kernel → Change Kernel → Python (EE551 Palette)**.
5. Optionally, add your own JPG or PNG images to the `images/` folder.
6. Choose **Run → Run All Cells**, or run the cells from top to bottom.
7. Select an image from the dropdown and choose the number of colors.
8. Click **Generate Palette** to display the image, extracted colors, and their proportions.
9. Click a HEX code to copy it, or use Previous/Next to browse additional colors.
10. Click **Export CSV** to save the palette in the `output/` folder.

### From Python

```python
from image_analyzer import ImageAnalyzer
from visualization import show_palette

image = "images/Quebrada_de_las_Conchas_04.jpg"
palette = ImageAnalyzer(image).extract_dominant_colors(6)

print(palette)                                # readable summary
show_palette(image, palette)                  # image and labeled swatches
palette.export_palette("output/palette.csv")  # RGB, HEX, Percentage columns
```

`export_palette()` creates the `output/` folder if needed. It raises a `ValueError` if the palette is empty, the file name does not end in `.csv`, the path is a folder, or the location cannot be written.

## Image Sources and Licensing

| File | Source | Author | License |
|---|---|---|---|
| `images/Quebrada_de_las_Conchas_04.jpg` | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Quebrada_de_las_Conchas_04.jpg) | Bernard Gagnon | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| `images/Emosson_Construction.jpg` | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Emosson_Construction.jpg) | Unknown, possibly Heinz Baumann, Comet Photo AG (Zürich) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| `images/sample.png` | Sample Pantone color palette | — | Used for testing only |

The images are used unmodified for educational, non-commercial testing and demonstration.

## Dominant Color Extraction

Uses Pillow quantization with K-means refinement and frequency and RGB distance scoring to generate diverse palettes. A smaller image is used for faster color extraction, while proportions are calculated using the original image. The results are stored in a `ColorPalette` object, sorted from most to least dominant.

## Group Contributions
Emma:
- Developed image loading and RGB pixel analysis using Pillow and NumPy.
- Implemented RGB-to-HEX conversion and initial notebook integration.
- Created Pytest tests for image processing, color conversion, and error handling.
- Implemented dominant-color extraction with K-means refinement.
- Developed frequency and distance scoring to improve palette diversity.
- Added color-count validation and tested extraction across multiple images.
- Implemented color proportion calculations using RGB distance.
- Added Pytest tests for extraction, proportion accuracy, and invalid color counts.
- Updated existing tests after ColorPalette integration and added a composition test.
- Integrated image analysis, palette visualization, and CSV export into the main notebook.
- Created an interactive interface with image previews, color selection, HEX copying, and palette navigation.

Julia:
- Created ColorPalette class to store dominant RGB colors and their percentages.
- Added methods to retrieve colors and proportions.
- Integrated ColorPalette with ImageAnalyzer using composition.
- Implemented __str__() for palette information.
- Implemented __getitem__() for indexing colors and proportions.
- Implemented __len__() for palette sizing purporses.
- Used map() to convert RGB values to HEX codes.
- Used list comprehension to format palette data.

Drashti:
- Implemented `export_palette()` to save RGB, HEX, and percentages to CSV using pathlib.
- Implemented `visualization.py` to display the image with labeled color swatches using Matplotlib.
- Added Pytest tests for CSV export functionality and accuracy.
- Added CSV export error handling (empty palettes, non-CSV names, folder paths, unwritable locations) with tests.
- Wrote README dependencies, Windows/macOS setup and run instructions, Jupyter kernel setup, file descriptions, and image sources/licensing.


## Next group tasks
- Add Pytest tests for palette operations and integration
- Update README with this info as we go: 
    Project title
    Project description, including project overview and functionalities
    Project file/module structure
    Project dependencies/environments/libraries, and how to install them on Windows or Mac. For Jupyter Notebook, specify the kernel information
    How the project requirements (both Parts 1 and 2) and grading rubrics (on page 3) are met
    Step-by-step and detailed instructions on how to run the program on Windows or Mac.
    Group member names, emails, and Stevens IDs
    Main contributions of each group member
    Project Video - YouTube Unlisted Link
