import pandas as pd
import numpy as np
from tweepy import OAuthHandler, API
from tweepy import Cursor
from localConf import (consumer_key, consumer_secret, access_token, access_token_secret)
from database import DataBase
from database import TWITTER_USER_INSERT, TWITTER_TWEETS_INSERT, GET_TWITTER_ID


class TweeterAPI(object):
    """Class to extract the tweets and twitter id details from Twitter using tweepy module"""
    def __init__(self):
        """Initialize the tweepy api with security keys"""
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = API(self.auth)

    def get_user_timeline(self, target_user):
        """This method will give the detailed information about twitter user passed and store in database
        Before storing into database it will check whether user exists on database of not if not it will write entries
        """
        statuses = []
        tweet_count = 0
        flag = False
        target_user = target_user.lower()
        db = DataBase()
        t_id = db.execute_query(GET_TWITTER_ID % target_user).fetchone()
        print(t_id)

        if t_id is None:
            flag = True

        for status in Cursor(self.api.user_timeline, id=target_user).items():
            hashtags = ''
            mentions = ''
            tweet_count += 1

            if hasattr(status, "entities"):
                entities = status.entities
                if "hashtags" in entities:
                    for ent in entities["hashtags"]:
                        if ent is not None and "text" in ent:
                            hashtag = ent["text"]
                            if hashtag is not None:
                                hashtags += hashtag + ', '
                                # hashtags.append(hashtag)
                if "user_mentions" in entities:
                    for ent in entities["user_mentions"]:
                        if ent is not None:
                            if "screen_name" in ent:
                                name = ent["screen_name"]
                                if name is not None:
                                    mentions += name + ', '
                                    # mentions.append(name)

            if flag:
                user_detail = ((status.user.id, status.user.created_at, status.user.verified, status.user.name,
                                status.user.screen_name, status.user.lang, status.user.location, status.user.url,
                                status.user.favourites_count, status.user.statuses_count, status.user.followers_count,
                                status.user.friends_count, status.user.description, status.user.following,
                                status.user.listed_count, status.user.default_profile_image, status.user.default_profile,
                                status.user.profile_background_color, status.user.profile_image_url, status.user.time_zone,
                                status.user.utc_offset),)
                db.execute_bulk_query(TWITTER_USER_INSERT, user_detail)
                db.commit()
                flag = False
                t_id = db.execute_query(GET_TWITTER_ID % target_user).fetchone()
                print(t_id)

            tweet_detail = (status.id, status.created_at, status.lang, status.text,
                            status.favorite_count, status.retweeted, status.source, status.favorited,
                            status.retweet_count, status.place, status.coordinates, status.user.geo_enabled, status.geo,
                            hashtags, mentions, t_id[0])
            statuses.append(tweet_detail)
            tweet_detail = (tweet_detail, )

            db.execute_bulk_query(TWITTER_TWEETS_INSERT, tweet_detail)
            db.commit()
        db.close()
        df = pd.DataFrame(statuses)
        df.to_csv('deepak_test.csv')


if __name__ == '__main__':
    obj = TweeterAPI()
    obj.get_user_timeline('lily')

