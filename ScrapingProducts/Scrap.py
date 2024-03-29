from Utilities.Utils import get_page_source
from Utilities.MetadataUtils import *
from Utilities.ServiceBusUtils import *
from Utilities.CosmosUtils import *
from ScrapingProducts.AmazonRateLimiterException import AmazonRateLimiterException

# Import libraries
from bs4 import BeautifulSoup
import logging as logger
import time
import json

AMAZON_ERROR = "Sorry! Something went wrong on our end. Please go back and try again or go to Amazon's home page."


def program(thread_id):
    run_a_thread(thread_id)


def run_a_thread(thread_id):
    print("starting thread: " + str(thread_id))
    try:
        retrieve_url_scrap_and_insert_into_db()
    except AmazonRateLimiterException as a:
        print("Amazon rate limited us. Will sleep for 20 minutes.")
        close_connection()
        time.sleep(1200)
    except Exception as e:
        print("Some unknown error.")
        print(e)
    # while True:
    #     try:
    #         retrieve_url_scrap_and_insert_into_db()
    #         # Change ip for next request
    #         os.system('sudo service tor reload')
    #     except AmazonRateLimiterException as a:
    #         print("Amazon rate limited us. Will sleep for 20 minutes.")
    #         time.sleep(1200)
    #     except Exception as e:
    #         print("Some unknown error.")
    #         print(e)


def get_candidate_metadata(url):
    try:
        print("Getting candidate metadata===========")
        print(url)
        page = get_page_source(url)

        if AMAZON_ERROR in page:
            raise AmazonRateLimiterException

        soup1 = BeautifulSoup(page, "html.parser")
        soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

        top_category = get_top_category(soup2)
        # bsr_category = category
        bottom_category = get_bottom_category(soup2)

        metadata = {
            'id': get_asin(url),
            'name': get_name(soup2),
            'topCategory': top_category,
            'bottomCategory': bottom_category,
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

        if not validate_item_exists(get_asin(url)):
            candidate_metadata = get_candidate_metadata(url)

            if candidate_metadata is not None:
                insert_entry(candidate_metadata)
                complete_message(message)
        else:
            complete_message(message)

    except AmazonRateLimiterException as a:
        raise AmazonRateLimiterException
    except Exception as e:
        print(e)
        raise Exception("Some exception occurred.")
