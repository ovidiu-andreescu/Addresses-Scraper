from db_config.db_setup import Site, CrawledLinks, RawContent, engine
from sqlalchemy.orm import sessionmaker
from itemadapter import ItemAdapter


class SqlPipeline:
    def open_spider(self, spider):
        self.engine = engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        row = CrawledLinks(
            domain_id=self.session.query(Site).filter(Site.domain == adapter.get('domain')).first().id,
            page_url=adapter.get('url'),
            page_type=adapter.get('page_type'),
            http_status=adapter.get('http_status'),
        )

        self.session.add(row)
        self.session.commit()

        row = [RawContent(
            url_id=self.session.query(CrawledLinks).filter(CrawledLinks.page_url == adapter.get('url')).first().id,
            tag=content) for content in adapter.get('content')]

        self.session.add_all(row)
        self.session.commit()

        return item
