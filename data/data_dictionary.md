# Data Dictionary

Dataset: `data/raw/ecommerce_orders_raw.csv` (5,020 rows × 28 columns; each row contains information about an order).
This dataset is synthetic.

- **Raw dtype** refers to the data type of the column (as per pandas) upon loading from the original file (obtained via `df.info()`).
- **Meaning** describes what the column represents. This may differ from the 'Raw dtype' (e.g., `Order_Date` might be stored as text, even though it represents a date).

Items marked as **(assumed)** have been inferred through data analysis; their accuracy has not been verified against any specific source.

| # | Column | Raw dtype | Meaning | Description | Values / range | Known issues |
|---|--------|-----------|---------|-------------|----------------|--------------|
| 1 | Order_ID | str | identifier | Order identifier | `ORD7xxxxx` | 20 duplicate rows |
| 2 | Order_Date | str | date | Date the order was placed | 3 formats: `YYYY-MM-DD`, `DD/MM/YYYY`, `Mon DD, YYYY` | Mixed formats; must be converted to datetime |
| 3 | Customer_ID | str | identifier | Customer identifier | `C1xxxx` | Not consistent with name, age or gender (same ID, different people) |
| 4 | Customer_Name | str | text | Customer name | 88 unique values (80 after trimming spaces) | 122 missing; 8 with extra spaces; shared across many IDs |
| 5 | Gender | str | categorical | Customer gender | Male, Female | 174 missing; 12 spellings; extra spaces in 820 rows |
| 6 | Age | float64 | whole number | Customer age in years | about 18–75 | 168 missing (float64 because of missing values); impossible values (-3 to 125) |
| 7 | Country | str | categorical | Customer country | 6 countries: Germany, France, Austria, Netherlands, Switzerland, Belgium | 23 spellings; extra spaces in 458 rows |
| 8 | Region | str | categorical | State or province | 20 values | None found |
| 9 | City | str | categorical | Customer city | 32 values | 128 missing |
| 10 | Customer_Segment | str | categorical | Customer type | Consumer, Corporate, Small Business | 128 missing |
| 11 | Product_ID | str | identifier | Product identifier | `P1001`–`P1020` | None found |
| 12 | Product_Name | str | categorical | Product name | 20 products | None found |
| 13 | Category | str | categorical | Product category | Electronics, Office, Home & Kitchen, Fashion, Sports | 17 spellings |
| 14 | Sub_Category | str | categorical | Product sub-category | 14 values | None found |
| 15 | Quantity | int64 | whole number | Units ordered | 1–5 | 3 rows with 0 or negative values |
| 16 | Unit_Price | float64 | decimal | List price per unit before discount | about 17–436 (currency not stated) | None found |
| 17 | Discount | float64 | decimal (fraction) | Discount as a fraction of the price | mostly 0–0.35 | 199 missing; 2 invalid values (-0.15, 1.4) |
| 18 | Sales | float64 | decimal | Order line revenue after discount | `Quantity × Unit_Price × (1 − Discount)` | Cannot be recomputed where inputs are missing or invalid |
| 19 | Cost | float64 | decimal | Cost **per unit** | about 7–313 | None found |
| 20 | Profit | float64 | decimal | Profit of the order line | `Sales − Quantity × Cost` | Negative values are valid losses, not errors |
| 21 | Payment_Method | str | categorical | How the customer paid | Debit Card, Credit Card, PayPal, Bank Transfer | 135 missing |
| 22 | Order_Status | str | categorical | Final status of the order | Delivered, Returned, Cancelled | Cancelled orders still have ratings and delivery days |
| 23 | Shipping_Method | str | categorical | Shipping option | Standard, Express, Pickup | None found |
| 24 | Delivery_Days | float64 | whole number | Days from order to delivery **(assumed)** | 0–10 | 202 missing (float64 because of missing values); negative values (-5) |
| 25 | Customer_Rating | float64 | decimal | Customer rating of the order, expected scale 1–5 **(assumed)** | 1.0–5.0 expected | 283 missing; values outside 1–5 (0, 7) |
| 26 | Returned | int64 | binary flag | 1 if the order was returned, else 0 | 0, 1 | Exact copy of `Order_Status = Returned` |
| 27 | Marketing_Channel | str | categorical | Channel that brought the customer | Email, Organic Search, Social Media, Affiliate, Direct, Paid Search | 132 missing |
| 28 | Device_Type | str | categorical | Device used to place the order | Desktop, Mobile, Tablet | None found |

Raw dtype summary (matches `df.info()`): float64 × 8, int64 × 2, str × 18.

## Relationships between columns

- `Sales = Quantity × Unit_Price × (1 − Discount)` holds in all rows where the inputs are valid.
- `Profit = Sales − Quantity × Cost` holds in all rows with a positive quantity.
- `Returned` is identical to `Order_Status == "Returned"`.