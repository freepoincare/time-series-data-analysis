"""Functions for loading raw and processed data."""

import pandas as pd


def load_data(file_path):
    """Load the selected time-series dataset.

    TODO: Implement according to the selected data format.
    """
    df = pd.read_csv(file_path)

    print(df.head(10))
    print(f"dataset shape: {df.shape}")
    print(f"dataset columns: {df.columns}")
    print(df.info())
    print(df.describe())

    return df
