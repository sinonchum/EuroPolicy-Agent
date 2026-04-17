import os
import logging
from neo4j import GraphDatabase

logger = logging.getLogger("EPA-Neo4j")

class Neo4jManager:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD")
        if not self.password:
            raise ValueError("NEO4J_PASSWORD environment variable is required")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def setup_schema(self):
        """
        初始化大图谱的 Schema：定义核心节点、约束及索引
        根据 FormexParser 提取出的数据结构进行量身定制。
        """
        with self.driver.session() as session:
            # 1. 唯一性约束：确保同一个 CELEX 法规不会被重复创建
            session.run("""
                CREATE CONSTRAINT unique_directive_celex IF NOT EXISTS 
                FOR (d:Directive) REQUIRE d.celex_id IS UNIQUE
            """)
            
            # 2. 唯一性约束：特定法规下的具体条款编号
            session.run("""
                CREATE CONSTRAINT unique_article_id IF NOT EXISTS 
                FOR (a:Article) REQUIRE a.article_id IS UNIQUE
            """)

            # 3. 唯一性约束：补贴 ID
            session.run("""
                CREATE CONSTRAINT unique_subsidy_id IF NOT EXISTS 
                FOR (s:Subsidy) REQUIRE s.subsidy_id IS UNIQUE
            """)

            logger.info("✅ Neo4j Schema (约束与索引) 初始化完成。")

    def ingest_parsed_document(self, celex_id: str, parsed_data: dict):
        """
        将 FormexParser 输出的字典直接落库，构建图拓扑网络。
        """
        with self.driver.session() as session:
            # 步骤 1: 创建核心法规节点 (包括通过 timeline 提取的时间锚点)
            timeline = parsed_data.get("timeline", {})
            metadata = parsed_data.get("metadata", {})
            title = metadata.get("title", "")
            
            session.run("""
                MERGE (d:Directive {celex_id: $celex})
                SET d.title = $title,
                    d.date_publication = $pub_date,
                    d.date_entry_force = $force_date
            """, celex=celex_id, title=title, 
                 pub_date=timeline.get("DATE.PUBLICATION"), 
                 force_date=timeline.get("DATE.ENTRY.FORCE"))

            # 步骤 2: 建立法规间的交叉引用脉络 (引用网络)
            references = parsed_data.get("references", [])
            for ref_celex in references:
                session.run("""
                    MATCH (source:Directive {celex_id: $source_celex})
                    MERGE (target:Directive {celex_id: $target_celex})
                    MERGE (source)-[:REFERENCES]->(target)
                """, source_celex=celex_id, target_celex=ref_celex)

            # 步骤 3: 提取并关联具体法条
            articles = parsed_data.get("articles", [])
            for art in articles:
                # 构建独立 Article ID：CELEX_ArticleNum
                art_id = f"{celex_id}_Art_{art['number']}"
                session.run("""
                    MATCH (d:Directive {celex_id: $celex})
                    MERGE (a:Article {article_id: $art_id})
                    SET a.number = $number, a.text = $text
                    MERGE (d)-[:HAS_ARTICLE]->(a)
                """, celex=celex_id, art_id=art_id, number=art['number'], text=art['text'])

            # 步骤 4: 暂时将初筛的合规义务抽象为游离节点，后续交由 Agent 处理
            obligations = parsed_data.get("obligations", [])
            for idx, obli in enumerate(obligations):
                ob_id = f"{celex_id}_Obligation_{idx}"
                session.run("""
                    MATCH (d:Directive {celex_id: $celex})
                    MERGE (o:Obligation {obligation_id: $ob_id})
                    SET o.description = $desc
                    MERGE (d)-[:CONTAINS_OBLIGATION]->(o)
                """, celex=celex_id, ob_id=ob_id, desc=obli)
                
            # 步骤 5: 攻击性模块 - 提取财务激励 (Subsidy)
            subsidies = parsed_data.get("subsidies", [])
            for idx, sub in enumerate(subsidies):
                sub_id = f"{celex_id}_Subsidy_{idx}"
                # 创建补贴节点并关联法规
                session.run("""
                    MATCH (d:Directive {celex_id: $celex})
                    MERGE (s:Subsidy {subsidy_id: $sub_id})
                    SET s.type = $type, s.amount = $amount, s.description = $desc
                    MERGE (d)-[:PROVIDES_INCENTIVE]->(s)
                """, celex=celex_id, sub_id=sub_id, 
                     type=sub.get("type", "Grant"), 
                     amount=sub.get("amount", "TBD"), 
                     desc=sub.get("description", ""))
                
                # 关联目标行业
                target_industries = sub.get("target_industries", ["General"])
                for industry in target_industries:
                    session.run("""
                        MATCH (s:Subsidy {subsidy_id: $sub_id})
                        MERGE (i:Industry {name: $industry_name})
                        MERGE (s)-[:TARGETS]->(i)
                    """, sub_id=sub_id, industry_name=industry)
                
            logger.info(f"✅ 文档 {celex_id} 已成功映射入 Neo4j 知识图谱（含财务激励模块）。")

# 实例化样例
if __name__ == "__main__":
    db = Neo4jManager()
    db.setup_schema()
    db.close()
