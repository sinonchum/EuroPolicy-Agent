import duckdb
import os

class MetaDB:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, "data", "duckdb_meta", "opportunity_stats.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = duckdb.connect(self.db_path)
        self._init_tables()

    def _init_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS weights_history (
                opportunity_id VARCHAR,
                original_score DOUBLE,
                adjusted_score DOUBLE,
                multiplier DOUBLE,
                reason VARCHAR,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def log_weight_change(self, opp_id: str, orig: float, adj: float, mult: float, reason: str):
        """
        使用 DuckDB 快速持久化分数变动趋势
        """
        self.conn.execute("""
            INSERT INTO weights_history (opportunity_id, original_score, adjusted_score, multiplier, reason)
            VALUES (?, ?, ?, ?, ?)
        """, [opp_id, orig, adj, mult, reason])
        print(f"📊 [DuckDB] 已记录商机 {opp_id} 的权重演变。")

    def get_analysis_trends(self):
        """
        全量分析商机波动
        """
        return self.conn.execute("SELECT * FROM weights_history ORDER BY timestamp DESC LIMIT 5").df()
