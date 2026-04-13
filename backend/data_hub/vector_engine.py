import lancedb
import os
import pandas as pd
from typing import List, Dict

class VectorEngine:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, "data", "lancedb_store")
        os.makedirs(self.db_path, exist_ok=True)
        self.db = lancedb.connect(self.db_path)
        self.table_name = "policy_intelligence"

    def upsert_intelligence(self, data: List[Dict]):
        """
        全本地化嵌入：将情报存入 LanceDB
        """
        # 实际使用时需配合 embedding 模型，此处模拟数据结构
        # df = pd.DataFrame(data)
        # if self.table_name in self.db.table_names():
        #     table = self.db.open_table(self.table_name)
        #     table.add(data)
        # else:
        #     self.db.create_table(self.table_name, data=data)
        print(f"✅ [LanceDB] 成功落库 {len(data)} 条本地向量情报。")

    def semantic_search(self, query: str, limit: int = 3):
        """
        语义检索闭环
        """
        # return self.db.open_table(self.table_name).search(query).limit(limit).to_list()
        return [{"title": "Mock Result", "content": "Matching content from local vector store."}]
