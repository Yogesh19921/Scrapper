from Utilities.Utils import get_page_source
from Utilities.MetadataUtils import *
from Utilities.ServiceBusUtils import *
from Utilities.CosmosUtils import *

# Import libraries
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import logging as logger
import time
import json


def create_group():
    it = True
    while it:
        candidate_urls = get_candidate_urls()
        # print(candidate_urls[:1])
        candidates_metadata = get_candidates_metadata(candidate_urls)

        print("============================================")
        # print(candidates_metadata)
        print("Scraped URLs:" + str(len(candidates_metadata)))
        print("Total Urls: " + str(len(candidate_urls)))
        print("============================================")

        # it = False


def get_candidates_metadata(urls):
    all_metadata = []
    futures = []

    executor = ThreadPoolExecutor()

    for url in urls:
        futures.append(executor.submit(get_candidate_metadata, url))

    for future in futures:
        res = future.result()
        if res is not None:
            all_metadata.append(res)

    return all_metadata


def get_candidate_metadata(url):
    try:
        page = get_page_source(url)
        soup1 = BeautifulSoup(page, "html.parser")
        soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
        metadata = {
            'id': get_asin(url),
            'name': get_name(soup2),
            'category': get_category(soup2),
            'price': get_price(soup2),
            'ASIN': get_asin(url),
            'reviews': get_reviews(soup2),
            'rating': get_rating(soup2),
            'url': url,
            'quantity': "NA",  # TBD with jungleScout Api
            'revenue': "NA",
            'dimensions': get_product_dimensions(soup2)
        }
        insert_entry(metadata)

        return metadata
    except Exception as e:
        logger.error("Error occured: " + str(e))
        logger.error("URL:" + str(url))
        time.sleep(5)
        return None


def get_candidate_urls():
    message = get_message()[0]
    message_json = json.loads(str(message))
    search_url = message_json['search']
    print(search_url)
    page = get_page_source(search_url)
    soup1 = BeautifulSoup(page, "html.parser")

    hrefs = soup1.find_all("a",
                           {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

    candidate_urls = []
    for href in hrefs:
        candidate_urls.append("https://amazon.com" + href.attrs['href'])

    if len(hrefs) <= 0:
        print("=============No hrefs found.=====================" + search_url)
        text_file = open(message_json['ASIN'], "w")
        text_file.write(page)
        text_file.close()
        # print(page)
        time.sleep(100)

    complete_message(message)
    return candidate_urls
