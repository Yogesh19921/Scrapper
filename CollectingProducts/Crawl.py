# Import files
from Utilities.Utils import get_page_source
from Utilities.MetadataUtils import *

# Import libraries
from bs4 import BeautifulSoup
import logging as logger
import time


def crawl_item(href):
    try:
        curr_url = "https://amazon.com" + href.attrs['href']
        page = get_page_source(curr_url)
        soup1 = BeautifulSoup(page, "html.parser")
        soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
        BSR = get_best_sellers_rank(page)

        category = get_category(soup2)
        bsr_category = category

        product = {
            'name': get_name(soup2),
            'category': category,
            'price': get_price(soup2),
            'ASIN': get_asin(curr_url),
            'reviews': get_reviews(soup2),
            'rating': get_rating(soup2),
            'search': get_search(category, curr_url),
            'url': curr_url,
            'BSR': BSR
        }

        return product
    except Exception as e:
        logger.error("Error occurred: " + str(e))
        logger.error("URL:" + str(href.attrs['href']))
        time.sleep(5)
        return None
