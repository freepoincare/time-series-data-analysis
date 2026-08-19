# AI 데이터 분석 프로젝트

## Step-by-Step Guide

이 문서는 **「AI 데이터 분석: 데이터 기반 트렌드 분석」** 과제를 처음부터 최종 제출까지 단계별로 진행하기 위한 실전 가이드입니다.

---

# Step 0. 프로젝트 목표 이해하기

이 프로젝트의 핵심은 단순히 그래프를 만드는 것이 아닙니다.

> **데이터 → 질문 → 분석 → 시각화 → 관찰 → 해석 → 인사이트 → 결론**

이 흐름을 완성하는 것이 가장 중요합니다.

최종적으로 다음 질문에 답할 수 있어야 합니다.

* 어떤 데이터를 분석했는가?
* 왜 이 데이터를 선택했는가?
* 무엇을 알고 싶었는가?
* 데이터를 어떻게 정제했는가?
* 어떤 분석 방법을 사용했는가?
* 그래프에서 무엇을 발견했는가?
* 그 현상을 어떻게 해석할 수 있는가?
* 그래서 어떤 의미가 있는가?
* 분석의 한계는 무엇인가?

---

# Step 1. 프로젝트 폴더 확인

먼저 프로젝트 구조를 확인합니다.

```text
ai-time-series-analysis/
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
├── images/
├── notebooks/
│   └── analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_cleaning.py
│   ├── time_series_analysis.py
│   └── visualization.py
├── tests/
│   ├── __init__.py
│   └── test_data_cleaning.py
├── docs/
│   ├── analysis_plan.md
│   └── ai_usage_log.md
├── analysis.py
├── README.md
├── REPORT.md
├── requirements.txt
└── .gitignore
```

처음에는 모든 파일을 완성하려고 하지 않습니다.

**분석 → 결과 확인 → 코드 정리 → 리포트 작성** 순서로 진행합니다.

---

# Step 2. 분석 주제 선정

먼저 시계열 데이터 하나를 선택합니다.

가능한 주제:

* 주식 가격
* 암호화폐 가격
* 환율
* 기온
* 강수량
* 판매량
* 웹사이트 방문자 수
* YouTube 조회수
* 검색량
* 전력 사용량
* 대기오염
* 교통량
* 관광객 수

### 좋은 주제의 조건

다음 조건을 만족하는 데이터를 선택하는 것이 좋습니다.

* 시간 순서가 존재한다.
* 데이터가 100개 이상이다.
* 날짜/시간 컬럼이 있다.
* 숫자로 분석할 수 있는 변수가 있다.
* 변화나 패턴을 발견할 가능성이 있다.
* 신뢰할 수 있는 출처가 있다.

### 추천

처음 하는 프로젝트라면 너무 복잡한 데이터보다 다음과 같은 형태가 좋습니다.

```text
Date        Value
2024-01-01  102
2024-01-02  105
2024-01-03  101
...
```

데이터가 복잡할수록 데이터 전처리에 시간이 많이 들어갑니다.

---

# Step 3. 분석 질문 3개 만들기

데이터를 선택한 후 바로 그래프를 그리지 않습니다.

먼저 질문을 만듭니다.

최소 3개의 질문을 작성합니다.

예를 들어 주가 데이터를 선택했다면:

```text
1. 전체 기간 동안 가격은 상승 또는 하락 추세를 보였는가?
2. 가장 큰 상승/하락은 언제 발생했는가?
3. 특정 기간이나 월에 반복적인 패턴이 존재하는가?
```

좋은 질문은 분석 방법과 연결됩니다.

예:

```text
질문
↓
어떤 데이터를 봐야 하는가?
↓
어떤 분석을 해야 하는가?
↓
어떤 그래프가 필요한가?
```

---

# Step 4. 분석 계획 작성

`docs/analysis_plan.md`를 먼저 작성합니다.

다음 내용을 결정합니다.

