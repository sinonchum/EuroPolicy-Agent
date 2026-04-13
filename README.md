# EuroPolicy-Agent (EPA) 🇪🇺🤖

> **Transforming EU Regulatory Complexity into Actionable Business Intelligence.**

Developed by **Simon Qin**, EuroPolicy-Agent (EPA) is a high-performance, AI-driven intelligence terminal designed to help energy companies navigate and capitalize on the chaotic landscape of EU policy changes (e.g., RED III, CBAM).

---

## 🏛️ Purpose
The primary goal of EPA is to provide **Aggressive Lead Generation** based on regulatory shifts. It doesn't just "summarize" laws; it calculates ROI, identifies specific subsidy windows, and generates high-authority sales pitches with "Evidence Chain Closure."

## 🚀 "Zero-Ops" Lightweight Architecture
Designed for the modern local-first workflow, EPA features a highly RAM-Optimized architecture, running entirely without external database servers.

### Core Stack & Attributions
EPA is built on the shoulders of these incredible open-source projects:

- **Storage (Zero-Ops Layer)**:
    - [LanceDB](https://lancedb.com/): Embedded vector database for zero-config semantic search.
    - [DuckDB](https://duckdb.org/): Analytical database for weights history and episodic memory.
    - [NetworkX](https://networkx.org/): Lightweight in-memory graph for policy cross-referencing.
- **Intelligence & Scrapping**:
    - [Firecrawl](https://www.firecrawl.dev/): Transforming complex web data into LLM-ready Markdown.
    - [Jina Reader](https://jina.ai/reader/): Lightning-fast URL-to-Markdown conversion.
    - [Tavily AI](https://tavily.com/): Specialized search for high-signal energy market pulse.
- **Frontend (Bloomberg Intelligence Style)**:
    - [Next.js](https://nextjs.org/): Turbo-charged React framework.
    - [Apache ECharts](https://echarts.apache.org/): High-density financial data visualization.
    - [Zustand](https://github.com/pmndrs/zustand): Ultra-lean state management.
    - [Lucide React](https://lucide.dev/): Consistent professional iconography.
    - [Tailwind CSS](https://tailwindcss.com/): High-impact dark theme aesthetics.

---

## ✨ Key Features

### 1. Global Energy Market Pulse (GEP)
Autonomous "hunting" for external news (Market Trends, Policy Shifts) that dynamically adjusts the **Opportunity Score** of internal policy nodes. 

### 2. Evolutionary Memory
Inspired by **Mem0**, EPA features:
- **Episodic Memory**: Tracks the last 50 decisions and search results.
- **Semantic Memory**: Automatically updates entity facts when cleaner intel is discovered.

### 3. Bloomberg-Style Multi-Language UI
A high-density, mission-critical dashboard supporting **English, Simplified Chinese, French, and German**. Switching languages re-triggers AI-based sales pitch generation synchronized for the target market.

---

## 🛠️ Quick Start

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
python main.py
```
*Port 8000. Memory target: < 200MB.*

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev -- --turbo
```
*Port 3000. Features Bloomberg Dark theme + i18n.*

---

## 👤 Author
**Simon Qin**
*Specialist in Agentic Workflows & Regulatory Intelligence.*

---
*Disclaimer: EPA is an alpha release. Decisions should be verified with legal experts.*
