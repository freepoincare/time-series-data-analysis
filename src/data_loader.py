"""Functions for loading raw and processed data."""

import pandas as pd


def load_raw_data(file_path: str) -> pd.DataFrame:
    """Load the raw Seoul daily temperature dataset.

    Expects a CSV with columns: date, tavg, tmin, tmax, station_ID, location.
    The 'date' column is expected in 'dd/mm/yyyy' format.

    Args:
        file_path: Path to the raw CSV file.

    Returns:
        DataFrame with parsed date column and basic info printed.
    """
    df = pd.read_csv(file_path)

    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Missing values:\n{df.isnull().sum()}")
    print(f"Duplicate rows: {df.duplicated().sum()}")

    return df


def load_processed_data(file_path: str) -> pd.DataFrame:
    """Load the processed Seoul temperature dataset.

    The processed CSV already includes derived columns: year, month, day,
    day_of_year, season_year, season, summer_like, winter_like, warm_day,
    hot_day, over_35, cold_day.

    Args:
        file_path: Path to the processed CSV file.

    Returns:
        DataFrame with 'date' column parsed as datetime.
    """
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    return df
