import pandas as pd
import numpy as np
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
        return data

