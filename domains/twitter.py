import tweepy

consumer_key = 'OjeXg57oNqKhp28mvRiCvpxBS'
consumer_secret = 'gMQ9VDlJhEqN1N9PwDdqWM8FMOIX6ygIq5HU8eUuGVSG0hbBid'
access_token = '354161158-httZ4TgGq7YafR89T6RNnwutSnB38plX5xjSegBI'
access_token_secret = '0CRPdxvR3OMeiheWOBTTQUnWYFMhWUgfMgsDAcTMGjKUq'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)