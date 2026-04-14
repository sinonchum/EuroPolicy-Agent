import gc
import json
import logging
import os
import re
import sys
import asyncio
from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

# 系统路径配置
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 核心组件导入
from config.light_storage import LightStorage
from cross_lingual_engine.embeddings import RemoteEmbeddings
from i18n_resources import get_localized_value, OPPORTUNITY_TRANSLATIONS, OPPORTUNITY_QUERIES
from data_hub.web_scout import WebScout
from reasoning_agents.pulse_processor import PulseProcessor
from data_hub.memory_core import EvolutionaryMemory
from reasoning_agents.evolution_loop import EvolutionLoop

# LangGraph 推理引擎
try:
    from reasoning_agents.policy_graph_agent import epa_reasoning_engine
    REASONING_ENGINE_AVAILABLE = True
    logger_init = logging.getLogger("EPA-Init")
    logger_init.info("✅ LangGraph 推理引擎已加载。")
except ImportError as e:
    REASONING_ENGINE_AVAILABLE = False
    logger_init = logging.getLogger("EPA-Init")
    logger_init.warning(f"⚠️ LangGraph 推理引擎不可用: {e}，将使用 mock 数据。")

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


def parse_opportunity_report(raw_text: str) -> list[dict]:
    """
    将 LLM 输出（可能含 JSON 或自然语言）解析为结构化商机列表。
    兼容三种格式：
      1. 纯 JSON
      2. ```json ... ``` 代码块
      3. 自然语言 → 提取关键字段生成兜底卡片
    """
    if not raw_text:
        return []

    text = raw_text.strip()

    # 尝试 1: 直接 JSON 解析
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return [data]
    except (json.JSONDecodeError, ValueError):
        pass

    # 尝试 2: 从 markdown 代码块提取 JSON
    json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1).strip())
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                return [data]
        except (json.JSONDecodeError, ValueError):
            pass

    # 尝试 3: 提取 JSON 对象块（以 { 开头）
    obj_match = re.search(r'\{[^{}]*(?:"Target_Sector"|"Sales_Pitch"|"target_sector")[^{}]*\}', text, re.DOTALL)
    if obj_match:
        try:
            data = json.loads(obj_match.group(0))
            return [data]
        except (json.JSONDecodeError, ValueError):
            pass

    # 兜底: 将整个文本作为单个商机的描述
    return [{"raw_text": text}]


