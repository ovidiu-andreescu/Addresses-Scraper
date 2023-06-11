# Documentation

The goal of the following program is to extract a list of domains from a 'parquet' file, crawl through the URLs found and extract the physical addresses that might be found.

For data and impressions on the project see the jupyer notebook. The .md and .ipynb were written with jupyter lab.
# Languages

#### __Python__

# Libraries

#### __pandas__ - read the 'parquet' file, process the data
#### __SQLAlchemy__ - manage storage for scraped data, processsed data, SQLite
#### __Scrapy__ - crawl and scrape the websites
#### __bs4__ - extract the html content
#### __transformers__ - extract the potential addresses from the scraped pages
#### __libpostal/pypostal__ - extract address components such as country, region, road, road number

# Structure of the project

The project has multiple modules such as: db_config, scrapeAddresses, util:

    - db_config
        ~ db_setup.py: database and tables intitialisation

    - scrapeAddresses
        - scrapeAddresses
            - spiders
                ~ address_spider.py: spider crawler, how it receives the data from the websites
            ~ items.py: structure of the parsed data
            ~ pipelines.py: sends the data to the database
            ~ middlewares.py: middlewares
            ~ settings.py: settings for the scraper
        ~ run_scrapy.py: makes the spider accesible to the rest of the project

    - utils
        - address_parser.py: extract the parts of the addresses and store them to the database  

At the root of the project there are also files that assure the functionality of the program:

    main.py - defines the flow of the program
    
    project_config.py - variables used in different modules, configurations
    
    list of company websites.snappy.parquet - the dataset of domains

    sites.db - database for the raw and processed data

    Data and Impressions.ipynb - notebook, shows some data, personal reflections on the project 
    
    README.md - instructions for the reader
    
# How it works
First thing, a database where the raw and processed data will be stored is created. The database will contain the domains that Scrapy is going to look at, the urls that are scraped, the type of page that is scraped (home, contact, location, etc.), the text from which the address will be extracted/divided and the parts of the address (country, region, city, postcode, road, road_number), if they are found. The list of domains to be scrawled is extracted from the provided 'parquet' file using pandas and inserted into the database, in 'site' table.
    
    Table             Columns                                           Explanation
    
    site              id, domain                                        the domains to be looked at are added here                     
    
    crawled_links     id, domain_id, page_type, http_status             each domain has pages like home, contact, location
    
    raw_content       id, url_id, tag                                   the pottential addresses on a page are added here

    address           id, domain_id, country, region, state,            address components are extracted and put here
                    city, postcode, road, road_number
    
Moving forward, Scrapy will start its work and parse through each domain, looking especially for contact and location pages. The links accessed are savedin 'crawled_links' table. The content of the pages of interest is going to be emptied of unnecessary content and the text is going to be extracted from the remaining page. The text is ordered by tag, each tag is analyzed for potential addresses using BERT + transformers, and is added in the 'row_content' table if it fulfills the conditions.

The final stage consists in looking through the obtained data and try to divide the addresses by parts using libpostal/pypostal library. The results are added to the 'address' table.