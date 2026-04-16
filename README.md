# EuroPolicy-Agent (EPA) 🇪🇺🤖

> **Transforming EU Regulatory Complexity into Actionable Business Intelligence.**

Developed by **Simon Qin**, EPA is an AI-driven intelligence terminal that helps energy companies navigate EU policy changes (RED III, CBAM) and convert regulatory shifts into concrete sales opportunities.

---

## 🏛️ What It Does

EPA doesn't just summarize laws. It:

- **Scrapes** EU regulatory sources (Eur-Lex, EC energy pages) in real time
- **Reasons** through a multi-agent pipeline: legal analysis → opportunity extraction → sales strategy generation
- **Scores** opportunities with urgency ratings and financial impact estimates
- **Generates** evidence-backed sales pitches ("According to [Regulation] Art. [X], failure to act by [date] risks [amount]...")
- **Adapts** across 4 languages (EN, ZH, FR, DE) with market-specific output

---

## 🚀 Architecture

```
┌──────────────────────────────────────────────────┐
│  Frontend (Next.js)  │  Backend (FastAPI)        │
│  • Bloomberg Dark UI │  • LangGraph Agent Chain  │
│  • ECharts Radars    │  • Web Scraping (Scrapling)│
│  • i18n (4 langs)    │  • Evolutionary Memory    │
│  • Zustand Store     │  • Pulse Processor        │
├──────────────────────┴───────────────────────────┤
│  Storage: LanceDB + DuckDB + NetworkX            │
│  (Zero external DB servers required)             │
└──────────────────────────────────────────────────┘
```

---

## ⚡ Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
scrapling install --force   # browser deps for web scraping
python main.py              # → http://localhost:8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --turbo      # → http://localhost:3000
```

### Configuration

Create `backend/.env`:

```env
GOOGLE_API_KEY=your_key       # Required: Google Gemini API key
TAVILY_API_KEY=your_key       # Optional: enhanced web search
JINA_API_KEY=your_key         # Optional: URL-to-Markdown
```

---

## 🧠 Agent Pipeline

Each query flows through 4 reasoning nodes:

1. **Graph Retriever** — pulls relevant policy context from the knowledge graph
2. **Legal Expert** — translates dense regulation text into clear compliance obligations
3. **Opportunity Scout** — identifies subsidy windows, financial incentives, and urgency scores
4. **Sales Strategist** — generates contract-ready sales strategies and pricing adjustments

---

## 📡 Key APIs

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/opportunities` | GET | Run the full reasoning pipeline. Params: `lang`, `geo`, `sector`, `query` |
| `/api/v1/sync-global-pulse` | POST | Trigger background news sync + evolution cycle |
| `/api/v1/status` | GET | System health and memory usage |
| `/api/v1/agent-evolution-status` | GET | Evolutionary memory stats |
| `/api/v1/debug/pipeline` | GET | Raw pipeline output for debugging |

---

## ⚠️ Alpha Release

EPA is under active development. Regulatory interpretations should be verified with legal experts before making business decisions.

---

**Author:** Simon Qin | **License:** MIT
