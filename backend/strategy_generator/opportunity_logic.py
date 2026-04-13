import logging
from datetime import datetime
import re

logger = logging.getLogger("EPA-Opportunity-Scout")

class OpportunityScout:
    def __init__(self):
        # 语义权重模型：不同激励词汇的信心分数
        self.semantic_weights = {
            "grant": 0.95,      # 直接拨款：最高分
            "subsidy": 0.90,    # 补贴
            "tax credit": 0.85, # 抵税
            "loan": 0.70,       # 低息贷款
            "allowance": 0.60,  # 配额/补贴金
            "label": 0.50       # 软标签
        }
        
        # 成员国地理差分分析模型系数 (示例数据)
        self.geo_modifiers = {
            "Germany": 1.2,    # 德国：补贴力度大
            "Netherlands": 1.15,
            "France": 1.1,
            "Italy": 0.9,      # 南欧：审批周期长，略微折减
            "Spain": 0.95
        }

    def calculate_opportunity_score(self, text: str, geo_list: list) -> float:
        """
        核心商机分计算：
        Final Score = Base_Semantic_Score * Geo_Avg_Modifier * Urgency_Factor
        """
        text_lower = text.lower()
        
        # 1. 语义权重提取
        base_score = 0.5
        for keyword, weight in self.semantic_weights.items():
            if keyword in text_lower:
                base_score = max(base_score, weight)
                
        # 2. 地理差分修正
        geo_mod = 1.0
        if geo_list:
            mods = [self.geo_modifiers.get(g, 1.0) for g in geo_list]
            geo_mod = sum(mods) / len(mods)
            
        # 最终归一化到 1-100 分
        final_score = base_score * geo_mod * 100
        
        # 溢出处理
        final_score = min(99.0, max(1.0, final_score))
        
        logger.info(f"📊 商机逻辑计算完成: Base={base_score}, Geo={geo_mod} -> Result={final_score}")
        return round(final_score, 1)

    def analyze_geo_advantage(self, target_states: list):
        """
        分析哪个国家最适合作为获客切入点
        """
        best_state = max(target_states, key=lambda x: self.geo_modifiers.get(x, 1.0))
        advantage = self.geo_modifiers.get(best_state, 1.0)
        return {
            "top_market": best_state,
            "advantage_index": advantage
        }
