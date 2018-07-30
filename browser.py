from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType

import proxy

path = r'C:\Users\kumar\Downloads\geckodriver-v0.19.1-win64\geckodriver.exe'


class Browser:
    @staticmethod
    def get_browser():
        """start and quit the browser with proxy"""
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.http_proxy = proxy.PROXIES
        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)
        browser = webdriver.Firefox(desired_capabilities=capabilities, executable_path=path)
        wait = WebDriverWait(browser, 30)
        return browser, wait


    @staticmethod
    def quit_browser(browser):
        """Closing browser"""
        return browser.quit()
