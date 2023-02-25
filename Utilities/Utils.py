from Utilities.user_agent import random_ua

from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import random

PROXY = "socks5://localhost:9050"


def get_options():
    options = EdgeOptions()
    user_agent = random_ua
    options.add_argument("--proxy-server=%s" % PROXY)
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(f'user-agent={user_agent}')
    return options


def get_page_source(page_url, scroll=False):
    # randomize scrolling, so amazon doesn't get suspicious
    if not scroll:
        scroll = random.choice([True, False])

    driver = webdriver.Edge(options=get_options(), service=EdgeService(EdgeChromiumDriverManager().install()))
    driver.get(page_url)
    if scroll:
        # randomize scroll amount as well
        scroll_amount = random.randint(3, 10)
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, total_height, scroll_amount):
            driver.execute_script("window.scrollTo(0, {});".format(i))
            total_height = int(driver.execute_script("return document.body.scrollHeight"))

    content = driver.page_source
    driver.quit()
    return content
