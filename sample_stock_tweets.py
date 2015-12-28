from datetime import datetime
import re
import twitter
twitter_stream = twitter.TwitterStream(auth=twitter.OAuth(
            keycodes["access_token"],
            keycodes["access_token_secret"],
            keycodes["consumer_key"],
            keycodes["consumer_secret"]))
iterator = twitter_stream.statuses.sample()

i = 0
j = 0
k = 0
f = []
stocksymbol = re.compile("[A-Z][A-Z]")
print(datetime.now())
for tweet in iterator:
    i += 1
    try:
        if tweet["lang"] == "en" and stocksymbol.search(tweet["text"]):
            k += 1
            print(str(tweet))
        j += 1
    except KeyError:
        pass
iterator.close()
print(datetime.now())
