import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS
from pprint import pprint


CHROME_DRIVER = r'C:\Users\kumadee\Downloads\chromedriver_win32\chromedriver.exe'
URL = 'https://angel.co/companies'
COLOUMNS = ['Company Name', 'Description', 'Joined', 'Location', 'Market', 'Website', 'Employee Size', 'Fund Raised', 'Tweeter Link']
XPATH_COMPANIES = '//div[contains(@class, "dc59 frw44 _a _jm")]'
CLASS_JOINED = 'column joined'
CLASS_LOCATION = 'column location'
CLASS_MARKET = 'column market'
CLASS_WEBSITE = 'column website'
CLASS_SIZE = 'column company_size hidden_column'
CLASS_RAISED = 'column hidden_column raised'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'


def start():
    """Start the Selenium driver and return driver and wait object"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER)
    wait = WebDriverWait(driver, 30)
    return driver, wait


def stop(driver):
    return driver.quit()


def find_data(soup, classname):
    return soup.find('div', attrs={'class': '%s' % classname}).find('div', attrs={'class': 'value'}).text.strip()


def find_url_link(soup, classname):
    try:
        return soup.find('a', attrs={'class': '%s' % classname})['href']
    except:
        pass


def find_tweeter_account(soup, classname):
    link = find_url_link(soup, classname)
    print("Link:", link)
    res = requests.get(link, headers={'user-agent': USER_AGENT})
    soup_link = BS(res.content, 'lxml')
    return find_url_link(soup_link, 'fontello-twitter u-uncoloredLink twitter_url')


def main(results):
    company_list = []
    count = 0
    for result in results:
        if count > 0:
            try:
                soup = BS(result.get_attribute('innerHTML'), 'lxml')
                tweeter_link = find_tweeter_account(soup, 'startup-link')
                company_name = soup.find('div', class_='text').find('a', class_='startup-link').text.strip()
                company_description = soup.find('div', attrs={'class': 'pitch'}).text.strip()
                joined = find_data(soup, CLASS_JOINED).replace("’", ' ')
                location = find_data(soup, CLASS_LOCATION)
                market = find_data(soup, CLASS_MARKET)
                website = find_data(soup, CLASS_WEBSITE)
                size = find_data(soup, CLASS_SIZE).replace("-", ' to ')
                raised = find_data(soup, CLASS_RAISED)
            except Exception as e:
                print(f'Error: {e.__doc__}')
                pass
            else:
                company_list.append((company_name, company_description, joined, location, market, website, size, raised, tweeter_link))
                print((company_name, company_description, joined, location, market, website, size, raised, tweeter_link))
        count += 1

    df = pd.DataFrame(company_list, columns=COLOUMNS)
    df.to_csv('startup.csv', index=False)


if __name__ == '__main__':
    pprint("Extracting Start-UP Company details....")
    driver, wait = start()
    driver.get(URL)
    results = wait.until(EC.presence_of_all_elements_located((By.XPATH, XPATH_COMPANIES)))
    main(results)
    stop(driver)
    pprint("Completed !!!!!!")
