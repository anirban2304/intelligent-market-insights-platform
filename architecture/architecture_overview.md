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
