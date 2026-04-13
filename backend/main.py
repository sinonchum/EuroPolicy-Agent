import gc
import logging
import os
import sys
import asyncio
from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

# 系统路径配置
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 核心组件导入
from config.light_storage import LightStorage
from cross_lingual_engine.embeddings import RemoteEmbeddings
from i18n_resources import get_localized_value, OPPORTUNITY_TRANSLATIONS
from data_hub.web_scout import WebScout
from reasoning_agents.pulse_processor import PulseProcessor
from data_hub.memory_core import EvolutionaryMemory
from reasoning_agents.evolution_loop import EvolutionLoop

# 初始化日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EPA-Unified-Backend")

app = FastAPI(title="EuroPolicy Agent (Evolving & Optimized)", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 核心引擎实例化 (RAM-Friendly)
storage = LightStorage()
embedder = RemoteEmbeddings()
web_scout = WebScout()
pulse_proc = PulseProcessor()
memory = EvolutionaryMemory()
evolver = EvolutionLoop(memory)

market_context = {"global_multiplier": 1.0, "latest_news": []}

@app.middleware("http")
async def memory_management_middleware(request, call_next):
    response = await call_next(request)
    gc.collect() 
    return response

@app.get("/api/v1/status")
async def get_status():
    import psutil
    process = psutil.Process(os.getpid())
    return {
        "status": "Running",
        "memory_mb": round(process.memory_info().rss / 1024 / 1024, 2),
        "evolution_engine": "Active",
        "optimization": "Lightweight / RAM-Optimized"
    }

@app.get("/api/v1/agent-evolution-status")
async def get_evolution_status():
    return evolver.get_evolution_summary()

@app.get("/api/v1/opportunities")
async def get_opportunities(
    lang: str = Query("en"),
    geo: str = Query(None),
    sector: str = Query(None)
):
    """
    获客雷达 API：支持多语言与区域/行业过滤
    """
    logger.info(f"🚀 [API] Request: Lang={lang}, Geo={geo}, Sector={sector}")
    
    # 构建高保真模拟数据
    titles = {
        "en": ["RED III Hydrogen Subsidy Alert", "CBAM Steel Export Opportunity"],
        "zh": ["RED III 氢能补贴预警", "CBAM 钢铁出口商机"],
        "fr": ["Alerte Subvention Hydrogène RÉD III", "Opportunité Exportation Acier CBAM"],
        "de": ["RED III Wasserstoff-Förderalarm", "CBAM Stahl-Exportgelegenheit"]
    }
    
    pitches = {
        "en": ["According to RED III Art. 22a, avoid loss...", "Leverage green premiums..."],
        "zh": ["根据第15条指令，避免损失...", "利用绿色溢价..."],
        "fr": ["Selon l'Art. 15, évitez la perte...", "Utilisez les primes vertes..."],
        "de": ["Gemäß Art. 15: Jetzt handeln...", "Nutzen Sie grüne Prämien..."]
    }

    mock_opps = [
        {
            "id": "OPP_01",
            "title": titles.get(lang, titles["en"])[0],
            "score": round(95.5 * market_context["global_multiplier"], 1),
            "target_sector": get_localized_value("Hydropower", lang),
            "subsidy_type": get_localized_value("Capital Grant", lang),
            "geo_focus": ["Germany", "Netherlands"],
            "sales_pitch": pitches.get(lang, pitches["en"])[0],
            "urgency": get_localized_value("urgency_high", lang)
        },
        {
            "id": "OPP_02",
            "title": titles.get(lang, titles["en"])[1],
            "score": round(78.0 * market_context["global_multiplier"], 1),
            "target_sector": get_localized_value("Heavy Industry", lang),
            "subsidy_type": get_localized_value("Tax Exemption", lang),
            "geo_focus": ["France", "Spain"],
            "sales_pitch": pitches.get(lang, pitches["en"])[1],
            "urgency": get_localized_value("urgency_medium", lang)
        }
    ]

    # 过滤逻辑
    if geo:
        mock_opps = [o for o in mock_opps if any(geo.lower() in g.lower() for g in o['geo_focus'])]
    if sector:
        mock_opps = [o for o in mock_opps if sector.lower() in o['target_sector'].lower()]

    return {"opportunities": mock_opps, "pulse_ticker": market_context["latest_news"][:3]}

@app.post("/api/v1/sync-global-pulse")
async def sync_pulse(query: str = "EU Grid Market 2026"):
    async def process_sync():
        raw_news = await web_scout.search_energy_trends(query)
        for news in raw_news:
             memory.store_episode(query, news['title'], "Sync")
        await evolver.run_evolution_cycle()
        gc.collect()

    asyncio.create_task(process_sync())
    return {"status": "Sync triggered"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
