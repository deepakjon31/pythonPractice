"""
This Module will check whether the website allow to extract data/information or not
"""

import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup as BS


def _validate_url(url):
    """Basic url validation"""
    return re.search(r'(https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(?=/)?', url)


def _get_base_url(url):
    """Get the basic url"""
    baseurl = _validate_url(url)
    if baseurl:
        return baseurl.group()
    else:
        raise ValueError('Invalid url !!!')


def _get_domain_name(self, url):
    """Get domain name"""
    domain = self.get_base_url(url)
    if '//' in domain:
        if domain.count('.') == 3:
            return domain.split('.')[-3]
        else:
            return domain.split('.')[-2]


def _get_robots(url):
    """Get robots.txt file contents form given url"""
    robots_url = _get_base_url(url)+'/robots.txt'
    res = requests.get(robots_url)
    if res.status_code == 200:
        return BS(res.content, 'lxml')
    else:
        pprint("Not Found robots.txt !")
        return "ALL"
        # raise ValueError("Not Found robots.txt !")


def _find_web_crawling_perimission(url):
    """Get allow and disallow permission from robots.txt file"""

    robotscontent = _get_robots(url)
    if robotscontent == 'ALL':
        return 'ALL', 'None'
    else:
        disallow = re.findall(r'Disallow.*', robotscontent.find('p').text)
        allow = re.findall(r'Allow.*', robotscontent.find('p').text)
        return (allow, disallow)


def _find_disallow(permission, checker):
    length = len([dis for dis in permission for chek in checker.strip().split() if chek in dis.split(':')[1].strip()])
    return length


def can_fetch(url, checker=None):
    """Get web scrawling is permitted or not"""
    try:
        _get_base_url(url)
        if checker is None:
            checker = url.split('/')[3:]

        permission = _find_web_crawling_perimission(url)
        if permission[0] == 'ALL':
            return True
        # length = len([dis for dis in disallow if dis.split(':')[1].strip() in ['/', 'admin', '/*', '/?']])
        # length = len([dis for dis in permission[1] if checker.strip() in dis.split(':')[1].strip()])

        if _find_disallow(permission[1], checker) > 0:
            return False
        return True

    except Exception as e:
        # return True
        pprint(f'Exception: {e}')


def find_all_allow(url):
    """Get all the allows permission"""
    return _find_web_crawling_perimission(url)[0] if _find_web_crawling_perimission(url) else True


def find_all_disallow(url):
    """Get all the disallow permission"""
    return _find_web_crawling_perimission(url)[1] if _find_web_crawling_perimission(url) else False


if __name__ == '__main__':
    pass
