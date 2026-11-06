# Cleaning Decisions

This file records every cleaning decision: what the problem was, how many rows were affected, what was done and why. The raw file (`data/raw/ecommerce_orders_raw.csv`) is never modified. All changes are made in `notebooks/02_data_cleaning.ipynb` and saved to `data/processed/ecommerce_orders_clean.csv`.

Problems come from the Step 1 summary in `notebooks/01_data_understanding.ipynb`.

## Decisions made

| # | Issue | Rows affected | Action | Why |
|---|-------|---------------|--------|-----|
| 1 | Extra leading/trailing spaces in text columns | Gender: 820, Country: 458, Customer_Name: 8 | Removed with `str.strip()` on all text columns | Values such as ` m ` and `Germany ` were counted as different categories |

## Planned (not done yet)

Each item moves to the table above when it is done, with its row count, action and reason.

| # | Issue | Planned action |
|---|-------|----------------|
| 2 | `Order_Date` stored as text in 3 formats | Parse each format separately, combine into one datetime column |
| 3 | Inconsistent spellings in Gender, Country, Category | Map to standard names (2, 6 and 5 values) |
| 4 | 20 exact duplicate rows | Remove duplicates |
| 5 | Impossible values (Age, Quantity, Discount, Customer_Rating, Delivery_Days) | Decide per column: set to missing or remove rows |
| 6 | Missing values in 10 columns | Decide column by column (leave, fill with "Unknown", or recover from other columns) |
| 7 | Cancelled orders with ratings and delivery days | Decide: set to missing or keep and document |
| 8 | `Returned` duplicates `Order_Status` | Decide which column to keep |
| 9 | `Customer_ID` not consistent with name, age, gender | Cannot be fixed; document as a limitation |