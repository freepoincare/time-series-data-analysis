# 시계열 데이터 주요 수식 구조

시계열 분석에서 가장 기본이 되는 시계열 분해 구조와 대표적인 예측 모델인 ARIMA의 수학적 공식을 정리해 드립니다.

------------------------------

## 1. 시계열 데이터의 기본 분해 수식 (Time Series Decomposition)

실제 관측값 $Y_t$는 크게 가법 모형(Additive Model)과 승법 모형(Multiplicative Model) 두 가지 방식으로 수식화합니다.

### ① 가법 모형 (Additive Model)

변동의 폭이 시간에 따라 일정한 경우에 사용합니다.

$$Y_t = T_t + S_t + C_t + I_t$$ 

* $T_t$ (Trend): 장기 추세 성분
* $S_t$ (Seasonality): 주기적인 계절성 성분
* $C_t$ (Cyclical): 경기 변동 같은 순환 성분 (종종 추세에 포함됨)
* $I_t$ (Irregular/Noise): 무작위 노이즈 (오차항 $\epsilon_t$)

### ② 승법 모형 (Multiplicative Model)

시간이 흐를수록 변동의 폭이 커지거나 작아지는 경우에 사용합니다.

$$Y_t = T_t \times S_t \times C_t \times I_t$$ 

------------------------------

## 2. ARIMA(p, d, q) 모델의 수학적 수식

ARIMA 모델은 AR(자기회귀), I(차분), MA(이동평균) 세 가지 수학적 메커니즘이 결합된 수식입니다. 기본적으로 안정성(Stationary)을 확보한 시계열 데이터 $y_t$에 대해 아래와 같이 정의됩니다.

## 📌 최종 ARIMA(p, d, q) 수식

$$y_t = c + \phi_1 y_{t-1} + \phi_2 y_{t-2} + \dots + \phi_p y_{t-p} + \epsilon_t + \theta_1 \epsilon_{t-1} + \theta_2 \epsilon_{t-2} + \dots + \theta_q \epsilon_{t-q}$$ 

* $y_t$: 원래 데이터 $Y_t$를 $d$번 차분(Differencing)하여 안정화한 데이터
* $c$: 상수항 (Constant)
* $\epsilon_t$: 현재 시점의 백색 잡음(White Noise) 혹은 예측 오차
* $\phi_1, \dots, \phi_p$: AR(자기회귀) 계수 (과거의 내 값이 현재에 미치는 영향력)
* $\theta_1, \dots, \theta_q$: MA(이동평균) 계수 (과거의 내 오차가 현재에 미치는 영향력)

------------------------------

## 3. 후방 연산자(Backshift Operator, $B$)를 사용한 표현

통계학 논문이나 교재에서는 수식을 간결하게 만들기 위해 후방 연산자 $B$ (또는 $L$, Lag operator)를 주로 사용합니다. ($B y_t = y_{t-1}$)
$$\phi_p(B) (1-B)^d Y_t = c + \theta_q(B) \epsilon_t$$ 

* $\phi_p(B) = 1 - \phi_1 B - \dots - \phi_p B^p$ : AR 부분 다항식
* $(1-B)^d$ : $d$차 차분을 뜻하는 연산식
* $\theta_q(B) = 1 + \theta_1 B + \dots + \theta_q B^q$ : MA 부분 다항식

------------------------------

혹시 위 수식들 중에서 특정 계수($\phi, \theta$)를 추정하는 방법(예: MLE, OLS)이나 차분($(1-B)^d$)의 실제 계산 과정이 궁금하신가요? 구체적으로 알고 싶은 부분을 말씀해 주시면 상세히 풀어드리겠습니다.

