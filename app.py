"""Streamlit Web Dashboard for Seoul Historical Temperature Time-Series Analysis.

Allows interactive exploration of long-term temperature trends, extreme heat days (>=35°C),
seasonal transition expansion/contraction, and 5-year summer temperature forecasting
with modern Plotly interactive charts.
"""

from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats

# Set page configuration
st.set_page_config(
    page_title="Seoul Temperature Analysis Dashboard",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


@st.cache_data
def load_all_data():
    """Load preprocessed datasets from data/processed directory."""
    dataset_processed = pd.read_csv(DATA_PROCESSED_DIR / "dataset_processed.csv")
    dataset_processed["date"] = pd.to_datetime(dataset_processed["date"])

    annual_temp = pd.read_csv(DATA_PROCESSED_DIR / "annual_temperature.csv")
    annual_35 = pd.read_csv(DATA_PROCESSED_DIR / "annual_over_35.csv")
    # Support both monthly_ratio.csv (new) and monthly_temperature_characteristics.csv (legacy)
    if (DATA_PROCESSED_DIR / "monthly_ratio.csv").exists():
        monthly_chars = pd.read_csv(DATA_PROCESSED_DIR / "monthly_ratio.csv")
    elif (DATA_PROCESSED_DIR / "monthly_temperature_characteristics.csv").exists():
        monthly_chars = pd.read_csv(DATA_PROCESSED_DIR / "monthly_temperature_characteristics.csv")
    else:
        # Compute dynamically from dataset_processed if neither exists
        monthly_chars = (
            dataset_processed.groupby(["year", "month"])
            .agg(
                summer_like_ratio=("summer_like", "mean"),
                winter_like_ratio=("winter_like", "mean")
            )
            .reset_index()
            .query("not (year == 2026 and month == 8)")
        )

    # Ensure percentage columns exist
    if "summer_like_percent" not in monthly_chars.columns and "summer_like_ratio" in monthly_chars.columns:
        monthly_chars["summer_like_percent"] = monthly_chars["summer_like_ratio"] * 100.0
    if "winter_like_percent" not in monthly_chars.columns and "winter_like_ratio" in monthly_chars.columns:
        monthly_chars["winter_like_percent"] = monthly_chars["winter_like_ratio"] * 100.0

    trend_results = pd.read_csv(DATA_PROCESSED_DIR / "trend_analysis_results.csv")
    seasonal_results = pd.read_csv(DATA_PROCESSED_DIR / "seasonal_expansion_trend_results.csv")
    arima_forecast = pd.read_csv(DATA_PROCESSED_DIR / "arima_summer_forecast.csv")

    return {
        "dataset_processed": dataset_processed,
        "annual_temp": annual_temp,
        "annual_35": annual_35,
        "monthly_chars": monthly_chars,
        "trend_results": trend_results,
        "seasonal_results": seasonal_results,
        "arima_forecast": arima_forecast
    }


data = load_all_data()
df_daily = data["dataset_processed"]
df_annual = data["annual_temp"]
df_35 = data["annual_35"]
df_monthly = data["monthly_chars"]
df_trend = data["trend_results"]
df_seasonal = data["seasonal_results"]
df_arima = data["arima_forecast"]

# ---------------------------------------------------------
# Sidebar: Controls & Navigation
# ---------------------------------------------------------
st.sidebar.title("🌡️ Seoul Climate Dashboard")
st.sidebar.markdown(
    "**Time-Series Analysis of Seoul Temperatures (1907–2026)**\n\n"
    "<small>Based on Korea Meteorological Administration (KMA) Station #108 (Songwol-dong).</small>",
    unsafe_allow_html=True
)
st.sidebar.link_button("💻 View on GitHub", "https://github.com/freepoincare/time-series-data-analysis")

# Navigation tabs
tab_options = [
    "Overview",
    "Temperature Trends",
    "Extreme Heat (≥35°C)",
    "Seasonal Expansion",
    "5-Year Forecast",
    "Methods & Limitations"
]
selected_tab = st.sidebar.radio("Navigation", tab_options)

st.sidebar.markdown("---")
st.sidebar.subheader("Interactive Filters")

min_data_year = int(df_annual["year"].min())
max_data_year = int(df_annual["year"].max())

year_range = st.sidebar.slider(
    "Select Year Range:",
    min_value=min_data_year,
    max_value=max_data_year,
    value=(min_data_year, max_data_year),
    step=1
)

st.sidebar.info(
    f"📅 **Active Filter Range:** {year_range[0]} – {year_range[1]}\n\n"
    "⚠️ *Note: 1950–1953 (Korean War) has observational gaps and 1907 & 2026 data are partial.*"
)

# Filtered datasets based on selected year range
df_annual_filtered = df_annual[(df_annual["year"] >= year_range[0]) & (df_annual["year"] <= year_range[1])].copy()
df_35_filtered = df_35[(df_35["year"] >= year_range[0]) & (df_35["year"] <= year_range[1])].copy()
df_monthly_filtered = df_monthly[(df_monthly["year"] >= year_range[0]) & (df_monthly["year"] <= year_range[1])].copy()
df_daily_filtered = df_daily[(df_daily["year"] >= year_range[0]) & (df_daily["year"] <= year_range[1])].copy()

# =========================================================
# 1. Overview Tab
# =========================================================
if selected_tab == "Overview":
    st.title("🏙️ Seoul Historical Temperature Analysis (1907–2026)")
    st.markdown(
        """
        This dashboard presents the empirical findings from a 118-year longitudinal time-series analysis 
        of daily temperature observations in Seoul, South Korea (KMA Station #108). 
        The study investigates structural warming trends, asymmetric seasonal warming, 
        extreme heat frequency, transition month expansions, and future 5-year climate forecasts.
        """
    )

    st.markdown("### 📌 Key Findings at a Glance")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="100-Year Annual Warming",
            value="+2.60 °C",
            delta="Linear OLS (p < 0.001)",
            help="Annual average temperature warming rate per 100 years."
        )

    with col2:
        st.metric(
            label="Winter vs. Summer Warming",
            value="1.71x Faster",
            delta="Winter: +2.90°C | Summer: +1.69°C",
            help="Winter temperatures warm at +2.90°C/century vs Summer at +1.69°C/century."
        )

    with col3:
        st.metric(
            label="May Summer-like Shift",
            value="+29.41 %p",
            delta="Per 100 Years (p < 0.001)",
            help="Proportion of summer-like days (Tavg >= 20°C) in May has risen dramatically."
        )

    with col4:
        st.metric(
            label="5-Year Summer Forecast",
            value="25.94 °C",
            delta="ARIMA(0,1,1) (2026–2030)",
            help="Projected 2026-2030 summer average temperature baseline."
        )

    st.markdown("---")
    st.markdown("### ❓ Core Research Questions Addressed")
    st.caption("Click any question card below to reveal its analytical finding.")

    questions = [
        {
            "id": 1,
            "q": "1. Has Seoul's summer temperature increased significantly over the long term?",
            "a": "**Finding:** **Yes.** Summer average temperatures (June–August) have risen by **+1.69°C per 100 years** (Linear OLS $p = 2.49 \\times 10^{-11}$, Mann-Kendall Sen's slope = $+0.0175^\\circ\\text{C}/\\text{yr}$, $p < 0.001$), confirming a statistically significant structural warming trend."
        },
        {
            "id": 2,
            "q": "2. Have extreme heat days (Tmax ≥ 35°C) increased monotonically?",
            "a": "**Finding:** **No monotonic trend ($p = 0.475$).** Days with $T_{\\text{max}} \\ge 35^\\circ\\text{C}$ do not follow a smooth linear trajectory. Instead, they manifest as severe intermittent outliers concentrated in specific atmospheric blocking/heat-dome years (e.g., 1994, 2018, 2025)."
        },
        {
            "id": 3,
            "q": "3. What is the difference between summer and winter warming rates?",
            "a": "**Finding:** **Asymmetric Warming.** Winter temperatures warmed at **+2.90°C / 100 years**, which is **1.71 times faster** than summer warming (+1.69°C / 100 years; Sen's slope ratio is also 1.71x)."
        },
        {
            "id": 4,
            "q": "4. Is summer expanding into transition months (May and September)?",
            "a": "**Finding:** **Yes (Structural Summer Expansion).** Summer-like days ($T_{\\text{avg}} \\ge 20^\\circ\\text{C}$) in May have increased by **+29.41 %p per 100 years** and in September by **+36.58 %p per 100 years**, indicating earlier onset and delayed departure of summer."
        },
        {
            "id": 5,
            "q": "5. Is winter contracting in transition months (March and November)?",
            "a": "**Finding:** **Yes (Winter Contraction).** Winter-like days ($T_{\\text{avg}} \\le 5^\\circ\\text{C}$) in March decreased by **-38.17 %p per 100 years** and in November by **-18.22 %p per 100 years**, shifting the climate regime toward shorter winters and longer warm periods."
        },
        {
            "id": 6,
            "q": "6. What is the 5-year forecast for Seoul's summer average temperature?",
            "a": "**Finding:** **Persistent High Baseline.** The $\\text{ARIMA}(0,1,1)$ model projects a sustained high summer average baseline of **25.94°C** for 2026–2030 (95% CI: $24.22^\\circ\\text{C} \\sim 27.65^\\circ\\text{C}$), outperforming linear regression in backtests (MAE 0.959°C vs 1.370°C)."
        }
    ]

    if "active_question_id" not in st.session_state:
        st.session_state["active_question_id"] = None  # All questions closed by default

    for item in questions:
        q_id = item["id"]
        is_active = (st.session_state["active_question_id"] == q_id)
        btn_label = f"▼ {item['q']}" if is_active else f"▶ {item['q']}"
        
        if st.button(btn_label, key=f"btn_q_{q_id}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state["active_question_id"] = None if is_active else q_id
            st.rerun()

        if is_active:
            st.info(item["a"])

# =========================================================
# 2. Temperature Trends Tab
# =========================================================
elif selected_tab == "Temperature Trends":
    st.title("📈 Long-Term Temperature Trends & Asymmetric Warming")
    st.markdown(
        """
        Analyze long-term temperature trends in Seoul across different temperature metrics 
        (Annual Average, Min, Max, Summer, and Winter) over your selected year range.
        """
    )

    trend_mode = st.selectbox(
        "Select Temperature Metric / View:",
        [
            "Annual Temperatures (Avg, Min, Max)",
            "10-Year Moving Average (Annual Avg)",
            "Linear Regression Trendline (Annual Avg)",
            "Summer vs. Winter Comparison (Asymmetric Warming)"
        ]
    )

    if trend_mode == "Annual Temperatures (Avg, Min, Max)":
        selected_temp_vars = st.multiselect(
            "Select Temperature Variables to Display:",
            ["Annual Average Temp", "Annual Average Min Temp", "Annual Average Max Temp"],
            default=["Annual Average Temp", "Annual Average Min Temp", "Annual Average Max Temp"]
        )

        fig = go.Figure()

        if "Annual Average Temp" in selected_temp_vars:
            fig.add_trace(go.Scatter(
                x=df_annual_filtered["year"],
                y=df_annual_filtered["avg_temp"],
                mode="lines+markers",
                name="Annual Average Temp",
                line=dict(color="#1f2937", width=2.2),
                marker=dict(size=4),
                hovertemplate="<b>Year:</b> %{x}<br><b>Avg Temp:</b> %{y:.2f} °C<extra></extra>"
            ))

        if "Annual Average Min Temp" in selected_temp_vars:
            fig.add_trace(go.Scatter(
                x=df_annual_filtered["year"],
                y=df_annual_filtered["avg_min_temp"],
                mode="lines+markers",
                name="Annual Average Min Temp",
                line=dict(color="#2563eb", width=1.8),
                marker=dict(size=3),
                hovertemplate="<b>Year:</b> %{x}<br><b>Min Temp:</b> %{y:.2f} °C<extra></extra>"
            ))

        if "Annual Average Max Temp" in selected_temp_vars:
            fig.add_trace(go.Scatter(
                x=df_annual_filtered["year"],
                y=df_annual_filtered["avg_max_temp"],
                mode="lines+markers",
                name="Annual Average Max Temp",
                line=dict(color="#dc2626", width=1.8),
                marker=dict(size=3),
                hovertemplate="<b>Year:</b> %{x}<br><b>Max Temp:</b> %{y:.2f} °C<extra></extra>"
            ))

        fig.update_layout(
            title=f"Annual Temperature in Seoul ({year_range[0]}–{year_range[1]})",
            xaxis_title="Year",
            yaxis_title="Temperature (°C)",
            hovermode="x unified",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=0.97, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=60, b=40),
            height=480
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            "> **Observation:** Note that minimum temperatures (blue) have increased faster than maximum temperatures (red), "
            "reflecting night-time heat trapping and urban heat island (UHI) effects."
        )

    elif trend_mode == "10-Year Moving Average (Annual Avg)":
        col_w, col_blank = st.columns([2, 2])
        with col_w:
            window_size = st.slider("Select Moving Average Window (Years):", min_value=3, max_value=20, value=10, step=1)
        
        ma = df_annual_filtered["avg_temp"].rolling(window=window_size).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_annual_filtered["year"],
            y=df_annual_filtered["avg_temp"],
            mode="lines+markers",
            name="Annual Average Temp",
            line=dict(color="#9ca3af", width=1.2),
            marker=dict(size=4, color="#9ca3af"),
            hovertemplate="<b>Year:</b> %{x}<br><b>Observed Avg:</b> %{y:.2f} °C<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=df_annual_filtered["year"],
            y=ma,
            mode="lines",
            name=f"{window_size}-Year Moving Average",
            line=dict(color="#ea580c", width=3),
            hovertemplate=f"<b>Year:</b> %{{x}}<br><b>{window_size}y Moving Avg:</b> %{{y:.2f}} °C<extra></extra>"
        ))

        fig.update_layout(
            title=f"Long-Term Temperature Trend in Seoul ({window_size}-Year Moving Average)",
            xaxis_title="Year",
            yaxis_title="Temperature (°C)",
            hovermode="x unified",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=0.97, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=60, b=40),
            height=480
        )
        st.plotly_chart(fig, use_container_width=True)

    elif trend_mode == "Linear Regression Trendline (Annual Avg)":
        valid_annual = df_annual_filtered.dropna(subset=["avg_temp"])
        x = valid_annual["year"]
        y = valid_annual["avg_temp"]

        if len(valid_annual) >= 2:
            slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
            trend_line = intercept + slope * x
        else:
            slope, intercept, r_val, p_val, std_err = np.nan, np.nan, np.nan, np.nan, np.nan
            trend_line = pd.Series(dtype=float)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode="markers",
            name="Annual Average Temp",
            marker=dict(color="#1f2937", size=6, opacity=0.7),
            hovertemplate="<b>Year:</b> %{x}<br><b>Observed:</b> %{y:.2f} °C<extra></extra>"
        ))
        if len(valid_annual) >= 2:
            fig.add_trace(go.Scatter(
                x=x,
                y=trend_line,
                mode="lines",
                name=f"Linear Trend (Slope: {slope:.4f} °C/yr, p={p_val:.3e})",
                line=dict(color="#dc2626", width=2.5),
                hovertemplate="<b>Year:</b> %{x}<br><b>Trendline:</b> %{y:.2f} °C<extra></extra>"
            ))

        fig.update_layout(
            title=f"Linear Trend of Annual Average Temperature ({year_range[0]}–{year_range[1]})",
            xaxis_title="Year",
            yaxis_title="Temperature (°C)",
            hovermode="x unified",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=0.97, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=60, b=40),
            height=480
        )
        st.plotly_chart(fig, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Fitted Slope", f"{slope:.4f} °C / yr", f"{slope*100:.2f} °C / 100 yr")
        c2.metric("R² Score", f"{r_val**2:.3f}")
        c3.metric("p-value", f"{p_val:.2e}", "Statistically Significant" if p_val < 0.05 else "Not Significant")

    elif trend_mode == "Summer vs. Winter Comparison (Asymmetric Warming)":
        summer_winter = (
            df_daily_filtered[df_daily_filtered["season"].isin(["Summer", "Winter"])]
            .groupby(["year", "season"])["tavg"]
            .mean()
            .reset_index()
            .pivot(index="year", columns="season", values="tavg")
            .reset_index()
        )

        fig = go.Figure()
        if "Summer" in summer_winter.columns:
            fig.add_trace(go.Scatter(
                x=summer_winter["year"],
                y=summer_winter["Summer"],
                mode="lines+markers",
                name="Summer (Jun–Aug)",
                line=dict(color="#b91c1c", width=2),
                marker=dict(size=4),
                hovertemplate="<b>Year:</b> %{x}<br><b>Summer Avg:</b> %{y:.2f} °C<extra></extra>"
            ))
        if "Winter" in summer_winter.columns:
            fig.add_trace(go.Scatter(
                x=summer_winter["year"],
                y=summer_winter["Winter"],
                mode="lines+markers",
                name="Winter (Dec–Feb)",
                line=dict(color="#1d4ed8", width=2),
                marker=dict(size=4),
                hovertemplate="<b>Year:</b> %{x}<br><b>Winter Avg:</b> %{y:.2f} °C<extra></extra>"
            ))

        fig.update_layout(
            title=f"Summer vs. Winter Average Temperature ({year_range[0]}–{year_range[1]})",
            xaxis_title="Year",
            yaxis_title="Average Temperature (°C)",
            hovermode="x unified",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=0.97, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=60, b=40),
            height=480
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📊 Benchmark Trend Test Summary (Full 118-Year Record)")
    st.dataframe(
        df_trend.rename(columns={
            "dataset": "Time Series",
            "linear_slope_per_year": "Linear Slope (°C/yr)",
            "linear_p_value": "Linear p-value",
            "linear_r_value": "Linear R",
            "mann_kendall_trend": "Mann-Kendall Trend",
            "mann_kendall_p_value": "MK p-value",
            "sen_slope": "Sen's Slope (°C/yr)"
        }),
        use_container_width=True
    )

# =========================================================
# 3. Extreme Heat (≥35°C) Tab
# =========================================================
elif selected_tab == "Extreme Heat (≥35°C)":
    st.title("🔥 Extreme Heat Days Analysis ($T_{\\text{max}} \\ge 35^\\circ\\text{C}$)")
    st.markdown(
        """
        Explores the frequency and occurrence pattern of extreme heat days defined as daily maximum temperature 
        $T_{\\text{max}} \\ge 35^\\circ\\text{C}$.
        """
    )

    valid_35 = df_35_filtered.dropna(subset=["days_over_35"])
    x_35 = valid_35["year"]
    y_35 = valid_35["days_over_35"]

    if len(valid_35) >= 2:
        slope_35, intercept_35, r_35, p_35, _ = stats.linregress(x_35, y_35)
        trend_35 = intercept_35 + slope_35 * x_35
    else:
        slope_35, intercept_35, r_35, p_35 = np.nan, np.nan, np.nan, np.nan
        trend_35 = pd.Series(dtype=float)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x_35,
        y=y_35,
        name="Observed Days ≥ 35°C",
        marker=dict(
            color=y_35,
            colorscale="Reds",
            line=dict(color="#991b1b", width=1)
        ),
        hovertemplate="<b>Year:</b> %{x}<br><b>Heatwave Days (≥35°C):</b> %{y} days<extra></extra>"
    ))
    if len(valid_35) >= 2:
        fig.add_trace(go.Scatter(
            x=x_35,
            y=trend_35,
            mode="lines",
            name=f"Linear Trend (Slope: {slope_35:.4f} d/yr, p={p_35:.3f})",
            line=dict(color="#7f1d1d", width=2.5),
            hovertemplate="<b>Year:</b> %{x}<br><b>Fitted Trend:</b> %{y:.2f} days<extra></extra>"
        ))

    fig.update_layout(
        title=f"Annual Number of Days with Tmax ≥ 35°C ({year_range[0]}–{year_range[1]})",
        xaxis_title="Year",
        yaxis_title="Number of Days",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=0.97, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40),
        height=480
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    max_days_val = int(y_35.max()) if len(y_35) > 0 else 0
    max_days_year = int(x_35.loc[y_35.idxmax()]) if len(y_35) > 0 and max_days_val > 0 else "N/A"

    col1.metric("Highest Recorded Heatwave Days", f"{max_days_val} Days", f"Year {max_days_year}")
    col2.metric("Mann-Kendall Trend Result", "No Trend", "p = 0.475 (Full record)")
    col3.metric("Selected Period OLS p-value", f"{p_35:.4f}", "Not Significant (p > 0.05)" if p_35 >= 0.05 else "Significant")

    st.markdown("---")
    st.markdown("### 💡 Interpretation & Key Insight")
    st.markdown(
        r"""
        - **Intermittent Extreme Outliers:** Unlike average temperatures which exhibit smooth, steady long-term warming, 
          extreme heat days ($\ge 35^\circ\text{C}$) do **not** follow a continuous monotonic increase ($p = 0.475$).
        - **Atmospheric Heat Dome Clustering:** Extreme heat occurs in explosive, sporadic clusters during specific years characterized 
          by dual high-pressure blocking systems (Tibetan High + North Pacific High).
        - **Amplified Risk:** Even though the occurrence is intermittent, because baseline background temperatures have risen significantly, 
          future heat-dome events have the potential to produce record-breaking compound heatwave intensities.
        """
    )

