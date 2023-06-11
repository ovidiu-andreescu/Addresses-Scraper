import scrapy


class SqlItem(scrapy.Item):
    domain = scrapy.Field()
    url = scrapy.Field()
    page_type = scrapy.Field()
    http_status = scrapy.Field()
    content = scrapy.Field()