```markdown
# Analysis Plan

## 1. Dataset

- Dataset:
- Source:
- Period:
- Number of data points:
- Main variables:

## 2. Questions

1.
2.
3.

## 3. Data Cleaning

- Missing values:
- Duplicates:
- Outliers:
- Date handling:

## 4. Analysis Methods

1.
2.

## 5. Visualizations

1.
2.
3.

## 6. Expected Insights

-
-
-

## 7. Limitations

-
-
```

처음부터 정확하게 작성할 필요는 없습니다.

분석하면서 수정해도 됩니다.

---

# Step 5. 데이터 수집

선택한 데이터를 다운로드합니다.

예를 들어 CSV 파일이라면:

```text
data/raw/my_dataset.csv
```

에 저장합니다.

중요한 것은 **원본 데이터를 그대로 보관하는 것**입니다.

```text
data/
├── raw/
│   └── original_data.csv
└── processed/
    └── cleaned_data.csv
```

`raw` 데이터는 직접 수정하지 않는 것을 권장합니다.

---

# Step 6. 데이터 출처 기록

`data/README.md`에 데이터 정보를 기록합니다.

```markdown
# Data

## Raw Data

- Source:
- URL:
- Collection date:
- Time period:
- License:
- File name:

## Processed Data

- Original file:
- Cleaning performed:
- Transformation performed:
```

특히 다음 정보를 반드시 기록합니다.

* 데이터 출처
* 데이터 기간
* 데이터 다운로드/수집 방법
* 라이선스 또는 사용 조건

---

# Step 7. Python 환경 설정

Python 3.10 이상을 사용합니다.

프로젝트 폴더에서 가상환경을 사용하는 것을 권장합니다.

```bash
python -m venv .venv
```

가상환경을 활성화합니다.

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

필요한 라이브러리를 설치합니다.

```bash
pip install pandas matplotlib jupyter
```

필요하다면 추가 라이브러리를 설치합니다.

예:

```bash
pip install seaborn numpy
```

설치한 라이브러리는 나중에 `requirements.txt`에 기록합니다.

```bash
pip freeze > requirements.txt
```

---

# Step 8. 데이터 불러오기

먼저 Jupyter Notebook에서 데이터를 확인합니다.

`notebooks/analysis.ipynb`

```python
import pandas as pd

df = pd.read_csv("../data/raw/my_dataset.csv")

df.head()
```

데이터가 제대로 읽혔는지 확인합니다.

---

# Step 9. 데이터 기본 정보 확인

다음 내용을 확인합니다.

### 데이터 크기

```python
df.shape
```

최소 100개 이상의 데이터 포인트가 있는지 확인합니다.

### 컬럼

```python
df.columns
```

### 데이터 타입

```python
df.info()
```

### 통계 정보

```python
df.describe()
```

### 결측치

```python
df.isnull().sum()
```

### 중복 데이터

```python
df.duplicated().sum()
```

이 단계의 목적은:

> **"내 데이터가 정확히 어떤 상태인지 이해하는 것"**

입니다.

---

# Step 10. 날짜 컬럼 처리

시계열 분석에서는 날짜가 매우 중요합니다.

예를 들어 날짜 컬럼이 `Date`라면:

```python
df["Date"] = pd.to_datetime(df["Date"])
```

그리고 날짜순으로 정렬합니다.

```python
df = df.sort_values("Date")
```

필요하다면 index로 설정합니다.

```python
df = df.set_index("Date")
```

이제 시간 순서에 따라 데이터를 분석할 수 있습니다.

---

# Step 11. 결측치 처리

먼저 결측치를 확인합니다.

```python
df.isnull().sum()
```

결측치가 없다면:

```text
결측치 없음
```

이라고 기록하면 됩니다.

결측치가 있다면 데이터 특성에 맞는 방법을 선택합니다.

예:

```python
df = df.dropna()
```

또는:

```python
df["Value"] = df["Value"].interpolate()
```

중요한 것은 **어떤 방법을 사용했는지와 왜 사용했는지 설명하는 것**입니다.

예:

```text
결측치가 연속적인 시계열 데이터에서 소수 존재했기 때문에
선형 보간법을 사용하여 값을 추정하였다.
```

