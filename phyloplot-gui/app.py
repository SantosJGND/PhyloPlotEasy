import PySimpleGUI as sg
import pandas as pd
from pathlib import Path
import subprocess
import os

def main():
    sg.theme("DarkBlue3")  # Modern theme
    font = ("Arial", 12)
    select_text_color = "#D3D3D3"  # Light gray text color
    button_color = ("black", "#D3D3D3")  # Light gray button color

    layout = [
        [sg.Text("Select Metadata File:", font=font, text_color=select_text_color), sg.Input(key="-METADATA-", enable_events=True), sg.FileBrowse(font=font, button_color=button_color)],
        [sg.Text("Select Newick File:", font=font, text_color=select_text_color), sg.Input(key="-NEWICK-", enable_events=True), sg.FileBrowse(font=font, button_color=button_color)],
        [sg.Text("Select Marker Column:", font=font, text_color=select_text_color), sg.Combo([], key="-MARKER_COLUMN-", size=(30, 1), readonly=True, font=font)],
        [sg.Text("Select Highlight Column:", font=font, text_color=select_text_color), sg.Combo([], key="-HIGHLIGHT_COLUMN-", size=(30, 1), readonly=True, enable_events=True, font=font)],
        [sg.Text("Select Sample Label Column:", font=font, text_color=select_text_color), sg.Combo([], key="-LABEL_COLUMN-", size=(30, 1), readonly=True, font=font)],
        [sg.Text("Label Size (1-20):", font=font, text_color=select_text_color), sg.Input(key="-LABEL_SIZE-", size=(10, 1), font=font, default_text="5")],
        [sg.Text("Tip Size (1-10):", font=font, text_color=select_text_color), sg.Input(key="-TIP_SIZE-", size=(10, 1), font=font, default_text="5")],
        [sg.Text("Select Values to Highlight:", font=font, text_color=select_text_color)],
        [sg.Listbox(values=[], key="-HIGHLIGHT_VALUES-", size=(40, 10), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, font=font)],
        [
            sg.Button("Generate Plot", size=(15, 1), button_color=button_color, font=font), 
            sg.Button("Save PNG", size=(15, 1), button_color=button_color, font=font), 
            sg.Button("Save PDF", size=(15, 1), button_color=button_color, font=font), 
            sg.Button("Exit", size=(10, 1), button_color=button_color, font=font)]
    ]

    # Create the window
    window = sg.Window("Phylogenetic Tree Plotter", layout)

    metadata_df = None

    while True:
        event, values = window.read()

        # Exit the application
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

        # Load metadata file and populate dropdowns
        if event == "-METADATA-":
            metadata_file = values["-METADATA-"]
            if Path(metadata_file).is_file():
                metadata_df = pd.read_csv(metadata_file, sep="\t")
                columns = metadata_df.columns.tolist()
                window["-MARKER_COLUMN-"].update(values=columns)
                window["-HIGHLIGHT_COLUMN-"].update(values=columns)
                window["-LABEL_COLUMN-"].update(values=columns)

        # Populate highlight values when a highlight column is selected
        if event == "-HIGHLIGHT_COLUMN-" and metadata_df is not None:
            highlight_column = values["-HIGHLIGHT_COLUMN-"]
            if highlight_column in metadata_df.columns:
                unique_values = metadata_df[highlight_column].dropna().unique().tolist()
                window["-HIGHLIGHT_VALUES-"].update(values=unique_values)


        # Generate the plot
        if event == "Save PNG" or event == "Save PDF":

            metadata_file = values["-METADATA-"]
            newick_file = values["-NEWICK-"]
            marker_column = values["-MARKER_COLUMN-"]
            highlight_column = values["-HIGHLIGHT_COLUMN-"]
            label_column = values["-LABEL_COLUMN-"]
            highlight_values = values["-HIGHLIGHT_VALUES-"]
            label_size = values["-LABEL_SIZE-"]
            tip_size = values["-TIP_SIZE-"]
            format_file = "png" if event == "SAVE PNG" else "pdf"

            # Validate inputs
            if not metadata_file or not newick_file or not marker_column or not label_column:
                sg.popup_error("Please fill in all fields!")
                continue
                
                
            if not highlight_column:
                highlight_column = "NA"
            if not highlight_values:
                highlight_values_str = "NA"
            else:
                highlight_values_str = ",".join(highlight_values)

            

            try:
                label_size = int(label_size)
                tip_size = int(tip_size)
                if not (1 <= label_size <= 20):
                    raise ValueError("Label size must be between 1 and 20.")
                if not (1 <= tip_size <= 10):
                    raise ValueError("Tip size must be between 1 and 10.")
            except ValueError as e:
                sg.popup_error(f"Invalid input: {e}")
                continue

            # Call the R script using subprocess
            try:
                subprocess.run(
                    [
                        "Rscript",
                        "ggtree_trial.R",  # Path to your R script
                        metadata_file,
                        newick_file,
                        marker_column,
                        highlight_column,
                        highlight_values_str,
                        label_column,
                        str(label_size),
                        str(tip_size),
                        format_file,
                    ],
                    check=True
                )
                sg.popup("Plot generated successfully!")

            except subprocess.CalledProcessError as e:
                sg.popup_error(f"Error generating plot: {e}")

        # Generate the plot
        if event == "Generate Plot":
            metadata_file = values["-METADATA-"]
            newick_file = values["-NEWICK-"]
            marker_column = values["-MARKER_COLUMN-"]
            highlight_column = values["-HIGHLIGHT_COLUMN-"]
            label_column = values["-LABEL_COLUMN-"]
            highlight_values = values["-HIGHLIGHT_VALUES-"]
            label_size = values["-LABEL_SIZE-"]
            tip_size = values["-TIP_SIZE-"]

            # Validate inputs
            if not metadata_file or not newick_file or not marker_column or not label_column:
                sg.popup_error("Please fill in all fields!")
                continue
                
            if not highlight_column:
                highlight_column = "NA"
            if not highlight_values:
                highlight_values_str = "NA"
            else:
                highlight_values_str = ",".join(highlight_values)

                
            try:
                label_size = int(label_size)
                tip_size = int(tip_size)
                if not (1 <= label_size <= 20):
                    raise ValueError("Label size must be between 1 and 20.")
                if not (1 <= tip_size <= 10):
                    raise ValueError("Tip size must be between 1 and 10.")
            except ValueError as e:
                sg.popup_error(f"Invalid input: {e}")
                continue

            # Convert highlight values to a comma-separated string

            # Call the R script using subprocess
            try:
                subprocess.run(
                    [
                        "Rscript",
                        "ggtree_trial.R",  # Path to your R script
                        metadata_file,
                        newick_file,
                        marker_column,
                        highlight_column,
                        highlight_values_str,
                        label_column,
                        str(label_size),
                        str(tip_size),
                        "png",
                    ],
                    check=True
                )
                sg.popup("Plot generated successfully!")
                # Open the plot automatically
                plot_file = "phylogenetic_tree.png"  # Ensure this matches the output file in your R script
                if os.path.exists(plot_file):
                    subprocess.run(["xdg-open", plot_file])  # For Linux
                    # subprocess.run(["open", plot_file])  # For macOS
                    # subprocess.run(["start", plot_file], shell=True)  # For Windows
            except subprocess.CalledProcessError as e:
                sg.popup_error(f"Error generating plot: {e}")

    window.close()

if __name__ == "__main__":
    main()