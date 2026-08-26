# 🌡️ 시계열 데이터 분석

서울시 장기 일일 기온 데이터를 기반으로 기온 변화의 장기 추세와 계절 변화를 분석하고 예측하는 시계열 분석 프로젝트이다. 35°C 이상 고온일수의 변화, 여름·겨울 기온 및 계절 변화 추세를 분석하고, Linear Regression과 ARIMA를 활용하여 향후 5년간 서울의 여름 평균기온을 예측한다. 또한 분석 결과를 Streamlit 기반의 인터랙티브 대시보드로 구현하여 기간과 조건에 따라 결과를 탐색할 수 있도록 구성하였다.

* 프로젝트 기간: 2026-08-19 ~ 2026-08-25
* 분석 리포트: [REPORT.md](REPORT.md)
* 대시보드 링크: [seoul-temperature-analysis.streamlit.app](https://seoul-temperature-analysis.streamlit.app/)

## 📌 목차
1. [📖 프로젝트 개요](#-프로젝트-개요)
2. [📁 디렉터리 구조](#-디렉터리-구조)
3. [🔄 데이터 분석 수행 구조 및 순서](#-데이터-분석-수행-구조-및-순서)
4. [💻 개발 환경](#-개발-환경)
5. [🚀 실행 방법](#-실행-방법)
6. [📊 인터랙티브 웹 대시보드 (Streamlit)](#-인터랙티브-웹-대시보드-streamlit)

---

## 📖 프로젝트 개요

* **분석 주제:** 서울시 과거 1907-2026년의 일별 기온 관측 시계열 데이터 분석을 통한 장기 온난화 추세 규명, 계절 확장/축소 패턴 진단 및 향후 5개년(2026-2030년) 여름철 평균기온 예측
* **선정 데이터:** 기상청 기상자료개방포털(KMA) 종관기상관측(ASOS) 서울기상관측소(지점번호 108, 송월동) 일별 기온 데이터 (총 42,236건)
* **주요 목적:** 
  - 100년 이상의 연속 공공 기상 시계열을 바탕으로 장기 기온 상승률을 정량적으로 규명
  - 여름과 겨울의 비대칭적 온난화 속도 비교 검증
  - 환절기(5월·9월 및 11월·3월) 기온 특성 분석을 통한 실질적 여름 기간의 확장 및 겨울 기간의 축소(Seasonal Boundary Shift) 패턴 진단
  - ARIMA(0,1,1) 및 선형 회귀 모델(Linear Regression) 기반 미래 5개년(2026~2030년) 여름철 평균기온 예측 및 불확실성(95% 신뢰구간) 제시

---

## 🔄 데이터 분석 수행 구조 및 순서

본 프로젝트는 원시 데이터 수집부터 최종 웹 서비스 배포까지 총 6단계의 모듈화된 파이프라인으로 구성되어 있다.

1. **데이터 수집 및 정제 & 전처리 (`1_EDA_preprocessing.ipynb`):**
   - 날짜 포맷 표준화, 파생 변수(`season`, `summer_like`, `winter_like`, `over_35` 등) 추출
   - 1.5×IQR 기반 이상치 검증 및 한국전쟁(1950~1953) 결측 기간의 보간 배제 처리
2. **기술 통계 및 시계열 집계 (`2_descriptive_analysis.ipynb`):**
   - 연평균/최고/최저 기온, 계절별 평균 기온, 폭염(≥35°C) 일수 집계
3. **장기 추세 통계 분석 (`3_trend_analysis.ipynb`):**
   - 10년 이동평균을 통한 기저 기온 상승 추세 규명
   - OLS 선형 회귀 및 비모수 Mann-Kendall 검정, Sen's Slope 산출
4. **계절 경계 확장/축소 분석 (`4_seasonal_expansion_analysis.ipynb`):**
   - 일평균 20°C 이상(여름다운 날), 5°C 이하(겨울다운 날) 기준 전이월(5·9·11·3월) 비율 추세 분석 (5월/9월 초·늦여름화, 3월/11월 겨울 축소)
5. **여름철 기온 예측 (`5_prediction.ipynb`):**
   - ADF 단위근 검정 기반 정상성 확보 후 ARIMA(0,1,1) 및 선형 회귀 모델 구축
   - 최근 5개년 백테스팅(MAE/RMSE) 평가 및 2026~2030년 95% 예측 구간 산출
6. **서비스화 및 리포트 작성 (`app.py` / `REPORT.md`):**
   - Plotly 기반의 인터랙티브 Streamlit 웹 대시보드 구축 및 종합 리포트 작성

---

## 📁 디렉터리 구조

```text
time-series-analysis/
├── data/                                    # 데이터셋 디렉터리
│   ├── raw/                                 # KMA 원본 관측 데이터 (dataset_original.csv)
│   └── processed/                           # 정제 및 가공 집계 데이터 (CSV)
├── images/                                  # 분석 및 시각화 이미지
│   └── plots/                               # 파이프라인에서 생성된 통계 차트 (01~15)
├── notebooks/                               # 단계별 탐색적 데이터 분석 (Jupyter Notebooks)
│   ├── 0_intro.ipynb                        # 프로젝트 소개 및 가이드
│   ├── 1_EDA_preprocessing.ipynb            # 데이터 정제, EDA 및 이상치 검정
│   ├── 2_descriptive_analysis.ipynb         # 기술 통계 및 연도/계절별 집계
│   ├── 3_trend_analysis.ipynb               # 이동평균, 선형회귀 및 Mann-Kendall 검정
│   ├── 4_seasonal_expansion_analysis.ipynb  # 환절기 계절 확장/축소 분석
│   └── 5_prediction.ipynb                   # ARIMA 및 선형회귀 여름 기온 5년 예측
├── src/                                     # 모듈화된 핵심 소스 코드
│   ├── data_cleaning.py                     # 결측치/이상치 처리 및 파생변수 생성
│   ├── data_loader.py                       # 데이터 로딩 및 인코딩 처리
│   ├── time_series_analysis.py              # 회귀분석, Mann-Kendall, ARIMA 모델링
│   └── visualization.py                     # 표준 차트 생성 모듈
├── analysis.py                              # 전체 분석 파이프라인 일괄 실행 스크립트
├── app.py                                   # Streamlit 기반 인터랙티브 웹 대시보드
├── REPORT.md                                # 최종 종합 분석 리포트
├── README.md                                # 프로젝트 설명서
└── requirements.txt                         # 프로젝트 의존성 목록
```

---

## 💻 개발 환경

* **언어:** Python 3.10 이상
* **주요 라이브러리:**
  - **데이터 가공 & 수치 계산:** `pandas`, `numpy`, `scipy`
  - **통계 & 머신러닝:** `statsmodels`, `scikit-learn`, `pymannkendall`
  - **데이터 시각화:** `matplotlib`, `plotly`
  - **인터랙티브 웹 대시보드:** `streamlit`
  - **Notebook 환경:** `jupyter`

---

## 🚀 실행 방법

### 1. 저장소 클론

```bash
git clone git@github.com:freepoincare/time-series-data-analysis.git
cd time-series-data-analysis
```

### 2. 환경 설정 및 패키지 설치

```bash
# 가상환경 생성 및 활성화 (선택)
python -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# 의존성 패키지 설치
pip install -r requirements.txt
```

### 3. 전체 분석 파이프라인 일괄 실행

원시 데이터 전처리부터 모든 통계 분석 및 시각화 차트 생성을 한 번에 실행한다:

```bash
python analysis.py
```
> 실행 완료 시 가공 데이터(`data/processed/*.csv`) 및 그래프 이미지(`images/plots/*.png`)가 자동 생성된다.

또는 각 Jupyter Notebook 파일 안에서 상단에 [Run All] 클릭하거나 각 cell를 단계별로 실행.

---

## 📊 인터랙티브 웹 대시보드 (Streamlit)

서울시 118년 기온 시계열 분석 결과를 사용자가 기간과 조건을 실시간으로 변경하며 탐색할 수 있는 반응형 웹 대시보드이다.

* 대시보드 링크: [\[seoul-temperature-analysis.streamlit.app\]](https://seoul-temperature-analysis.streamlit.app/)

### 🌟 주요 기능
1. **인터랙티브 컨트롤:**
   - **연도 범위 슬라이더 (1907~2026):** 원하는 과거 기간을 자유롭게 설정하여 통계 및 차트 실시간 재계산
   - **기온 변수 토글:** 연평균, 연최저, 연최고 기온 선택 및 비교
   - **계절/월 선택 필터:** 전이월(5월, 9월, 3월, 11월)별 비율 변화, 히트맵, 28년 주기(1908-1935 vs 1998-2025) 비교
   - **예측 모델 비교:** ARIMA(0,1,1)과 선형 회귀 예측선 및 95% 신뢰구간 인터랙티브 전환
2. **Plotly 인터랙티브 시각화:**
   - 마우스 호버(Hover) 시 연도, 월, 기온, 비율(%) 등 상세 툴팁 제공
   - 줌(Zoom), 팬(Pan), 범례 클릭을 통한 개별 계열 표시/숨김 지원
3. **단일 확장형 핵심 질문 아코디언(Accordion):**
   - 대시보드 개요 탭에서 6대 핵심 연구 질문 카드를 클릭 시 해당 질문의 통계적 결론이 펼쳐지는 반응형 UI

### 🖥️ 로컬 실행 방법

(streamlit 설치 필요)
```bash
streamlit run app.py
```
> 명령 실행 후 브라우저가 자동 실행되며 `http://localhost:8501`에서 대시보드 탐색 가능.

### ☁️ Streamlit Community Cloud 배포 방법

1. 변경 사항을 GitHub 원격 저장소에 commit 및 push한다:
   ```bash
   git add app.py requirements.txt README.md
   git commit -m "feat: add interactive Streamlit dashboard"
   git push origin main
   ```
2. [Streamlit Community Cloud](https://share.streamlit.io/)에 접속하여 로그인한다.
3. **New app**을 클릭하고 해당 GitHub 저장소, 브랜치(`main`), 메인 파일 경로(`app.py`)를 선택한다.
4. **Deploy** 버튼을 누르면 수 분 내로 공개 배포 URL이 생성된다.

