# Well Log Analysis Project

This project is designed for analyzing well logs and the data derived from them. It includes various components for data processing, visualization, and exploratory analysis.

## Current Features

### Well Log Visualization
- Multi-track well log plotting with formation tops overlay
- Support for LAS (Log ASCII Standard) file format
- Automated parsing of well log curves including:
  - Caliper and Bit Size
  - Gamma Ray
  - Density  
  - Neutron
  - Sonic (P-wave and S-wave)
  - Resistivity (Micro, Medium, Deep)
- Formation tops displayed as horizontal lines across all tracks

### Data Files Included
- `Well 1.txt`: LAS format well log data with multiple curves
- `Tops_Well-1.txt`: Formation tops with depths (FM-1 through FM-10)

## Project Structure

- **data/**: Contains datasets used in the analysis.
  - **README.md**: Documentation related to the data sources, formats, and preprocessing steps.
  
- **notebooks/**: Contains Jupyter notebooks for analysis.
  - **exploratory_analysis.ipynb**: Notebook for exploratory data analysis of well logs.

- **src/**: Contains the source code for data processing and visualization.
  - **data_processing.py**: Functions and classes for processing well log data.
  - **visualization.py**: Functions for visualizing well log data.
  - **utils.py**: Utility functions to support the main functionality.

- **tests/**: Contains unit tests for the project.
  - **test_data_processing.py**: Unit tests for data processing functions.

- **requirements.txt**: Lists the dependencies required for the project.

## Installation

To install the required packages, run:

```
pip install -r requirements.txt
```

## Usage

### Quick Start - View Well Logs
```bash
# Run the visualization directly
python src/visualization.py
```

This will display a 6-track well log panel with formation tops.

### Programmatic Usage
```python
from src.visualization import plot_well_log_tracks
import pandas as pd

# Load your data into a DataFrame
df = pd.read_csv('your_well_data.csv')

# Define which logs to plot in each track
log_tracks = [
    ["CALI", "BS"],           # Caliper/Bit Size
    ["GR"],                   # Gamma Ray  
    ["DEN"],                  # Density
    ["NEU"],                  # Neutron
    ["AC", "ACS"],            # Sonic
    ["RMIC", "RMED", "RDEP"]  # Resistivity
]

# Create the plot
plot_well_log_tracks(df, "DEPT", log_tracks)
```

### Original Installation Instructions
1. Load the well log data using the functions in `data_processing.py`.
2. Perform exploratory analysis using the Jupyter notebook in the `notebooks` directory.
3. Visualize the results using the functions in `visualization.py`.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.