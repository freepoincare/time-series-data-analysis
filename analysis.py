"""Main entry point for the time-series analysis project."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
IMAGE_DIR = PROJECT_ROOT / "images"


def main():
    """Run the analysis pipeline."""
    print("AI time-series analysis project")
    print("TODO: implement data loading, cleaning, analysis, and visualization.")


if __name__ == "__main__":
    main()
