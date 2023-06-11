from db_config.db_setup import RawContent, CrawledLinks, Address, engine
from sqlalchemy.orm import sessionmaker
from postal.parser import parse_address
import pandas as pd

def extract_addresses(group):
    addresses = []
    for tag in group['tag']:
        addr = parse_address(tag)
        address = {'url_id': group.name,
                   'country': [],
                   'region': [],
                   'state': [],
                   'city': [],
                   'postcode': [],
                   'road': [],
                   'road_number': []}
        for comp in addr:
            if comp[1] in address:
                address[comp[1]].append(comp[0])

        max_len = max(len(l) for key, l in address.items() if key != 'url_id')
        for key, l in address.items():
            if key != 'url_id' and len(l) < max_len:
                address[key].extend([None] * (max_len - len(l)))

        addresses.append(pd.DataFrame.from_dict(address))

    df = pd.concat(addresses)
    df = df.dropna(how='all', subset=['country', 'region', 'state', 'city', 'postcode', 'road', 'road_number'])
    df = df.drop_duplicates()

    return df


def insert_addr():
    df = pd.read_sql_table('raw_content', engine)
    address_df = df.groupby('url_id').apply(extract_addresses)

    Session = sessionmaker(bind=engine)
    session = Session()

    for _, row in address_df.iterrows():
        data = Address(
            domain_id= session.query(CrawledLinks.domain_id).filter(CrawledLinks.id==int(row['url_id'])).first()[0],
            country=row['country'],
            region=row['region'],
            state=row['state'],
            city=row['city'],
            postcode=row['postcode'],
            road=row['road'],
            road_number=row['road_number'],
        )
        session.add(data)

    session.commit()
    session.close()
