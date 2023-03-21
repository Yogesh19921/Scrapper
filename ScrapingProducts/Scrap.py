from Utilities.Utils import get_page_source
from Utilities.MetadataUtils import *
from Utilities.ServiceBusUtils import *
from Utilities.CosmosUtils import *
from AmazonRateLimiterException import AmazonRateLimiterException

# Import libraries
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import logging as logger
import time
import json

AMAZON_ERROR = "Sorry! Something went wrong on our end. Please go back and try again or go to Amazon's home page."


def program():
    futures = []
    executor = ThreadPoolExecutor()

    for i in range(10):
        futures.append(executor.submit(run_a_thread()))

    for future in futures:
        res = future.result()


def run_a_thread():
    while True:
        try:
            retrieve_url_scrap_and_insert_into_db()
        except AmazonRateLimiterException as a:
            print("Amazon rate limited us. Will sleep for 100 seconds")
            time.sleep(100)
        except Exception as e:
            print("Some unknown error.")
            print(e)


def get_candidate_metadata(url):
    try:
        print("Getting candidate metadata===========")
        print(url)
        page = get_page_source(url)

        if AMAZON_ERROR in page:
            raise AmazonRateLimiterException

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

        return metadata
    except AmazonRateLimiterException as a:
        raise AmazonRateLimiterException
    except Exception as e:
        logger.error("Error occurred: " + str(e))
        logger.error("URL:" + str(url))
        return None


def retrieve_url_scrap_and_insert_into_db():
    try:
        message = get_message()[0]
        message_json = json.loads(str(message))
        url = message_json['url']

        candidate_metadata = get_candidate_metadata(url)

        if candidate_metadata is not None:
            insert_entry(candidate_metadata)
            complete_message(message)

    except AmazonRateLimiterException as a:
        raise AmazonRateLimiterException
    except Exception as e:
        print(e)
        raise Exception("Some exception occurred.")
