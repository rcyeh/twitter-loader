from datetime import datetime
import re
import sys
import twitter

keys = { "consumer_key": "./api_key.txt",
         "consumer_secret": "./api_secret.txt",
         "access_token": "./access_token.txt",
         "access_token_secret": "./access_token_secret.txt" }
keycodes = {}
for k, v in keys.items():
    with open(v, "r") as f:
        keycodes[k] = f.readline().rstrip()

twitter_stream = twitter.TwitterStream(auth=twitter.OAuth(
            keycodes["access_token"],
            keycodes["access_token_secret"],
            keycodes["consumer_key"],
            keycodes["consumer_secret"]))
iterator = twitter_stream.statuses.sample()

stocksymbol = re.compile("(^|\s)\$[A-Z]{1,6}(\s|$)")

i = 0
j = 0
k = 0
f = []
divisor = 10
print(str(datetime.now()), file=sys.stderr)
for tweet in iterator:
    i += 1
    try:
        #if tweet["lang"] == "en" and stocksymbol.search(tweet["text"]):
        if len(tweet["entities"]["symbols"]) > 0:
            k += 1
            print(str(tweet))
        j += 1
        if i >= 10000000:
            break
        if 0 == i % divisor:
            print(str(datetime.now()) + " msgs " + str(i) +
                    " tweets " + str(j) +
                    " matches " + str(k), file=sys.stderr)
            if divisor < 1000:
                divisor *= 10
            elif divisor < 128000:
                divisor *= 2
            else:
                divisor = 200000
    except KeyError:
        pass
iterator.close()
