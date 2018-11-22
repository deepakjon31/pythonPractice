import numpy as np
import pandas as pd
import logging as log
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS
from pprint import pprint

import database
from database import (COMPANIES_LIST_INSERT, INVESTORS_INSERT, JOBS_INSERT, EMPLOYEES_INSERT, GET_COMPANY_ID,
                      FUNDING_INSERT)


CHROME_DRIVER = r'C:\Users\kumadee\Downloads\chromedriver_win32\chromedriver.exe'
URL = 'https://angel.co/companies'
COLUMNS = ['Company Name', 'Description', 'Joined', 'Location', 'Market', 'Website', 'Employee Size', 'Fund Raised', 'Tweeter Link']
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
XPATH_TWEETER_URL = "//a[contains(@class, 'fontello-twitter u-uncoloredLink twitter_url')]"
XPATH_FACEBOOK_URL = "//a[contains(@class, 'fontello-facebook u-uncoloredLink facebook_url')]"
XPATH_JOBS = "//div[contains(@class, 'group-listings s-grid-colMd18')]/div/div"
XPATH_TEAM = "//div[contains(@class, 'section team')]/div/div"
FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
DATEFMT = '%m/%d/%Y %I:%M:%S %p'
LOG_FILE = r'log\angel_list.log'
log.basicConfig(level=log.DEBUG, format=FORMAT, datefmt=DATEFMT, filename=LOG_FILE, filemode='w')

now = datetime.now().strftime('%d/%m/%Y')
db = database.DataBase()


