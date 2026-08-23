"""Visualization functions for time series data analysis.

Generates and saves formatted plots to the images/plots directory:
  01_raw_temperature_timeseries.png
  02_temperature_distribution.png
  03_tmin_tmax_relationship.png
  04_temperature_boxplots.png
  05_annual_temperature_history.png
  06_summer_winter_temperature.png
  07_annual_days_over_35.png
  08_annual_temp_moving_average.png
  09_annual_temp_linear_trend.png
  10_annual_days_over_35_trend.png
  11_summer_like_heatmap.png
  12_winter_like_heatmap.png
  13_seasonal_expansion_comparison.png
  14_summer_forecast_linear.png
  15_summer_forecast_arima.png
"""

from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


def plot_raw_time_series(df: pd.DataFrame, save_path: Optional[Path] = None):
    """Plot raw daily temperature time series (tavg, tmax, tmin)."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df["date"], df["tavg"], color="black", label="Avg Temperature", alpha=0.7, linewidth=0.8)
    ax.plot(df["date"], df["tmax"], 'r--', label="Max Temperature", alpha=0.6, linewidth=0.5)
    ax.plot(df["date"], df["tmin"], 'b--', label="Min Temperature", alpha=0.6, linewidth=0.5)
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Seoul Daily Temperature (1907–2026)")
    ax.legend(loc="upper left")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_temperature_distribution(df: pd.DataFrame, save_path: Optional[Path] = None):
    """Plot distribution histogram of daily average temperature."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df["tavg"].dropna(), bins=50, color="skyblue", edgecolor="black")
    ax.set_xlabel("Average Temperature (°C)")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Daily Average Temperature")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_tmin_tmax_scatter(df: pd.DataFrame, save_path: Optional[Path] = None):
    """Scatter plot showing relationship between daily min and max temperature."""
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(df["tmin"], df["tmax"], s=5, alpha=0.3, color="teal")
    ax.set_xlabel("Minimum Temperature (°C)")
    ax.set_ylabel("Maximum Temperature (°C)")
    ax.set_title("Relationship Between Daily Min and Max Temperature")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_temperature_boxplots(df: pd.DataFrame, save_path: Optional[Path] = None):
    """Boxplot of tavg, tmax, and tmin."""
    fig, ax = plt.subplots(figsize=(5, 5))
    df.boxplot(column=["tavg", "tmax", "tmin"], ax=ax)
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature Distribution (Boxplot)")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_annual_temperature_history(annual_temp: pd.DataFrame, save_path: Optional[Path] = None):
    """Plot annual average, min, and max temperature over time."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(annual_temp["year"], annual_temp["avg_temp"], 'k-', label="Annual Average Temp", linewidth=1.2)
    ax.plot(annual_temp["year"], annual_temp["avg_min_temp"], 'b--', label="Annual Average Min Temp", alpha=0.7)
    ax.plot(annual_temp["year"], annual_temp["avg_max_temp"], 'r--', label="Annual Average Max Temp", alpha=0.7)
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Annual Average Temperature in Seoul (1907–2026)")
    ax.legend(loc="lower right")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_summer_winter_temperature(seasonal_pivot: pd.DataFrame, save_path: Optional[Path] = None):
    """Plot historical Summer vs Winter average temperature."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(seasonal_pivot["year"], seasonal_pivot["Summer"], label="Summer", color="red", alpha=0.8)
    ax.plot(seasonal_pivot["year"], seasonal_pivot["Winter"], label="Winter", color="blue", alpha=0.8)
    ax.set_xlabel("Year")
    ax.set_ylabel("Average Temperature (°C)")
    ax.set_title("Summer and Winter Average Temperature in Seoul")
    ax.legend()
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_annual_days_over_35(annual_over_35: pd.DataFrame, save_path: Optional[Path] = None):
    """Bar chart of annual days with maximum temperature >= 35°C."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(annual_over_35["year"], annual_over_35["days_over_35"], color="crimson", alpha=0.6)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Days")
    ax.set_title("Annual Number of Days with Tmax ≥ 35°C")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_moving_average_trend(annual_temp: pd.DataFrame, save_path: Optional[Path] = None):
    """Plot 10-year moving average against annual temperature."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ma = annual_temp["avg_temp"].rolling(window=10).mean()
    ax.plot(annual_temp["year"], annual_temp["avg_temp"], label="Annual Average Temperature", alpha=0.4, color="gray")
    ax.plot(annual_temp["year"], ma, label="10-Year Moving Average", linewidth=2.5, color="darkorange")
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Long-Term Temperature Trend in Seoul (10-Year Moving Average)")
    ax.legend()
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_linear_trend(annual_temp: pd.DataFrame, save_path: Optional[Path] = None):
    """Plot annual temperature with linear regression trendline."""
    fig, ax = plt.subplots(figsize=(12, 5))
    x = annual_temp["year"]
    y = annual_temp["avg_temp"]
    slope, intercept, r_val, p_val, _ = stats.linregress(x, y)
    trend_line = intercept + slope * x

    ax.scatter(x, y, s=15, color="black", alpha=0.6, label="Annual Average Temperature")
    ax.plot(x, trend_line, color="red", linewidth=2, label=f"Linear Trend (slope={slope:.4f}°C/year, p={p_val:.4g})")
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Linear Trend of Annual Average Temperature in Seoul")
    ax.legend()
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_days_over_35_trend(annual_over_35: pd.DataFrame, save_path: Optional[Path] = None):
    """Plot bar chart of days >= 35°C with linear trend overlay."""
    fig, ax = plt.subplots(figsize=(12, 5))
    x = annual_over_35["year"]
    y = annual_over_35["days_over_35"]
    slope, intercept, _, p_val, _ = stats.linregress(x, y)
    trend_line = intercept + slope * x

    ax.bar(x, y, color="salmon", alpha=0.7, label="Days ≥ 35°C")
    ax.plot(x, trend_line, color="darkred", linewidth=2, label=f"Linear Trend (p={p_val:.4g})")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Days")
    ax.set_title("Annual Number of Days with Maximum Temperature ≥ 35°C (with Trend)")
    ax.legend()
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_summer_heatmap(monthly_ratio: pd.DataFrame, save_path: Optional[Path] = None):
    """Heatmap of summer-like day percentages across May-September."""
    summer_trans = monthly_ratio[monthly_ratio["month"].isin([5, 6, 7, 8, 9])]
    pivot = summer_trans.pivot(index="year", columns="month", values="summer_like_percent")

    fig, ax = plt.subplots(figsize=(6, 8))
    im = ax.imshow(pivot, aspect="auto", interpolation="nearest", cmap="YlOrRd")
    fig.colorbar(im, ax=ax, label="Summer-like Days (%)")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns)
    ax.set_xlabel("Month")
    ax.set_ylabel("Year Index")
    ax.set_title("Summer-like Days (%) by Year and Month (May–Sep)")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_winter_heatmap(monthly_ratio: pd.DataFrame, save_path: Optional[Path] = None):
    """Heatmap of winter-like day percentages across Nov-March."""
    winter_trans = monthly_ratio[monthly_ratio["month"].isin([11, 12, 1, 2, 3])]
    pivot = winter_trans.pivot(index="year", columns="month", values="winter_like_percent")

    fig, ax = plt.subplots(figsize=(6, 8))
    im = ax.imshow(pivot, aspect="auto", interpolation="nearest", cmap="YlGnBu")
    fig.colorbar(im, ax=ax, label="Winter-like Days (%)")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns)
    ax.set_xlabel("Month")
    ax.set_ylabel("Year Index")
    ax.set_title("Winter-like Days (%) by Year and Month (Nov–Mar)")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_seasonal_expansion_comparison(df: pd.DataFrame, save_path: Optional[Path] = None):
    """Compare summer-like and winter-like percentages between early (1907-1936) and recent (1997-2026) periods."""
    early = df[df["year"].between(1907, 1936)]
    recent = df[df["year"].between(1997, 2026)]

    early_summer = early.groupby("month")["summer_like"].mean() * 100
    recent_summer = recent.groupby("month")["summer_like"].mean() * 100
    early_winter = early.groupby("month")["winter_like"].mean() * 100
    recent_winter = recent.groupby("month")["winter_like"].mean() * 100

    months = list(range(1, 13))

    fig, axes = plt.subplots(1, 2, figsize=(14, 4))

    # Summer-like comparison
    axes[0].plot(months, early_summer.loc[months], marker="o", label="1907–1936", color="steelblue")
    axes[0].plot(months, recent_summer.loc[months], marker="o", label="1997–2026", color="firebrick")
    axes[0].set_title("Summer-like Days (%): Early vs Recent")
    axes[0].set_xlabel("Month")
    axes[0].set_ylabel("Summer-like Days (%)")
    axes[0].set_xticks(months)
    axes[0].legend()

    # Winter-like comparison
    axes[1].plot(months, early_winter.loc[months], marker="o", label="1907–1936", color="steelblue")
    axes[1].plot(months, recent_winter.loc[months], marker="o", label="1997–2026", color="firebrick")
    axes[1].set_title("Winter-like Days (%): Early vs Recent")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Winter-like Days (%)")
    axes[1].set_xticks(months)
    axes[1].legend()

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_summer_forecast_linear(
    summer_annual: pd.DataFrame,
    forecast_df: pd.DataFrame,
    slope: float,
    intercept: float,
    p_val: float,
    save_path: Optional[Path] = None
):
    """Plot historical summer temperature and 5-year Linear Regression forecast."""
    fig, ax = plt.subplots(figsize=(12, 5))
    x_hist = summer_annual["year"]
    y_hist = summer_annual["summer_avg_temp"]
    trend_line = intercept + slope * x_hist

    ax.scatter(x_hist, y_hist, color="black", s=15, label="Historical Summer Temp")
    ax.plot(x_hist, trend_line, color="blue", linewidth=1.5, label=f"Trend (slope={slope:.4f}°C/year)")
    ax.plot(forecast_df["year"], forecast_df["predicted_summer_avg_temp"], color="red", marker="o", linewidth=2, label="Linear Regression Forecast (5y)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Summer Average Temperature (°C)")
    ax.set_title("5-Year Forecast of Seoul Summer Average Temperature (Linear Regression)")
    ax.legend()
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)


def plot_summer_forecast_arima(
    summer_ts: pd.Series,
    forecast_df: pd.DataFrame,
    save_path: Optional[Path] = None
):
    """Plot historical summer temperature and 5-year ARIMA(0,1,1) forecast with confidence intervals."""
    fig, ax = plt.subplots(figsize=(12, 5))
    recent_ts = summer_ts.iloc[-50:]  # Focus on last 50 years for visual clarity

    ax.plot(recent_ts.index, recent_ts.values, label="Historical Summer Temp (Last 50 Years)", color="black")
    ax.plot(forecast_df["year"], forecast_df["forecast_temp"], label="ARIMA(0,1,1) Forecast", color="crimson", marker="o", linewidth=2)
    ax.fill_between(
        forecast_df["year"],
        forecast_df["lower_95"],
        forecast_df["upper_95"],
        color="pink",
        alpha=0.3,
        label="95% Confidence Interval"
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Summer Average Temperature (°C)")
    ax.set_title("5-Year Forecast of Seoul Summer Average Temperature (ARIMA)")
    ax.legend(loc="upper left")
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)
