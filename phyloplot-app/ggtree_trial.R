library(ggtree)
library(ggplot2)
library(ggtreeExtra)
library(dplyr)

args <- commandArgs(trailingOnly = TRUE)

# Read arguments from the command line


metadata_file <- args[1]
newick_file <- args[2]
marker_column <- args[3]
highlight_column <- args[4]
highlights_list <- args[5]
label_column <- args[6]
letter_size <- as.numeric(args[7])
marker_size <- as.numeric(args[8])
output_file <- args[9]

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

tree <- read.tree(newick_file)
metadata <- read.table(metadata_file, sep = "\t", header = TRUE, stringsAsFactors = FALSE)

metadata$sample_id <- gsub(" ", "_", metadata[[label_column]])
marker_factor <- metadata[[marker_column]]
label <- metadata[[label_column]]
label2 <- gsub(" ", "_", label)
if (!marker_column %in% colnames(metadata)) {
  stop(paste("Column", marker_column, "not found in metadata."))
}


metadata_df <- data.frame(label = metadata$sequence, label_two = label2, marker_column = marker_factor, stringsAsFactors = FALSE)
metadata_df$label_two <- as.factor(metadata_df$label_two)
tree2 <- full_join(tree, metadata_df, by = "label")

p <- ggtree(tree) + coord_cartesian(clip = "off") + theme_tree2(plot.margin = unit(c(16, 90, 15, 10), "mm"))
dew <- p %<+% metadata_df + geom_tiplab(aes(label = label_two), size = letter_size, hjust = -0.2)

# set legent title too marker_column
dew <- dew + geom_tippoint(aes(color = marker_column), size = marker_size) +
  scale_color_brewer(palette = "Set2") +
  theme(legend.position = "left") +
  labs(color = marker_column)

for (highlight in highlights_list) {
  highlight_rows <- grep(highlight, metadata[[highlight_column]])
  highlight_leaves <- metadata_df$label[highlight_rows]
  highlight_node <- MRCA(tree, highlight_leaves)
  dew <- dew + geom_highlight(node = highlight_node, fill = "red", alpha = 0.2)
}

ggsave(
  filename = output_file,
  plot = dew, width = 12, height = 9, dpi = 300
)
