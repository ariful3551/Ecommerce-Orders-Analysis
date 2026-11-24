# Summary of Results and Recommendations

This summary answers five business questions about an e-commerce orders dataset (2023-01-01 to 2025-12-31). Details, tables and charts are in `notebooks/03_eda_visualization.ipynb` and `notebooks/04_business_questions.ipynb`.

> The data is **synthetic** (generated with ChatGPT for learning). The results describe this dataset only and are not real-world business insights.

## Scope and rules

- Raw file: 5,020 rows. After cleaning: 5,000 rows (20 duplicates removed). Cleaning decisions are in `docs/cleaning_decisions.md`.
- **Cancelled orders are excluded** from sales and profit (256 orders). The analysis uses 4,744 revenue orders.
- **Returned orders are kept**, because the data does not say whether the money was refunded.
- Total sales: 848,957. Total profit: 203,627 (margin 24.0%). Currency is not stated.
- Profit margin = profit ÷ sales.

## Results

### 1. How do sales and profit change over time?

- Sales: 286,476 (2023), 271,947 (2024, -5.1%), 290,534 (2025, +6.8%). 2025 is only 1.4% above 2023.
- Profit did not follow: 2025 profit (68,367) is 3.2% below 2023 (70,606) because the margin slipped every year: 24.6%, 23.8%, 23.5%.
- The average discount did not change over the years (0.185 to 0.186), so discounts do not explain the lower margin.
- Quarter 4 is the weakest quarter in each of the three years (three years of synthetic data are too little to call it seasonal).

### 2. Which categories and products bring the most revenue and profit?

- Electronics (33.7% of sales, profit 70,489) and Home & Kitchen (28.5%) are the largest categories.
- Robot Vacuum is the top product in both sales (130,099, 15.3%) and profit (19,748). The five biggest products bring 55.5% of all sales.
- The two biggest products have the lowest margins: Office Chair 10.9% and Robot Vacuum 15.2%. Office Chair makes 72.1% of Office sales, which largely explains why Office has the weakest category margin (18.1%).
- Sports has the best margin (47.8%) but only 3.7% of sales.

### 3. How do discounts affect quantity and profit?

- Discounts do not raise the quantity per order: the average is about 1.9 in every discount band (correlation 0.02).
- The margin falls from 36.5% (0-5% discount) to 5.8% (30-35%).
- 155 orders (3.3%) lost money. The first loss appears at an 18.5% discount; losses are rare below 25% (6 orders) and common above 30% (134 of 155, or 14.1% of orders in that band).
- Office has the highest share of loss-making orders (7.1%).

### 4. Which channels, segments and countries perform best?

- Country: Germany brings 43.5% of sales (369,311) because it has the most orders (2,076), not bigger orders.
- Segment: Consumer brings 56.4% of sales, again because of the number of orders.
- Marketing channel: the six known channels are balanced (15.7% to 16.8% of sales each). Email has the best profit and margin among them (35,035 and 24.7%).
- Margins are almost the same inside each group (countries 22.9% to 24.9%, channels 23.2% to 24.7%, segments 23.6% to 24.2%), so the differences are in volume, not in profitability.

### 5. How do shipping method and delivery time relate to rating and returns?

- Delivery time differs a lot by shipping method (Pickup 1.00 day, Express 2.49, Standard 6.03) but the average rating is almost the same (3.96 to 3.99).
- Delivery days and rating are almost unrelated (correlation -0.04).
- The return rate is 7.3% (344 orders) and stays between 6.2% and 7.9% across delivery bands. Pickup has the highest rate (9.3%), but the gap is small and could be chance.

## Recommendations

1. **Review discounts above 30%.** They give a 5.8% margin, 86.5% of all loss-making orders, and no larger orders. Test a lower maximum (for example 25%) and compare orders and margin.
2. **Review the price or cost of Office Chair and Robot Vacuum.** They bring 28.4% of sales at margins of 10.9% and 15.2%, so a small improvement has a large effect.
3. **Track margin, not only sales.** Sales recovered in 2025, but the margin fell for three years in a row.
4. **Do not pay for faster shipping to raise ratings.** In this data speed does not change the rating. Collect a return reason to find out why orders are returned.
5. **Reduce the dependence on Germany** (43.5% of sales). Consider growing the other countries, for example the Netherlands, where the average order is the highest (196.3).
6. **Do not move marketing budget between channels based on this data.** The channels are almost equal and no channel cost is available.

## Limitations

- Synthetic data, three years only.
- `Customer_ID` is not consistent with name, age and gender, so customer-level questions (such as repeat buying) are not answered. The analysis counts orders, not unique customers.
- `Age` (171), `Delivery_Days` (449) and `Customer_Rating` (522) have missing values that were kept as missing and ignored in averages.
- No data on marketing cost, shipping cost, return reasons or refunds. Recommendations that depend on them are suggestions to test, not conclusions.