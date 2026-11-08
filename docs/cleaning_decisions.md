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
| 5 | Impossible values | Age: 4 (-3, 0, 97, 125), Discount: 2 (-0.15, 1.4), Customer_Rating: 2 (0, 7), Delivery_Days: 1 (-5) | Set to missing | A wrong number is worse than an unknown one; the rows stay for other analysis |
| 6 | Quantity <= 0 | 3 (0, -2, -1) | Recovered with `(Sales - Profit) / Cost` -> 1, 2, 2 | `Profit = Sales - Quantity × Cost` holds in all valid rows, so the true quantity can be derived instead of deleting the rows |
| 7 | Missing `Discount` | 199 | Recovered with `1 - Sales / (Quantity × Unit_Price)`, rounded to 3 decimals. Recovered values range from 0.002 to 0.35 | `Sales` follows this formula in all valid rows. On rows with a known discount the largest error was 0.00083, so the method is reliable. Done after fixing `Quantity` and invalid discounts |
| 8 | Missing `City` | 128 | 70 filled from `Region` where the region has only one city in the data; 58 set to "Unknown" | The region fixes the city only when it has one city; the rest would be a guess. The planned questions do not use `City` |
| 9 | Missing Gender, Customer_Segment, Payment_Method, Marketing_Channel, Customer_Name | 174 / 128 / 135 / 130 / 121 | Filled with "Unknown" | No other column can recover them. About 29% of rows in the raw file (1,451 of 5,020) had at least one missing value, so deleting rows would lose too much data |
| 10 | Missing Age, Delivery_Days, Customer_Rating | 171 / 202 / 285 | Left as missing on purpose | Filling with an average would add made-up numbers; averages and other statistics ignore missing values anyway |

Note: the missing-value counts in Step 2 differ slightly from Step 1. Removing the 20 duplicates removed a few missing values, and setting impossible values to missing created new ones (Age +4, Customer_Rating +2, Discount +2, Delivery_Days +1).

## Planned (not done yet)

Each item moves to the table above when it is done, with its row count, action and reason.

| # | Issue | Planned action |
|---|-------|----------------|
| 11 | Cancelled orders with ratings and delivery days | Decide: set to missing or keep and document |
| 12 | `Returned` duplicates `Order_Status` | Decide which column to keep |
| 13 | `Customer_ID` not consistent with name, age, gender | Cannot be fixed; document as a limitation |