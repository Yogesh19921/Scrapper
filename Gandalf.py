from CollectingProducts.Collect import collect_and_send_url_to_sb
from CollectingProducts.Collect import crawl_and_generate_search_url
import sys

if __name__ == "__main__":
    arg = sys.argv[1]

    if arg == "collect":
        collect_and_send_url_to_sb(arg)

    if arg == "crawl":
        crawl_and_generate_search_url(arg)