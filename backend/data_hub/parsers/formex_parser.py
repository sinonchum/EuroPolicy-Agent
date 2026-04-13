from lxml import etree
import logging
from typing import List, Dict, Optional

logger = logging.getLogger("EPA-Parser")

class FormexParser:
    def __init__(self):
        # 定义 Formex 常用的命名空间（根据实际文档可能需要调整）
        self.ns = {'f': 'http://publications.europa.eu/celex'} 

    def parse_file(self, file_path: str) -> Dict:
        """解析本地 Formex XML 文件并提取结构化法律实体"""
        try:
            tree = etree.parse(file_path)
            root = tree.getroot()
            
            return {
                "metadata": self._extract_metadata(root),
                "articles": self._extract_articles(root),
                "obligations": self._identify_obligations(root),
                "references": self._extract_references(root),
                "timeline": self._extract_timeline(root)
            }
        except Exception as e:
            logger.error(f"解析失败 {file_path}: {e}")
            return {}

    def _extract_metadata(self, root) -> Dict:
        """提取基础元数据"""
        # 注意: 实际 xpath 可能需要根据对应的 Formex 文档架构调整
        return {
            "title": root.xpath("string(//TITLE)"),
            # 可以在此添加更多元数据提取逻辑
        }

    def _extract_articles(self, root) -> List[Dict]:
        """提取所有条款内容"""
        articles = []
        # Formex 中条款通常由 <ARTICLE> 标签标识
        for art in root.xpath("//ARTICLE"):
            num = art.xpath("string(TI.ART)")
            content = art.xpath("string(PARAG)")
            articles.append({"number": num, "text": content.strip()})
        return articles

    def _identify_obligations(self, root) -> List[str]:
        """
        初步提取：寻找带有强烈义务色彩的段落
        2026 策略：这里先做结构化提取，后续交给 reasoning_agents 进行 NLP 判定
        """
        # 寻找包含 "shall", "must", "is required to" 等关键词的段落
        keywords = ["shall", "must", "required", "obligation", "deadline"]
        obligations = []
        for parag in root.xpath("//PARAG"):
            text = parag.xpath("string(.)").lower()
            if any(k in text for k in keywords):
                obligations.append(text.strip())
        return obligations

    def _extract_references(self, root) -> List[str]:
        """提取条款交叉引用"""
        references = []
        # <REF.DOC.CELEX> 通常包含被引用法律的 CELEX ID
        for ref in root.xpath("//REF.DOC.CELEX"):
            ref_text = ref.xpath("string(.)").strip()
            if ref_text:
                references.append(ref_text)
        return list(set(references)) # 去重

    def _extract_timeline(self, root) -> Dict[str, str]:
        """提取关键时间轴的节点"""
        timeline = {}
        # 常见日期节点，如发布日期、生效日期等
        date_nodes = ["DATE.PUBLICATION", "DATE.ENTRY.FORCE"]
        for node_name in date_nodes:
            # 找到对应节点并获取文本（日期通常存储在节点内或属性中）
            nodes = root.xpath(f"//{node_name}")
            if nodes:
                timeline[node_name] = nodes[0].xpath("string(.)").strip()
        return timeline
