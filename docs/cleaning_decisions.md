# Cleaning Decisions

This file records every cleaning decision: what the problem was, how many rows were affected, what was done and why. The raw file (`data/raw/ecommerce_orders_raw.csv`) is never modified. All changes are made in `notebooks/02_data_cleaning.ipynb` and saved to `data/processed/ecommerce_orders_clean.csv`.

Problems come from the Step 1 summary in `notebooks/01_data_understanding.ipynb`.

## Decisions made

| # | Issue | Rows affected | Action | Why |
|---|-------|---------------|--------|-----|
| 1 | Extra leading/trailing spaces in text columns | Gender: 820, Country: 458, Customer_Name: 8 | Removed with `str.strip()` on all text columns | Values such as ` m ` and `Germany ` were counted as different categories |
| 2 | `Order_Date` stored as text in 3 formats | All 5,020 (`YYYY-MM-DD`: 4,410, `DD/MM/YYYY`: 466, `Mon DD, YYYY`: 144) | Parsed each format separately with an explicit format string and combined them into one datetime column. 0 dates failed. Range: 2023-01-01 to 2025-12-31 | Text dates cannot be used for monthly or yearly analysis. The slash format is day/month/year: in Step 1 the first part was greater than 12 in 303 rows and the second part never was, so reading it as month/day would be wrong |
| 3 | Inconsistent spellings | Gender: 12 spellings, Country: 23 labels, Category: 17 labels | Mapped to standard names with mapping dictionaries: Gender 2 values (Male, Female), Country 6 countries, Category 5 categories. No new missing values (Gender missing count unchanged at 174) | The same value was counted as several categories, which would split any grouping. `Woman`/`woman` was mapped to `Female` because the data has no `Man` label, so it is the same group written differently |
| 4 | Exact duplicate rows | 20 (0.4%) | Removed with `drop_duplicates()`. 5,020 -> 5,000 rows. `Order_ID` is now unique | In Step 1 the number of duplicate rows equaled the number of repeated `Order_ID` values, so every repeat was a full copy of another row |

## Planned (not done yet)

Each item moves to the table above when it is done, with its row count, action and reason.

| # | Issue | Planned action |
|---|-------|----------------|
| 5 | Impossible values (Age, Quantity, Discount, Customer_Rating, Delivery_Days) | Decide per column: set to missing or remove rows |
| 6 | Missing values in 10 columns | Decide column by column (leave, fill with "Unknown", or recover from other columns) |
| 7 | Cancelled orders with ratings and delivery days | Decide: set to missing or keep and document |
| 8 | `Returned` duplicates `Order_Status` | Decide which column to keep |
| 9 | `Customer_ID` not consistent with name, age, gender | Cannot be fixed; document as a limitation |          