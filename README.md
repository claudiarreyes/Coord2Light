# Coord2Light

=== Stil testing this project NOT READY ===

Coord2Light is a Python pipeline that transforms celestial coordinates into lightcurves and power spectra using the `lightkurve` package and NASA's MAST archive.

## Features
- Search and download lightcurve tables based on celestial coordinates.
- Automatically classify and save science lightcurves (`type='S'`).
- Query Gaia DR3 for the closest matches to target coordinates.
- Automatically compute distance modulus (DM) and estimated absolute G magnitude (`abs_gmag_estimated`).
- Store metadata and downloaded lightcurves in an organized structure.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Coord2Light.git
   cd Coord2Light
   ```
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
## Usage
1. Prepare a CSV file containing the following columns:

* target_name: Name of the target
* alpha: Right Ascension (degrees)
* delta: Declination (degrees)

2. Run the pipeline:
   ```
   python coord2light/main.py
   ````
3. Output:

* Lightcurve tables saved in data/tables.
* Science lightcurves saved in data/lightcurves.
* Updated DataFrame with metadata saved as a pickle file.

## License
   This project is licensed under the MIT License.
