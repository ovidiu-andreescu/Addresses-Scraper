from scrapeAddresses.scrapeAddresses.spiders.address_spider import AddressSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


class Scraper:
    def __init__(self):
        settings_file_path = 'scrapeAddresses.scrapeAddresses.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = AddressSpider

    def run_spiders(self):
        self.process.crawl(self.spider)
        self.process.start()
