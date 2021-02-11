import tweepy
import datetime
import config
import csv
import re


CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET
ACCESS_TOKEN = config.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET

#認証
def get_twitter_api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit = True)
    return api


api = get_twitter_api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

data = []
for page in range(1, 36):
    results = api.user_timeline(screen_name="Noda00572069", count=10, page=page)
    for r in results:
        tweet = []
        text = re.sub("\n+", "．", r.text)
        tweet.append(text)
        data.append(tweet)


fcsv = open("NodaTweet.csv", "w", newline="", encoding="utf_8_sig")
writer = csv.writer(fcsv, lineterminator="\n")
for row in data:
    writer.writerow(row)

fcsv.close()



