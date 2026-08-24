# AI Data Analysis: Data-Driven Trend Analysis [![starline](https://raw.githubusercontent.com/qoomon/qoomon/refs/heads/main/starlines/qoomon/5dfcdf8eec66a051ecd85625518cfd13@gist/starline.svg)](https://github.com/qoomon/starline)

## 📌 목차

---

## 📖 프로젝트 개요

<!-- Describe the selected time-series dataset and the purpose of the analysis. -->

---

## 📁 디렉터리 구조

```text
ai-time-series-analysis/
├── data/
│   ├── raw/
│   └── processed/
├── images/
├── notebooks/
├── src/
├── tests/
├── docs/
├── analysis.py
├── app.py
├── REPORT.md
├── README.md
└── requirements.txt
```

---

## 데이터 분석 수행 구조/순서

---

## 개발 환경

---

## 실행 방법

### Requirements

```bash
pip install -r requirements.txt
```

### Run

```bash
python analysis.py
```

---

## Dashboard

### Overview
This project includes an interactive web dashboard built with **Streamlit** to facilitate dynamic exploration of Seoul's 119-year historical temperature observations (1907–2026, KMA Station #108).

Streamlit 대시보드를 통해 서울의 장기 기온 변화, 35°C 이상 고온일수, 계절 변화 및 5년 기온 예측 결과를 기간과 조건을 변경하며 탐색할 수 있다.

**Dashboard:** [Streamlit Dashboard](YOUR_URL)

### Features
1. **Interactive Filters:**
   - **Year Range Slider:** Filter historical data dynamically between 1907 and 2026.
   - **Metric Selectors:** Switch between Annual (Avg/Min/Max), 10-year moving averages, linear trends, and Summer vs. Winter comparisons.
   - **Seasonal Controls:** Switch between transition months (May, September, March, November), heatmaps, and 30-year era comparisons (1907–1936 vs. 1997–2026).
   - **Forecast Model Selector:** Compare ARIMA(0,1,1) (with 95% confidence intervals) and Linear Regression forecasts for 2026–2030.
2. **Key Modules:**
   - **Overview:** Executive summary metrics, 100-year warming rate (+2.95°C/century), asymmetric seasonal warming, and key research questions.
   - **Temperature Trends:** Multi-metric historical lines, moving average smoothing, and OLS regressions.
   - **Extreme Heat (≥35°C):** Heatwave days bar charts and non-parametric Mann-Kendall trend interpretation.
   - **Seasonal Expansion:** Analysis of summer expansion in May/September and winter contraction in March/November.
   - **5-Year Forecast:** 2026–2030 summer average temperature forecasts with ARIMA(0,1,1) uncertainty bands and backtest metrics.
   - **Methods & Limitations:** Statistical methodology descriptions and caveats (Korean War gap, 2026 partial data, single-station microclimate).

### Local Execution

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

3. A browser opens automatically at `http://localhost:8501`.

### Streamlit Community Cloud Deployment

1. Push this repository to GitHub:
   ```bash
   git add app.py requirements.txt README.md
   git commit -m "feat: add Streamlit web dashboard for temperature analysis"
   git push (origin main)
   ```
2. Navigate to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **"New app"**, select your GitHub repository, branch (`main`), and set Main file path to `app.py`.
4. Click **"Deploy"**.
5. Your public deployment URL will be generated in the format:
   `https://<your-username>-<repo-name>-app-<hash>.streamlit.app`
