from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import re
import json
from sensitive import give_twitter_credentials
from watson_tone_analyser import sentiment

ckey, csecret, atoken, asecret = give_twitter_credentials()


def cleans_tweet(tweet):
    """clean tweet text by removing links, special characters"""
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split())


class Listener(StreamListener):

    def on_data(self, data):
        try:
            data = json.loads(data)
            raw_tweets = data['text']
            tweet = cleans_tweet(raw_tweets)
            print(tweet)
            sent_json = sentiment(tweet)
            with open("Output.txt", "a") as text_file:
                text_file.write(sent_json + "\n")
            print(sent_json)
            return True
        except:
            pass

    def on_error(self, status):
        print(status)


def main():
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    twitterstream = Stream(auth, Listener())

    topics = []

    n = int(input('Number of topics to be filtered by : '))

    for i in range(n):
        topic = input('Enter topic : ')
        topics.append(topic)

    twitterstream.filter(track=topics, languages=['en'])


if __name__ == '__main__':
    main()
