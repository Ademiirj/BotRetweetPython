import tweepy
import time
import json

def executaBot(consumer_key, consumer_secret,access_token,access_token_secret, key_words,tweets_per_query, bot_user):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    new_tweets = 0
    fail_tweets = 0
##Criando um for para que todas as palavras sejam pesquisadas
    for querry in key_words:
        print ("Searching word: " + querry)

        for tweet in tweepy.Cursor(api.search, q=querry,result_type = 'recent', tweet_mode="extended").items(tweets_per_query ):
            user = tweet.user.screen_name
            id = tweet.id
            url = 'https://twitter.com/' + user +  '/status/' + str(id)
            try:
                ##Fazendo com que o BOT não retweet os proprios tweets
                if not tweet.retweeted or user != bot_user: 
                    tweet.retweet()
                    new_tweets += 1
                    print (url)
            except:
                fail_tweets += 1   
    print ("New Tweets: " + str(new_tweets))
    print ("Fail Tweets: "+str(fail_tweets))

try:
    config_json = open ('config.json', 'r')
    configuracoes = json.load(config_json)
    configurado = True
except Exception as error:
    print("Settings file not found...")
    print(error)
    configurado = False

if(configurado):
    
    while 1:
        executaBot(
        configuracoes["consumer_key"],
        configuracoes["consumer_secret"],
        configuracoes["access_token"],
        configuracoes["access_token_secret"],
        configuracoes["key_words"],
        configuracoes["tweets_per_query"],
        configuracoes["bot_user"]
        )
        time.sleep(configuracoes["sleep_seconds"])
else:
    print("Due to lack of settings file the application is being closed...")
