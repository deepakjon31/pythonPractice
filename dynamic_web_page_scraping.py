from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_field_text_if_exists(item, selector):
    """Extracts a field by a CSS selector if exists."""
    try:
        return item.find_element_by_css_selector(selector).text
    except NoSuchElementException:
        return ""


def get_link_if_exists(item, selector):
    """Extracts an href attribute value by a CSS selector if exists."""
    try:
        return item.find_element_by_css_selector(selector).get_attribute("href")
    except NoSuchElementException:
        return ""


driver = webdriver.Chrome(executable_path=r'C:\Users\Downloads\chromedriver_win32\chromedriver.exe')
wait = WebDriverWait(driver, 10)

driver.get("https://www.zebra.com/us/en/partners/partner-application-locator.html")

location = driver.find_element_by_css_selector('.partnerLocation input')
location.clear()
location.send_keys("Colorado, USA")

# select the first suggestion from a suggestion dropdown
dropdown_suggestion = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul[id^=typeahead] li a')))
dropdown_suggestion.click()

# click more until no more results to load
while True:
    try:
        more_button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'showmore-bg'))).click()
    except TimeoutException:
        break

# wait for results to load
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.seclection-result .partners-detail')))

# parse results
for result in driver.find_elements_by_css_selector('.seclection-result .partners-detail'):
    name = get_field_text_if_exists(result, 'a')
    address = get_field_text_if_exists(result, '.fullDetail-cmpAdres')
    phone = get_field_text_if_exists(result, '.fullDetail-cmpAdres p[ng-if*=phone]')
    website = get_link_if_exists(result, 'a[ng-if*=website]')

    print(name, address, phone, website)

driver.quit()