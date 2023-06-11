import scrapy
import tldextract

from scrapeAddresses.scrapeAddresses.items import SqlItem
from bs4 import BeautifulSoup
from project_config import domains
from scrapy.linkextractors import LinkExtractor
from project_config import nlp


class AddressSpider(scrapy.Spider):
    name = 'addressSpider'

    allowed_domains = domains['domain'].tolist()
    start_urls = list(map(lambda d: 'http://' + d, allowed_domains))

    def follow_link(self, url):
        return ('/contact' in url or '/location' in url or '/kontakt' in url) and '?' not in url

    def preprocess(self, soup):
        content = []

        for tag in soup.find_all():
            if not tag.find_all():
                tag_text = tag.get_text(strip=True)
                tag_len = len(tag_text.split(' '))
                ner_results = nlp(tag_text)

                if any(ent['entity'] == 'B-LOC' for ent in ner_results) and 2 <= tag_len <= 10:
                    content.append(tag_text)

        return content

    def parse(self, response):
        item = SqlItem()

        if 'text/html' in response.headers.get('Content-Type').decode():
            soup = BeautifulSoup(response.text, 'lxml')
            rm_tags = ['script', 'style', 'nav', 'form', 'h1', 'h2', 'h3',
                       'h4', 'h5', 'h6', 'button', 'title', 'img', 'a']

            for tag in soup(rm_tags):
                tag.decompose()

            item['content'] = self.preprocess(soup)

            extracted = tldextract.extract(response.url)
            item['domain'] = '{}.{}'.format(extracted.domain, extracted.suffix)
            item['url'] = response.url

            if '/contact' in response.url or 'kontakt' in response.url:
                item['page_type'] = 'contact'
            elif '/location' in response.url:
                item['page_type'] = 'location'
            else:
                item['page_type'] = 'home'

            item['http_status'] = response.status

            yield item

        links = LinkExtractor(allow_domains=self.allowed_domains).extract_links(response)

        for url in links:
            if not self.follow_link(url.url):
                continue

            yield response.follow(url, callback=self.parse)
