import os
import logging
import asyncio
from typing import List, Dict, Optional
from scrapling.fetchers import StealthyFetcher, StealthySession, Fetcher
from scrapling.parser import Selector

logger = logging.getLogger("EPA-ScraplingScout")

class WebScout:
    def __init__(self):
        self.scrapling_available = True
        try:
            # 测试Scrapling是否可用
            from scrapling.fetchers import Fetcher
            logger.info("🕷️ [Scrapling] 初始化成功")
        except ImportError as e:
            logger.warning(f"⚠️ [Scrapling] 不可用: {e}")
            self.scrapling_available = False

    async def hunt_intelligence(self, url: str) -> str:
        """
        使用 Scrapling 抓取网页并返回 Markdown 文本
        """
        if not self.scrapling_available:
            logger.warning("⚠️ [Scrapling] 不可用，返回模拟数据")
            return f"# Intelligence Report for {url}\\n\\nScrapling not available. Using mock data."
        
        logger.info(f"🕸️ [Scrapling] 正在抓取高价值网页: {url}")
        
        try:
            # 使用Scrapling的异步隐身抓取器
            from scrapling.fetchers import AsyncStealthySession
            
            async with AsyncStealthySession(headless=True, solve_cloudflare=True) as session:
                page = await session.fetch(
                    url,
                    google_search=False,  # 禁用Google搜索以提高速度
                    block_ads=True,  # 阻止广告
                    ai_targeted=True  # AI优化模式
                )
                
                # 提取主要内容
                content = self._extract_main_content(page)
                
                logger.info(f"✅ [Scrapling] 成功抓取: {len(content)} 字符")
                return content
            
        except Exception as e:
            logger.error(f"❌ [Scrapling] 抓取失败: {type(e).__name__}: {e}")
            # 回退到简单抓取
            try:
                from scrapling.fetchers import Fetcher
                page = Fetcher.get(url, stealthy_headers=True)
                content = self._extract_main_content(page)
                logger.info(f"✅ [Scrapling-回退] 成功抓取: {len(content)} 字符")
                return content
            except Exception as fallback_error:
                logger.error(f"❌ [Scrapling-回退] 也失败了: {fallback_error}")
                return f"# Intelligence Report for {url}\\n\\nFailed to fetch content. Error: {str(e)}"

    def _extract_main_content(self, page) -> str:
        """
        从页面提取主要内容并转换为Markdown格式
        """
        try:
            # 尝试提取文章主体内容
            main_selectors = [
                'article', '.article', '.post', '.content', '.main-content',
                'main', '#main', '#content', '.entry-content', '.post-content'
            ]
            
            content_parts = []
            
            # 尝试不同的选择器
            for selector in main_selectors:
                elements = page.css(selector)
                if elements:
                    for element in elements[:3]:  # 限制前3个元素
                        text = element.text
                        if text and len(text) > 50:  # 过滤太短的内容
                            content_parts.append(text.strip())
                    if content_parts:
                        break
            
            # 如果没找到主要内容，提取所有段落
            if not content_parts:
                paragraphs = page.css('p')
                for p in paragraphs[:10]:  # 限制前10个段落
                    text = p.text
                    if text and len(text) > 30:
                        content_parts.append(text.strip())
            
            # 如果还是没内容，提取body文本
            if not content_parts:
                body = page.css('body')
                if body:
                    content_parts.append(body[0].text[:2000])  # 限制长度
            
            # 组合内容
            if content_parts:
                content = "\n\n".join(content_parts)
                # 简单清理
                content = content.replace('\\n', '\n').replace('\\t', ' ')
                # 添加标题
                title = page.css('title')
                title_text = title[0].text if title else "Intelligence Report"
                return f"# {title_text}\n\n{content}"
            
            return "No content extracted"
            
        except Exception as e:
            logger.error(f"❌ [Scrapling] 内容提取失败: {e}")
            return f"Content extraction failed: {str(e)}"

    async def search_and_scrape(self, query: str) -> List[Dict]:
        """
        搜索并抓取的组合拳
        这里我们可以集成搜索API或直接抓取已知的欧盟政策网站
        """
        if not self.scrapling_available:
            logger.warning("⚠️ [Scrapling] 不可用，返回模拟数据")
            return [{"url": "https://eu-policy.eu", "content": "Mock content"}]
        
        logger.info(f"🔍 [Scrapling] 搜索并抓取: {query}")
        
        # 欧盟政策相关网站列表
        eu_policy_sites = [
            "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32023R0956",  # CBAM
            "https://energy.ec.europa.eu/topics/renewable-energy/renewable-energy-directive-recast_en",  # RED III
            "https://climate.ec.europa.eu/eu-action/eu-emissions-trading-system-eu-ets_en",  # EU ETS
            "https://ec.europa.eu/commission/presscorner/home/en",  # 欧委会新闻
        ]
        
        results = []
        
        try:
            # 使用Scrapling的异步会话模式抓取多个网站
            from scrapling.fetchers import AsyncStealthySession
            
            async with AsyncStealthySession(headless=True, solve_cloudflare=True) as session:
                for site_url in eu_policy_sites[:2]:  # 限制前2个站点
                    try:
                        logger.info(f"🕷️ [Scrapling] 正在抓取: {site_url}")
                        page = await session.fetch(
                            site_url,
                            google_search=False,
                            block_ads=True,
                            ai_targeted=True
                        )
                        content = self._extract_main_content(page)
                        
                        results.append({
                            "url": site_url,
                            "title": page.css('title')[0].text if page.css('title') else "EU Policy Document",
                            "content": content,
                            "source": "Scrapling"
                        })
                        
                        logger.info(f"✅ [Scrapling] 成功抓取 {site_url}: {len(content)} 字符")
                        
                    except Exception as e:
                        logger.error(f"❌ [Scrapling] 抓取失败 {site_url}: {e}")
                        continue
            
            # 如果没有成功抓取任何网站，返回模拟数据
            if not results:
                logger.info("📦 [Scrapling] 使用模拟数据")
                results = [
                    {
                        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32023R0956",
                        "title": "CBAM Regulation (EU) 2023/956",
                        "content": "# CBAM Regulation\n\nThe Carbon Border Adjustment Mechanism (CBAM) is a tool to put a fair price on the carbon emitted during the production of carbon intensive goods that are entering the EU.",
                        "source": "Mock"
                    },
                    {
                        "url": "https://energy.ec.europa.eu/topics/renewable-energy/renewable-energy-directive-recast_en",
                        "title": "Renewable Energy Directive (RED III)",
                        "content": "# Renewable Energy Directive\n\nThe revised Renewable Energy Directive (RED III) sets an increased binding target of at least 42.5% renewable energy in the EU's overall energy mix by 2030.",
                        "source": "Mock"
                    }
                ]
            
        except Exception as e:
            logger.error(f"❌ [Scrapling] 批量抓取失败: {e}")
            # 返回模拟数据
            results = [{"url": "https://eu-policy.eu", "content": "Mock content due to error"}]
        
        return results

    async def fetch_eurlex_document(self, celex: str, language: str = "ENG") -> Optional[str]:
        """
        专门用于抓取Eur-Lex文档
        """
        url = f"https://eur-lex.europa.eu/legal-content/{language}/TXT/?uri=CELEX:{celex}"
        logger.info(f"📄 [Scrapling] 抓取Eur-Lex文档: {celex} ({language})")
        
        try:
            content = await self.hunt_intelligence(url)
            return content
        except Exception as e:
            logger.error(f"❌ [Scrapling] Eur-Lex文档抓取失败: {e}")
            return None

# 测试代码
if __name__ == "__main__":
    import asyncio
    
    async def test():
        scout = WebScout()
        
        # 测试单个页面抓取
        content = await scout.hunt_intelligence("https://energy.ec.europa.eu/topics/renewable-energy/renewable-energy-directive-recast_en")
        print(f"抓取内容长度: {len(content)}")
        print(content[:200])
        
        # 测试搜索和抓取
        results = await scout.search_and_scrape("EU CBAM hydrogen subsidies 2026")
        print(f"\n搜索结果数量: {len(results)}")
        for result in results:
            print(f"- {result['title']}: {len(result['content'])} 字符")
    
    asyncio.run(test())