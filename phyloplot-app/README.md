# PhyloPlot App

## Overview

PhyloPlot is a Python-based browser application designed to visualize phylogenetic trees with metadata. It allows users to select metadata and Newick files, choose columns for markers and highlights, and generate annotated phylogenetic tree plots using an integrated R script.

## Features

- **File Selection**: Easily select metadata and Newick files through the GUI.
- **Column Selection**: Choose columns for markers and highlights from the metadata file.
- **Highlight Values**: Select specific values to highlight on the phylogenetic tree.
- **Automated Plot Generation**: Generates a phylogenetic tree plot using the `ggtree` R package.
- **Plot Preview**: Automatically opens the generated plot for review.

## Requirements

- **Python 3.7+** with the following packages installed:

  - `pandas`
  - `streamlit` for streamlit app
  - `flask` for flask app

- **R** with the following R packages installed:
  - `ggtree`
  - `ggplot2`
  - `ggtreeExtra`

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd plot_tree_gui
   ```

2. Create conda environment:

```bash
conda create --name <env> --file conda-requirements.txt
```

3. Activate the environment

```bash
conda activate <env>
```

3. Install R packages:

```bash
Rscript -e "install.packages(c('ggtree', 'ggplot2', 'ggtreeExtra'))"
```

4. Create python environment:

```bash
python -m pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python app.py
```

2. Use the GUI to:

- Select the metadata and Newick files.
- Choose the marker and highlight columns.
- Select values to highlight.

3. Click Generate Plot to create the phylogenetic tree plot.
