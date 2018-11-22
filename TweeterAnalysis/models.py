from database import DataBase

GET_COMPANIES = "select date, company_name, description, joined, location, market, website, employee_size, fund_raised  from companies_list"
GET_INVESTORS = "select date, inv_name, inv_title, inv_url, inv_bio from investors where company_id='%s'"
GET_JOBS = "select date, job_designation, job_location, job_type, job_salary from jobs where company_id='%s'"
GET_EMPLOYEE = "select date, emp_name, emp_title, emp_url, emp_present, emp_bio from employees where company_id='%s'"
GET_FUNDS = "select date, fund_raised, fund_date from funds where company_id='%s'"
GET_COMPANY_ID = "select id from companies_list where lower(company_name)='%s'"
GET_COMPANY_DESC = "select description from companies_list where lower(company_name)='%s'"
GET_TWITTER_USER_DETAIL = "select user_created_at, user_name, user_screen_name, user_location, user_likes_count, user_tweets_count, user_followers_count, user_friends_count from twitter_users where lower(user_screen_name)='%s'"
GET_TWITTER_USER_ID = "select id from twitter_users where lower(user_screen_name)='%s'"
GET_TWITTER_URL = "select tweeter_link  from companies_list where lower(company_name)='%s'"
GET_TWITTER_TWEETS = "select status_created_at, status_text, hashtags, mentions from twitter_tweets where user_id='%s'"
HEADER_JOB = (('date', 'job_designation', 'job_location', 'job_type', 'job_salary'),)
HEADER_EMPLOYEE = (('date', 'emp_name', 'emp_title', 'emp_url', 'emp_present', 'emp_bio'),)
HEADER_INVESTOR = (('Date', 'Investor Name', 'Investor Title', 'Investor url', 'Investor bio'),)
HEADER_FUND = (('Date', 'fund_raised', 'fund_date'),)
HEADER_TWITTER_TWEETS = (('status_created_at', 'status_text', 'hashtags', 'mentions'),)

class Query(object):
    def __init__(self):
        self.db = DataBase()

    def get_company(self):
        return self.db.execute_query(GET_COMPANIES).fetchall()

    def get_investors(self, company_name):
        c_id = self.get_company_id(company_name)
        return self.db.execute_query(GET_INVESTORS % c_id).fetchall()

    def get_jobs(self, company_name):
        c_id = self.get_company_id(company_name)
        return self.db.execute_query(GET_JOBS % c_id).fetchall()

    def get_employees(self, company_name):
        c_id = self.get_company_id(company_name)
        return self.db.execute_query(GET_EMPLOYEE % c_id).fetchall()

    def get_funds(self, company_name):
        c_id = self.get_company_id(company_name)
        return self.db.execute_query(GET_FUNDS % c_id).fetchall()

    def get_about_company(self, company_name):
        about = self.db.execute_query(GET_COMPANY_DESC % company_name).fetchone()
        if about is not None:
            return about
        raise KeyError(f'company name not found {company_name}')

    def get_company_id(self, company_name):
        c_id = self.db.execute_query(GET_COMPANY_ID % company_name).fetchone()
        if c_id is not None:
            return c_id[0]
        raise KeyError(f"company_id Not Found: {company_name}")

    def get_twitter_user_detail(self, twitter_user):
        return self.db.execute_query(GET_TWITTER_USER_DETAIL % twitter_user).fetchall()

    def get_twitter_user_id(self, user_name):
        t_id = self.db.execute_query(GET_TWITTER_USER_ID % user_name).fetchone()
        if t_id is not None:
            return t_id[0]
        raise KeyError(f'User ID not found {user_name}')

    def get_twitter_tweets(self, user_name):
        t_id = self.get_twitter_user_id(user_name)
        return self.db.execute_query(GET_TWITTER_TWEETS % t_id).fetchall()

    def get_tweeter_url(self, company_name):
        tweeter_url = self.db.execute_query(GET_TWITTER_URL % company_name).fetchone()
        if tweeter_url is not None:
            return tweeter_url[0]
        raise KeyError(f"Tweeter url Not Found {company_name}")

    def close(self):
        self.db.close()


def get_feature_query(feature, company_name):
    if 'job' in feature.lower():
        query = Query()
        jobs = query.get_jobs(company_name)
        query.close()
        return jobs, HEADER_JOB
    elif 'employee' in feature.lower():
        query = Query()
        employee = query.get_employees(company_name)
        query.close()
        return employee, HEADER_EMPLOYEE
    elif 'investor' in feature.lower():
        query = Query()
        investor = query.get_investors(company_name)
        query.close()
        return investor, HEADER_INVESTOR
    elif 'fund' in feature.lower():
        query = Query()
        fund = query.get_funds(company_name)
        query.close()
        return fund, HEADER_FUND
    elif 'about' in feature.lower():
        query = Query()
        about = query.get_about_company(company_name)
        query.close()
        return about
    elif 'twitteruser' in feature.lower():
        query = Query()
        twitter_user = query.get_twitter_user_detail(company_name)
        query.close()
        return twitter_user
    elif 'twittertweets' in feature.lower():
        query = Query()
        twitter_tweets = query.get_twitter_tweets(company_name)
        query.close()
        return twitter_tweets, HEADER_TWITTER_TWEETS
    elif 'tweeter_url' in feature.lower():
        query = Query()
        tweeter_url = query.get_tweeter_url(company_name)
        query.close()
        return tweeter_url

