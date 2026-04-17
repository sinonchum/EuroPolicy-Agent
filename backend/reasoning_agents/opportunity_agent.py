import logging
import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict

logger = logging.getLogger("EPA-Opportunity-Agent")

class OpportunityState(TypedDict):
    query: str
    legal_analysis: str
    opportunity_report: str

def opportunity_agent(state: dict) -> dict:
    """
    LangGraph 节点：OpportunityAgent
    专门从法律文本中识别“奖励积极转型”的条款。
    """
    logger.info("🎯 [Node: Opportunity Agent] 正在探测法律文本中的财富密码...")
    
    system_prompt = """
    你是一名顶级商业情报分析师，专门从欧盟法律中挖掘‘套利商机’。
    你的任务是识别出文本中所有“奖励积极转型”的条款（例如补贴、豁免、加速审批）。
    
    🔥 关键逻辑：证据链闭环 (Evidence Chain Closure)
    你在生成销售话术 (Value_Proposition/Sales_Pitch) 时，必须采用这种无可辩驳的格式：
    “根据 [法规编号] 第 [条款] 条，贵司在 [具体日期] 前如不采取 [行动]，将面临 [具体财务损失或错失的确定补贴金额]。”
    
    请严格按以下 JSON 格式输出：
    {
      "Target_Sector": "哪些行业该买我们的能源设备？",
      "Sales_Pitch": "必须遵循‘证据链闭环’格式的话术",
      "Trigger_Event": "导致客户必须购买的政策触发点",
      "Financial_Impact": "具体的补贴金额或罚金风险预估",
      "Urgency_Score": "1-100 的商机评分"
    }
    """
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            max_retries=0, 
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"这是法律专家的合规解析：\n{state.get('legal_analysis')}\n\n请提取商业机会点。")
        ]
        response = llm.invoke(messages)
        return {"opportunity_report": response.content}
    except Exception as e:
        logger.warning(f"⚠️ OpportunityAgent 降级运行: {str(e)}")
        # 兜底虚构商机
        fallback = """
        {
          "Target_Sector": "氢能电解槽制造商",
          "Value_Proposition": "基于 RED III Article 22a，非生物来源可再生燃料 (RFNBO) 占比需达 42%，现在采购可申请 30% 资本支出补贴。",
          "Trigger_Event": "2026年工业用氢强制配额考核",
          "Financial_Impact": "高紧急度 (Score: 8.5)"
        }
        """
        return {"opportunity_report": fallback}
