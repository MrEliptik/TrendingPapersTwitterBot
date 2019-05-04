from scraper import Scraper
from twitterBot import Twitter
import time

star_emoji            = u'\U00002B50'
paper_emojj           = u'\U0001F4C4'
upward_trend_emoji    = u'\U0001F4C8'
link_emoji            = u'\U0001F517'

# Scrap
scrappy = Scraper() 
print('[INFO] Scraping trending papers..')
scrappy.scrapTrending()
print('[INFO] Done scraping!')

# Create string for tweet
tweets = []
for (i, paper) in enumerate(scrappy.trendingPapers):
    tweet = '[' + str(i+1) + '/' + str(len(scrappy.trendingPapers)) + '] '  \
        + upward_trend_emoji + ' - '                                              \
        + paper['title'] + ' - ' + paper['nb_stars'] + ' '                        \
        + star_emoji + ' - ' + paper_emojj + ' ' + paper['pdf']                         \
        + ' - ' + link_emoji + ' ' + paper['github']
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