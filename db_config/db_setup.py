from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from project_config import db_path

engine = create_engine('sqlite:////' + db_path, echo=False)
Base = declarative_base()


class Site(Base):
    __tablename__ = 'site'

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String)
    # success = Column(Boolean)

    def __init__(self, domain, success):
        self.domain = domain
        # self.success = success


class CrawledLinks(Base):
    __tablename__ = 'crawled_links'

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain_id = Column(Integer, ForeignKey('site.id'))
    page_url = Column(String)
    page_type = Column(String)
    http_status = Column(Integer)

    def __init__(self, domain_id, page_url, page_type, http_status):
        self.domain_id = domain_id
        self.page_url = page_url
        self.page_type = page_type
        self.http_status = http_status

class RawContent(Base):
    __tablename__ = 'raw_content'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey('crawled_links.id'))
    tag = Column(String)

    def __init__(self, url_id, tag):
        self.url_id = url_id
        self.tag = tag

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain_id = Column(Integer, ForeignKey('site.id'))
    country = Column(String)
    region = Column(String)
    state = Column(String)
    city = Column(String)
    postcode = Column(String)
    road = Column(String)
    road_number = Column(String)

    def __init__(self, domain_id, country, region, state,  city, postcode, road, road_number):
        self.domain_id = domain_id
        self.country = country
        self.region = region
        self.state = state
        self.city = city
        self.postcode = postcode
        self.road = road
        self.road_number = road_number


def setup_db():
    Base.metadata.create_all(engine)
