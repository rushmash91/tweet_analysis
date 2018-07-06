from nltk.corpus import twitter_samples
from random import shuffle
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import tweepy
import re
import json
from sensitive import give_credentials


consumer_key, consumer_secret, access_token, access_token_secret = give_credentials()


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def clean_tweet(tweet):
    """clean tweet text by removing links, special characters"""
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split())


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    
    def on_data(self, data):
        # decode json
        data_dict = json.loads(data)
        
        try:
            # pass tweet into TextBlog
            tweet = TextBlob(clean_tweet(data_dict['text']))

            # categorize tweet into pos and neg sentiment
            if tweet.sentiment.polarity < 0:
                sentiment = 'neg'
            elif tweet.sentiment.polarity == 0:
                sentiment = 'neutral'
            else:
                sentiment = 'pos'

            # outputs sentiment polarity
            print('{}:   ({}: {})'.format(tweet, tweet.sentiment.polarity, sentiment))
        except:
            print("ERRORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR!")
    
    def on_status(self, status):
        print(status.text)
        
    # on failure
    def on_error(self, status):
        print(status)

input_text = 'trump'

# create a stream
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=[input_text])



"""Using nltk"""
pos_tweets = twitter_samples.strings('positive_tweets.json')
neg_tweets = twitter_samples.strings('negative_tweets.json')
print(len(pos_tweets), len(neg_tweets))

pos_tweets_set = []
neg_tweets_set = []
for tweet in pos_tweets:
    pos_tweets_set.append((tweet, 'pos'))
for tweet in neg_tweets:
    neg_tweets_set.append((tweet, 'neg'))
    
# radomize pos_reviews_set and neg_reviews_set
shuffle(pos_tweets_set)
shuffle(neg_tweets_set)

train = pos_tweets_set[100:800] + neg_tweets_set[100:800]
test = pos_tweets_set[:100] + neg_tweets_set[:100]
print(len(train), len(test))

clf = NaiveBayesClassifier(train_set=train)  # trained model

print(clf.accuracy(test))
print(clf.show_informative_features(10))

text = "It is great."
print(clf.classify(text))

text = "The script was predictable. However, it was a great movie. I loved it."
blob = TextBlob(text, classifier=clf)
print(blob.classify())
for sentence in blob.sentences:
    print ("{} ({})".format(sentence, sentence.classify()))

