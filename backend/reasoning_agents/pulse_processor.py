import logging
from typing import List, Dict

logger = logging.getLogger("EPA-PulseProcessor")

class PulseProcessor:
    def __init__(self):
        # 情感与趋势映射
        self.sentiment_map = {
            "bullish": 1.25,   # 正面信号：提升商机分
            "neutral": 1.0,    # 中性
            "bearish": 0.75    # 负面信号：降低商机分
        }

    def analyze_signal(self, context: str) -> Dict:
        """
        利用 LLM (此处为逻辑模拟) 分析搜集到的信息。
        分类：Market_Trend, Policy_Signal, Competitor_Move
        """
        context_lower = context.lower()
        
        signal_type = "Market_Trend"
        sentiment = "neutral"
        
        # 逻辑判断 (实际应由 LLM 完成)
        if "price volatility" in context_lower or "shortage" in context_lower:
            signal_type = "Market_Trend"
            sentiment = "bearish" # 供应短缺/价格波动通常增加成本风险
        elif "budget" in context_lower or "law" in context_lower:
            signal_type = "Policy_Signal"
            sentiment = "bullish" if "increase" in context_lower else "bearish"
            
        return {
            "type": signal_type,
            "sentiment": sentiment,
            "impact_multiplier": self.sentiment_map.get(sentiment, 1.0)
        }

    def adjust_opportunity_weights(self, current_score: float, signals: List[Dict]) -> float:
        """
        动态权重修正引擎：
        New_Score = Original_Score * Avg(Signal_Impact)
        """
        if not signals:
            return current_score
            
        multipliers = [s['impact_multiplier'] for s in signals]
        avg_multiplier = sum(multipliers) / len(multipliers)
        
        new_score = current_score * avg_multiplier
        # 边界保护
        final_score = min(99.0, max(5.0, new_score))
        
        logger.info(f"📊 [Pulse Adjustment] 原分: {current_score} -> 修正分: {final_score} (系数: {avg_multiplier})")
        return round(final_score, 1)

    def generate_ticker_text(self, signal: Dict, raw_title: str) -> str:
        """
        生成前端 Ticker 使用的简讯
        """
        emoji = "📈" if signal['sentiment'] == "bullish" else "⚠️"
        return f"{emoji} [{signal['type']}] {raw_title}: Market impact detected - Adjusting opportunity calibration."
