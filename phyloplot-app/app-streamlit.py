import streamlit as st
import pandas as pd
import subprocess

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
        generate_plot = st.button("Generate Plot")
        save_as_png = st.button("Save as PNG")
        save_as_pdf = st.button("Save as PDF")

    # Right column: Display the plot
    with col2:
        if generate_plot or save_as_png or save_as_pdf:
            if metadata_file and newick_file and marker_column and label_column:
                # Save uploaded files
                with open("metadata.tsv", "wb") as f:
                    f.write(metadata_file.getbuffer())
                with open("tree.nwk", "wb") as f:
                    f.write(newick_file.getbuffer())

                # Prepare highlight values
                highlight_values_str = ",".join(highlight_values) if highlight_values else "NA"

                # Determine the output format
                output_format = "png" if save_as_png else "pdf" if save_as_pdf else "png"

                # Run the R script
                try:
                    subprocess.run(
                        [
                            "Rscript",
                            "ggtree_trial.R",
                            "metadata.tsv",
                            "tree.nwk",
                            marker_column,
                            highlight_column if highlight_column != "None" else "NA",
                            highlight_values_str,
                            label_column,
                            str(label_size),
                            str(tip_size),
                            output_format,
                        ],
                        check=True,
                    )
                    if output_format == "png":
                        st.image("phylogenetic_tree.png", caption="Generated Phylogenetic Tree")

                    else:
                        st.success("PDF saved as phylogenetic_tree.pdf")

                    with open(f"phylogenetic_tree.{output_format}", "rb") as file:
                        st.download_button(
                            label=f"Download {output_format.upper()}",
                            data=file,
                            file_name="phylogenetic_tree." + output_format,
                            mime=f"image/{output_format}" if output_format == "png" else "application/pdf",
                        )

                except subprocess.CalledProcessError as e:
                    st.error(f"Error generating plot: {e}")
            else:
                st.error("Please fill in all required fields!")