---

# Step 12. 이상치 확인

이상치가 있는지 확인합니다.

기본적인 방법으로 boxplot을 사용할 수 있습니다.

```python
df["Value"].plot(kind="box")
```

또는 통계적인 기준을 사용할 수 있습니다.

중요한 점은:

> 이상치라고 해서 무조건 삭제하면 안 됩니다.

예를 들어 주가가 하루에 크게 상승했다면 그것은 오류가 아니라 실제 중요한 사건일 수 있습니다.

따라서:

```text
이상치 발견
↓
데이터 오류인가?
↓
실제 사건인가?
↓
처리할 것인가?
```

를 판단합니다.

---

# Step 13. 첫 번째 그래프 만들기

가장 먼저 **전체 시계열 추이**를 확인합니다.

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.plot(df.index, df["Value"])

plt.title("Time-Series Trend")
plt.xlabel("Date")
plt.ylabel("Value")

plt.tight_layout()
plt.savefig("../images/01_time_series.png", dpi=300)
plt.show()
```

이 그래프는 가장 기본적인 그래프입니다.

하지만 그래프를 만들었다고 분석이 끝난 것이 아닙니다.

---

# Step 14. 그래프를 보고 "관찰" 작성

그래프를 보고 먼저 **Fact**를 작성합니다.

예:

```text
관찰:
2024년 3월부터 6월까지 값이 약 120에서 160으로 증가했다.
```

이것은 데이터에서 직접 확인할 수 있는 내용입니다.

반면:

```text
해석:
AI 관련 수요 증가 때문에 값이 상승했을 가능성이 있다.
```

이것은 해석 또는 가설입니다.

둘을 구분해야 합니다.

### 좋은 분석 구조

```text
관찰(Fact)
↓
근거(Evidence)
↓
해석(Interpretation)
↓
가능한 원인(Why)
↓
의미/행동(Action)
```

---

# Step 15. 첫 번째 시계열 분석 적용

과제에서는 최소 2가지 시계열 분석 기법을 사용해야 합니다.

가장 추천하는 방법 중 하나는 **이동평균(Moving Average)**입니다.

예:

```python
df["MA_7"] = df["Value"].rolling(7).mean()
```

그래프로 표현합니다.

```python
plt.figure(figsize=(12, 6))

plt.plot(df.index, df["Value"], label="Value")
plt.plot(df.index, df["MA_7"], label="7-Day Moving Average")

plt.title("Value and 7-Day Moving Average")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()

plt.tight_layout()
plt.savefig("../images/02_moving_average.png", dpi=300)
plt.show()
```

### 왜 이동평균을 사용하는가?

일별 데이터의 단기적인 노이즈를 줄이고 전체적인 추세를 더 쉽게 보기 위해 사용할 수 있습니다.

---

# Step 16. 두 번째 시계열 분석 적용

두 번째 방법은 데이터에 맞게 선택합니다.

가능한 방법:

* 변화율
* 수익률
* 변동성
* 표준편차
* 월별 평균
* 요일별 평균
* 월별 변화
* 구간별 통계

예를 들어 변화율을 계산한다면:

```python
df["Change_Rate"] = df["Value"].pct_change() * 100
```

그리고 시각화합니다.

```python
plt.figure(figsize=(12, 6))

plt.plot(df.index, df["Change_Rate"])

plt.title("Change Rate Over Time")
plt.xlabel("Date")
plt.ylabel("Change Rate (%)")

plt.tight_layout()
plt.savefig("../images/03_change_rate.png", dpi=300)
plt.show()
```

---

# Step 17. 세 번째 분석 또는 시각화 추가

과제에서는 시각화 2개가 필수이고 3개 이상이 권장됩니다.

가능하면 세 번째 그래프까지 만듭니다.

예:

```text
01_time_series.png
02_moving_average.png
03_monthly_analysis.png
```

또는:

```text
01_price_trend.png
02_moving_average.png
03_change_rate.png
```

그래프마다 **서로 다른 질문에 답할 수 있도록** 만드는 것이 좋습니다.

단순히 비슷한 그래프 3개를 만드는 것은 피합니다.

---

# Step 18. 인사이트 3개 도출

이제 과제에서 가장 중요한 단계입니다.

최소 3개의 인사이트를 작성합니다.

각 인사이트는 다음 구조를 사용합니다.

```markdown
### Insight 1

