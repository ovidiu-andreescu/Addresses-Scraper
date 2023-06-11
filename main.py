from db_config.db_setup import setup_db, engine
from project_config import domains
from scrapeAddresses.run_scrapy import Scraper
from utils.address_parser import insert_addr

def main():
    setup_db()

    domains.to_sql('site', con=engine, if_exists='replace', index=False)

    scraper = Scraper()
    scraper.run_spiders()

    insert_addr()

if __name__ == '__main__':
    main()
