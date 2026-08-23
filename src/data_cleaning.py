"""Data cleaning and transformation functions."""

import pandas as pd


# ---------------------------------------------------------------------------
# Outlier detection
# ---------------------------------------------------------------------------

def find_iqr_outliers(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Detect outliers using the IQR method (1.5 × IQR rule).

    The 1.5 multiplier covers ~99.3 % of a normal distribution, making it a
    standard choice for temperature data where extreme but physically valid
    values can occur.

    Args:
        df: Input DataFrame.
        column: Name of the numeric column to check.

    Returns:
        DataFrame of rows identified as outliers.
    """
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

    print(f"\n{column}")
    print(f"  Q1: {q1:.2f},  Q3: {q3:.2f},  IQR: {iqr:.2f}")
    print(f"  Lower bound: {lower_bound:.2f},  Upper bound: {upper_bound:.2f}")
    print(f"  Number of outliers: {len(outliers)}")

    return outliers


# ---------------------------------------------------------------------------
# Cleaning pipeline
# ---------------------------------------------------------------------------

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate the raw Seoul temperature DataFrame.

    Steps performed:
      1. Parse 'date' from 'dd/mm/yyyy' string to datetime.
      2. Report – but do not drop – the two missing tmin/tmax values
         (they are retained as NaN; downstream aggregations handle them
         via pandas' default skipna behaviour).
      3. Assert no duplicate dates exist.
      4. Drop uninformative columns: 'station_ID', 'location'
         (only one station, Seoul, is present in the dataset).

    Args:
        df: Raw DataFrame as returned by ``load_raw_data``.

    Returns:
        Cleaned DataFrame ready for transformation.
    """
    # --- 1. Parse dates ---
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")

    # --- 2. Report missing values ---
    missing = df.isnull().sum()
    if missing.any():
        print("Missing values per column:")
        print(missing[missing > 0])
    else:
        print("No missing values found.")

    # --- 3. Check for duplicates ---
    dup_rows = df.duplicated().sum()
    dup_dates = df["date"].duplicated().sum()
    print(f"Duplicate rows: {dup_rows}")
    print(f"Duplicate dates: {dup_dates}")
    assert dup_dates == 0, "Unexpected duplicate dates in dataset."

    # --- 4. Drop uninformative columns (if present) ---
    cols_to_drop = [c for c in ["station_ID", "location"] if c in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        print(f"Dropped columns: {cols_to_drop}")

    print(f"\nCleaned dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


# ---------------------------------------------------------------------------
# Feature engineering / transformation
# ---------------------------------------------------------------------------

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived time and temperature-category columns.

    New columns added:
      - year, month, day, day_of_year  – temporal breakdown of 'date'
      - season                         – meteorological season (Spring/Summer/
                                         Autumn/Winter) based on month
      - summer_like  (0/1)  – tavg >= 20 °C  (KMA summer criterion)
      - winter_like  (0/1)  – tavg <= 5 °C   (KMA winter criterion)
      - warm_day     (0/1)  – 25 <= tmax < 30 °C
      - hot_day      (0/1)  – 30 <= tmax < 35 °C
      - over_35      (0/1)  – tmax >= 35 °C  (extreme heat day)
      - cold_day     (0/1)  – tmax <= 10 °C AND tmin < 0 °C

    Args:
        df: Cleaned DataFrame as returned by ``clean_data``.

    Returns:
        Transformed DataFrame with all derived columns.
    """
    df = df.copy()

    # --- Temporal features ---
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_of_year"] = df["date"].dt.dayofyear

    # --- Season (meteorological) ---
    def _get_season(month: int) -> str:
        if month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        elif month in [9, 10, 11]:
            return "Autumn"
        else:
            return "Winter"

    df["season"] = df["month"].apply(_get_season)

    # --- Temperature-based indicators ---
    df["summer_like"] = (df["tavg"] >= 20).astype(int)
    df["winter_like"] = (df["tavg"] <= 5).astype(int)
    df["warm_day"]    = ((df["tmax"] >= 25) & (df["tmax"] < 30)).astype(int)
    df["hot_day"]     = ((df["tmax"] >= 30) & (df["tmax"] < 35)).astype(int)
    df["over_35"]     = (df["tmax"] >= 35).astype(int)
    df["cold_day"]    = ((df["tmax"] <= 10) & (df["tmin"] < 0)).astype(int)

    print("\n=== Transformed Data Summary ===")
    print(f"Columns: {list(df.columns)}")
    print(f"Year range: {df['year'].min()} – {df['year'].max()}")
    print(f"Summer-like days : {df['summer_like'].sum()}")
    print(f"Winter-like days : {df['winter_like'].sum()}")
    print(f"Extreme heat days: {df['over_35'].sum()}")

    return df