**관찰(Fact)**  
<!-- 데이터에서 직접 확인한 사실 -->

**근거(Evidence)**  
<!-- 구체적인 수치 또는 기간 -->

**해석(Why)**  
<!-- 가능한 이유 또는 가설 -->

**행동(Action)**  
<!-- 추가 분석 또는 의사결정에 어떤 의미가 있는가 -->
```

예:

```markdown
### Insight 1

**관찰(Fact)**  
2024년 3월부터 6월까지 값이 지속적으로 상승했다.

**근거(Evidence)**  
해당 기간의 값이 약 120에서 160으로 증가했다.

**해석(Why)**  
해당 기간에 특정 외부 요인이 증가에 영향을 주었을 가능성이 있다.

**행동(Action)**  
추가적으로 해당 기간의 외부 이벤트와 데이터를 비교할 필요가 있다.
```

---

# Step 19. Observation과 Interpretation 구분

이 과제에서 특히 중요합니다.

### Observation

데이터에서 직접 확인할 수 있는 것:

```text
2024년 5월 값이 전월 평균보다 15% 높았다.
```

### Interpretation

그 이유에 대한 해석:

```text
계절적 요인이 영향을 주었을 가능성이 있다.
```

### 잘못된 방식

```text
5월에는 날씨가 좋아서 판매량이 증가했다.
```

데이터만으로 날씨를 분석하지 않았다면 이것은 근거 없는 결론이 될 수 있습니다.

### 더 좋은 방식

```text
5월 판매량이 전월보다 증가했다.
이는 계절적 요인이나 외부 환경의 영향을 받았을 가능성이 있으나,
현재 분석에서는 해당 요인을 직접 검증하지 않았다.
```

---

# Step 20. 결과를 REPORT.md에 작성

이제 `REPORT.md`를 완성합니다.

권장 구조:

```markdown
# 분석 제목

## 1. 분석 주제 및 선정 이유

## 2. 분석 질문

1.
2.
3.

## 3. 데이터 설명

## 4. 데이터 정제

### 4.1 기본 정보

### 4.2 결측치

### 4.3 이상치

## 5. 시계열 분석

### 5.1 이동평균

### 5.2 변화율

## 6. 분석 결과 및 시각화

### 6.1 시각화 1

### 6.2 시각화 2

### 6.3 시각화 3

## 7. 인사이트

### Insight 1

### Insight 2

### Insight 3

## 8. 결론

## 9. 한계점

## 10. AI 사용 로그
```

---

# Step 21. 시각화 파일 확인

`images/` 폴더에 최종 그래프가 있어야 합니다.

예:

```text
images/
├── 01_time_series.png
├── 02_moving_average.png
└── 03_change_rate.png
```

그리고 `REPORT.md`에서 이미지가 정상적으로 표시되는지 확인합니다.

```markdown
![Time-Series Trend](images/01_time_series.png)
```

---

# Step 22. AI 사용 로그 작성

AI를 사용했다면 반드시 기록합니다.

`docs/ai_usage_log.md`에 기록합니다.

예:

```markdown
| Date | Task | AI Tool | Prompt / Request Summary | Why AI Was Used | What Was Accepted/Changed | Verification Method |
|---|---|---|---|---|---|---|
| 2026-08-20 | Data cleaning | ChatGPT | Missing value handling 방법 질문 | 대안 탐색 | interpolation 사용 | 직접 결과 확인 |
| 2026-08-20 | Visualization | ChatGPT | Moving average 코드 작성 | 코드 작성 지원 | 일부 수정 | 직접 실행 및 결과 확인 |
| 2026-08-21 | Interpretation | ChatGPT | 그래프 해석 아이디어 요청 | 대안 탐색 | 최종 해석은 직접 작성 | 원본 데이터와 비교 |
```

핵심은 **AI가 최종 분석을 대신했다는 인상을 주지 않는 것**입니다.

AI는 다음과 같이 활용할 수 있습니다.

```text
AI
↓
코드 아이디어
↓
분석 방법 제안
↓
대안 탐색
↓
사용자가 직접 검증
↓
최종 판단
```

---

# Step 23. Python 코드 정리

분석이 끝난 후 Notebook에 작성한 코드를 정리합니다.

처음부터 `src/`를 완벽하게 구현할 필요는 없습니다.

분석이 완료된 후 다음과 같이 정리할 수 있습니다.

```text
src/
├── data_loader.py
├── data_cleaning.py
├── time_series_analysis.py
└── visualization.py
```

예를 들어:

```python
# data_loader.py

