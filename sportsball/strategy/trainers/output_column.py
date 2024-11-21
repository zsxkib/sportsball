"""Output column."""

OUTPUT_COLUMN = "output"


def output_prob_column(class_idx: int) -> str:
    """Produce a column name for the output probability for a class."""
    return f"output_prob_{class_idx}"
