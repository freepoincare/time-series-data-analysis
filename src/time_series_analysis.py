"""Time-series analysis functions.

Implements all analytical methods from the exploratory and modeling notebooks:
  - Descriptive summary aggregations (annual, seasonal, over 35°C, monthly characteristics)
  - 10-year and 5-year moving averages
  - Linear regression trend analysis (using scipy.stats.linregress)
  - Non-parametric Mann-Kendall trend tests and Sen's slope (using pymannkendall)
  - Transition month edge analysis (May, Sept, Nov, Mar)
  - Summer temperature forecasting using Linear Regression and ARIMA(0,1,1)
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from scipy import stats
import pymannkendall as mk
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ---------------------------------------------------------------------------
# 1. Descriptive Aggregations
# ---------------------------------------------------------------------------

def calculate_annual_temperature(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate annual average, minimum, and maximum temperatures."""
    annual_temp = (
        df.groupby("year")
        .agg(
            avg_temp=("tavg", "mean"),
            avg_min_temp=("tmin", "mean"),
            avg_max_temp=("tmax", "mean")
        )
        .reset_index()
    )
    return annual_temp


def calculate_seasonal_temperature(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate seasonal average temperature pivot table for Summer and Winter."""
    seasonal_temp = (
        df[df["season"].isin(["Summer", "Winter"])]
        .groupby(["year", "season"])["tavg"]
        .mean()
        .reset_index()
    )
    pivot = seasonal_temp.pivot(
        index="year",
        columns="season",
        values="tavg"
    ).reset_index()
    return pivot


def calculate_annual_over_35(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the annual count of extreme heat days (Tmax >= 35°C)."""
    return df.groupby("year")["over_35"].sum().reset_index(name="days_over_35")


def calculate_monthly_characteristics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly summer-like and winter-like day ratios and percentages."""
    monthly = (
        df.groupby(["year", "month"])
        .agg(
            summer_like_ratio=("summer_like", "mean"),
            winter_like_ratio=("winter_like", "mean")
        )
        .reset_index()
    )
    monthly["summer_like_percent"] = monthly["summer_like_ratio"] * 100.0
    monthly["winter_like_percent"] = monthly["winter_like_ratio"] * 100.0
    return monthly


# ---------------------------------------------------------------------------
# 2. Trend Analysis
# ---------------------------------------------------------------------------

def calculate_moving_average(series: pd.Series, window: int = 10) -> pd.Series:
    """Calculate rolling moving average with specified window size."""
    return series.rolling(window=window).mean()


def run_linear_regression(x: pd.Series, y: pd.Series) -> Dict[str, Any]:
    """Perform linear regression and return statistical metrics."""
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return {
        "slope": slope,
        "intercept": intercept,
        "r_value": r_value,
        "r_squared": r_value ** 2,
        "p_value": p_value,
        "std_err": std_err,
        "change_per_100_years": slope * 100.0
    }


def run_mann_kendall_test(series: pd.Series) -> Dict[str, Any]:
    """Perform Mann-Kendall trend test and compute Sen's slope."""
    result = mk.original_test(series)
    return {
        "trend": result.trend,
        "p_value": result.p,
        "tau": result.Tau,
        "sen_slope": result.slope
    }


def analyze_all_trends(df: pd.DataFrame) -> pd.DataFrame:
    """Compute trend metrics (Linear regression + Mann-Kendall) across key temperature series.

    Series evaluated:
      - Annual Average Temperature
      - Summer Average Temperature
      - Winter Average Temperature
      - Days >= 35°C
    """
    annual_temp = calculate_annual_temperature(df)
    annual_35 = calculate_annual_over_35(df)

    summer_temp = (
        df[df["season"] == "Summer"]
        .groupby("year")["tavg"]
        .mean()
        .reset_index(name="summer_avg_temp")
    )
    winter_temp = (
        df[df["season"] == "Winter"]
        .groupby("year")["tavg"]
        .mean()
        .reset_index(name="winter_avg_temp")
    )

    series_dict = {
        "Annual Average Temperature": (annual_temp["year"], annual_temp["avg_temp"]),
        "Summer Average Temperature": (summer_temp["year"], summer_temp["summer_avg_temp"]),
        "Winter Average Temperature": (winter_temp["year"], winter_temp["winter_avg_temp"]),
        "Days >= 35 degC": (annual_35["year"], annual_35["days_over_35"])
    }

    records = []
    for name, (x, y) in series_dict.items():
        lr = run_linear_regression(x, y)
        mk_res = run_mann_kendall_test(y)
        records.append({
            "dataset": name,
            "linear_slope_per_year": lr["slope"],
            "linear_p_value": lr["p_value"],
            "linear_r_value": lr["r_value"],
            "mann_kendall_trend": mk_res["trend"],
            "mann_kendall_p_value": mk_res["p_value"],
            "sen_slope": mk_res["sen_slope"]
        })

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# 3. Seasonal Expansion Analysis
# ---------------------------------------------------------------------------

def analyze_seasonal_expansion(monthly_ratio: pd.DataFrame) -> pd.DataFrame:
    """Analyze long-term trends in transition months (May, Sept for Summer; Nov, Mar for Winter)."""
    configs = [
        ("Summer", 5, "summer_like_percent"),
        ("Summer", 9, "summer_like_percent"),
        ("Winter", 11, "winter_like_percent"),
        ("Winter", 3, "winter_like_percent"),
    ]

    results = []
    for season_name, month, var_name in configs:
        m_data = monthly_ratio[monthly_ratio["month"] == month].dropna(subset=[var_name]).copy()
        x = m_data["year"]
        y = m_data[var_name]

        lr = run_linear_regression(x, y)
        mk_res = run_mann_kendall_test(y)

        results.append({
            "season": season_name,
            "month": month,
            "slope": lr["slope"],
            "r_squared": lr["r_squared"],
            "linear_p_value": lr["p_value"],
            "change_per_100_years": lr["change_per_100_years"],
            "mk_trend": mk_res["trend"],
            "mk_p_value": mk_res["p_value"],
            "sen_slope": mk_res["sen_slope"]
        })

    return pd.DataFrame(results)


# ---------------------------------------------------------------------------
# 4. Forecasting: Linear Regression and ARIMA
# ---------------------------------------------------------------------------

def check_stationarity(series: pd.Series) -> Dict[str, Any]:
    """Run Augmented Dickey-Fuller (ADF) test on a time series."""
    adf_res = adfuller(series.dropna())
    return {
        "adf_statistic": adf_res[0],
        "p_value": adf_res[1],
        "is_stationary": adf_res[1] < 0.05
    }


def forecast_summer_linear(
    summer_df: pd.DataFrame,
    forecast_years: int = 5
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """Forecast future summer average temperature using Linear Regression."""
    # Fit on all complete years
    train_df = summer_df[summer_df["year"] < 2026].copy()

    # Train/test split evaluation on last 5 years
    eval_train = train_df.iloc[:-forecast_years]
    eval_test = train_df.iloc[-forecast_years:]

    slope_eval, intercept_eval, _, _, _ = stats.linregress(eval_train["year"], eval_train["summer_avg_temp"])
    test_pred = intercept_eval + slope_eval * eval_test["year"]

    metrics = {
        "mae": float(mean_absolute_error(eval_test["summer_avg_temp"], test_pred)),
        "rmse": float(np.sqrt(mean_squared_error(eval_test["summer_avg_temp"], test_pred)))
    }

    # Final fit on full dataset
    slope, intercept, r_value, p_value, std_err = stats.linregress(train_df["year"], train_df["summer_avg_temp"])
    last_year = int(train_df["year"].max())
    future_years_arr = np.arange(last_year + 1, last_year + forecast_years + 1)
    future_pred = intercept + slope * future_years_arr

    forecast_df = pd.DataFrame({
        "year": future_years_arr,
        "predicted_summer_avg_temp": future_pred
    })

    return forecast_df, metrics


def forecast_summer_arima(
    summer_df: pd.DataFrame,
    order: Tuple[int, int, int] = (0, 1, 1),
    forecast_years: int = 5
) -> Tuple[pd.DataFrame, Dict[str, float], Any]:
    """Forecast future summer average temperature using ARIMA model."""
    complete_df = summer_df[summer_df["year"] < 2026].copy()
    ts = complete_df.set_index("year")["summer_avg_temp"]

    # Train/test evaluation
    eval_train = ts.iloc[:-forecast_years]
    eval_test = ts.iloc[-forecast_years:]

    eval_model = ARIMA(eval_train, order=order).fit()
    eval_forecast = eval_model.get_forecast(steps=len(eval_test)).predicted_mean

    metrics = {
        "mae": float(mean_absolute_error(eval_test, eval_forecast)),
        "rmse": float(np.sqrt(mean_squared_error(eval_test, eval_forecast)))
    }

    # Fit model on entire series
    final_model = ARIMA(ts, order=order).fit()
    forecast_res = final_model.get_forecast(steps=forecast_years)
    forecast_mean = forecast_res.predicted_mean
    conf_int = forecast_res.conf_int()

    last_year = int(ts.index.max())
    future_years_idx = list(range(last_year + 1, last_year + forecast_years + 1))

    forecast_df = pd.DataFrame({
        "year": future_years_idx,
        "forecast_temp": forecast_mean.values,
        "lower_95": conf_int.iloc[:, 0].values,
        "upper_95": conf_int.iloc[:, 1].values
    })

    return forecast_df, metrics, final_model
