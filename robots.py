
def validate_url(url):
    """Basic url validation"""
    return re.search(r'(https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(?=/)?', url)

def get_base_url(url):
    """Get the basic url"""
    baseurl = validate_url(url)
    if baseurl:
        return baseurl.group()
    else:
        raise ValueError('Invalid url !!!')

def get_domain_name(self, url):
    """Get domain name"""
    domain = self.get_base_url(url)
    if '//' in domain:
        if domain.count('.') == 3:
            return domain.split('.')[-3]
        else:
            return domain.split('.')[-2]

def get_robots(url):
    """Get robots.txt file contents form given url"""
    robots_url = get_base_url(url)+'/robots.txt'
    res = requests.get(robots_url)
    if res.status_code == 200:
        return BS(res.content, 'lxml')
    else:
        raise ValueError("Not Found robots.txt !")

def find_web_crawling_perimission(url):
    """Get allow and disallow permission from robots.txt file"""
    robotscontent = get_robots(url).find('p').text
    disallow = re.findall(r'Disallow.*', robotscontent)
    allow = re.findall(r'Allow.*', robotscontent)
    return (allow, disallow)

def check(url):
    """Get web scrawling is permitted or not"""
    allow, disallow = find_web_crawling_perimission(url)
    length = len([i for i in disallow if i.split(':')[1].strip() in ['/', 'admin', '/*', '/?']])
    if length > 0:
        return "Not Allowed"
    else:
        return "Allowed"

def find_all_allow(url):
    """Get all the allows permission"""
    return find_web_crawling_perimission(url)[0]

def find_all_disallow(url):
    """Get all the disallow permission"""
    return find_web_crawling_perimission(url)[1]


if __name__ == '__main__':
    pass
