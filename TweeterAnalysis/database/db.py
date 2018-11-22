import os
import sqlite3

COMPANIES_LIST_TABLE = "create table if not exists companies_list(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date, company_name NOT NULL, description, joined, location, market, website, employee_size, fund_raised, tweeter_link, facebook_link, angel_url)"
COMPANIES_LIST_INSERT = "insert into companies_list (date, company_name, description, joined, location, market, website, employee_size, fund_raised, tweeter_link, facebook_link, angel_url) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
INVESTORS_TABLE = "create table if not exists investors(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date, inv_name, inv_title, inv_url, inv_bio, company_id INTEGER NOT NULL, FOREIGN KEY(company_id) REFERENCES companies_list(id))"
INVESTORS_TABLE_INSERT = "insert into investors (date, inv_name, inv_title, inv_url, inv_bio, company_id) values (?, ?, ?, ?, ?, ?)"
JOBS_TABLE = "create table if not exists jobs(id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date, job_designation, job_location, job_type, job_salary, job_other, company_id INTEGER NOT NULL, FOREIGN KEY(company_id) REFERENCES companies_list(id))"
JOBS_INSERT = "insert into jobs (date, job_designation, job_location, job_type, job_salary, job_other, company_id) values(?, ?, ?, ?, ?, ?, ?)"
EMPLOYEES_TABLE = "create table if not exists employees(id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date, emp_name, emp_title, emp_url, emp_bio, emp_present, company_id INTEGER NOT NULL, FOREIGN KEY(company_id) REFERENCES companies_list(id))"
EMPLOYEES_INSERT = "insert into employees (date, emp_name, emp_title, emp_url, emp_bio, emp_present, company_id) values (?, ?, ?, ?, ?, ?, ?)"

TWITTER_USER_TABLE = "create table if not exists twitter_users(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, scrape_date, user_id, user_created_at, user_verified,	user_name,	user_screen_name, user_lang, user_location, user_url, user_likes_count, user_tweets_count,	user_followers_count, user_friends_count, user_descriptions, user_following, user_listed_count,	user_default_profile_image, user_default_profile,	user_profile_bg_color,	user_profile_image_url,	user_time_zone,	user_utc_offset)"
TWITTER_USER_INSERT = "insert into twitter_users (user_id, user_created_at, user_verified,	user_name,	user_screen_name, user_lang, user_location, user_url, user_likes_count, user_tweets_count,	user_followers_count, user_friends_count, user_descriptions, user_following, user_listed_count,	user_default_profile_image, user_default_profile,	user_profile_bg_color,	user_profile_image_url,	user_time_zone,	user_utc_offset) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"


TWITTER_TWEETS = "create table if not exists twitter_tweets(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, status_id, status_created_at, status_lang, status_text, status_favorite_count, status_retweeted, status_source, status_favorited, status_retweet_count, status_place, status_coordinates, status_geo_enabled, status_geo, hashtags, mentions, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES companies_list(user_id))"
TWITTER_TWEETS_INSERT = "insert into twitter_tweets (status_id, status_created_at, status_lang, status_text, status_favorite_count, status_retweeted, status_source, status_favorited, status_retweet_count, status_place, status_coordinates, status_geo_enabled, status_geo, hashtags, mentions, user_id) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"




BASE_PATH = os.path.abspath(os.path.dirname(__file__))

DB_PATH = BASE_PATH + '\database.db'


class DataBase(object):

    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def execute_query(self, query):
        return self.cursor.execute(query)

    def execute_bulk_query(self, query, row):
        return self.cursor.executemany(query, row)


db = DataBase()
# t = "create table if not exists funds(id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date, fund_date, fund_raised, company_id INTEGER NOT NULL, FOREIGN KEY(company_id) REFERENCES companies_list(id))"
# db.execute_query(t)
# db.execute_query(INVESTORS_TABLE)
# db.execute_query(EMPLOYEES_TABLE)

# com = [('Zipline International', '134', '6/17/2018', '', '', '', '51 to 200', '25000000', 'https://angel.co/zipline-international-1', 'https://angel.co/zipline-international-1', ''),]
# #
# db.execute_bulk_query(COMPANIES_LIST_INSERT, com)
# # db.execute_query('drop table companies_list')

# db.execute_query(INVESTORS_TABLE)
# com_id = db.execute_query("select id from companies_list where company_name='Zipline International'").fetchone()
# if com_id is not None:
#     com_id = com_id[0]
#     print(com_id)
#
# db.execute_bulk_query(INVESTORS_TABLE_INSERT, "<>")


# q = [("Senior Software Engineer, Android", "Los Angeles", "Full Time", "$130k-$180K", "$180k Â· 0.1% â€“ 0.5%", com_id),]

# q = [("12/2/2018", "Alexis Forde", "Customer Support Manager", "https://angel.co/alexis-forde", "Driven professional specializing in account management, logistics and operations. Accustomed to wearing different hats and helping any team at any capacity.", "YES", com_id),]
# db.execute_bulk_query(q1, q)
# db.execute_query('drop table twitter_users')
TWITTER_USER_TABLE = "create table if not exists twitter_users(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, " \
                     "user_id, user_created_at, user_verified,	user_name,	user_screen_name, user_lang," \
                     "user_location, user_url, user_likes_count, user_tweets_count,	user_followers_count," \
                     "user_friends_count, user_descriptions, user_following, user_listed_count,	user_default_profile_image," \
                     "user_default_profile,	user_profile_bg_color,	user_profile_image_url,	user_time_zone,	user_utc_offset)"


TWITTER_TWEETS = "create table if not exists twitter_tweets(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, status_id, status_created_at, status_lang, status_text, status_favorite_count, status_retweeted, status_source, status_favorited, status_retweet_count, status_place, status_coordinates, status_geo_enabled, status_geo, hashtags, mentions, user_id NOT NULL, FOREIGN KEY(user_id) REFERENCES twitter_users(id))"

db.execute_query(TWITTER_TWEETS)
db.commit()
db.close()
