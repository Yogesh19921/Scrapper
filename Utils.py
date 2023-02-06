from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def get_page_source(page_url, scroll=False):
    options = EdgeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")

    driver = webdriver.Edge(options=options, service=EdgeService(EdgeChromiumDriverManager().install()))

    driver.get(page_url)
    if scroll:
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, total_height, 5):
            driver.execute_script("window.scrollTo(0, {});".format(i))
            total_height = int(driver.execute_script("return document.body.scrollHeight"))

    content = driver.page_source
    driver.quit()

    return content
