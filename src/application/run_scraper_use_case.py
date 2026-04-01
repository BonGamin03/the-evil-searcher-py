import os
import sys
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from infrastructure.futbolCrawler.futbolCrawler.spiders.as_spider import AsSpider
from infrastructure.futbolCrawler.futbolCrawler.spiders.marca_spider import MarcaSpider
from infrastructure.futbolCrawler.futbolCrawler.spiders.espn_spider import EspnSpider
from infrastructure.futbolCrawler.futbolCrawler.spiders.tudn_spider import TudnSpider

class RunFullScraperUseCase:
    def execute(self) -> None:
        
        src_dir = Path(__file__).resolve().parents[1]                 # .../src
        scrapy_proj_dir = src_dir / "infrastructure" / "futbolCrawler" # contiene futbolCrawler/
        sys.path.insert(0, str(scrapy_proj_dir))

        os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "futbolCrawler.settings")

        settings = Settings()
        settings.setmodule("futbolCrawler.settings", priority="project")

        process = CrawlerProcess(settings)
        process.crawl(AsSpider)
        process.crawl(MarcaSpider)
        process.crawl(EspnSpider)
        process.crawl(TudnSpider)
        process.start()  # bloquea hasta terminar