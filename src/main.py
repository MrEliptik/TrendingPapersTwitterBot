from scraper import Scraper
from twitterBot import Twitter
import time

# Scrap
scrappy = Scraper() 
print('[INFO] Scraping trending papers..')
scrappy.scrapTrending()
print('[INFO] Done scraping!')

# Create string for tweet
tweets = []
for (i, paper) in enumerate(scrappy.trendingPapers):
    tweet = '[' + str(i+1) + '/' + str(len(scrappy.trendingPapers)) + '] '  \
        + paper['title'] + ' - ' + paper['nb_stars']                        \
        + ' stars - pdf: ' + paper['pdf']                                   \
        + ' - github: ' + paper['github']
    print(tweet)
    tweets.append(tweet)
# Create API object
print('[INFO] Connecting to twitter..')
bot = Twitter()
print('[INFO] Connected!')

print('[INFO] Tweeting..')
for (i, tweet) in enumerate(tweets):
    print('>> Tweet' + str(i))
    bot.tweet(tweet)
    time.sleep(5)
print('[INFO] Finished tweeting!')