# =========================================================
# 4. Seasonal Expansion Tab
# =========================================================
elif selected_tab == "Seasonal Expansion":
    st.title("🍂 Seasonal Boundary Expansion & Contraction")
    st.markdown(
        """
        Evaluates whether seasons are structurally expanding or contracting using criteria:
        - **Summer-like Day:** Daily average temperature $T_{\\text{avg}} \\ge 20^\\circ\\text{C}$
        - **Winter-like Day:** Daily average temperature $T_{\\text{avg}} \\le 5^\\circ\\text{C}$
        """
    )

    season_view = st.radio(
        "Select Exploration View:",
        ["Transition Month Trends (May, Sep, Nov, Mar)", "Monthly Ratio Heatmaps", "Early vs. Recent Era Comparison"],
        horizontal=True
    )

    if season_view == "Transition Month Trends (May, Sep, Nov, Mar)":
        month_choice = st.selectbox(
            "Select Transition Month to Inspect:",
            [
                "May (Early Summer Expansion - Tavg ≥ 20°C)",
                "September (Late Summer Expansion - Tavg ≥ 20°C)",
                "March (Early Spring Warming / Winter Contraction - Tavg ≤ 5°C)",
                "November (Late Autumn / Winter Contraction - Tavg ≤ 5°C)"
            ]
        )

        month_map = {
            "May (Early Summer Expansion - Tavg ≥ 20°C)": (5, "summer_like_percent", "Summer-like Days (%) in May", "#b91c1c"),
            "September (Late Summer Expansion - Tavg ≥ 20°C)": (9, "summer_like_percent", "Summer-like Days (%) in September", "#ea580c"),
            "March (Early Spring Warming / Winter Contraction - Tavg ≤ 5°C)": (3, "winter_like_percent", "Winter-like Days (%) in March", "#2563eb"),
            "November (Late Autumn / Winter Contraction - Tavg ≤ 5°C)": (11, "winter_like_percent", "Winter-like Days (%) in November", "#1e3a8a")
        }

        m_num, m_col, m_title, m_color = month_map[month_choice]
        m_df = df_monthly_filtered[df_monthly_filtered["month"] == m_num].dropna(subset=[m_col]).copy()

        x_m = m_df["year"]
        y_m = m_df[m_col]
        slope_m, intercept_m, r_m, p_m, _ = stats.linregress(x_m, y_m)
        trend_m = intercept_m + slope_m * x_m

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_m,
            y=y_m,
            mode="markers",
            name="Observed Monthly Ratio (%)",
            marker=dict(color=m_color, size=6, opacity=0.7),
            hovertemplate="<b>Year:</b> %{x}<br><b>Ratio:</b> %{y:.1f}%<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=x_m,
            y=trend_m,
            mode="lines",
            name=f"Trend (Slope: {slope_m:.3f} %p/yr, p={p_m:.2e})",
            line=dict(color="#111827", width=2.5),
            hovertemplate="<b>Year:</b> %{x}<br><b>Fitted Trend:</b> %{y:.1f}%<extra></extra>"
        ))

        fig.update_layout(
            title=f"{m_title} ({year_range[0]}–{year_range[1]})",
            xaxis_title="Year",
            yaxis_title="Days Ratio (%)",
            hovermode="x unified",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=60, b=40),
            height=480
        )
        st.plotly_chart(fig, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Change Rate per 100 Years", f"{slope_m * 100:+.2f} %p")
        c2.metric("R² Score", f"{r_m**2:.3f}")
        c3.metric("p-value", f"{p_m:.2e}", "Significant (p < 0.001)")

    elif season_view == "Monthly Ratio Heatmaps":
        h_col1, h_col2 = st.columns(2)

        with h_col1:
            st.subheader("☀️ Summer-like Days (May–Sep)")
            summer_trans = df_monthly_filtered[df_monthly_filtered["month"].isin([5, 6, 7, 8, 9])]
            pivot_s = summer_trans.pivot(index="year", columns="month", values="summer_like_percent")
            month_names_s = {5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep"}
            x_labels_s = [month_names_s.get(c, str(c)) for c in pivot_s.columns]

            fig_s = go.Figure(data=go.Heatmap(
                z=pivot_s.values,
                x=x_labels_s,
                y=pivot_s.index,
                colorscale="YlOrRd",
                colorbar=dict(title="%"),
                hovertemplate="<b>Year:</b> %{y}<br><b>Month:</b> %{x}<br><b>Summer-like Days:</b> %{z:.1f}%<extra></extra>"
            ))
            # Chronological top-to-bottom order on Y-axis
            fig_s.update_layout(
                title="Summer-like Ratio (%) (Tavg ≥ 20°C)",
                xaxis_title="Month",
                yaxis_title="Year",
                yaxis=dict(autorange="reversed"),
                template="plotly_white",
                margin=dict(l=40, r=40, t=50, b=40),
                height=560
            )
            st.plotly_chart(fig_s, use_container_width=True)

        with h_col2:
            st.subheader("❄️ Winter-like Days (Nov–Mar)")
            winter_trans = df_monthly_filtered[df_monthly_filtered["month"].isin([11, 12, 1, 2, 3])]
            pivot_w = winter_trans.pivot(index="year", columns="month", values="winter_like_percent")
            winter_col_order = [m for m in [11, 12, 1, 2, 3] if m in pivot_w.columns]
            pivot_w = pivot_w.reindex(columns=winter_col_order)
            month_names_w = {11: "Nov", 12: "Dec", 1: "Jan", 2: "Feb", 3: "Mar"}
            x_labels_w = [month_names_w.get(c, str(c)) for c in pivot_w.columns]

            fig_w = go.Figure(data=go.Heatmap(
                z=pivot_w.values,
                x=x_labels_w,
                y=pivot_w.index,
                colorscale="YlGnBu",
                colorbar=dict(title="%"),
                hovertemplate="<b>Year:</b> %{y}<br><b>Month:</b> %{x}<br><b>Winter-like Days:</b> %{z:.1f}%<extra></extra>"
            ))
            # Chronological top-to-bottom order on Y-axis
            fig_w.update_layout(
                title="Winter-like Ratio (%) (Tavg ≤ 5°C)",
                xaxis_title="Month",
                yaxis_title="Year",
                yaxis=dict(autorange="reversed"),
                template="plotly_white",
                margin=dict(l=40, r=40, t=50, b=40),
                height=560
            )
            st.plotly_chart(fig_w, use_container_width=True)

    elif season_view == "Early vs. Recent Era Comparison":
        st.subheader("🗓️ 28-Year Era Shift: 1908–1935 vs. 1998–2025")

        early_mc = df_monthly[df_monthly["year"].between(1908, 1935)]
        recent_mc = df_monthly[df_monthly["year"].between(1998, 2025)]

        early_summer = early_mc.groupby("month")["summer_like_percent"].mean()
        recent_summer = recent_mc.groupby("month")["summer_like_percent"].mean()
        early_winter = early_mc.groupby("month")["winter_like_percent"].mean()
        recent_winter = recent_mc.groupby("month")["winter_like_percent"].mean()

        months = list(range(1, 13))
        month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        col_c1, col_c2 = st.columns(2)

        with col_c1:
            fig_es = go.Figure()
            fig_es.add_trace(go.Scatter(
                x=month_labels,
                y=[early_summer.get(m, 0) for m in months],
                mode="lines+markers",
                name="1908–1935 (Early Era)",
                line=dict(color="#475569", width=2.2),
                marker=dict(size=6),
                hovertemplate="<b>Month:</b> %{x}<br><b>Early Era Summer-like:</b> %{y:.1f}%<extra></extra>"
            ))
            fig_es.add_trace(go.Scatter(
                x=month_labels,
                y=[recent_summer.get(m, 0) for m in months],
                mode="lines+markers",
                name="1998–2025 (Recent Era)",
                line=dict(color="#dc2626", width=2.5),
                marker=dict(size=7),
                hovertemplate="<b>Month:</b> %{x}<br><b>Recent Era Summer-like:</b> %{y:.1f}%<extra></extra>"
            ))
            fig_es.update_layout(
                title="Summer-like Days (%): Early vs. Recent",
                xaxis_title="Month",
                yaxis_title="Summer-like Days (%)",
                hovermode="x unified",
                template="plotly_white",
                legend=dict(orientation="v", yanchor="bottom", y=0.95, xanchor="right", x=1),
                margin=dict(l=40, r=40, t=50, b=40),
                height=450
            )
            st.plotly_chart(fig_es, use_container_width=True)

        with col_c2:
            fig_ew = go.Figure()
            fig_ew.add_trace(go.Scatter(
                x=month_labels,
                y=[early_winter.get(m, 0) for m in months],
                mode="lines+markers",
                name="1908–1935 (Early Era)",
                line=dict(color="#475569", width=2.2),
                marker=dict(size=6),
                hovertemplate="<b>Month:</b> %{x}<br><b>Early Era Winter-like:</b> %{y:.1f}%<extra></extra>"
            ))
            fig_ew.add_trace(go.Scatter(
                x=month_labels,
                y=[recent_winter.get(m, 0) for m in months],
                mode="lines+markers",
                name="1998–2025 (Recent Era)",
                line=dict(color="#2563eb", width=2.5),
                marker=dict(size=7),
                hovertemplate="<b>Month:</b> %{x}<br><b>Recent Era Winter-like:</b> %{y:.1f}%<extra></extra>"
            ))
            fig_ew.update_layout(
                title="Winter-like Days (%): Early vs. Recent",
                xaxis_title="Month",
                yaxis_title="Winter-like Days (%)",
                hovermode="x unified",
                template="plotly_white",
                legend=dict(orientation="v", yanchor="bottom", y=0.95, xanchor="right", x=1),
                margin=dict(l=40, r=40, t=50, b=40),
                height=450
            )
            st.plotly_chart(fig_ew, use_container_width=True)

    st.markdown("### 📊 Transition Month Trend Statistics (1907-2026)")
    st.dataframe(
        df_seasonal.rename(columns={
            "season": "Season Type",
            "month": "Month",
            "slope": "Annual Slope (%p/yr)",
            "change_per_100_years": "Change per 100 Years (%p)",
            "linear_p_value": "Linear p-value",
            "r_squared": "R²",
            "mk_trend": "Mann-Kendall Trend",
            "mk_p_value": "MK p-value",
            "sen_slope": "Sen's Slope (%p/yr)"
        }),
        use_container_width=True
    )

# =========================================================
# 5. 5-Year Forecast Tab
# =========================================================
elif selected_tab == "5-Year Forecast":
    st.title("🔮 5-Year Summer Average Temperature Forecast (2026–2030)")
    st.markdown(
        """
        Presents time-series forecasting models for Seoul summer average temperature (June–August),
        comparing **Linear Regression Trend Extrapolation** and **ARIMA(0,1,1)** with interactive 95% confidence bands and hover tooltips.
        """
    )

    summer_hist = (
        df_daily[(df_daily["season"] == "Summer") & (df_daily["year"] < 2026)]
        .groupby("year")["tavg"]
        .mean()
        .reset_index(name="summer_avg_temp")
        .dropna(subset=["summer_avg_temp"])
    )

    forecast_model_choice = st.radio(
        "Select Forecasting Model:",
        ["ARIMA(0,1,1) (Recommended)", "Linear Regression", "Comparison View"],
        horizontal=True
    )

    if forecast_model_choice == "ARIMA(0,1,1) (Recommended)":
        recent_summer = summer_hist.iloc[-50:]

        fig = go.Figure()
        # Historical observations
        fig.add_trace(go.Scatter(
            x=recent_summer["year"],
            y=recent_summer["summer_avg_temp"],
            mode="lines+markers",
            name="Historical Summer Temp (Last 50 Years)",
            line=dict(color="#1f2937", width=2),
            marker=dict(size=4),
            hovertemplate="<b>Year:</b> %{x}<br><b>Observed Summer Avg:</b> %{y:.2f} °C<extra></extra>"
        ))

        # ARIMA Confidence Interval (Upper bound)
        fig.add_trace(go.Scatter(
            x=df_arima["year"],
            y=df_arima["upper_95"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        ))
        # ARIMA Confidence Interval (Lower bound with filled shaded area)
        fig.add_trace(go.Scatter(
            x=df_arima["year"],
            y=df_arima["lower_95"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(239, 68, 68, 0.2)",
            name="95% Confidence Interval",
            hovertemplate="<b>Year:</b> %{x}<br><b>95% CI Lower:</b> %{y:.2f} °C<extra></extra>"
        ))

        # ARIMA Point Forecast
        fig.add_trace(go.Scatter(
            x=df_arima["year"],
            y=df_arima["forecast_temp"],
            mode="lines+markers",
            name="ARIMA(0,1,1) Forecast",
            line=dict(color="#dc2626", width=3),
            marker=dict(size=8, symbol="circle"),
            hovertemplate="<b>Year:</b> %{x}<br><b>ARIMA Forecast:</b> %{y:.2f} °C<br><b>95% CI:</b> [%{customdata[0]:.2f} ~ %{customdata[1]:.2f}] °C<extra></extra>",
            customdata=np.stack((df_arima["lower_95"], df_arima["upper_95"]), axis=-1)
        ))

        fig.update_layout(
            title="5-Year Forecast of Seoul Summer Average Temperature (ARIMA 0,1,1)",
            xaxis_title="Year",
            yaxis_title="Summer Average Temperature (°C)",
            hovermode="x unified",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=0.95, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=60, b=40),
            height=480
        )
        st.plotly_chart(fig, use_container_width=True)

    elif forecast_model_choice == "Linear Regression":
        slope_s, intercept_s, _, p_s, _ = stats.linregress(summer_hist["year"], summer_hist["summer_avg_temp"])
        fut_years = np.arange(2026, 2031)
        fut_preds = intercept_s + slope_s * fut_years
        hist_trend = intercept_s + slope_s * summer_hist["year"]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=summer_hist["year"],
            y=summer_hist["summer_avg_temp"],
            mode="markers",
            name="Historical Summer Temp",
            marker=dict(color="#1f2937", size=5, opacity=0.7),
            hovertemplate="<b>Year:</b> %{x}<br><b>Observed Summer Avg:</b> %{y:.2f} °C<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=summer_hist["year"],
            y=hist_trend,
            mode="lines",
            name=f"Historical Trend (Slope: {slope_s:.4f} °C/yr)",
            line=dict(color="#2563eb", width=2),
            hovertemplate="<b>Year:</b> %{x}<br><b>Trendline:</b> %{y:.2f} °C<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=fut_years,
            y=fut_preds,
            mode="lines+markers",
            name="Linear Regression Forecast (2026–2030)",
            line=dict(color="#dc2626", width=2.8, dash="dash"),
            marker=dict(size=8, symbol="diamond"),
            hovertemplate="<b>Year:</b> %{x}<br><b>LR Forecast:</b> %{y:.2f} °C<extra></extra>"
        ))

        fig.update_layout(
            title="5-Year Forecast of Seoul Summer Average Temperature (Linear Regression)",
            xaxis_title="Year",
            yaxis_title="Summer Average Temperature (°C)",
            hovermode="x unified",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=0.95, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=60, b=40),
            height=480
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        # Comparison View
        slope_s, intercept_s, _, _, _ = stats.linregress(summer_hist["year"], summer_hist["summer_avg_temp"])
        fut_years = np.arange(2026, 2031)
        fut_preds_lr = intercept_s + slope_s * fut_years
        recent_s = summer_hist.iloc[-40:]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=recent_s["year"],
            y=recent_s["summer_avg_temp"],
            mode="lines+markers",
            name="Historical Summer Temp",
            line=dict(color="#4b5563", width=1.5),
            marker=dict(size=4),
            hovertemplate="<b>Year:</b> %{x}<br><b>Observed:</b> %{y:.2f} °C<extra></extra>"
        ))

        # ARIMA Confidence Interval (Upper bound)
        fig.add_trace(go.Scatter(
            x=df_arima["year"],
            y=df_arima["upper_95"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        ))
        # ARIMA Confidence Interval (Lower bound with filled shaded area)
        fig.add_trace(go.Scatter(
            x=df_arima["year"],
            y=df_arima["lower_95"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(239, 68, 68, 0.2)",
            name="ARIMA 95% Confidence Interval",
            hovertemplate="<b>Year:</b> %{x}<br><b>ARIMA CI Lower:</b> %{y:.2f} °C<extra></extra>"
        ))

        fig.add_trace(go.Scatter(
            x=df_arima["year"],
            y=df_arima["forecast_temp"],
            mode="lines+markers",
            name="ARIMA(0,1,1) Forecast",
            line=dict(color="#dc2626", width=2.8),
            marker=dict(size=8, symbol="circle"),
            hovertemplate="<b>Year:</b> %{x}<br><b>ARIMA Forecast:</b> %{y:.2f} °C<br><b>95% CI:</b> [%{customdata[0]:.2f} ~ %{customdata[1]:.2f}] °C<extra></extra>",
            customdata=np.stack((df_arima["lower_95"], df_arima["upper_95"]), axis=-1)
        ))

        fig.add_trace(go.Scatter(
            x=fut_years,
            y=fut_preds_lr,
            mode="lines+markers",
            name="Linear Regression Forecast",
            line=dict(color="#2563eb", width=2.5, dash="dash"),
            marker=dict(size=8, symbol="diamond"),
            hovertemplate="<b>Year:</b> %{x}<br><b>Linear Forecast:</b> %{y:.2f} °C<extra></extra>"
        ))

        fig.update_layout(
            title="Model Forecast Comparison: ARIMA(0,1,1) vs. Linear Regression (2026–2030)",
            xaxis_title="Year",
            yaxis_title="Summer Average Temperature (°C)",
            hovermode="x unified",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=0.95, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=60, b=40),
            height=480
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 5-Year Forecast Table & Confidence Intervals")
    display_forecast = df_arima.copy()
    display_forecast.columns = ["Year", "ARIMA Point Forecast (°C)", "95% CI Lower Bound (°C)", "95% CI Upper Bound (°C)"]
    st.dataframe(display_forecast.style.format("{:.2f}", subset=["ARIMA Point Forecast (°C)", "95% CI Lower Bound (°C)", "95% CI Upper Bound (°C)"]), use_container_width=True)

    st.markdown("### 🔍 Model Validation & Evaluation (Recent 5-Year Backtest)")
    val_col1, val_col2 = st.columns(2)
    with val_col1:
        st.markdown(
            r"""
            **ARIMA(0,1,1) Model:**
            - **MAE:** `0.959 °C` (Superior precision)
            - **RMSE:** `1.164 °C`
            - **Stationarity:** 1st differenced series satisfies ADF test ($p = 4.11 \times 10^{-21}$).
            """
        )
    with val_col2:
        st.markdown(
            r"""
            **Linear Regression Model:**
            - **MAE:** `1.370 °C`
            - **RMSE:** `1.513 °C`
            - **Trend Slope:** $+0.0169^\circ\text{C}/\text{yr}$ ($+1.69^\circ\text{C}/100\text{yr}$)
            """
        )

# =========================================================
# 6. Methods & Limitations Tab
# =========================================================
elif selected_tab == "Methods & Limitations":
    st.title("⚙️ Analysis Methods & Project Limitations")

    st.markdown("### 🧪 Statistical & Time-Series Methods")
    st.markdown(
        r"""
        1. **Descriptive & Aggregation Analysis:**
           - Calculated annual and seasonal aggregates (mean, min, max) using `pandas`.
           - Applied IQR (Interquartile Range) method ($1.5 \times \text{IQR}$) for anomaly/outlier verification.
        
        2. **Moving Averages (Smoothing):**
           - Utilized 10-year rolling window moving averages to filter high-frequency interannual noise (El Niño/La Niña cycles) and reveal underlying climate trajectories.
        
        3. **Ordinary Least Squares (OLS) Linear Regression:**
           - Estimated decadal and centennial temperature rate of change ($^\circ\text{C}/\text{year}$, $^\circ\text{C}/100\text{years}$), $R^2$ goodness of fit, and parametric $p$-values.
        
        4. **Mann-Kendall Trend Test & Sen's Slope:**
           - Conducted non-parametric Mann-Kendall rank tests (`pymannkendall`) to establish monotonic trend significance robust against non-normality and outliers.
           - Computed median-based Sen's slope estimators.
        
        5. **Transition Month Seasonal Boundary Analysis:**
           - Modeled monthly occurrence percentages for summer-like ($T_{\text{avg}} \ge 20^\circ\text{C}$) and winter-like ($T_{\text{avg}} \le 5^\circ\text{C}$) days in shoulder months (May, Sep, Nov, Mar).
        
        6. **Time-Series Forecasting (ARIMA & Linear Regression):**
           - Verified stationary properties via Augmented Dickey-Fuller (ADF) test.
           - Fitted $\text{ARIMA}(0,1,1)$ capturing short-term autocorrelation with 95% forecasting intervals, cross-validated against Linear Regression via 5-year rolling backtests (MAE/RMSE).
        """
    )

    st.markdown("---")
    st.markdown("### ⚠️ Research Limitations")
    st.markdown(
        """
        1. **Korean War Observational Gap (1950–1953):**
           - Approximately 3 years and 3 months of observation records are missing due to the Korean War. 
           - To preserve statistical integrity, artificial interpolation was strictly avoided. Missing years are excluded from continuous sequential modeling.
        
        2. **Incomplete 2026 Observation Year:**
           - Observations for 2026 are recorded up to August 19, 2026. 
           - Incomplete 2026 data is excluded from full-year annual aggregations and summer forecasts to avoid negative bias.
        
        3. **Confounding between Global Warming and Urban Heat Island (UHI):**
           - Analysis relies on the single Songwol-dong station (ASOS #108). 
           - The relative quantitative contributions of planetary greenhouse warming vs. high-density urban microclimate heating (artificial building heat, lack of ventilation, asphalt thermal retention) cannot be strictly separated from a single station.
        
        4. **Single-Station Spatial Representation:**
           - Intra-city microclimates in Seoul can vary by 3–5°C depending on topography, elevation, and proximity to the Han River. Single-point ASOS data represents the historical benchmark station rather than uniform conditions across all 25 autonomous districts.
        
        5. **Exogenous Macro-Climate Forcings in Forecasting:**
           - ARIMA and Linear Regression are univariate statistical models based on historical temporal patterns and do not dynamically simulate atmospheric physics, greenhouse gas concentration scenarios (SSPs), volcanic eruptions, or solar cycles.
        """
    )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.85em;'>"
    "Seoul Time Series Temperature Analysis Dashboard | Source: KMA ASOS #108 | Built with Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True
)
