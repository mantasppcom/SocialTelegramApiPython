import tweepy
import json
import variables
import random


class TwitterApi:
    def __init__(self, screen_name, consumer_key, consumer_secret, access_token, access_token_secret):

        self.screen_name = screen_name
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)
        self.tweets = self.api.user_timeline(screen_name, count=200)

    def get_tweets(self):
        tweets_list = []
        for tweet in self.tweets:
            tweets_list.append(tweet._json['id'])
        return tweets_list


class Tweets:
    def __init__(self, tweets):
        self.tweets = tweets

    def get_random_tweet(self):
        random_number = random.randint(0, len(self.tweets) - 1)
        return self.tweets[random_number]

    def get_last_tweet(self):
        return self.tweets[0]


class TwitterLinks:
    def __init__(self, random_tweet, last_tweet, screen_name):
        self.random_tweet = random_tweet
        self.last_tweet = last_tweet
        self.screen_name = screen_name
        
    def generate_tweet_link(self):
        hyperlink_of_random_tweet = 'https://twitter.com/{0}/status/{1}'.format(
            self.screen_name,
            self.random_tweet
        )

        hyperlink_of_last_tweet = 'https://twitter.com/{0}/status/{1}'.format(
            self.screen_name,
            self.last_tweet
        )

        return hyperlink_of_random_tweet, hyperlink_of_last_tweet


def twitter_main(screen_name):
    twitterapi = TwitterApi(
        screen_name,
        variables.CONSUMER_KEY,
        variables.CONSUMER_SECRET,
        variables.ACCESS_TOKEN,
        variables.ACCESS_TOKEN_SECRET
    )

    tweets = Tweets(twitterapi.get_tweets())

    links = TwitterLinks(
        tweets.get_random_tweet(),
        tweets.get_last_tweet(),
        screen_name
    )

    return links