def start():
    """Start the Selenium driver and return driver and wait object"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER, chrome_options=chrome_options)
    wait = WebDriverWait(driver, 30)
    log.info('Selenium driver Started')
    return driver, wait


def stop(driver):
    log.info("Selenium driver closed")
    return driver.quit()


driver, wait = start()


class CompaniesDetails(object):

    def click_on_viewall(self):
        log.info("Clicking on viewall")
        try:
            viewall = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'view_all')))
        except (NoSuchElementException, TimeoutException):
            pass
        else:
            time.sleep(2)
            for view in viewall:
                view.click()
        time.sleep(2)
        log.info("Clicked on viewall")

    def find_jobs(self, company_name, company_id):
        log.info(f"Getting jobs: {company_name}")
        try:
            all_jobs = wait.until(EC.presence_of_all_elements_located((By.XPATH, XPATH_JOBS)))
        except (NoSuchElementException, TimeoutException):
            return None
        for job in all_jobs:
            job_designation = job.find_element_by_class_name('u-fontSize18').text
            job_description = job.find_element_by_xpath('//div[contains(@class, "listing-data")]').text
            job_salary, job_other = '', ''
            try:
                job_description_split = job_description.split('·')
                des_length = len(job_description_split)
                if des_length == 2:
                    job_location = job_description_split[0].strip()
                    job_type = ' '.join(job_description_split[1]).strip()
                else:
                    job_location = job_description_split[0].strip()
                    job_type = ' '.join(job_description_split[1]).strip()
                    job_salary = ' '.join(job_description_split[2]).strip()
                    job_other = ' '.join(job_description_split[3]).strip()

            except AttributeError:
                log.error(f"find_jobs:", exe_info=True)
                pass
            else:
                if company_id is not None:
                    job_values = [(now, job_designation, job_location, job_type, job_salary, job_other, company_id[0]), ]
                    db.execute_bulk_query(JOBS_INSERT, job_values)
                else:
                    log.debug(f'{company_name} id not found in DB')
        log.info(f"Getting jobs done: {company_name}")

    def get_investors(self, company_name, company_id):
        log.info(f"Getting investors: {company_name}")
        try:
            inve = wait.until(EC.presence_of_all_elements_located((By.XPATH, XPATH_INVESTORS)))
        except (NoSuchElementException, TimeoutException):
            return None
        inve_len = len(wait.until(EC.presence_of_all_elements_located((By.XPATH, XPATH_INVESTORS + "/preceding-sibling::h4"))))
        log.debug(f'length of inve_len: {inve_len} and  length of inve: {len(inve)}')
        if inve_len == 1 and len(inve) == 2:
            self.find_funding(inve[0], company_name, company_id)
            members = self.get_members(inve[1], company_id)
        elif inve_len == 2 and len(inve) == 2:
            members = self.get_members(inve[0], company_id)
        elif inve_len == 2 and len(inve) == 3:
            self.find_funding(inve[0], company_name, company_id)
            members = self.get_members(inve[1], company_id)
        elif inve_len == 1 and len(inve) == 1:
            members = self.get_members(inve[0], company_id)
        else:
            return None
            # raise ValueError()
        log.info(f"Getting investors done: {company_name}")
        if company_id is not None:
            # investors_values = [members, ]
            self._execute(INVESTORS_INSERT, members)
        else:
            log.debug(f'{company_name} id not found in DB')

    def find_funding(self, inve, company_name, company_id):
        log.info(f"Getting funding: {company_name}")
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
        if len(fun) > 0:
            if company_id is not None:
                funds = pd.DataFrame(list(zip(dat, fun)), columns=['fund_date', 'fund_raised'])
                funds['date'], funds['company_id'] = now, company_id[0]
                funds = funds[['date', 'fund_date', 'fund_raised', 'company_id']]
                funding_values = [tuple(x) for x in funds.values]
                self._execute(FUNDING_INSERT, funding_values)
            else:
                log.debug(f'{company_name} id not found in DB')
        log.info(f"Getting funding done: {company_name}")

    def find_teams(self,company_name, company_id):
        log.info(f"Getting teams: {company_name}")
        try:
            teams = wait.until(EC.presence_of_all_elements_located((By.XPATH, XPATH_TEAM)))
        except (NoSuchElementException, TimeoutException):
            return None
        team_length = len(teams)
        pst_team = ''
        if team_length == 1:
            p_teams = teams[0]
            p_teams = self.get_members(p_teams, company_id)
        elif team_length >= 2:
            p_teams, pst_teams = teams[0], teams[1]
            p_teams = self.get_members(p_teams, company_id)
            pst_team = self.get_members(pst_teams, company_id)
        else:
            raise ValueError("Check teams variable !")
        log.info(f"Getting teams done: {company_name}")
        if len(p_teams) > 0:
            df2 = None
            df = pd.DataFrame(p_teams, columns=['date', 'emp_name', 'emp_title', 'emp_url', 'emp_bio', 'company_id'])
            df['emp_present'] = 'YES'

            if isinstance(pst_team, list) and len(pst_team) > 0:
                df1 = pd.DataFrame(pst_team, columns=['date', 'emp_name', 'emp_title', 'emp_url', 'emp_bio', 'company_id'])
                df1['emp_present'] = 'NO'
                df2 = df.append(df1)
                # df2 = df2.values.tolist()
            if df2 is not None:
                if company_id is not None:
                    df2 = df2[['date', 'emp_name', 'emp_title', 'emp_url', 'emp_bio', 'emp_present', 'company_id']]
                    employee_values = [tuple(x) for x in df2.values]
                    self._execute(EMPLOYEES_INSERT, employee_values)
                else:
                    log.debug(f'{company_name} id not found in DB')
            else:
                if company_id is not None:
                    df = df[['date', 'emp_name', 'emp_title', 'emp_url', 'emp_bio', 'emp_present', 'company_id']]
                    employee_values = [tuple(x) for x in df.values]
                    self._execute(EMPLOYEES_INSERT, employee_values)
                else:
                    log.debug(f'{company_name} id not found in DB')

    def get_members(self, teams, company_id):
        log.info("Getting members")
        members_list = []
        members = teams.find_elements_by_class_name('role')
        for member in members:
            try:
                mem = member.find_element_by_class_name('name').find_element_by_tag_name('a')
                emp_name, emp_url = mem.text, mem.get_attribute("href")
                emp_title = self.get_member_title(member)
                emp_bio = self.get_member_bio(member)
                members_list.append((now, emp_name, emp_title, emp_url, emp_bio, company_id[0]))
            except Exception as e:
                log.error("get_members:", exc_info=True)
                pass
        log.info("Getting members done")
        return members_list

    def get_member_title(self, emp):
        log.info("Getting member title")
        emp_title = emp.find_element_by_class_name('role_title').text
        if len(emp_title) < 2:
            emp_title = np.nan
        log.info("Getting member title done")
        return emp_title

    def get_member_bio(self, emp):
        log.info("Getting member bio")
        try:
            emp_bio = emp.find_element_by_class_name('bio').text
        except NoSuchElementException:
            emp_bio = np.nan
        log.info("Getting member bio done")
        return emp_bio

    def get_company_id(self, company_name):
        query = GET_COMPANY_ID % company_name

        return db.execute_query(query).fetchone()

    def _execute(self, insert, values):
        db.execute_bulk_query(insert, values)


class Companies(CompaniesDetails):

    def __init__(self, url):
        self.open_url(url)

    def open_url(self, url):
        log.info(f"Opening url: {url}")
        return driver.get(url)

    def get_companies_page(self):
        log.info("Getting all companies...")
        return wait.until(EC.presence_of_all_elements_located((By.XPATH, XPATH_COMPANIES)))

    def get_companies(self):
        count = 0
        results = self.get_companies_page()

        for result in results:
            if count > 2:
                try:
                    soup = BS(result.get_attribute('innerHTML'), 'lxml')
                    company_url = self.get_company_url(soup, 'startup-link')
                    company_name = soup.find('div', class_='text').find('a', class_='startup-link').text.strip()
                    company_description = soup.find('div', attrs={'class': 'pitch'}).text.strip()
                    joined = self.get_data(soup, CLASS_JOINED).replace("’", ' ')
                    location = self.get_data(soup, CLASS_LOCATION)
                    market = self.get_data(soup, CLASS_MARKET)
                    website = self.get_data(soup, CLASS_WEBSITE)
                    size = self.get_data(soup, CLASS_SIZE).replace("-", ' to ')
                    raised = self.get_data(soup, CLASS_RAISED)
                    log.info("Opening new tab")
                    driver.execute_script("window.open()")
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(3)
                    driver.get(f"{company_url}")
                    log.info(f"Opening url: {company_url}")
                    tweeter_link = self.tweeter_url()
                    facebook_link = self.facebook_url()
                    com = [(now, company_name, company_description, joined, location, market, website, size, raised,
                            tweeter_link, facebook_link, company_url), ]
                    company_id = self.get_company_id(company_name)
                    if company_id is None:
                        self._execute(COMPANIES_LIST_INSERT, com)
                        company_id = self.get_company_id(company_name)

                    # self.click_on_viewall()
                    # self.get_investors(company_name, company_id)
                    # self.find_teams(company_name, company_id)
                    # self.open_url(company_url + '/jobs')
                    # self.find_jobs(company_name, company_id)
                    db.commit()
                    driver.close()
                    log.info("Closed new opened tab")
                    driver.switch_to.window(driver.window_handles[0])
                except StaleElementReferenceException as e:
                    log.error(f'get_companies Stale: {e}', exc_info=True)
                    pass
                except Exception as e:
                    log.error(f'get_companies: {e}', exc_info=True)
                    pass
            count += 1

    def get_single_company(self, url):
        company_name = url.split('/')[-1]
        company_id = self.get_company_id(company_name)
        if company_id is None:
            raise KeyError(f"company ID not found for: {company_name}")
        self.open_url(url)
        self.click_on_viewall()
        self.get_investors(company_name, company_id)
        self.find_teams(company_name, company_id)
        self.open_url(url + '/jobs')
        self.find_jobs(company_name, company_id)
        db.commit()
        driver.close()

    def get_data(self, soup, classname):
        log.info("Invoked to get_data")
        return soup.find('div', attrs={'class': '%s' % classname}).find('div', attrs={'class': 'value'}).text.strip()

    def get_company_url(self, soup, classname):
        log.info("Invoked to get_company_url")
        try:
            return soup.find('a', attrs={'class': '%s' % classname})['href']
        except:
            pass

    def tweeter_url(self):
        log.info("Invoked to tweeter_url")
        try:
            url = wait.until(EC.presence_of_element_located((By.XPATH, XPATH_TWEETER_URL))).get_attribute('href')
        except (NoSuchElementException, TimeoutException):
            return None
        else:
            if 'twitter' not in url:
                return None
            return url

    def facebook_url(self):
        log.info("Invoked to facebook_url")
        try:
            url = wait.until(EC.presence_of_element_located((By.XPATH, XPATH_FACEBOOK_URL))).get_attribute('href')
        except (NoSuchElementException, TimeoutException):
            return None
        else:
            if 'facebook' not in url:
                return None
            return url


if __name__ == '__main__':
    pprint("Extracting Start-UP Company details....")
    obj = Companies(URL)
    # obj.get_companies()
    obj.get_single_company('https://angel.co/joist')
    db.close()
    stop(driver)
    pprint("Completed !!!!!!")