def load_data(file_path):
    ...
```

```python
# data_cleaning.py

def clean_data(data):
    ...
```

```python
# time_series_analysis.py

def calculate_moving_average(data):
    ...
```

```python
# visualization.py

def create_visualizations(data):
    ...
```

---

# Step 24. 테스트

간단한 테스트를 작성합니다.

```bash
pytest
```

또는 최소한 Python 파일이 정상적으로 실행되는지 확인합니다.

```bash
python analysis.py
```

---

# Step 25. 재현성 확인

다른 사람이 프로젝트를 받아도 실행할 수 있는지 확인합니다.

확인할 것:

```text
[ ] Python 버전이 명시되어 있는가?
[ ] requirements.txt가 있는가?
[ ] 데이터 출처가 적혀 있는가?
[ ] 데이터를 어떻게 얻는지 설명되어 있는가?
[ ] 실행 방법이 README에 있는가?
[ ] 이미지 경로가 정상인가?
[ ] Notebook이 처음부터 끝까지 실행되는가?
```

---

# Step 26. README.md 완성

README에는 프로젝트를 빠르게 이해할 수 있는 정보를 넣습니다.

추천 구조:

```markdown
# Project Title

## Overview

## Analysis Questions

## Dataset

## Analysis Methods

## Key Insights

## Visualizations

## Project Structure

## Installation

## Usage

## Limitations

