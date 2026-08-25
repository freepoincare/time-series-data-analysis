"""Main execution pipeline for the Seoul Time Series Temperature Analysis project.

Executes end-to-end data processing, statistical time series analysis,
forecasting, and plot generation, saving all outputs to data/processed/ and images/plots/.
"""

import os
import sys
from pathlib import Path

# Configure utf-8 encoding for Windows standard output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

from src.data_loader import load_raw_data, load_processed_data
from src.data_cleaning import clean_data, transform_data, find_iqr_outliers
from src.time_series_analysis import (
    calculate_annual_temperature,
    calculate_seasonal_temperature,
    calculate_annual_over_35,
    calculate_monthly_characteristics,
    analyze_all_trends,
    analyze_seasonal_expansion,
    forecast_summer_linear,
    forecast_summer_arima,
    run_linear_regression
)
from src import visualization as viz

PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "dataset_original.csv"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DATA_PATH = PROCESSED_DATA_DIR / "dataset_processed.csv"
PLOTS_DIR = PROJECT_ROOT / "images" / "plots"


def run_pipeline():
    """Run full analysis pipeline."""
    print("=" * 70)
    print("SEOUL TIME SERIES TEMPERATURE ANALYSIS PIPELINE")
    print("=" * 70)

    # Ensure output directories exist
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # Step 1: Load and Preprocess Raw Data
    # -------------------------------------------------------------------------
    print("\n[Step 1/5] Loading & Preprocessing Raw Data...")
    raw_df = load_raw_data(str(RAW_DATA_PATH))
    
    # Generate initial EDA plots from raw data
    print("  -> Generating raw data visualizations...")
    viz.plot_raw_time_series(raw_df, PLOTS_DIR / "01_raw_temperature_timeseries.png")
    viz.plot_temperature_distribution(raw_df, PLOTS_DIR / "02_temperature_distribution.png")
    viz.plot_tmin_tmax_scatter(raw_df, PLOTS_DIR / "03_tmin_tmax_relationship.png")

    cleaned_df = clean_data(raw_df)
    processed_df = transform_data(cleaned_df)

    # Check IQR outliers and plot boxplots
    find_iqr_outliers(processed_df, "tavg")
    find_iqr_outliers(processed_df, "tmin")
    find_iqr_outliers(processed_df, "tmax")
    viz.plot_temperature_boxplots(processed_df, PLOTS_DIR / "04_temperature_boxplots.png")

    # Save processed dataset
    processed_df.to_csv(PROCESSED_DATA_PATH, index=False, encoding="utf-8-sig")
    print(f"  -> Saved processed dataset to {PROCESSED_DATA_PATH}")

    # -------------------------------------------------------------------------
    # Step 2: Descriptive Analysis & Aggregations
    # -------------------------------------------------------------------------
    print("\n[Step 2/5] Performing Descriptive Analysis & Aggregations...")
    annual_temp = calculate_annual_temperature(processed_df)
    annual_temp.to_csv(PROCESSED_DATA_DIR / "annual_temperature.csv", index=False, encoding="utf-8-sig")

    seasonal_pivot = calculate_seasonal_temperature(processed_df)
    seasonal_pivot.to_csv(PROCESSED_DATA_DIR / "seasonal_temperature.csv", index=False, encoding="utf-8-sig")

    annual_35 = calculate_annual_over_35(processed_df)
    annual_35.to_csv(PROCESSED_DATA_DIR / "annual_over_35.csv", index=False, encoding="utf-8-sig")

    monthly_chars = calculate_monthly_characteristics(processed_df)
    monthly_chars.to_csv(PROCESSED_DATA_DIR / "monthly_ratio.csv", index=False, encoding="utf-8-sig")

    # Descriptive plots
    viz.plot_annual_temperature_history(annual_temp, PLOTS_DIR / "05_annual_temperature_history.png")
    viz.plot_summer_winter_temperature(seasonal_pivot, PLOTS_DIR / "06_summer_winter_temperature.png")
    viz.plot_annual_days_over_35(annual_35, PLOTS_DIR / "07_annual_days_over_35.png")

    # -------------------------------------------------------------------------
    # Step 3: Trend Analysis (Moving Average, Linear Regression, Mann-Kendall)
    # -------------------------------------------------------------------------
    print("\n[Step 3/5] Performing Trend Analysis (Linear Regression & Mann-Kendall)...")
    trend_results = analyze_all_trends(processed_df)
    trend_results.to_csv(PROCESSED_DATA_DIR / "trend_analysis_results.csv", index=False, encoding="utf-8-sig")
    print("  -> Trend Results:")
    print(trend_results)

    viz.plot_moving_average_trend(annual_temp, PLOTS_DIR / "08_annual_temp_moving_average.png")
    viz.plot_linear_trend(annual_temp, PLOTS_DIR / "09_annual_temp_linear_trend.png")
    viz.plot_days_over_35_trend(annual_35, PLOTS_DIR / "10_annual_days_over_35_trend.png")

    # -------------------------------------------------------------------------
    # Step 4: Seasonal Expansion Analysis
    # -------------------------------------------------------------------------
    print("\n[Step 4/5] Performing Seasonal Expansion Analysis...")
    seasonal_exp_results = analyze_seasonal_expansion(monthly_chars)
    seasonal_exp_results.to_csv(PROCESSED_DATA_DIR / "seasonal_expansion_trend_results.csv", index=False, encoding="utf-8-sig")
    print("  -> Seasonal Expansion Results:")
    print(seasonal_exp_results)

    viz.plot_summer_heatmap(monthly_chars, PLOTS_DIR / "11_summer_like_heatmap.png")
    viz.plot_winter_heatmap(monthly_chars, PLOTS_DIR / "12_winter_like_heatmap.png")
    viz.plot_seasonal_expansion_comparison(processed_df, PLOTS_DIR / "13_seasonal_expansion_comparison.png")

    # -------------------------------------------------------------------------
    # Step 5: Forecasting (Linear Regression & ARIMA)
    # -------------------------------------------------------------------------
    print("\n[Step 5/5] Forecasting Future Summer Temperatures (5 Years)...")
    summer_annual = (
        processed_df[processed_df["season"] == "Summer"]
        .groupby("year")["tavg"]
        .mean()
        .reset_index(name="summer_avg_temp")
    )

    # 5.1 Linear Forecast
    linear_forecast_df, linear_metrics = forecast_summer_linear(summer_annual, forecast_years=5)
    print(f"  -> Linear Regression Forecast Evaluation: MAE={linear_metrics['mae']:.3f}°C, RMSE={linear_metrics['rmse']:.3f}°C")
    
    # Fit for plotting line parameters
    train_clean = summer_annual[summer_annual["year"] < 2026]
    lr_full = run_linear_regression(train_clean["year"], train_clean["summer_avg_temp"])
    viz.plot_summer_forecast_linear(
        train_clean,
        linear_forecast_df,
        lr_full["slope"],
        lr_full["intercept"],
        lr_full["p_value"],
        PLOTS_DIR / "14_summer_forecast_linear.png"
    )

    # 5.2 ARIMA Forecast
    arima_forecast_df, arima_metrics, _ = forecast_summer_arima(summer_annual, order=(0, 1, 1), forecast_years=5)
    print(f"  -> ARIMA(0,1,1) Forecast Evaluation: MAE={arima_metrics['mae']:.3f}°C, RMSE={arima_metrics['rmse']:.3f}°C")
    print("  -> Future 5-Year ARIMA Forecast:")
    print(arima_forecast_df)

    arima_forecast_df.to_csv(PROCESSED_DATA_DIR / "arima_summer_forecast.csv", index=False, encoding="utf-8-sig")

    summer_ts = train_clean.set_index("year")["summer_avg_temp"]
    viz.plot_summer_forecast_arima(summer_ts, arima_forecast_df, PLOTS_DIR / "15_summer_forecast_arima.png")

    print("\n" + "=" * 70)
    print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print(f"Processed CSV data saved in: {PROCESSED_DATA_DIR}")
    print(f"Plots saved in: {PLOTS_DIR}")
    print("=" * 70)


def main():
    """Main function entry point."""
    run_pipeline()


if __name__ == "__main__":
    main()
