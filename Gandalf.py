from CollectingProducts.Collect import collect_and_send_url_to_sb
from CollectingProducts.Collect import crawl_and_generate_search_url
import sys

if __name__ == "__main__":
    arg = sys.argv[1]

    if arg == "collect":
        url = sys.argv[2]
        collect_and_send_url_to_sb(url)

    if arg == "crawl":
        url = sys.argv[2]
        crawl_and_generate_search_url(url)