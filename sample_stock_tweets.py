from datetime import datetime
import json
import os
import re
import sys
import gzip
import twitter

def main(arglist):
    try:
        filenum = arglist[1]
    except:
        filenum = str(int(datetime.utcnow().timestamp()))

    scriptdir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(scriptdir, "secrets.json"), "rt") as f:
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
    with gzip.open("sample_tweets_" + filenum + ".json.gz", "at") as sample_tweets:
        with gzip.open("entity_tweets_" + filenum + ".json.gz", "at") as entity_tweets:
            for tweet in iterator:
                i += 1
                jt = json.dumps(tweet)
                print(jt, file=sample_tweets)
                try:
                    #if tweet["lang"] == "en" and stocksymbol.search(tweet["text"]):
                    if len(tweet["entities"]["symbols"]) > 0:
                        k += 1
                        print(jt, file=entity_tweets)
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

if __name__ == "__main__":
    main(sys.argv)
