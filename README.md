# Intelligent Market Insights Platform

## Objective

This project demonstrates an enterprise-grade financial data platform built using Azure Databricks and Azure Data Lake.

The platform ingests and processes multiple financial data sources such as stock prices, financial news, and social media sentiment. It follows a lakehouse architecture with Bronze, Silver, and Gold layers and integrates Agentic AI to generate explainable market insights and stock recommendations.

## Business Problem

Investment decisions often rely on fragmented data sources such as market prices, news articles, and social media signals. These sources arrive in different formats and at different frequencies, making it difficult to create reliable and timely insights.

This project solves that problem by building a scalable lakehouse platform that unifies structured and unstructured financial data and enables AI agents to reason over market signals.

## Platform Migration Plan

The current version runs locally using CSV-based Bronze, Silver, and Gold outputs.

The next phase migrates the pipeline to Azure Databricks using:

- Azure Data Lake Gen2 for cloud storage
- Delta Lake for Bronze, Silver, and Gold tables
- Unity Catalog for governance
- Databricks Workflows for orchestration
- Azure OpenAI for LLM-based explanation generation
