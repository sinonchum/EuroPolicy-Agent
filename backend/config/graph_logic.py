import networkx as nx
import logging
import os

logger = logging.getLogger("EPA-GraphLogic")

class GraphEngine:
    def __init__(self, mode="local"):
        self.mode = mode # 'local' for NetworkX, 'remote' for Neo4j
        if self.mode == "local":
            self.graph = nx.DiGraph()
            logger.info("🕸️ [NetworkX] 启动本地轻量化图逻辑引擎。")
        else:
            # 此处可保留之前的 Neo4jManager 调用逻辑
            pass

    def add_policy_link(self, source: str, target: str, rel_type: str):
        """
        添加法律引用链接
        """
        if self.mode == "local":
            self.graph.add_edge(source, target, relationship=rel_type)
            logger.info(f"🔗 [Graph] 已建立引用: {source} -> {target}")

    def query_cross_references(self, node_id: str):
        """
        查询交叉引用拓扑
        """
        if self.mode == "local":
            return list(self.graph.successors(node_id)) if node_id in self.graph else []
        return []
