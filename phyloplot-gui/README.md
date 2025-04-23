# Simple Phylogenetic Tree Plotter GUI

## Overview

The **Phylogenetic Tree Plotter GUI** is a Python-based graphical user interface (GUI) tool designed to simplify the process of visualizing phylogenetic trees. It allows users to select metadata and Newick files, choose columns for markers and highlights, and generate annotated phylogenetic tree plots using an integrated R script.

## Features

- **File Selection**: Easily select metadata and Newick files through the GUI.
- **Column Selection**: Choose columns for markers and highlights from the metadata file.
- **Highlight Values**: Select specific values to highlight on the phylogenetic tree.
- **Automated Plot Generation**: Generates a phylogenetic tree plot using the `ggtree` R package.
- **Plot Preview**: Automatically opens the generated plot for review.

## Requirements

- **Python 3.7+**
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

### Usage

1. Run the application:

```bash
python app.py
```

2. Use the GUI to:

- Select the metadata and Newick files.
- Choose the marker and highlight columns.
- Select values to highlight.

3. Click Generate Plot to create the phylogenetic tree plot.
4. The plot will be saved as phylogenetic_tree_with_metadata.png and automatically opened for review.

## File Format Requirements

Metadata File: A tab-delimited file containing sample metadata.
Newick File: A valid Newick format file representing the phylogenetic tree.

## Example Output

The generated plot will include:

Tip points colored based on the selected marker column.
Highlighted clades based on the selected highlight values.

## License

This tool is open-source and distributed under the MIT License.

## Acknowledgments

This tool leverages the following technologies:

PySimpleGUI for the GUI.
R and the ggtree package for phylogenetic tree visualization.
