import tweepy

# Set up your Twitter API credentials
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define the topics or keywords you want to track
topics = ["#AI", "#DataScience", "#Data"]

# Collect recent tweets on these topics
tweet_data = {}
for topic in topics:
    tweets = api.search(q=topic, count=10)  # You can adjust the count as needed
    tweet_data[topic] = [tweet.text for tweet in tweets]

# Perform analysis on the collected data (e.g., sentiment analysis, topic modeling)

# Summarize the trends
for topic, tweets in tweet_data.items():
    print(f"Trending topic: {topic}")
    print(f"Number of tweets: {len(tweets)}")
    print("Sample tweets:")
    for i, tweet in enumerate(tweets[:5]):
        print(f"{i+1}: {tweet}")
    print("\n")
