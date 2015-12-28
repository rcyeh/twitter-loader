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

stocksymbol = re.compile("\s[A-Z][A-Z]|\s\$[A-Z][A-Z]") # too broad
stocksymbol = re.compile("\$[A-Z]")

i = 0
j = 0
k = 0
f = []
print(str(datetime.now()), file=sys.stderr)
for tweet in iterator:
    i += 1
    try:
        if tweet["lang"] == "en" and stocksymbol.search(tweet["text"]):
            k += 1
            print(str(tweet))
        j += 1
        if i >= 2000000000:
            break
        if 0 == i % 10000:
            print(str(datetime.now()) + " msgs " + str(i) +
                    " tweets " + str(j) +
                    " matches " + str(k), file=sys.stderr)
    except KeyError:
        pass
iterator.close()
