# 📋 Finance AI Agent Use Cases

## 1. Equity Research Analyst Agent
**Industry:** Finance / Investment Banking
**Description:** An agent that monitors SEC filings, earnings calls, and news to generate an autonomous "Investment Thesis" and peer comparison report.

### 🛠️ Tools Used
- **Data Source**: Yahoo Finance API / Alpha Vantage.
- **Brain**: GPT-4o / Claude 3.5 Sonnet.
- **RAG**: SEC EDGAR database crawler.

---

## 2. Fraud Investigation Agent (Compliance)
**Industry:** Finance / Banking
**Description:** Monitors transaction streams and flags suspicious behavior using a combination of deterministic rules and LLM-based reasoning for anomaly explanation.

### 🛠️ Tools Used
- **Stream**: Apache Flink / Kafka.
- **Analysis**: Custom trained LightGBM + LLM Reasoning.

---

## 3. Personal Wealth Manager Agent
**Industry:** Finance / Fintech
**Description:** Provides personalized tax-loss harvesting and portfolio rebalancing advice based on user risk profiles.

### 🛠️ Tools Used
- **Logic**: Agno (formerly Phidata) Finance Toolkit.
- **UI**: Streamlit Dashboard.
