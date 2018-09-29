
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
        pprint("Not Found robots.txt !")
        return "ALL"
        # raise ValueError("Not Found robots.txt !")

def find_web_crawling_perimission(url):
    """Get allow and disallow permission from robots.txt file"""
    robotscontent = get_robots(url)
    if robotscontent == 'ALL':
        return 'ALL','None'
    else:
        disallow = re.findall(r'Disallow.*', robotscontent.find('p').text)
        allow = re.findall(r'Allow.*', robotscontent.find('p').text)
        return (allow, disallow)

def check(url):
    """Get web scrawling is permitted or not"""
    try:
        allow, disallow = find_web_crawling_perimission(url)
        if allow == 'ALL':
            return True
        length = len([i for i in disallow if i.split(':')[1].strip() in ['/', 'admin', '/*', '/?']])
        if length > 0:
            return True
    except TypeError:
        return False

def find_all_allow(url):
    """Get all the allows permission"""
    return find_web_crawling_perimission(url)[0] if find_web_crawling_perimission(url) else True

def find_all_disallow(url):
    """Get all the disallow permission"""
    if find_web_crawling_perimission(url):
        return find_web_crawling_perimission(url)[1]
