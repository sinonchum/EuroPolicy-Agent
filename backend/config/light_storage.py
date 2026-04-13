import lancedb
import networkx as nx
import os
import logging

logger = logging.getLogger("EPA-LightStorage")

class LightStorage:
    def __init__(self):
        # 1. 初始化 LanceDB (本地文件模式)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, "data", "lancedb_store")
        os.makedirs(self.db_path, exist_ok=True)
        self.vector_db = lancedb.connect(self.db_path)
        
        # 2. 初始化内存图 (NetworkX)
        self.policy_graph = nx.DiGraph()
        logger.info("⚡ [LightStorage] 内存图与本地向量库已就绪，Neo4j 依赖已移除。")

    def sync_to_disk(self):
        """
        此处可以添加将内存图序列化到本地文件的逻辑，保持零运维特性。
        """
        pass

    def add_reference(self, source_celex: str, target_celex: str):
        self.policy_graph.add_edge(source_celex, target_celex, type="REFERENCES")
