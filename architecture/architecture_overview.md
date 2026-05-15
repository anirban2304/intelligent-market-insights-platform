# Architecture Overview

## High-Level Flow

1. Data Sources
   - Financial News (JSON/CSV)
   - Social Media Sentiment Data
   - Stock Price Data

2. Ingestion Layer (Bronze)
   - Raw data ingestion into Azure Data Lake
   - Stored as Delta tables in Bronze layer

3. Processing Layer (Silver)
   - Data cleaning and standardization
   - Schema enforcement
   - Deduplication

4. Feature Layer (Gold)
   - Aggregated datasets for analytics
   - Sentiment scores by stock
   - Daily stock performance metrics

5. Agentic AI Layer
   - Sentiment Analysis Agent
   - Market Signal Agent
   - Reasoning Agent for recommendations

6. Consumption Layer
   - Dashboard / Query interface
   - Natural language insights via AI agents

## Azure + Databricks Components

| Layer | Azure / Databricks Component | Purpose |
|---|---|---|
| Source Layer | Mock APIs / CSV / JSON files | Simulate stock prices, news, and social media data |
| Landing Zone | Azure Data Lake Gen2 | Store raw incoming files |
| Compute | Azure Databricks | Run ingestion, transformation, and AI workflows |
| Storage Format | Delta Lake | Reliable table storage with ACID transactions |
| Governance | Unity Catalog | Manage catalog, schema, table access, and lineage |
| Secret Management | Azure Key Vault | Store API keys and credentials securely |
| Orchestration | Databricks Workflows | Schedule and monitor pipelines |
| AI Layer | Azure OpenAI / LLM Framework | Build agents for sentiment, reasoning, and recommendations |
| Serving Layer | Databricks SQL / Power BI / Streamlit | Query and visualize final insights |
