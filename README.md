# Image Color Palette Generator

Description to be written here 

## Set up (Python 3.12–3.14)

In the project folder:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

For macOS/Linux, create the environment with `python3 -m venv .venv` and activate with `source .venv/bin/activate`.

## Test

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
- `main.ipynb` — Main notebook for running the program and displaying results.

### Python Modules
- `image_analyzer.py` — Loads images, analyzes RGB pixel data, and extracts dominant colors using Pillow and NumPy. Uses pixel frequency and color distance to generate diverse color palettes.
- `color_palette.py` — Will manage extracted colors, palette indexing, and CSV exports.
- `color_utils.py` — Converts RGB values to HEX and validates inputs.
- `visualization.py` — Will display images and color palettes using Matplotlib.

### Data and Output
- `images/` — Sample images for testing and demonstration.
- `output/` — Generated palette CSV files.

### Testing
- `tests/test_image_analyzer.py` — Tests image loading, pixel analysis, and error handling.
- `tests/test_color_utils.py` — Tests RGB-to-HEX conversion and input validation.
- `tests/test_color_palette.py` — Planned tests for palette operations and CSV exports.

### Other Files
- `requirements.txt` — Required Python libraries.
- `README.md` — Project documentation and setup instructions.
- `.gitignore` — Excludes temporary and environment files from Git.

## Run the notebook

Launch `jupyter notebook`, open `main.ipynb`, and select the environment's Python kernel. Run all cells from top to bottom.  Sample pictures sourced from Wikimedia Commons and a sample Pantone Color Palette are included in `images/`.

The notebook currently demonstrates image loading, unique color analysis, RGB-to-HEX conversion, and dominant-color extraction with a customizable number of colors. In its current state, it is developer-facing for informal testing and demonstration of functionality and function calls for other group members. 

## Dominant Color Extraction

Uses Pillow's color quantization with K-means refinement and NumPy to extract candidate colors. Colors are selected using weighted pixel frequency and RGB distance to reduce overlap and improve palette diversity. Supports palette sizes of 1–256 colors, depending on available colors.

## Group Contributions
Emma:
- Developed image loading and RGB pixel analysis using Pillow and NumPy.
- Implemented RGB-to-HEX conversion and initial notebook integration.
- Created Pytest tests for image processing, color conversion, and error handling.
- Implemented dominant-color extraction with K-means refinement.
- Developed frequency and distance scoring to improve palette diversity.
- Added color-count validation and tested extraction across multiple images.

## Next group tasks
- Calculate color proportions by assigning pixels to the closest extracted color
- Implement the `ColorPalette` class with `__str__` and `__getitem__`
- Display color swatches and save the palette to CSV
- Add Pytest tests for dominant-color extraction, color proportions, invalid color counts, palette operations, and CSV export
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