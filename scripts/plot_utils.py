from pathlib import Path  # Provides filesystem path handling utilities
import matplotlib.pyplot as plt  # Exposes the Matplotlib plotting interface
import atexit  # Allows registering cleanup callbacks on interpreter exit
import re  # Supplies regular expression helpers for slug creation

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # Resolves the repository root directory
OUT_DIR = PROJECT_ROOT / "reports" / "Datasets"  # Points to the default directory for saved figures
OUT_DIR.mkdir(parents=True, exist_ok=True)  # Creates the plots directory tree if it does not already exist


def slugify(text: str) -> str:  # Converts arbitrary text into a filesystem-friendly slug
    text = text.strip().lower()  # Normalizes the text by trimming edges and forcing lowercase
    text = re.sub(r"\s+", "_", text)  # Replaces runs of whitespace with single underscores
    text = re.sub(r"[^\w\-۰-۹ا-ی_]", "", text)  # Removes characters outside word chars and allowed numerals
    return text if text else "figure"  # Falls back to a generic label when no characters remain


def save_all_figs(title: str , dir: str) -> None:  # Saves all currently open Matplotlib figures to disk
    for i in plt.get_fignums():  # Iterates through every active Matplotlib figure number
        fig = plt.figure(i)  # Retrieves the figure object for the current index
        axes = fig.get_axes()  # Collects the axes to access potential titles
        explicit_title = slugify(title) if title else None  # Builds a slug from the provided title when present
        axis_title = slugify(axes[0].get_title()) if axes and axes[0].get_title() else None  # Derives a slug from the first axis title when available
        base = explicit_title or axis_title or f"figure_{i}"  # Chooses the first available slug or a numbered fallback
        filename = f"{base}_{i}.png"  # Appends the figure index to ensure unique filenames
        fig.savefig(OUT_DIR / dir / filename, dpi=300, bbox_inches="tight")  # Writes the figure to disk with high resolution and tight layout
    print(f"All figures saved in {OUT_DIR}")  # Confirms the save location after processing every figure
