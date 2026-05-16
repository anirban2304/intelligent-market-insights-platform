# Databricks Migration Notes

## Bronze Table Creation

The initial stock price ingestion pipeline was migrated from local pandas-based processing to Azure Databricks.

The stock price data is fetched from yfinance, standardized into clean column names, converted into a Spark DataFrame, and written as a Delta table under Unity Catalog.

## Column Standardization

Column names from external APIs may contain spaces or special characters, such as `Adj Close`.

Before writing to Delta tables, columns are standardized into snake_case format to improve compatibility with Spark SQL, Delta Lake, and downstream transformations.

Example:

| Source Column | Standardized Column |
|---|---|
| Date | trade_date |
| Open | open_price |
| High | high_price |
| Low | low_price |
| Close | close_price |
| Adj Close | adjusted_close_price |
| Volume | volume |
