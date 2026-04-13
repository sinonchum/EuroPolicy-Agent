import httpx
import os
import logging
from typing import List

logger = logging.getLogger("EPA-RemoteEmbeddings")

class RemoteEmbeddings:
    def __init__(self):
        self.api_key = os.getenv("EMBEDDING_API_KEY") # 可支持 OpenAI 或 DeepSeek
        self.api_url = "https://api.openai.com/v1/embeddings" # 示例端点
        self.model = "text-embedding-3-small"

    async def get_embedding(self, text: str) -> List[float]:
        """
        API 优先：禁止加载本地模型文件
        """
        if not self.api_key:
            logger.warning("⚠️ 无 API KEY，返回全零向量（仅用于调试）")
            return [0.0] * 1536

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.api_url,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"input": text, "model": self.model},
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()["data"][0]["embedding"]
            except Exception as e:
                logger.error(f"❌ Embedding API 获取失败: {str(e)}")
                return [0.0] * 1536
