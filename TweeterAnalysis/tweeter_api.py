import os
import re
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from tweepy import OAuthHandler, API

from localConf import (consumer_key, consumer_secret,
                       access_token, access_token_secret)


dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = dir_path + '\static\images'
# dir_path = r'C:\Users\kumadee\PycharmProjects\Practice\twitter\static\images'


class TweeterAPI(object):
    def __init__(self):
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = API(self.auth)
        if not self.api:
            print("Problem Connecting to API")

    def get_user(self, target_user):
        return self.api.get_user(target_user)

    def get_user_timeline(self, target_user):
        tweets = self.api.user_timeline(id=target_user, count=200)
        data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        data['len'] = np.array([len(tweet.text) for tweet in tweets])
        data['ID'] = np.array([tweet.id for tweet in tweets])
        data['Date'] = np.array([tweet.created_at for tweet in tweets])
        data['Source'] = np.array([tweet.source for tweet in tweets])
        data['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
        data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])
        data.to_csv('tweets_%s.csv' % target_user, index=False)
        # return data


class TweetsAnalyze(object):

    def __init__(self, target_user):
        file = 'tweets_%s.csv' % target_user
        if os.path.exists(os.path.join(os.path.dirname(__file__), file)):
            self.data = pd.read_csv(file)
            self.data['SA'] = np.array([self.analyze_sentiment(tweet) for tweet in self.data.Tweets])
            self.avg_tweets_length = np.mean(self.data.len)
            self.fav_max = np.max(self.data.Likes)
            self.rt_max = np.max(self.data.RTs)
            self.fav = self.data[self.data.Likes == self.fav_max].index[0]
            self.rt = self.data[self.data.RTs == self.rt_max].index[0]
        else:
            raise FileNotFoundError(f"Not Found {file}")
        #self.read_csv(file)

    def read_csv(self, file):

        if os.path.exists(os.path.join(os.path.dirname(__file__), file)):
            self.data = pd.read_csv(file)
            self.avg_tweets_length = np.mean(self.data.len)
            self.fav_max = np.max(self.data.Likes)
            self.rt_max = np.max(self.data.RTs)
            self.fav = self.data[self.data.Likes == self.fav_max].index[0]
            self.rt = self.data[self.data.RTs == self.rt_max].index[0]
        else:
            raise FileNotFoundError(f"Not Found {file}")

    def analyze_tweets(self):
        mean = np.mean(self.data['len'])
        more_liked_tweet = self.data['Tweets'][self.fav]
        total_likes = self.fav_max
        char_len_tweet = self.data['len'][self.fav]
        return mean, more_liked_tweet, total_likes, char_len_tweet

    def analyze_retweets(self):
        more_liked_retweet = self.data['Tweets'][self.rt]
        total_retweets = self.rt_max
        char_len_retweet = self.data['len'][self.rt]
        self.time_series()
        return more_liked_retweet, total_retweets, char_len_retweet

    def time_series(self):
        # tlen = pd.Series(data=self.data.len.values, index=self.data.Date)
        tfav = pd.Series(data=self.data.Likes.values, index=self.data.Date)
        tret = pd.Series(data=self.data.RTs.values, index=self.data.Date)
        # print("tweet", tret)
        # tlen.plot(figsize=(16,4), label="Tweets Length", legend=True)
        # tweets_len = dir_path + '\\tweets_len.png'
        # plt.savefig(tweets_len)
        tfav.plot(figsize=(16,4), label="Likes", legend=True)
        tret.plot(figsize=(16,4), label="Retweets", legend=True)
        timeseries = dir_path + '\\time_series.png'

        plt.savefig(timeseries)

        self.pie_chart()
        # return tlen, tfav, tret

    def pie_chart(self):
        sources = list(set(self.data.Source.tolist()))
        print(sources)
        percent = np.zeros(len(sources))
        for source in self.data.Source:
            for index in range(len(sources)):
                if source == sources[index]:
                    percent[index] += 1
                    pass
        percent /= 100
        pie_chart = pd.Series(percent, index=sources, name='Sources')
        pie_chart.plot.pie(fontsize=11, autopct='%.2f', figsize=(6, 6))
        fig_name = dir_path + '\\pie_chart.png'
        # print(fig_name)

        plt.savefig(fig_name)

        # return pie_chart

    def clean_tweet(self, tweet):

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):

        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def sentimental_analysis(self):
        try:
            # print(self.data.SA)
            pos_tweets = [tweet for index, tweet in enumerate(self.data['Tweets']) if self.data['SA'][index] > 0]
            neu_tweets = [tweet for index, tweet in enumerate(self.data['Tweets']) if self.data['SA'][index] == 0]
            neg_tweets = [tweet for index, tweet in enumerate(self.data['Tweets']) if self.data['SA'][index] < 0]
            total_tweet_length = len(self.data['Tweets'])
            return pos_tweets, neu_tweets, neg_tweets, total_tweet_length
        except Exception as e:
            print(e)
            pass

#
# columns = ['user_id', 'user_created_at', 'user_verified', 'user_name', 'user_screen_name', 'user_lang', 'user_location',
#            'user_url', 'user_likes_count', 'user_tweets_count', 'user_followers_count', 'user_friends_count',
#            'user_descriptions', 'user_following', 'user_listed_count', 'user_default_profile_image',
#            'user_default_profile', 'user_profile_bg_color', 'user_profile_image_url', 'user_time_zone',
#            'user_utc_offset', 'status_id', 'status_created_at', 'status_lang', 'status_text', 'status_favorite_count',
#            'status_retweeted', 'status_source', 'status_favorited', 'status_retweet_count', 'status_place',
#            'status_coordinates', 'status_geo_enabled', 'status_geo', 'hashtags', 'mentions']
#
# statuses = []
# tweet_count = 0
#
# for status in Cursor(api.user_timeline, id='heyhush').items():
#     hashtags = []
#     mentions = []
#     tweet_count += 1
#
#     if hasattr(status, "entities"):
#         entities = status.entities
#         if "hashtags" in entities:
#             for ent in entities["hashtags"]:
#                 if ent is not None and "text" in ent:
#                     hashtag = ent["text"]
#                     if hashtag is not None:
#                         hashtags.append(hashtag)
#         if "user_mentions" in entities:
#             for ent in entities["user_mentions"]:
#                 if ent is not None:
#                     if "screen_name" in ent:
#                         name = ent["screen_name"]
#                         if name is not None:
#                             mentions.append(name)
#     status = (status.user.id,
#               status.user.created_at,
#               status.user.verified,
#               status.user.name,
#               status.user.screen_name,
#               status.user.lang,
#               status.user.location,
#               status.user.url,
#               status.user.favourites_count,
#               status.user.statuses_count,
#               status.user.followers_count,
#               status.user.friends_count,
#               status.user.description,
#               status.user.following,
#               status.user.listed_count,
#               status.user.default_profile_image,
#               status.user.default_profile,
#               status.user.profile_background_color,
#               status.user.profile_image_url,
#               status.user.time_zone,
#               status.user.utc_offset,
#               status.id,
#               status.created_at,
#               status.lang,
#               status.text,
#               status.favorite_count,
#               status.retweeted,
#               status.source,
#               status.favorited,
#               status.retweet_count,
#               status.place,
#               status.coordinates,
#               status.user.geo_enabled,
#               status.geo,
#               hashtags,
#               mentions)
#     statuses.append(status)
#
# st = pd.DataFrame(statuses, columns=columns)
# st.to_csv('status_tweeter_deepak.csv', index=False)