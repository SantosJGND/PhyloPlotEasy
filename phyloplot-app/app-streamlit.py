import streamlit as st
import pandas as pd
import subprocess
import uuid
import os

st.set_page_config(
    page_title="Phylogenetic Tree Plotter",
    page_icon="🌳",
    layout="wide",
)
st.title("Phylogenetic Tree Plotter")

# Center the layout and adjust column widths
with st.container():
    col1, col2 = st.columns([1.5, 2.5])  # Adjust the width ratio (e.g., 1.5:2.5 for wider columns)

    # Left column: Parameter inputs
    with col1:
        # File uploaders
        metadata_file = st.file_uploader("Upload Metadata File", type=["tsv"])
        newick_file = st.file_uploader("Upload Newick File", type=["nwk"])

        # Initialize column options
        columns = []
        highlight_values_options = []

        # If metadata file is uploaded, read the headers
        if metadata_file:
            try:
                metadata_df = pd.read_csv(metadata_file, sep="\t")
                columns = metadata_df.columns.tolist()
            except Exception as e:
                st.error(f"Error reading metadata file: {e}")

        # Dropdowns for column selection
        marker_column = st.selectbox("Marker Column", options=columns, help="Select the column to use for marker colors.")
        highlight_column = st.selectbox("Highlight Column", options=["None"] + columns, help="Select the column to use for highlighting.")
        label_column = st.selectbox("Sample Label Column", options=columns, help="Select the column to use for sample labels.")

        # Update highlight values based on the selected highlight column
        if highlight_column != "None" and highlight_column in columns:
            highlight_values_options = metadata_df[highlight_column].dropna().unique().tolist()

        # Sliders for label and tip sizes
        label_size = st.slider("Label Size", 1, 20, 5)
        tip_size = st.slider("Tip Size", 1, 10, 5)

        # Multiselect for highlight values
        highlight_values = st.multiselect(
            "Highlight Values",
            options=highlight_values_options,
            help="Select values to highlight from the chosen highlight column."
        )

        # Buttons for generating and saving plots
        button_col1, button_col2, button_col3, button_col4, button_col5 = st.columns(5)
        with button_col1:
            generate_plot = st.button("Generate Plot")
        with button_col2:
            save_as_png = st.button("Save as PNG")
        with button_col3:
            save_as_pdf = st.button("Save as PDF")
        with button_col4:
            save_as_svg = st.button("Save as SVG")
        with button_col5:
            save_as_tiff = st.button("Save as TIFF")

    # Right column: Display the plot
    with col2:
        if generate_plot or save_as_png or save_as_pdf or save_as_svg or save_as_tiff:
            if metadata_file and newick_file and marker_column and label_column:
                # Generate a unique session ID
                session_id = str(uuid.uuid4())
                session_folder = f"tmp/session_{session_id}"
                os.makedirs(session_folder, exist_ok=True)

                # Save uploaded files in the session folder
                metadata_path = os.path.join(session_folder, "metadata.tsv")
                newick_path = os.path.join(session_folder, "tree.nwk")
                with open(metadata_path, "wb") as f:
                    f.write(metadata_file.getbuffer())
                with open(newick_path, "wb") as f:
                    f.write(newick_file.getbuffer())

                # Prepare highlight values
                highlight_values_str = ",".join(highlight_values) if highlight_values else "NA"

                # Determine the output format
                output_format = "png" if save_as_png else "pdf" if save_as_pdf else "svg" if save_as_svg else "tiff" if save_as_tiff else "png"
                output_file = os.path.join(session_folder, f"phylogenetic_tree.{output_format}")

                # Run the R script
                try:
                    subprocess.run(
                        [
                            "Rscript",
                            "ggtree_trial.R",
                            metadata_path,
                            newick_path,
                            marker_column,
                            highlight_column if highlight_column != "None" else "NA",
                            highlight_values_str,
                            label_column,
                            str(label_size),
                            str(tip_size),
                            output_file,
                        ],
                        check=True,
                    )
                    if output_format == "png":
                        st.image(output_file, caption="Generated Phylogenetic Tree")

                    st.success(f"Plot generated successfully! You can download it below.")

                    with open(output_file, "rb") as file:
                        st.download_button(
                            label=f"Download {output_format.upper()}",
                            data=file,
                            file_name=f"phylogenetic_tree.{output_format}",
                            mime=f"image/{output_format}" if output_format == "png" else f"application/{output_format}",
                        )

                except subprocess.CalledProcessError as e:
                    st.error(f"Error generating plot: {e}")
            else:
                st.error("Please fill in all required fields!")