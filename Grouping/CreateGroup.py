from Utilities.Utils import get_page_source
from Utilities.MetadataUtils import *

# Import libraries
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import logging as logger
import time

from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential

ENDPOINT = "https://scraping-grouping.documents.azure.com:443/"
DATABASE_NAME = "Scraping"
CONTAINER_NAME = "Groups"
key_path = PartitionKey(path="/ASIN")


def get_container():
    credential = DefaultAzureCredential()
    client = CosmosClient(url=ENDPOINT, credential=credential)
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
    c = database.create_container_if_not_exists(
        id=CONTAINER_NAME, partition_key=key_path, offer_throughput=400
    )
    return c


container = get_container()


def insert_entry(metadata):
    container.create_item(metadata)


def create_group(search_url):
    candidate_urls = get_candidate_urls(search_url)
    # print(candidate_urls[:1])
    candidates_metadata = get_candidates_metadata(candidate_urls)

    print("============================================")
    print(candidates_metadata)
    print("Scraped URLs:" + str(len(candidates_metadata)))
    print("Total Urls: " + str(len(candidate_urls)))
    print("============================================")


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
    page = get_page_source(url)
    soup1 = BeautifulSoup(page, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    try:
        metadata = {
            'id': get_asin(soup2),
            'name': get_name(soup2),
            'category': get_category(soup2),
            'price': get_price(soup2),
            'ASIN': get_asin(soup2),
            'reviews': get_reviews(soup2),
            'rating': get_rating(soup2),
            'url': url,
            'quantity': "NA",  # TBD with jungleScout Api
            'revenue': "NA",
            'dimensions': get_product_dimensions(soup2),
            'scrapeTime': time.time()
        }
        insert_entry(metadata)

    except Exception as e:
        logger.error("Error occured: " + str(e))
        logger.error("URL:" + str(url))
        time.sleep(5)
        return None

    return metadata


def get_candidate_urls(search_url):
    page = get_page_source(search_url)
    soup1 = BeautifulSoup(page, "html.parser")

    hrefs = soup1.find_all("a",
                           {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

    candidate_urls = []
    for href in hrefs:
        candidate_urls.append("https://amazon.com" + href.attrs['href'])
    return candidate_urls