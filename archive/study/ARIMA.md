# ARIMA

**ARIMA** stands for AutoRegressive Integrated Moving Average. It is one of the most widely used statistical models for analyzing and forecasting time series data.

At its core, ARIMA assumes that a series' past values and past prediction errors contain information that can predict its future trajectory.

ARIMA의 구조:

* AR (Autoregressive): 과거의 내 데이터로 미래를 예측 (추세 반영)
* I (Integrated): 차분(Differencing)을 통해 데이터의 추세를 제거하고 안정적으로 만듦
* MA (Moving Average): 과거 오차(Residual/Noise)의 이동평균을 사용하여 미래를 예측

수동 이동평균이 필요 없는 이유:

* ARIMA 모델의 'MA' 성분이 알아서 노이즈의 흐름을 파악해 줍니다.
* 만약 사용자가 이미 이동평균 필터를 필터링한 데이터를 ARIMA에 넣으면, 데이터의 변동성이 인위적으로 왜곡되어 ARIMA 모델이 시계열의 진짜 수학적 특성을 파악하지 못하고 예측력이 오히려 떨어집니다.

---

## The Three Components: $p, d, q$

An ARIMA model is denoted as **$\text{ARIMA}(p, d, q)$**, where each letter represents a specific mechanism:

### 1. **AR ($p$) — AutoRegression**

* **What it means:** The model uses the relationship between an observation and a number of lagged (past) observations.
* **Analogy:** Today's temperature is likely close to yesterday's temperature.
* **Parameter $p$:** The number of lag terms included in the model.

### 2. **I ($d$) — Integrated**

* **What it means:** Differencing the raw observations (subtracting an observation from the previous one) to make the time series **stationary** (meaning its statistical properties like mean and variance don't change over time).
* **Parameter $d$:** The number of times the data needs to be differenced to reach stationarity.

### 3. **MA ($q$) — Moving Average**

* **What it means:** The model uses the dependency between an observation and residual errors from a moving average model applied to lagged observations.
* **Analogy:** If an unexpected shock (like a sudden news event) hits yesterday, its effect gradually fades over the next few days.
* **Parameter $q$:** The size/order of the moving average window.

$$\hat{y}_t = \mu + \sum_{i=1}^p \phi_i y_{t-i} + \sum_{j=1}^q \theta_j \epsilon_{t-j} + \epsilon_t$$

---

## How to Proceed: Step-by-Step Workflow

Applying ARIMA follows the classic **Box-Jenkins methodology**, consisting of 4 primary steps:

1. **1. Stationarity Check & Preparation:** Identify d.
ARIMA requires stationary data to make reliable predictions.

* **Plot the data:** Look for visible trends, seasonality, or changing variance.
* **Statistical test:** Run the **Augmented Dickey-Fuller (ADF) test**. If $p \text{-value} > 0.05$, the data is non-stationary.
* **Difference the data:** Apply log transformations (for variance) or order-$1$ differencing ($d=1$) until the ADF test passes ($p \le 0.05$).


2. **2. Model Identification:** Find p and q.
Once stationary, determine the parameters $p$ and $q$ using diagnostic plots on the differenced series:

* **ACF (Autocorrelation Function) Plot:** Helps identify the Moving Average order $q$. (Look for the lag where autocorrelation drops off sharply).
* **PACF (Partial Autocorrelation Function) Plot:** Helps identify the AutoRegressive order $p$. (Look for the lag where partial autocorrelation cuts off).


3. **3. Model Estimation & Evaluation:** Select & Diagnose.
Fit candidate models (e.g., ARIMA(1,1,1), ARIMA(2,1,1)) using maximum likelihood estimation (MLE).

* **Compare criteria:** Use metrics like **AIC** (Akaike Information Criterion) or **BIC** — lower values indicate a better balance between accuracy and complexity.
* **Residual Diagnostics:** Check if model residuals behave like **white noise** (uncorrelated with mean = 0). Run a Ljung-Box test on residuals.


4. **4. Forecasting:** Out-of-sample prediction.
Use the selected model to project future values and plot confidence intervals. Validate out-of-sample performance using metrics like **RMSE** or **MAPE**.


---

## Quick Example in Python

Here is a standard implementation snippet using `statsmodels` and `pmdarima` (which automates parameter search via grid search):

```python
import statsmodels.api as sm
from pmdarima import auto_arima

# 1. Automatically find optimal (p, d, q) parameters
auto_model = auto_arima(
    df['value'], 
    seasonal=False,      # Set True and add 'm' for Seasonal ARIMA (SARIMA)
    trace=True, 
    suppress_warnings=True
)

print(auto_model.summary())

# 2. Fit the selected ARIMA model
model = sm.tsa.ARIMA(df['value'], order=auto_model.order)
results = model.fit()

# 3. Forecast future steps
forecast = results.get_forecast(steps=12)
forecast_df = forecast.summary_frame()

```

---

## Important Nuances

* **Seasonality:** If your data exhibits repeating seasonal patterns (e.g., monthly retail sales spikes every December), standard ARIMA won't capture it. Use **SARIMA** ($\text{ARIMA}(p,d,q) \times (P,D,Q)_m$) instead.
* **Exogenous Variables:** If external features influence your time series (e.g., temperature impacting electricity demand), upgrade to **SARIMAX**.