def normalize_opportunity(raw: dict, opp_id: str, lang: str) -> dict:
    """
    将 LLM 输出的任意格式统一为前端需要的 Opportunity Card 格式。
    """
    # 提取标题
    title = (
        raw.get("title")
        or raw.get("Title")
        or raw.get("Target_Sector", "")
    )
    if not title and raw.get("raw_text"):
        # 截取前 60 字符作为标题
        title = raw["raw_text"][:60].replace("\n", " ") + "..."

    # 提取分数
    score_raw = raw.get("score") or raw.get("Urgency_Score") or raw.get("urgency_score", 75)
    if isinstance(score_raw, str):
        # "8.5" → 85, "High (Score: 8.5)" → 85
        nums = re.findall(r'[\d.]+', score_raw)
        score_raw = float(nums[0]) if nums else 7.5
        if score_raw <= 10:
            score_raw = score_raw * 10
    score = round(float(score_raw) * market_context["global_multiplier"], 1)

    # 提取行业
    target_sector = (
        raw.get("target_sector")
        or raw.get("Target_Sector")
        or get_localized_value("Heavy Industry", lang)
    )

    # 提取补贴类型
    subsidy_type = (
        raw.get("subsidy_type")
        or raw.get("Financial_Impact")
        or get_localized_value("Capital Grant", lang)
    )

    # 提取销售话术
    sales_pitch = (
        raw.get("sales_pitch")
        or raw.get("Sales_Pitch")
        or raw.get("Value_Proposition")
        or raw.get("raw_text", "")
    )

    # 提取触发事件
    trigger = raw.get("Trigger_Event") or raw.get("trigger_event", "")

    # 提取地理焦点
    geo_focus = raw.get("geo_focus") or raw.get("geo", ["EU"])

    # 紧急度
    if score >= 85:
        urgency_key = "urgency_high"
    elif score >= 60:
        urgency_key = "urgency_medium"
    else:
        urgency_key = "urgency_low"
    urgency = get_localized_value(urgency_key, lang)

    return {
        "id": opp_id,
        "title": title,
        "score": score,
        "target_sector": target_sector,
        "subsidy_type": subsidy_type,
        "geo_focus": geo_focus if isinstance(geo_focus, list) else [geo_focus],
        "sales_pitch": sales_pitch,
        "urgency": urgency,
        "trigger_event": trigger,
    }


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
    sector: str = Query(None),
    query: str = Query(None, description="自定义分析查询，留空则使用语言默认查询"),
):
    """
    获客雷达 API：接入 LangGraph 推理引擎，从法规文本中提取真实商机。
    支持多语言、自定义查询、区域/行业过滤。
    """
    logger.info(f"🚀 [API] Request: Lang={lang}, Geo={geo}, Sector={sector}, Query={query}")

    # 决定使用哪个查询
    user_query = query or OPPORTUNITY_QUERIES.get(lang, OPPORTUNITY_QUERIES["en"])

    opportunities = []

    if REASONING_ENGINE_AVAILABLE:
        try:
            logger.info(f"🧠 [LangGraph] 启动推理管线，查询: {user_query[:80]}...")

            init_state = {
                "query": user_query,
                "graph_context": "",
                "legal_analysis": "",
                "opportunity_report": "",
                "sales_strategy": "",
            }

            # 运行 LangGraph 推理管线
            final_state = {}
            for state_update in epa_reasoning_engine.stream(init_state):
                for node_name, node_state in state_update.items():
                    if isinstance(node_state, dict):
                        final_state.update(node_state)
                    logger.info(f"  ⚙️ [Node: {node_name}] 执行完毕")

            # 解析 Opportunity Agent 输出
            raw_report = final_state.get("opportunity_report", "")
            raw_items = parse_opportunity_report(raw_report)

            # 解析 Sales Strategist 输出
            sales_strategy = final_state.get("sales_strategy", "")

            # 构造结构化商机卡片
            for idx, raw_item in enumerate(raw_items):
                opp_id = f"EPA_{idx + 1:03d}"
                normalized = normalize_opportunity(raw_item, opp_id, lang)

                # 如果 LLM 没给出具体话术，用 sales_strategy 填充
                if not normalized["sales_pitch"] and sales_strategy:
                    normalized["sales_pitch"] = sales_strategy[:200].replace("\\n", " ").replace("\n", " ")

                # 清理文本中的转义字符
                for key in ("sales_pitch", "title", "trigger_event"):
                    if normalized.get(key):
                        normalized[key] = normalized[key].replace("\\n", " ").replace("\\t", " ").strip()

                opportunities.append(normalized)

            logger.info(f"✅ [LangGraph] 推理完成，生成 {len(opportunities)} 个商机。")

        except Exception as e:
            logger.error(f"❌ [LangGraph] 推理异常: {type(e).__name__}: {e}")
            import traceback
            logger.error(traceback.format_exc())

    # 副作用: 记忆存储 + 乘数更新 (不阻塞主流程)
    if opportunities:
        try:
            memory.store_episode(user_query, str(raw_items[:2]), "LangGraph_Run")
        except Exception as e:
            logger.warning(f"⚠️ 记忆存储失败 (非致命): {e}")

        try:
            top_score = max(o["score"] for o in opportunities)
            market_context["global_multiplier"] = round(top_score / 85.0, 2)
        except Exception:
            pass

    # 兜底: 如果推理引擎不可用或无结果，使用 mock 数据
    if not opportunities:
        logger.info("📦 [Mock] 使用内置模拟数据。")
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

        opportunities = [
            {
                "id": "OPP_01",
                "title": titles.get(lang, titles["en"])[0],
                "score": round(95.5 * market_context["global_multiplier"], 1),
                "target_sector": get_localized_value("Hydropower", lang),
                "subsidy_type": get_localized_value("Capital Grant", lang),
                "geo_focus": ["Germany", "Netherlands"],
                "sales_pitch": pitches.get(lang, pitches["en"])[0],
                "urgency": get_localized_value("urgency_high", lang),
            },
            {
                "id": "OPP_02",
                "title": titles.get(lang, titles["en"])[1],
                "score": round(78.0 * market_context["global_multiplier"], 1),
                "target_sector": get_localized_value("Heavy Industry", lang),
                "subsidy_type": get_localized_value("Tax Exemption", lang),
                "geo_focus": ["France", "Spain"],
                "sales_pitch": pitches.get(lang, pitches["en"])[1],
                "urgency": get_localized_value("urgency_medium", lang),
            }
        ]

    # 过滤逻辑
    if geo:
        opportunities = [o for o in opportunities if any(geo.lower() in g.lower() for g in o.get("geo_focus", []))]
    if sector:
        opportunities = [o for o in opportunities if sector.lower() in o.get("target_sector", "").lower()]

    return {
        "opportunities": opportunities,
        "pulse_ticker": market_context["latest_news"][:3],
        "engine": "langgraph" if REASONING_ENGINE_AVAILABLE else "mock",
        "query_used": user_query,
    }

