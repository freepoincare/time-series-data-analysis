# Stationarity in Augmented Dickey-Fuller (ADF) test

In the context of the Augmented Dickey-Fuller (ADF) test, stationarity means that a time series has statistical properties that do not change over time.
If a time series is stationary, it behaves predictably, making it much easier to model and forecast.

---

## The 3 Criteria for Stationarity
For a time series to be considered stationary (specifically, weakly stationary), it must satisfy three conditions over time:

   1. Constant Mean: The series fluctuates around a stable average level. It has no upward or downward trend.
   2. Constant Variance: The amplitude of the fluctuations stays relatively consistent. It does not get wilder or quieter over time.
   3. Constant Autocovariance: The correlation between a data point ($Y_t$) and a past data point ($Y_{t-k}$) depends only on the distance (k) between them, not on the actual time (t).

---

## Why Stationarity Matters in the ADF Test
The ADF test is a statistical hypothesis test used to determine if a time series is stationary or non-stationary by checking for the presence of a unit root.

* Presence of a Unit Root = Non-Stationary: A unit root means the series has a unpredictable systematic trend (like a random walk) and a memory that lasts forever (shocks never fade away).
* Absence of a Unit Root = Stationary: The series is stable, and any sudden shock or jump will eventually decay, returning the series to its mean.

## How the ADF Test Evaluates Stationarity
The test sets up two competing hypotheses:

* Null Hypothesis (H₀): The time series has a unit root (It is non-stationary).
* Alternative Hypothesis (H₁): The time series does not have a unit root (It is stationary).

## How to interpret the results:
When you run the adfuller() test in Python (statsmodels), you look at the p-value or the ADF Statistic:

* If p-value ≤ 0.05 (or the ADF Statistic is more negative than the Critical Values): You reject H₀. The series is Stationary.
* If p-value > 0.05 (or the ADF Statistic is less negative than the Critical Values): You fail to reject H₀. The series is Non-Stationary (it has a trend or variance issue).

---
## What to do if your data is Non-Stationary?
If the ADF test tells you your data is non-stationary, you cannot use it directly in models like ARIMA. You must transform it first:

* Differencing: Subtract the previous value from the current value ($Y_t - Y_{t-1}$) to remove trends. (This is the most common fix).
* Log Transformation: Apply a logarithm to stabilize a widening variance.

---

## First-Order Differencing

```pyhon
import pandas as pd
from statsmodels.tsa.stattools import adfuller

# 1. Apply first-order differencing
df['differenced_data'] = df['your_column_name'].diff()

# 2. Drop the resulting NaN value in the first row
df_clean = df['differenced_data'].dropna()

# 3. Re-run the ADF test
new_result = adfuller(df_clean)
print(f"New ADF Statistic: {new_result[0]}")
print(f"New p-value: {new_result[1]}")
```

After first differencing:

* If the new p-value drops below 0.05: Your data is now stationary and ready for an ARIMA(p, 1, q) model, where the \(d\) parameter equals 1.

* If the new p-value is still above 0.05: You may need a second round of differencing (.diff().diff()) or a log transformation first if the fluctuations are getting wider over time.

---

## PACF and ACF plot interpretation

| Plot Pattern | Indicated Term | How to choose the value |
|---|---|---|
| PACF shuts off sharply after lag p | AR term (p) | Count how many consecutive bars exit the blue area on the PACF plot before dropping inside. | 
| ACF shuts off sharply after lag q | MA term (q) | Count how many consecutive bars exit the blue area on the ACF plot before dropping inside. |

Common Examples:
* Scenario A: PACF has 2 sharp bars outside the blue zone, then drops inside. ACF decays slowly like a wave.
   * Result: AR(2) model → ARIMA(2, 1, 0)
* Scenario B: ACF has 1 sharp bar outside the blue zone, then drops inside. PACF decays slowly.
   * Result: MA(1) model → ARIMA(0, 1, 1)

