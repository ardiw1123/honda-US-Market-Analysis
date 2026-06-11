# Honda US Market Analysis

An end-to-end data analysis and interactive dashboard project exploring Honda vehicle sales patterns across the United States — covering pricing dynamics, consumer satisfaction, hybrid adoption trends, and geographic market distribution.

> Built as a portfolio project targeting Business & Sales Analyst roles in the automotive industry.

---

## Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_red.svg)](https://your-app-link.streamlit.app)

> Replace the link above after deploying to [Streamlit Community Cloud](https://streamlit.io/cloud)

---

## Dashboard Preview

> Add a screenshot of your dashboard here after deployment.  
> `![Dashboard Preview](assets/preview.png)`

---

## Project Structure

```
honda-sales-analysis/
├── app.py                  # Streamlit dashboard (5 pages)
├── honda_eda.ipynb         # Exploratory Data Analysis notebook
├── honda_cleaned.csv       # Cleaned dataset used by the dashboard
├── honda_sell_data.csv     # Raw source dataset
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Dataset

| Attribute | Detail |
|---|---|
| Source | Honda vehicle listings — US market |
| Records | 4,949 vehicles |
| Year Range | 1981 – 2023 |
| Features | 34 attributes |
| States Covered | 53 |
| Model Families | 15 |
| Conditions | New, Used, Honda Certified |
| Fuel Types | Gasoline, Hybrid, Compressed Natural Gas |

**Key features:** `Price`, `Model_Family`, `Condition`, `Year`, `Mileage`, `Fuel_Type`, `State`, `Region`, `Consumer_Rating`, `Is_Hybrid`, `MPG_City`, `MPG_Highway`, and 6 consumer rating dimensions.

---

## Dashboard Pages

### 1. Executive Overview
High-level summary of the entire dataset — listing volume by model family, condition breakdown, price distribution, and listing trends by model year.

### 2. Pricing & Depreciation
Filterable analysis of vehicle pricing by model, condition, and year range — including a depreciation curve (price vs. vehicle age) and a price-vs-mileage scatter for used inventory.

### 3. Consumer Satisfaction
Radar chart comparison of 6 rating dimensions (Comfort, Interior Design, Performance, Value for Money, Exterior Styling, Reliability) across model families, with a value map plotting rating vs. average price.

### 4. Hybrid vs Gasoline
Side-by-side comparison of fuel types across price, fuel economy (MPG), consumer ratings, and hybrid adoption trends in new vehicle listings over time.

### 5. Market Geography
US choropleth map switchable between average price, listing volume, average rating, and hybrid share — with region-level breakdowns and a state-level detail table.

---

## Analysis Highlights (EDA Notebook)

- **Pearson correlation & ANOVA** to identify statistically significant price predictors
- **Depreciation analysis** by model family and vehicle age
- **Hybrid adoption trend** across model years in new vehicle segment
- **Consumer rating correlation matrix** across 6 satisfaction dimensions
- **Regional pricing disparities** across US states and geographic regions

---

## Tech Stack

| Component | Tools |
|---|---|
| Language | Python 3 |
| Dashboard | Streamlit |
| Visualization | Plotly Express, Plotly Graph Objects |
| Data Manipulation | Pandas, NumPy |
| Statistical Analysis | SciPy |
| EDA Notebook | Jupyter Notebook |

---

## Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-username/honda-sales-analysis.git
cd honda-sales-analysis
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the dashboard**
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## Requirements

Create a `requirements.txt` with the following:

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
scipy>=1.11.0
```

---

## Key Insights

- **Engine size, curb weight, and horsepower** are the strongest numerical predictors of vehicle price
- **RWD vehicles** command a statistically significant price premium over FWD (ANOVA p < 0.05)
- **Hybrid vehicles** are priced higher on average but score comparably to gasoline across all consumer rating dimensions
- **Value for Money** and **Reliability** are the highest-rated dimensions across the Honda lineup
- **West Coast states** show higher average prices, while the Midwest presents stronger value-for-money listings

---

## Author

**Ardi**
Information Systems — UPN "Veteran" Yogyakarta
[LinkedIn](https://linkedin.com/in/your-profile) · [GitHub](https://github.com/your-username)
