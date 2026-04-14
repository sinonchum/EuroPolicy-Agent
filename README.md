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
    - [Scrapling](https://scrapling.readthedocs.io/): Adaptive web scraping framework with anti-bot bypass (Cloudflare Turnstile), stealth browsing, and JavaScript rendering. **Now replaces Firecrawl for better reliability and cost efficiency.**
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

### 4. Advanced Web Scraping with Scrapling
EPA now uses **Scrapling** for web scraping, providing:
- **Anti-bot bypass**: Automatically handles Cloudflare Turnstile and other protections
- **Stealth browsing**: Undetectable scraping with realistic browser fingerprints
- **JavaScript rendering**: Full support for modern web applications
- **Concurrent crawling**: Spider framework for large-scale data collection
- **Adaptive parsing**: Automatically adapts to website changes

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

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory with the following variables:

```env
# Required: Google Gemini API Key for AI reasoning
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Tavily AI for enhanced web search
TAVILY_API_KEY=your_tavily_api_key_here

# Optional: Jina Reader for URL-to-Markdown conversion
JINA_API_KEY=your_jina_api_key_here

# Optional: Custom model configuration
# GOOGLE_MODEL=gemini-pro
# GOOGLE_EMBEDDING_MODEL=embedding-001

# Optional: Scrapling configuration
# SCRAPLING_TIMEOUT=30
# SCRAPLING_HEADLESS=true

# Optional: Application settings
# LOG_LEVEL=INFO
# MAX_MEMORY_MB=200
```

A template is provided in `backend/.env.example`.

### Scrapling Setup
Scrapling requires browser dependencies. After installing requirements:

```bash
# Install browser dependencies
scrapling install --force
```

This will download Chromium, Firefox, and WebKit browsers for stealth scraping.

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    EuroPolicy-Agent (EPA)                   │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Next.js)  │  Backend (FastAPI)  │  Data Layer    │
│  • Bloomberg UI      │  • LangGraph Agent  │  • LanceDB     │
│  • ECharts           │  • Web Scout        │  • DuckDB      │
│  • Zustand           │  • Pulse Processor  │  • NetworkX    │
│  • i18n (4 langs)    │  • Memory Core      │  • Scrapling   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Recent Updates

### v2.0 - Scrapling Integration (Latest)
- **Replaced Firecrawl with Scrapling** for better web scraping capabilities
- Added anti-bot bypass for Cloudflare-protected sites
- Implemented stealth browsing and JavaScript rendering
- Improved error handling and fallback mechanisms
- Enhanced content extraction with AI-optimized parsing

### v1.0 - Initial Release
- LangGraph-powered reasoning engine
- Multi-language support (EN, ZH, FR, DE)
- Evolutionary memory system
- Bloomberg-style dark theme UI

---

## 👤 Author
**Simon Qin**

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Disclaimer: EPA is an alpha release. Decisions should be verified with legal experts.*