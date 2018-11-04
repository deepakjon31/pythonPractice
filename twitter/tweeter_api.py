import os
import re
import pandas as pd
import numpy as np
from textblob import TextBlob
from tweepy import OAuthHandler, API

from localConf import (consumer_key, consumer_secret,
                       access_token, access_token_secret)


class TweeterAPI(object):
    def __init__(self):
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = API(self.auth)

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
        data.to_csv('tweets.csv', index=False)
        return data


class TweetsAnalyze(object):

    def __init__(self):
        file = 'tweets.csv'
        self.__read_csv(file)

    def __read_csv(self, file):

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
        more_liked_tweet = self.data['Tweets'][self.fav]
        total_likes = self.fav_max
        char_len_tweet = self.data['len'][self.fav]
        return more_liked_tweet, total_likes, char_len_tweet

    def analyze_retweets(self):
        more_liked_retweet = self.data['Tweets'][self.rt]
        total_retweets = self.rt_max
        char_len_retweet = self.data['len'][self.rt]
        return more_liked_retweet, total_retweets, char_len_retweet

    def time_series(self):
        tlen = pd.Series(data=self.data.len.values, index=self.data.Date)
        tfav = pd.Series(data=self.data.Likes.values, index=self.data.Date)
        tret = pd.Series(data=self.data.RTs.values, index=self.data.Date)
        return tlen, tfav, tret
        # tfav.plot(figsize=(16,4), label="Likes", legend=True)

    def pie_chart(self):
        sources = list(set(self.data.Source.tolist()))
        percent = np.zeros(len(sources))
        for source in self.data.Source:
            for index in range(len(sources)):
                if source == sources[index]:
                    percent[index] += 1
                    pass
        percent /= 100
        pie_chart = pd.Series(percent, index=sources, name='Sources')
        return pie_chart # pie_chart.plot.pie(fontsize=11, autopct='%.2f', figsize=(6, 6))

    def __clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def __analyze_sentiment(self, tweet):

        analysis = TextBlob(self.__clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def sentimental_analysis(self):
        self.data['SA'] = np.array([self.__analyze_sentiment(tweet) for tweet in self.data.Tweets])
        pos_tweets = [tweet for index, tweet in enumerate(self.data.Tweets) if self.data.SA.index > 0]
        neu_tweets = [tweet for index, tweet in enumerate(self.data.Tweets) if self.data.SA.index == 0]
        neg_tweets = [tweet for index, tweet in enumerate(self.data.Tweets) if self.data.SA.index < 0]
        return pos_tweets, neu_tweets, neg_tweets
        # len(pos_tweets)*100/len(data['Tweets'])

