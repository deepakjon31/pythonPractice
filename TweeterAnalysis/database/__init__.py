import os
import sqlite3

COMPANIES_LIST_TABLE = "create table if not exists companies_list(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date, company_name NOT NULL UNIQUE, description, joined, location, market, website, employee_size, fund_raised, tweeter_link, facebook_link, angel_url)"
COMPANIES_LIST_INSERT = "insert into companies_list (date, company_name, description, joined, location, market, website, employee_size, fund_raised, tweeter_link, facebook_link, angel_url) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
INVESTORS_TABLE = "create table if not exists investors(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date, inv_name, inv_title, inv_url, inv_bio, company_id INTEGER NOT NULL, FOREIGN KEY(company_id) REFERENCES companies_list(id))"
INVESTORS_INSERT = "insert into investors (date, inv_name, inv_title, inv_url, inv_bio, company_id) values (?, ?, ?, ?, ?, ?)"
JOBS_TABLE = "create table if not exists jobs(id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date, job_designation, job_location, job_type, job_salary, job_other, company_id INTEGER NOT NULL, FOREIGN KEY(company_id) REFERENCES companies_list(id))"
JOBS_INSERT = "insert into jobs (date, job_designation, job_location, job_type, job_salary, job_other, company_id) values(?, ?, ?, ?, ?, ?, ?)"
EMPLOYEES_TABLE = "create table if not exists employees(id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date, emp_name, emp_title, emp_url, emp_bio, emp_present, company_id INTEGER NOT NULL, FOREIGN KEY(company_id) REFERENCES companies_list(id))"
EMPLOYEES_INSERT = "insert into employees (date, emp_name, emp_title, emp_url, emp_bio, emp_present, company_id) values (?, ?, ?, ?, ?, ?, ?)"
FUNDING_TABLE = "create table if not exists funds(id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date, fund_date, fund_raised, company_id INTEGER NOT NULL, FOREIGN KEY(company_id) REFERENCES companies_list(id))"
FUNDING_INSERT = "insert into funds (date, fund_date, fund_raised, company_id) values (?, ?, ?, ?)"
TWITTER_USER_TABLE = "create table if not exists twitter_users(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, scrape_date, user_id, user_created_at, user_verified,	user_name,	user_screen_name, user_lang, user_location, user_url, user_likes_count, user_tweets_count,	user_followers_count, user_friends_count, user_descriptions, user_following, user_listed_count,	user_default_profile_image, user_default_profile,	user_profile_bg_color,	user_profile_image_url,	user_time_zone,	user_utc_offset)"
TWITTER_USER_INSERT = "insert into twitter_users (user_id, user_created_at, user_verified,	user_name,	user_screen_name, user_lang, user_location, user_url, user_likes_count, user_tweets_count,	user_followers_count, user_friends_count, user_descriptions, user_following, user_listed_count,	user_default_profile_image, user_default_profile,	user_profile_bg_color,	user_profile_image_url,	user_time_zone,	user_utc_offset) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
TWITTER_TWEETS = "create table if not exists twitter_tweets(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, status_id, status_created_at, status_lang, status_text, status_favorite_count, status_retweeted, status_source, status_favorited, status_retweet_count, status_place, status_coordinates, status_geo_enabled, status_geo, hashtags, mentions, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES twitter_users(id))"
TWITTER_TWEETS_INSERT = "insert into twitter_tweets (status_id, status_created_at, status_lang, status_text, status_favorite_count, status_retweeted, status_source, status_favorited, status_retweet_count, status_place, status_coordinates, status_geo_enabled, status_geo, hashtags, mentions, user_id) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
GET_COMPANY_ID = "select id from companies_list where lower(company_name)='%s'"
GET_TWITTER_ID = "select id from twitter_users where lower(user_screen_name)='%s'"


BASE_PATH = os.path.abspath(os.path.dirname(__file__))

DB_PATH = BASE_PATH + '\database.db'


class DataBase(object):

    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def execute_query(self, query):
        return self.cursor.execute(query)

    def execute_bulk_query(self, query, row):
        return self.cursor.executemany(query, row)
