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
- `image_analyzer.py` — Loads images, analyzes RGB pixel data, extracts diverse dominant colors, and calculates color proportions using Pillow and NumPy.
- `color_palette.py` — Will manage extracted colors, palette indexing, and CSV exports.
- `color_utils.py` — Converts RGB values to HEX and validates inputs.
- `visualization.py` — Will display images and color palettes using Matplotlib.

### Data and Output
- `images/` — Sample images for testing and demonstration.
- `output/` — Generated palette CSV files.

### Testing
- `tests/test_image_analyzer.py` — Tests image loading, pixel analysis, color extraction, proportions, and error handling.
- `tests/test_color_utils.py` — Tests RGB-to-HEX conversion and input validation.
- `tests/test_color_palette.py` — Planned tests for palette operations and CSV exports.

### Other Files
- `requirements.txt` — Required Python libraries.
- `README.md` — Project documentation and setup instructions.
- `.gitignore` — Excludes temporary and environment files from Git.

## Run the notebook

Launch `jupyter notebook`, open `main.ipynb`, and select the environment's Python kernel. Run all cells from top to bottom.  Sample pictures sourced from Wikimedia Commons and a sample Pantone Color Palette are included in `images/`.

The notebook currently demonstrates image loading, unique color analysis, RGB-to-HEX conversion, dominant-color extraction, and proportion calculations. In its current state, it is developer-facing for informal testing and demonstration of functionality and function calls for other group members. 

## Dominant Color Extraction

Uses Pillow quantization with K-means refinement and weighted frequency and RGB distance scoring to generate diverse palettes. Pixels are assigned to their closest palette color to calculate proportions, returned as an RGB-to-percentage dictionary sorted by dominance.

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

Julia:
- Created ColorPalette class to store dominant RGB colors and their percentages.
- Added methods to retrieve colors and proportions.
- Integrated ColorPalette with ImageAnalyzer using composition.
- Implemented __str__() for palette information.
- Implemented __getitem__() for indexing colors and proportions.
- Implemented __len__() for palette sizing purporses.
- Used map() to convert RGB values to HEX codes.
- Used list comprehension to format palette data.


## Next group tasks
- Display color swatches and export palettes to CSV
- Integrate modules into a user-friendly notebook
- Add Pytest tests for palette operations, CSV export, and integration
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
