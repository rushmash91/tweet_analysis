from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from sensitive import give_twitter_credentials
import sqlite3
import json

ckey , csecret, atoken, asecret = give_twitter_credentials()

connection = sqlite3.connect('tweets.db')
c = connection.cursor()


def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS tweets(id INT PRIMARY KEY, tweet TEXT NOT NULL, 
user TEXT NOT NULL , user_id INT NOT NULL UNIQUE, user_location TEXT, timestamp TEXT NOT NULL )""")


def sql_insert(id, tweet, user, user_id, user_location, timestamp):
    try:
        c.execute("INSERT INTO tweets(id, tweet, user, user_id, user_location, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                  (id, tweet, user, user_id, user_location, timestamp))
        connection.commit()
    except Exception:
        print('Insertion Failed')


class Listener(StreamListener):
    create_table()

    def on_data(self, data):
        data = json.loads(data)
        id = data['id']
        tweet = data['text']
        user = data['user']['name']
        user_id = data['user']['screen_name']
        user_location = data['user']['location']
        timestamp = data['created_at']
        print(tweet)
        sql_insert(id, tweet, user, user_id, user_location, timestamp)
        return True

    def on_error(self, status):
        print(status)


def main():
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    twitterStream = Stream(auth, Listener())
    topics = []

    n = int(input('Number of topics to be filtered by : '))

    for i in range(n):
        topic = input('Enter topic : ')
        topics.append(topic)

    twitterStream.filter(track=topics)


if __name__ == '__main__':
    main()






