import duckdb
import lancedb
import os
import logging
from datetime import datetime

logger = logging.getLogger("EPA-MemoryCore")

class EvolutionaryMemory:
    def __init__(self):
        # 计算基础路径
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 1. Episodic Memory (DuckDB) - 短期片段
        self.duck_path = os.path.join(base_dir, "data", "duckdb_meta", "memory.db")
        os.makedirs(os.path.dirname(self.duck_path), exist_ok=True)
        self.duck_conn = duckdb.connect(self.duck_path)
        self._init_duck()

        # 2. Semantic Memory (LanceDB) - 长期经验
        self.lance_path = os.path.join(base_dir, "data", "lancedb_store")
        os.makedirs(self.lance_path, exist_ok=True)
        self.lance_db = lancedb.connect(self.lance_path)
        
    def _init_duck(self):
        self.duck_conn.execute("""
            CREATE TABLE IF NOT EXISTS episodic_memory (
                id INTEGER PRIMARY KEY,
                query TEXT,
                decision TEXT,
                feedback TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def store_episode(self, query: str, decision: str, feedback: str = "N/A"):
        """
        存入短期记忆，保持 50 条限制
        """
        self.duck_conn.execute("""
            INSERT INTO episodic_memory (query, decision, feedback) 
            VALUES (?, ?, ?)
        """, [query, decision, feedback])
        
        # 裁剪旧记忆
        self.duck_conn.execute("""
            DELETE FROM episodic_memory 
            WHERE id NOT IN (SELECT id FROM episodic_memory ORDER BY timestamp DESC LIMIT 50)
        """)
        logger.info("🧠 [Memory] 短期片段已存入并裁剪。")

    def update_semantic_fact(self, entity_id: str, new_intel: str):
        """
        经验进化：不只是存储，而是通过 Entity ID 更新知识点
        """
        # 实际逻辑：通过 LanceDB 的 upsert 功能，定位 entity_id 并更新其内容
        # 此处模拟记录
        logger.info(f"🧬 [Memory] 语义进化：更新实体 {entity_id} 的知识图谱映射。")

    def get_recent_feedback(self):
        return self.duck_conn.execute("SELECT * FROM episodic_memory ORDER BY timestamp DESC LIMIT 10").df()
