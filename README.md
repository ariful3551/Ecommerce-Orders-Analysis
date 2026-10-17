# E-commerce Orders Analysis

End-to-end analysis of an e-commerce orders dataset: data understanding, data cleaning, exploratory data analysis (EDA), visualization and business insights, using Python and pandas.

> **Status:** 🚧 In progress. Currently working on Step 1 (Data Understanding).

---

## Table of Contents

1. [Project Goal](#project-goal)
2. [Dataset](#dataset)
3. [Disclaimer](#disclaimer)
4. [Workflow](#workflow)
5. [Business Questions](#business-questions)
6. [Data Cleaning Summary](#data-cleaning-summary)
7. [Key Findings](#key-findings)
8. [Project Structure](#project-structure)
9. [How to Run](#how-to-run)
10. [Tools](#tools)
11. [Author](#author)

---

## Project Goal

Understand sales, profit, discounts, delivery performance and returns of an online store, and answer practical business questions with data. The project is also a learning exercise that covers the full workflow of a small data analysis project: from a messy raw file to a clean dataset, visual exploration and written recommendations.

## Dataset

| Item | Details |
|------|---------|
| File | `data/raw/ecommerce_orders_raw.csv` |
| Size | 5,020 rows × 28 columns |
| Period covered | TBD (confirmed after date cleaning in Step 2) |
| Granularity | One row per order line |
| Source | Synthetic dataset generated with ChatGPT (OpenAI) for learning purposes |

The columns cover orders, customers, products, pricing and discounts, sales, cost and profit, payment, shipping and delivery, customer rating, returns, marketing channel and device type. A full column-by-column description is in [`data/data_dictionary.md`](data/data_dictionary.md).

The raw file is kept untouched. The cleaned version is saved separately in `data/processed/`.

## Disclaimer

All data in this project is **synthetic**. It does not represent a real company or real customers. Findings describe patterns in this generated dataset only and should not be treated as real-world business insights.

## Workflow

| Step | Notebook | Purpose | Status |
|------|----------|---------|--------|
| 1 | `notebooks/01_data_understanding.ipynb` | Inspect structure, types, missing values, duplicates and value ranges | 🔄 In progress |
| 2 | `notebooks/02_data_cleaning.ipynb` | Fix inconsistencies and produce a clean dataset | ⏳ Not started |
| 3 | `notebooks/03_eda_visualization.ipynb` | Explore distributions, trends and relationships with charts | ⏳ Not started |
| 4 | `notebooks/04_business_questions.ipynb` | Answer specific business questions and give recommendations | ⏳ Not started |

Every cleaning decision (what was wrong, how many rows, what was done and why) is documented in [`docs/cleaning_decisions.md`](docs/cleaning_decisions.md).

## Business Questions

_Draft list. It will be finalized after the exploratory analysis._

1. How do sales and profit change over time (month, quarter, year)?
2. Which product categories and products bring the most revenue, and which bring the most profit?
3. How do discounts affect quantity sold and profit? At what discount level do orders start losing money?
4. Which marketing channels, customer segments and countries perform best?
5. How do shipping method and delivery time relate to customer rating and returns?

## Data Cleaning Summary

_To be added after Step 2._

| Issue | Rows affected | Action | Reason |
|-------|---------------|--------|--------|
| TBD | TBD | TBD | TBD |

## Key Findings

_To be added after Steps 3 and 4._

## Project Structure

```text
Ecommerce_Orders_Analysis/
├── data/
│   ├── raw/                      # original data (never edited)
│   ├── processed/                # cleaned data
│   └── data_dictionary.md        # column descriptions
├── docs/
│   └── cleaning_decisions.md     # cleaning decisions and reasons
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_visualization.ipynb
│   └── 04_business_questions.ipynb
├── reports/
│   ├── figures/                  # saved charts
│   └── summary.md                # summary of results and recommendations
├── src/
│   └── cleaning.py               # reusable cleaning functions
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## How to Run

```bash
git clone https://github.com/ariful3551/Ecommerce-Orders-Analysis.git
cd Ecommerce-Orders-Analysis

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
jupyter notebook
```

Run the notebooks in order, from `01` to `04`. Notebook `02` creates `data/processed/ecommerce_orders_clean.csv`, which notebooks `03` and `04` read.

## Tools

Python, pandas, NumPy, Matplotlib, Jupyter Notebook, Git and GitHub.

## Author

**Ariful Islam**
GitHub: [@ariful3551](https://github.com/ariful3551)