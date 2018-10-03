"""
This Module will check whether the website allow to extract data/information or not
"""

import re
import requests
from http import HTTPStatus
from pprint import pprint
from bs4 import BeautifulSoup as BS


class Robots(object):

    def _validate_url(url):
        """Basic url validation"""
        return re.search(r'(https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(?=/)?', url)

    @staticmethod
    def _get_base_url(url):
        """Get the basic url"""
        baseurl = Robots._validate_url(url)
        if baseurl:
            return baseurl.group()
        else:
            suggestion = 'https://www.google.com'
            raise ValueError(f'Invalid url !!! it must be like: {suggestion}')

    @staticmethod
    def _get_domain_name(url):
        """Get domain name"""
        domain = Robots._get_base_url(url)
        if '//' in domain:
            if domain.count('.') == 3:
                return domain.split('.')[-3]
            else:
                return domain.split('.')[-2]

    @staticmethod
    def _get_robots(url):
        """Get robots.txt file contents form given url"""
        robots_url = Robots._get_base_url(url)+'/robots.txt'
        res = requests.get(robots_url)
        if res.status_code == HTTPStatus.OK:
            return BS(res.content, 'lxml')
        elif res.status_code == HTTPStatus.NOT_FOUND:
            pprint("Not Found robots.txt !")
            return "ALL"
            # raise ValueError("Not Found robots.txt !")
        else:
            raise PermissionError(f'{res.reason} {res.status_code}')

    @staticmethod
    def _find_web_crawling_perimission(url):
        """Get allow and disallow permission from robots.txt file"""

        robotscontent = Robots._get_robots(url)
        if robotscontent == 'ALL':
            return 'ALL', 'None'
        else:
            disallow = re.findall(r'Disallow.*', robotscontent.find('p').text)
            allow = re.findall(r'Allow.*', robotscontent.find('p').text)
            return (allow, disallow)

    @staticmethod
    def _find_disallow(permission, checker):
        length = len([dis for dis in permission for check in checker.strip().split() if check in dis.split(':')[1].strip()])
        return length

    @classmethod
    def can_fetch(cls, url, checker):
        """Get web scrawling is permitted or not"""
        try:
            # cls._get_base_url(url)
            if checker is None:
                checker = '/'.join(url.split('/')[3:])
                if len(checker) == 0:
                    checker = 'admin'

            permission = cls._find_web_crawling_perimission(url)

            if permission[0] == 'ALL':
                return True

            if cls._find_disallow(permission[1], checker) > 0:
                return False
            return True

        except Exception as e:
            # return True
            pprint(f'Exception: {e}')

    @classmethod
    def find_all_allow(cls, url):
        """Get all the allows permission"""
        return cls._find_web_crawling_perimission(url)[0] if cls._find_web_crawling_perimission(url) else True

    @classmethod
    def find_all_disallow(cls, url):
        """Get all the disallow permission"""
        return cls._find_web_crawling_perimission(url)[1] if cls._find_web_crawling_perimission(url) else False


def can_fetch(url, checker=None):
    return Robots.can_fetch(url, checker)


def find_all_allow(url):
    return Robots.find_all_allow(url)


def find_all_disallow(url):
    return Robots.find_all_disallow(url)


if __name__ == '__main__':
    pass

# print(can_fetch('http://www.google.com', '/search'))
# print(find_all_disallow('http://www.google.com/imgres'))
# print(can_fetch('http://www.google.com'))
# print(can_fetch('http://www.google.com/search/howsearchworks'))
