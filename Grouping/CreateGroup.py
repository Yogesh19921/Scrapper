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
        try:
            candidate_urls = get_candidate_urls()
            print("===========================Gotten candidate URLS")
            # print(candidate_urls[:1])
            candidates_metadata = get_candidates_metadata(candidate_urls)

            print("============================================")
            # print(candidates_metadata)
            print("Scraped URLs:" + str(len(candidates_metadata)))
            print("Total Urls: " + str(len(candidate_urls)))
            print("============================================")

            # it = False
        except Exception as e:
            print(e)
            print("Some error occurred. Will pause for 50 seconds")
            time.sleep(50)


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
        print("Getting candidate metadata===========")
        print(url)
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

def check_if_exists_in_db(asin):
    print("Got this asin:" + asin)
    return validate_item_exists(asin)


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
        # Filter sponsored content
        if '/gp/slredirect' in href.attrs['href']:
            continue


        print("Getting ASIN from :" + href.attrs['href'])
        # Check if we have already scraped this item by looking in the database
        if not check_if_exists_in_db(get_asin(href.attrs['href'])):
            long_href = href.attrs['href']
            short_href = long_href.split('ref=')[0]
            candidate_urls.append("https://amazon.com" + short_href)

    if len(hrefs) <= 0:
        print("=============No hrefs found.=====================" + search_url)
        text_file = open(message_json['ASIN'], "w")
        text_file.write(page)
        text_file.close()
        raise Exception("No links founds. Amazon probably blocked us")

    complete_message(message)
    return candidate_urls