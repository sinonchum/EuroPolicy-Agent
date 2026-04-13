import asyncio
import logging
import os
from data_hub.scrapers.eurlex_scraper import EurLexScraper
from data_hub.parsers.formex_parser import FormexParser
from config.neo4j_manager import Neo4jManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EPA-Orchestrator")

async def main():
    logger.info("🚀 启动 EuroPolicy-Agent 集成测试...")

    # 1. 初始化模块
    scraper = EurLexScraper()
    parser = FormexParser()
    db = Neo4jManager()

    # 确保目标数据目录存在
    os.makedirs("data_hub/raw_storage", exist_ok=True)

    # 确保 Neo4j 的 Schema 已初始化
    db.setup_schema()

    # 核心目标法案
    target_celex_ids = ["32023R0956", "32023L2413"] # CBAM 和 RED III

    for celex in target_celex_ids:
        logger.info(f"===> 开始处理: {celex} <===")
        
        # 步骤 A: 抓取与下载 (考虑到 REST API 的响应，这里直接针对固定 ID 下载)
        file_path = await scraper.fetch_document_content(celex, lang="ENG")
        
        if not file_path:
            logger.error(f"❌ 下载失败，跳过: {celex}")
            continue

        # 步骤 B: 解析 XML (Formex) 提取实体
        logger.info(f"正在进行纵深语义结构解析: {file_path}")
        parsed_data = parser.parse_file(file_path)

        # 步骤 C: 图谱投喂 (Neo4j 落库)
        logger.info(f"正在将解析结果映射至知识图谱...")
        db.ingest_parsed_document(celex, parsed_data)
        
        logger.info(f"✅ {celex} 链路闭环完成。\n")

    # 步骤 D: 验证大图谱的连通性 (查询交叉引用)
    logger.info(">>> 正在统计图谱网络中建立的交叉引用脉络 <<<")
    with db.driver.session() as session:
        result = session.run("MATCH ()-[r:REFERENCES]->() RETURN count(r) as total_references")
        ref_count = result.single()["total_references"]
        logger.info(f"🎉 当前图谱中已建立的交叉引用（REFERENCES）关系总数: {ref_count}")

    db.close()
    logger.info("集测顺利结束。")

if __name__ == "__main__":
    asyncio.run(main())
