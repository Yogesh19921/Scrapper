from Utilities.user_agent import random_ua

from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
import random
from amazoncaptcha import AmazonCaptcha
import re

PROXY = "socks5://localhost:9050"
VALIDATE_TEXT = "Sorry, we just need to make sure you're not a robot. For best results, please make sure your browser is accepting cookies."


def solve_captcha(driver):
    print("==============================Solving captcha======================================")
    img_src = driver.find_element(By.TAG_NAME, "img").get_attribute("src")
    captcha = AmazonCaptcha.fromlink(img_src)
    print("capthca image - " + str(img_src))
    solution = captcha.solve()
    print("Solution - " + str(solution))
    driver.find_element(By.ID, "captchacharacters").send_keys(str(solution))
    driver.find_element(By.TAG_NAME, "button").click()

    return driver.page_source


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

    if re.search(VALIDATE_TEXT, content, re.IGNORECASE):
        content = solve_captcha(driver)
        print("Solved captcha for : ============" + str(page_url))

    driver.quit()
    return content
