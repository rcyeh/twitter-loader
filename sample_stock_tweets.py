from datetime import datetime
import json
import re
import sys
import twitter

with open("secrets.json", "r") as f:
    keycodes = json.loads(f.read())

twitter_stream = twitter.TwitterStream(auth=twitter.OAuth(
            keycodes["access_token"],
            keycodes["access_token_secret"],
            keycodes["api_key"],
            keycodes["api_secret"]))
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
                    " matches " + str(k) +
                    " ratio " + str(1e-6 * int(1e6 * float(k)/j)) +
                    " poisson error " + str(1e-6 * int(1e6 * float(k)**0.5/j)), file=sys.stderr)
            if divisor < 1000:
                divisor *= 10
            elif divisor < 128000:
                divisor *= 2
            else:
                divisor = 200000
    except KeyError:
        pass
iterator.close()
