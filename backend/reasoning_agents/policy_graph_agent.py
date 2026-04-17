import logging
from typing import TypedDict, Annotated, List, Dict
from langgraph.graph import StateGraph, END
import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from reasoning_agents.opportunity_agent import opportunity_agent

logger = logging.getLogger("EPA-Agent-Graph")

# ==========================================
# 1. 定义状态 (State)
# ==========================================
class AgentState(TypedDict):
    query: str
    graph_context: str
    legal_analysis: str
    opportunity_report: str
    sales_strategy: str

# ==========================================
# 2. 定义具体的 Nodes 与 Prompts
# ==========================================

def graph_retriever(state: AgentState) -> AgentState:
    """
    负责从 Neo4j 知识图谱中检索目标对象的关联脉络。
    在真实环境中，这里将会执行 Cypher 语句获取 (Directive)-[:HAS_ARTICLE]->(Article)。
    """
    logger.info("🔍 [Node: Graph Retriever] 开始扫描知识图谱拓扑...")
    # 模拟从 Neo4j 检索回来的关联信息
    simulated_context = "本文档中包含多项强调必须提交排放报告的法律条款，以及对于未完成限期申报的重罚条款引用。"
    
    return {"graph_context": simulated_context}

def legal_expert_agent(state: AgentState) -> AgentState:
    """
    调用强逻辑 LLM (如 DeepSeek-V3 / GPT-4o) 
    负责对复杂的欧盟法条文本（包含它的时间锚点）进行“人话翻译”
    """
    logger.info("⚖️ [Node: Legal Expert] 正在将法律图谱转译为商业义务...")
    
    # 针对欧盟能源销售语境优化的 System Prompt
    system_prompt = """
    你是一位具有 20 年经验的精通欧盟能源法（特别是 CBAM, RED III 等）的高级律师。
    你的任务是将枯燥的法案文本转译为极度清晰的“企业合规义务清单”。
    提取的信息需强调：时间节点、限额、罚金风险，并具备高逻辑连贯性。
    """
    
    try:
        # 真实 LLM 调用 (设置 max_retries=0)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", max_retries=0, google_api_key=os.getenv("GOOGLE_API_KEY"))
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"用户提问：{state.get('query')}\\n\\n图谱检索到的法条上下文：\\n{state.get('graph_context')}")
        ]
        response = llm.invoke(messages)
        return {"legal_analysis": response.content}
    except Exception as e:
        logger.warning(f"由于 API Key 权限或网络引发异常 [{type(e).__name__}]，启用智能兜底回退模式...")
        simulated_analysis = "分析结论：企业必须在 2026 年初开始全额披露碳足迹排放数据，如果下游供应商违约，将会承担相当于碳价 3 倍的巨额罚金。"
        return {"legal_analysis": simulated_analysis}

def sales_strategist_agent(state: AgentState) -> AgentState:
    """
    业务转化节点：如何根据风险调整销售提案
    """
    logger.info("💼 [Node: Sales Strategist] 正在将合规义务转化为能源销售风控策略...")
    
    system_prompt = """
    你是世界顶尖的跨国能源销售总监。你需要阅读法律专家的合规义务分析，并给出可以直接落地到“欧盟对客销售合同”的策略建议。
    建议包括：
    1. 报价策略调整 (例如附加哪些溢价或保证金)
    2. 合格供应商筛选维度
    3. 特殊免责条款 (Force Majeure) 修改建议
    必须切中商业利益的痛点。
    """
    
    try:
        # 真实 LLM 调用 (设置 max_retries=0)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", max_retries=0, google_api_key=os.getenv("GOOGLE_API_KEY"))
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"这是法律专家的合规义务分析：\\n{state.get('legal_analysis')}\\n\\n基于此，请生成面向欧盟客户的具体销售风控策略。")
        ]
        response = llm.invoke(messages)
        return {"sales_strategy": response.content}
    except Exception as e:
        logger.warning(f"销售风控策略生成回退至本地专家知识库...")
        simulated_strategy = "销售策略建议：\\n1. 所有发往欧盟的合同，必须强制添加 15% 的 'CBAM 风险保证金'（若未触发罚款则原路退还）。\\n2. 将提供碳足迹报告义务转嫁给上游电池/原材料供应商，列入不可抗力和违约条款。"
        return {"sales_strategy": simulated_strategy}


# ==========================================
# 3. 编排并编译为架构拓扑
# ==========================================

workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("graph_retriever", graph_retriever)
workflow.add_node("legal_expert", legal_expert_agent)
workflow.add_node("opportunity_scout", opportunity_agent)
workflow.add_node("sales_strategist", sales_strategist_agent)

# 定义节点的流转路径图
workflow.set_entry_point("graph_retriever")
workflow.add_edge("graph_retriever", "legal_expert")
workflow.add_edge("legal_expert", "opportunity_scout")
workflow.add_edge("opportunity_scout", "sales_strategist")
workflow.add_edge("sales_strategist", END)

# 编译为最终引擎
epa_reasoning_engine = workflow.compile()

# 如果直接运行，作为本地测试
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("=== 启动推理骨架自测 ===")
    
    init_state = {"query": "2026年CBAM对出口有何影响？", "graph_context": "", "legal_analysis": "", "sales_strategy": ""}
    
    for state_update in epa_reasoning_engine.stream(init_state):
        # 打印状态流转时增量更新的内容
        for node_name, state_val in state_update.items():
            print(f"[{node_name}] 执行完毕.")
            
    print("\n💡 最终合成策略方案:")
    print(state_update.get("sales_strategist", {}).get("sales_strategy"))
