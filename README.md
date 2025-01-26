# Coord2Power

Coord2Power is a Python pipeline that transforms celestial coordinates into lightcurves and power spectra using the `lightkurve` package and NASA's MAST archive.

## Features
- Search and download lightcurve tables based on celestial coordinates.
- Automatically classify and save science lightcurves (`type='S'`).
- Store metadata and downloaded lightcurves in an organized structure.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Coord2Power.git
   cd Coord2Power

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