## AI Usage
```

README는 **프로젝트 소개용**이고,

`REPORT.md`는 **상세 분석 결과용**이라고 생각하면 됩니다.

---

# Step 27. GitHub 저장소 준비

GitHub에 repository를 생성합니다.

예:

```text
ai-time-series-analysis
```

프로젝트 폴더에서:

```bash
git init
```

파일을 확인합니다.

```bash
git status
```

파일을 추가합니다.

```bash
git add .
```

커밋합니다.

```bash
git commit -m "Complete time-series data analysis project"
```

GitHub repository를 연결합니다.

```bash
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
```

그리고 push합니다.

```bash
git push -u origin main
```

---

# Step 28. 최종 제출 전 체크리스트

## 데이터

* [ ] 시계열 데이터가 100개 이상인가?
* [ ] 데이터 출처를 기록했는가?
* [ ] 분석 기간을 기록했는가?
* [ ] 원본 데이터를 `data/raw/`에 보관했는가?
* [ ] 데이터 라이선스/사용 조건을 확인했는가?

## 분석

* [ ] 분석 질문이 3개 이상인가?
* [ ] 결측치를 확인했는가?
* [ ] 이상치를 확인했는가?
* [ ] 시계열 분석 기법을 2개 이상 적용했는가?
* [ ] 분석 결과에 구체적인 수치가 포함되어 있는가?

## 시각화

* [ ] 시각화가 최소 2개인가?
* [ ] 가능하면 3개 이상인가?
* [ ] 날짜가 올바르게 정렬되어 있는가?
* [ ] 축 이름이 명확한가?
* [ ] 범례가 필요한 경우 추가했는가?
* [ ] 그래프가 분석 질문과 연결되는가?

## 인사이트

* [ ] 인사이트가 최소 3개인가?
* [ ] Observation과 Interpretation을 구분했는가?
* [ ] 각 인사이트에 데이터 근거가 있는가?
* [ ] 단순히 그래프를 설명하는 데 그치지 않았는가?
* [ ] 가능한 원인과 한계를 구분했는가?

## 리포트

* [ ] `REPORT.md`가 완성되었는가?
* [ ] 분석 주제가 명확한가?
* [ ] 질문이 명확한가?
* [ ] 데이터 설명이 있는가?
* [ ] 시각화가 포함되어 있는가?
* [ ] 인사이트가 포함되어 있는가?
* [ ] 결론이 있는가?
* [ ] 한계점이 있는가?
* [ ] AI 사용 로그가 있는가?

## 코드

* [ ] Python 코드가 정상적으로 실행되는가?
* [ ] Notebook이 처음부터 끝까지 실행되는가?
* [ ] `requirements.txt`가 작성되어 있는가?
* [ ] 불필요한 코드가 제거되었는가?
* [ ] 변수명이 이해하기 쉬운가?

## GitHub

* [ ] README가 있는가?
* [ ] 코드가 올라가 있는가?
* [ ] REPORT.md가 올라가 있는가?
* [ ] 이미지가 정상적으로 표시되는가?
* [ ] 실행 방법이 설명되어 있는가?
* [ ] GitHub repository가 다른 사람에게 이해될 수 있는가?

---

# Step 29. 최종 프로젝트 구조

최종적으로 다음과 같은 형태를 목표로 합니다.

```text
ai-time-series-analysis/
│
├── data/
│   ├── raw/
│   │   └── original_dataset.csv
│   ├── processed/
│   │   └── cleaned_dataset.csv
│   └── README.md
│
├── images/
│   ├── 01_time_series.png
│   ├── 02_moving_average.png
│   └── 03_change_rate.png
│
├── notebooks/
│   └── analysis.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_cleaning.py
│   ├── time_series_analysis.py
│   └── visualization.py
│
├── tests/
│   ├── __init__.py
│   └── test_data_cleaning.py
│
├── docs/
│   ├── analysis_plan.md
│   └── ai_usage_log.md
│
├── analysis.py
├── README.md
├── REPORT.md
├── requirements.txt
└── .gitignore
```

---

# Step 30. 가장 중요한 작업 순서

전체 프로젝트를 한 줄로 정리하면 다음 순서로 진행합니다.

```text
1. 주제 선택
      ↓
2. 데이터 선택
      ↓
3. 분석 질문 3개 작성
      ↓
4. 데이터 다운로드
      ↓
5. 데이터 기본 정보 확인
      ↓
6. 결측치 / 이상치 확인
      ↓
7. 데이터 정제
      ↓
8. 첫 번째 시각화
      ↓
9. 시계열 분석 방법 1
      ↓
10. 시계열 분석 방법 2
      ↓
11. 두 번째 / 세 번째 시각화
      ↓
12. Observation 작성
      ↓
13. Interpretation 작성
      ↓
14. 인사이트 3개 도출
      ↓
15. 결론 및 한계점 작성
      ↓
16. AI 사용 로그 작성
      ↓
17. REPORT.md 완성
      ↓
18. README.md 완성
      ↓
19. 코드 정리
      ↓
20. 실행 및 재현성 테스트
      ↓
21. GitHub 업로드
      ↓
22. 최종 체크리스트 확인
```

---

# 핵심 원칙

이 프로젝트에서는 **복잡한 머신러닝 모델을 만드는 것보다 분석 과정과 해석의 논리**가 더 중요합니다.

가장 중요한 흐름은 다음과 같습니다.

> **Question → Data → Analysis → Visualization → Observation → Interpretation → Insight**

특히 다음 두 가지를 항상 구분합니다.

```text
Observation
"데이터에서 실제로 무엇이 보이는가?"

vs.

Interpretation
"왜 이런 현상이 나타났을까?"
```

그리고 최종적으로:

```text
Insight
"그래서 이것이 어떤 의미를 가지는가?"
```

까지 연결하면 좋은 분석 리포트가 됩니다.
