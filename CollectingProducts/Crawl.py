# Import files
from ScrapingProducts.AmazonRateLimiterException import AmazonRateLimiterException
from Utilities.Utils import get_page_source
from Utilities.MetadataUtils import *

# Import libraries
from bs4 import BeautifulSoup
import logging as logger
import time

AMAZON_ERROR = "Sorry! Something went wrong on our end. Please go back and try again or go to Amazon's home page."


def crawl_item(curr_url, retry=0):
    try:
        page = get_page_source(curr_url)

        if AMAZON_ERROR in page:
            raise AmazonRateLimiterException

        soup1 = BeautifulSoup(page, "html.parser")
        soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
        BSR = get_best_sellers_rank(page)

        top_category = get_top_category(soup2)
        #bsr_category = category
        bottom_category = get_bottom_category(soup2)

        category = ""
        if top_category != "NA":
            category = top_category
        else:
            category = bottom_category

        product = {
            'name': get_name(soup2),
            'topCategory': top_category,
            'bottomCategory': bottom_category,
            'price': get_price(soup2),
            'ASIN': get_asin(curr_url),
            'reviews': get_reviews(soup2),
            'rating': get_rating(soup2),
            'search': get_search(category, curr_url),
            'url': curr_url,
            'BSR': BSR
        }

        return product
    except AmazonRateLimiterException as a:
        print("Amazon is probably blocking us. Will sleep for 1800 seconds and retry")
        time.sleep(1800)
        if retry < 3:
            crawl_item(curr_url, retry + 1)
    except Exception as e:
        logger.error("Error occurred: " + str(e))
        logger.error("URL:" + str(curr_url))
        return None
