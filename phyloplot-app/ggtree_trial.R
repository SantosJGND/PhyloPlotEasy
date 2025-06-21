# Load required libraries
library(ggtree)
library(ggplot2)
library(ggtreeExtra)
library(dplyr)
library(Polychrome)

# Define variables and constants
args <- commandArgs(trailingOnly = TRUE)

# Input arguments
metadata_file <- args[1]
newick_file <- args[2]
marker_column <- args[3]
highlight_column <- args[4]
highlights_list <- args[5]
label_column <- args[6]
letter_size <- as.numeric(args[7])
marker_size <- as.numeric(args[8])
output_file <- args[9]
colorblind <- as.logical(args[10])
axis_scale <- as.logical(args[11])

# Constants
color_palette <- "Set2" # Color palette for markers
plot_margin <- unit(c(16, 90, 5, 10), "mm") # Plot margins
highlight_fill <- "red" # Highlight fill color
highlight_alpha <- 0.2 # Highlight transparency
plot_width <- 12 # Plot width
plot_height <- 9 # Plot height
plot_dpi <- 300 # Plot resolution

# Handle optional arguments
if (highlight_column == "NA") {
  highlight_column <- NULL
}
if (marker_column == "NA") {
  marker_column <- NULL
}
if (highlights_list == "NA") {
  highlights_list <- c()
} else {
  highlights_list <- unlist(strsplit(highlights_list, ","))
}

# Read input files
tree <- read.tree(newick_file)
metadata <- read.table(metadata_file, sep = "\t", header = TRUE, stringsAsFactors = FALSE)

# Process metadata
id_column <- colnames(metadata)[1] # ID column is always the first column
metadata$sample_id <- gsub(" ", "_", metadata[[label_column]])
marker_factor <- metadata[[marker_column]]
label <- metadata[[label_column]]
label2 <- gsub(" ", "_", label)

if (!marker_column %in% colnames(metadata)) {
  stop(paste("Column", marker_column, "not found in metadata."))
} else {
  # Count the number of unique values in the marker_column
  unique_markers <- unique(metadata[[marker_column]])
  num_unique_markers <- length(unique_markers)

  # Generate a color palette using the Polychrome package
  cat("Number of unique markers:", num_unique_markers, "\n")
  if (num_unique_markers > 0) {
    if (num_unique_markers <= 22) {
      color_palette <- kelly.colors(num_unique_markers)
      names(color_palette) <- unique_markers
    } else if (num_unique_markers <= 32) {
      color_palette <- glasbey.colors(num_unique_markers)
      names(color_palette) <- unique_markers
    } else if (num_unique_markers <= 36) {
      color_palette <- palette36.colors(num_unique_markers)
      names(color_palette) <- unique_markers
    } else if (num_unique_markers <= 50) {
      color_palette <- createPalette(num_unique_markers, c("#010101"), M = 1000)
      names(color_palette) <- unique_markers
    } else {
      color_palette <- createPalette(num_unique_markers, c("#010101"), M = 1000)
      names(color_palette) <- unique_markers
    }
  } else {
    stop("No unique values found in the marker column.")
  }
}

if (colorblind == TRUE) {
  color_palette <- colorDeficit(color_palette, "deut")
}

metadata_df <- data.frame(
  label = metadata[[id_column]],
  label_two = label2,
  marker_column = marker_factor,
  stringsAsFactors = FALSE
)
metadata_df$label_two <- as.factor(metadata_df$label_two)

# Join tree with metadata
tree2 <- full_join(tree, metadata_df, by = "label")

# Create base tree plot
p <- ggtree(tree) +
  coord_cartesian(clip = "off") + theme(plot.margin = plot_margin)

if (axis_scale == TRUE) {
  p <- p + theme_tree2(plot.margin = plot_margin)
} else {
  p <- p + geom_treescale(
    fontsize = 6, linesize = 2, color = "red",
    # width = 1, color = "red", x = 0,
    # x = max(tree$edge.length) + 0.5, # Adjust x position to move it to the right
    y = -1.5 # Adjust y position to place it below the tree
  )
}

# Add metadata to the plot
dew <- p %<+% metadata_df +
  geom_tiplab(aes(label = label_two), size = letter_size, hjust = -0.2)

# Add marker points and legend
dew <- dew +
  geom_tippoint(aes(color = marker_column), size = marker_size) +
  scale_color_manual(values = color_palette) +
  theme(legend.position = "left") +
  labs(color = marker_column)

# Highlight specified nodes
for (highlight in highlights_list) {
  highlight_rows <- grep(highlight, metadata[[highlight_column]])
  highlight_leaves <- metadata_df$label[highlight_rows]
  highlight_node <- MRCA(tree, highlight_leaves)
  dew <- dew + geom_highlight(node = highlight_node, fill = highlight_fill, alpha = highlight_alpha)
}

# Save the plot
ggsave(
  filename = output_file,
  plot = dew,
  width = plot_width,
  height = plot_height,
  dpi = plot_dpi
)