@app.get("/api/v1/debug/pipeline")
async def debug_pipeline(query: str = Query("EU CBAM hydrogen subsidies 2026")):
    """
    Debug 端点：直接运行 LangGraph 管线并返回完整中间状态，不做任何兜底。
    """
    if not REASONING_ENGINE_AVAILABLE:
        return {"error": "LangGraph engine not available"}

    init_state = {
        "query": query,
        "graph_context": "",
        "legal_analysis": "",
        "opportunity_report": "",
        "sales_strategy": "",
    }

    final_state = {}
    node_trace = []
    for state_update in epa_reasoning_engine.stream(init_state):
        for node_name, node_state in state_update.items():
            if isinstance(node_state, dict):
                final_state.update(node_state)
            node_trace.append(node_name)

    raw_report = final_state.get("opportunity_report", "")
    parsed = parse_opportunity_report(raw_report)

    return {
        "node_trace": node_trace,
        "graph_context": final_state.get("graph_context", ""),
        "legal_analysis": final_state.get("legal_analysis", ""),
        "opportunity_report_raw": raw_report,
        "opportunity_report_parsed": parsed,
        "sales_strategy": final_state.get("sales_strategy", ""),
    }

@app.post("/api/v1/sync-global-pulse")
async def sync_pulse(query: str = Query("EU Energy Policy 2026")):
    """
    触发后台同步：抓取新闻 + 存入记忆 + 运行进化循环。
    附带可选的 LangGraph 深度分析。
    """
    async def process_sync():
        try:
            # 1. 搜索能源趋势新闻
            raw_news = await web_scout.search_and_scrape(query)

            # 2. 分析每条新闻的信号
            for news in raw_news:
                title = news.get("title", "Untitled")
                signal = pulse_proc.analyze_signal(title)
                ticker_text = pulse_proc.generate_ticker_text(signal, title)
                memory.store_episode(query, title, signal["sentiment"])
                market_context["latest_news"].append(ticker_text)

            # 3. 只保留最近 20 条新闻
            market_context["latest_news"] = market_context["latest_news"][-20:]

            # 4. 根据信号调整全局乘数
            if raw_news:
                signals = [pulse_proc.analyze_signal(n.get("title", "")) for n in raw_news]
                multipliers = [s["impact_multiplier"] for s in signals]
                avg = sum(multipliers) / len(multipliers)
                market_context["global_multiplier"] = round(
                    max(0.5, min(2.0, avg)), 2
                )

            # 5. 运行进化循环
            await evolver.run_evolution_cycle()

            logger.info(f"✅ [Sync] 脉冲同步完成，新闻 {len(raw_news)} 条，乘数 {market_context['global_multiplier']}")

        except Exception as e:
            logger.error(f"❌ [Sync] 同步异常: {type(e).__name__}: {e}")
        finally:
            gc.collect()

    asyncio.create_task(process_sync())
    return {
        "status": "Sync triggered",
        "query": query,
        "engine": "langgraph" if REASONING_ENGINE_AVAILABLE else "mock",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
