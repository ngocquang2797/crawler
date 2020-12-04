# 'https://www.vulnerabilitycenter.com/#search=cve'

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options

import time
import json

desired_capabilities = DesiredCapabilities().CHROME
desired_capabilities['marionette'] = True
desired_capabilities['pageLoadStrategy'] = 'none'  # interactive

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

# crawl list id skybox in main page
def list_skyId(url):

    try:
        driver = Chrome(desired_capabilities=desired_capabilities, options=set_chrome_options())
        driver.get(url=url)
        table: WebElement = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.GMMNKTXCKDC")))
    except (TimeoutException, StaleElementReferenceException) as ex:
        print("Exception!!!!!")
        driver = Chrome(desired_capabilities=desired_capabilities, options=set_chrome_options())
        driver.get(url=url)
        table: WebElement = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.GMMNKTXCKDC")))

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tr.GMMNKTXCODC")))
    soup = BeautifulSoup(table.get_attribute('innerHTML'), 'html.parser')
    driver.close()
    rows = soup.find_all('tr')
    data = []
    for row in rows[1:]:  # skip the header row
        tds = row.find_all('td')
        columns = list(map(lambda td: td.text, tds))
        # obj = {
        #     'skybox_id': columns[0],
        #     'cve_id': columns[1],
        #     'vendor': columns[2],
        #     'severity': columns[3],
        #     'reported_at': columns[4],
        #     'modified_at': columns[5],
        #     'description': columns[6], }
        data.append(columns[0])
    return data

# crawl detail of element
def detail_id(id):
    url = 'https://www.vulnerabilitycenter.com/svc/SVC.html?fbclid=IwAR3qa6zE2HiESzv7hxIIvnlg7b6VEJ9tfrQ2-p6XwenFHLCEUJpPEqoBwsI#!vul={}'.format(
        id)

    try:
        driver = Chrome(desired_capabilities=desired_capabilities, options=set_chrome_options())
        driver.get(url=url)
        table: WebElement = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.svc-SectionTitle")))
    except (TimeoutException, StaleElementReferenceException) as ex:
        print("Exception!!!!!")
        driver = Chrome(desired_capabilities=desired_capabilities)
        driver.get(url=url)
        table: WebElement = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.svc-SectionTitle")))

    data = {}

    data['Title'] = BeautifulSoup(
        driver.find_element_by_css_selector('div.svc-SectionTitle').get_attribute('innerHTML'), 'html.parser').text
    data['Discription'] = BeautifulSoup(driver.find_element_by_css_selector('div.gwt-Label').get_attribute('innerHTML'),
                                        'html.parser').text

    VulDetailsLeft = BeautifulSoup(
        driver.find_element_by_css_selector('table.svc-VulDetailsLeft').get_attribute('innerHTML'), 'html.parser')
    VulDetailsLeftRows = VulDetailsLeft.find_all('tr')
    for row in VulDetailsLeftRows:
        td = row.find_all('td')
        data[td[0].text] = td[1].text

    VulDetailsRight = BeautifulSoup(
        driver.find_element_by_css_selector('table.svc-VulDetailsRight').get_attribute('innerHTML'), 'html.parser')
    VulDetailsRightRows = VulDetailsRight.find_all('tr')
    for row in VulDetailsRightRows:
        td = row.find_all('td')
        data[td[0].text] = td[1].text

    ttl = driver.find_elements_by_css_selector('div.svc-SectionTitle')
    tbCols = driver.find_elements_by_css_selector('tr.GMMNKTXCI3')
    element = driver.find_elements_by_css_selector('table.GMMNKTXCKDC')

    if len(tbCols) == 3 and len(element) == 3:
        for index in range(3):
            product_Cols = BeautifulSoup(
                tbCols[index].get_attribute('innerHTML'), 'html.parser')
            product_title = product_Cols.find_all('td')
            proTitles = [x.text for x in product_title]
            # print(proTitles)
            products = BeautifulSoup(
                element[index].get_attribute('innerHTML'), 'html.parser')
            productrows = products.find_all('tbody')[1].find_all('tr')
            data_product = []
            for row in productrows:
                obj = {}
                td = row.find_all('td')
                for i in range(len(td)):
                    obj[proTitles[i]] = td[i].text
                data_product.append(obj)
            data[BeautifulSoup(ttl[index + 1].get_attribute('innerHTML'), 'html.parser').text] = data_product

    driver.close()
    print(data)
    return data


def main():
    url = 'https://www.vulnerabilitycenter.com/svc/SVC.html?fbclid=IwAR3qa6zE2HiESzv7hxIIvnlg7b6VEJ9tfrQ2-p6XwenFHLCEUJpPEqoBwsI#search=@from=1/1/2019@to=12/31/2019@phrase=+vendor:Jenkins%20CI%20+severity:critical'
    ids = list_skyId(url)
    # ids = ['97539', '102448', '99861', '108858', '100700', '99917', '101087']
    print(ids)
    with open("data.json", "r+") as file:
        data = json.load(file)
        for id in ids:
            data.append(detail_id(id))
            file.seek(0)
            json.dump(data, file)

if __name__ == "__main__":
    main()