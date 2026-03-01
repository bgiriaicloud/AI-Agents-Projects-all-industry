# 📋 Supply Chain AI Agent Use Cases

## 1. Logistics Optimization Agent (OptiGuide)
**Industry:** Supply Chain / Logistics
**Description:** Combines real-time traffic, weather, and fuel prices with LLM reasoning to reroute thousands of shipments in response to a single major event (like a hurricane).

### 🛠️ Tools Used
- **Logic**: LangGraph (Handling branching logistical outcomes).
- **Brain**: GPT-4o.
- **Data**: Google Maps / OpenWeatherMap / MarineTraffic APIs.

---

## 2. Procurement Negotiation Bot
**Industry:** Supply Chain / Procurement
**Description:** Handles low-value, high-volume vendor negotiations for shelf-stable items, using game theory and LLM bargaining to save 3-5% on tail-spend.

### 🛠️ Tools Used
- **Logic**: Custom negotiation state machine.
- **Brain**: Claude 3.5 Sonnet (for tactical negotiation reasoning).
- **Control**: CrewAI (Agent 1: Negotiator, Agent 2: Compliance Reviewer).

---

## 3. Inventory Anomaly Detector
**Industry:** Supply Chain / Warehousing
**Description:** Identifies "ghost inventory" (discrepancies between system records and physical stock) by cross-referencing shipping receipts, sales logs, and warehouse camera feeds.

### 🛠️ Tools Used
- **Analysis**: Pandas / Scikit-learn integrated with an Agent.
- **Interface**: Tableau / PowerBI via API.
