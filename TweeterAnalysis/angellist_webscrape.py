import numpy as np
import pandas as pd
import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
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
CLASS_TWEETER = 'fontello-twitter u-uncoloredLink twitter_url'
XPATH_INVESTORS = "//div[contains(@class, 'past_financing section')]/div/div"
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


driver, wait = start()


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
    tweeter_account_link = find_url_link(soup_link, CLASS_TWEETER)
    return tweeter_account_link, link


def find_company_details(url):
    driver.get(url)
    # try:
    #     viewall = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'view_all')))
    # except NoSuchElementException:
    #     pass
    # else:
    #     time.sleep(2)
    #     for view in viewall:
    #         view.click()
    # time.sleep(2)

    # investors = driver.find_elements_by_xpath(XPATH_INVESTORS)
    # investors_length = len(driver.find_elements_by_xpath(XPATH_INVESTORS+"/preceding-sibling::h4"))
    # find_investors(investors, investors_length)

    find_jobs(driver)

    # teams = driver.find_elements_by_xpath("//div[contains(@class, 'section team')]/div/div")
    # find_teams(teams)


def find_jobs(drive):
    try:
        # jobs = drive.find_element_by_class_name('job-listings')
        all_jobs = drive.find_elements_by_xpath("//div[contains(@class, 'group-listings s-grid-colMd18')]/div/div")

        print("888888888888888888888888888888888")
    except NoSuchElementException:
        return None
    # jobs = jobs.find_elements_by_tag_name('li')
    # for job in jobs:
    #     all_jobs = job.find_elements_by_xpath("//div[contains(@class, 'group-listings s-grid-colMd18')]/div/div")
    for j in all_jobs:
        print(j.get_attribute('innerHTML'))
        job_designation = j.find_element_by_class_name('u-fontSize18').text
        job_description = j.find_element_by_xpath('//div[contains(@class, "listing-data")]').text
        print(job_designation, job_description)
        print("-------------------------------------")


def find_investors(inve, inve_len):
    if inve_len == 1 and len(inve) == 2:
        find_funding(inve[0])
        members = find_members(inve[1])
    elif inve_len == 2 and len(inve) == 2:
        members = find_members(inve[0])
    else:
        raise ValueError()

    print(members)


def find_funding(inve):
    dat, fun = [], []
    try:
        dates = inve.find_elements_by_class_name('date_display')
        for date in dates:
            dat.append(date.text)
        funds = inve.find_elements_by_class_name('raised')
        for fund in funds:
            fun.append(fund.text)
    except NoSuchElementException:
        date, fund = np.nan, np.nan
        dat.append(date)
        fun.append(fund)

    for i in zip(dat, fun):
        print("Investment: ", i)


def find_teams(teams):
    team_length = len(teams)
    if team_length == 1:
        p_teams = teams[0]
        p_teams = find_members(p_teams)
    elif team_length == 2:
        p_teams, pst_teams = teams[0], teams[1]
        p_teams = find_members(p_teams)
        # TODO
        pst_teams = find_members(pst_teams)
        # TODO
    else:
        raise ValueError("Check teams variable !")


def find_members(teams):
    members_list = []
    members = teams.find_elements_by_class_name('role')
    for member in members:
        mem = member.find_element_by_class_name('name').find_element_by_tag_name('a')
        emp_name, emp_url = mem.text, mem.get_attribute("href")
        emp_title = member_title(member)
        emp_bio = member_bio(member)
        members_list.append((emp_name, emp_title, emp_url, emp_bio))
    return members_list


def member_title(emp):
    emp_title = emp.find_element_by_class_name('role_title').text
    if len(emp_title) < 2:
        emp_title = np.nan
    return emp_title


def member_bio(emp):
    try:
        emp_bio = emp.find_element_by_class_name('bio').text
    except NoSuchElementException:
        emp_bio = np.nan
    return emp_bio


def main(results):
    company_list = []
    count = 0
    for result in results:
        if count > 0:
            try:
                soup = BS(result.get_attribute('innerHTML'), 'lxml')
                tweeter_link, company_url = find_tweeter_account(soup, 'startup-link')
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
                # company_list.append((company_name, company_description, joined, location, market, website, size, raised, tweeter_link))
                print((company_name, company_description, joined, location, market, website, size, raised, tweeter_link))

        count += 1

    df = pd.DataFrame(company_list, columns=COLOUMNS)
    df.to_csv('startup_56.csv', index=False)





if __name__ == '__main__':
    pprint("Extracting Start-UP Company details....")
    # driver, wait = start()
    # driver.get(URL)
    # results = wait.until(EC.presence_of_all_elements_located((By.XPATH, XPATH_COMPANIES)))
    # main(results)
    try:
        find_company_details('https://angel.co/drip-capital/jobs')
        # find_company_details('https://angel.co/drip-capital')
    except StaleElementReferenceException:
        pass
    # stop(driver)
    pprint("Completed !!!!!!")
