from flask import Flask, render_template, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        metadata_file = request.files["metadata_file"]
        newick_file = request.files["newick_file"]
        marker_column = request.form["marker_column"]
        highlight_column = request.form["highlight_column"]
        label_column = request.form["label_column"]
        label_size = request.form["label_size"]
        tip_size = request.form["tip_size"]
        highlight_values = request.form.getlist("highlight_values")

        # Save uploaded files
        metadata_file.save("metadata.tsv")
        newick_file.save("tree.nwk")

        # Run the R script
        highlight_values_str = ",".join(highlight_values)
        subprocess.run(
            [
                "Rscript",
                "ggtree_trial.R",
                "metadata.tsv",
                "tree.nwk",
                marker_column,
                highlight_column,
                highlight_values_str,
                label_column,
                label_size,
                tip_size,
                "png"
            ],
            check=True
        )

        # Return the generated plot
        return send_file("phylogenetic_tree.png", as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)