import twitter
import os
import emoji
from pymongo import MongoClient
import sys

def tweet():
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

    OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = os.environ['OAUTH_TOKEN_SECRET']


    client = MongoClient('mongodb://heroku_980w3n73:tq6ghn78k9lbjfieqgpn2ii43d@ds049935.mongolab.com:49935/heroku_980w3n73')
    #collection=client['heroku_980w3n73']['tweet'].insert_one({'tweet_id':'123456'})

    lastTweetId = client['heroku_980w3n73']['tweet'].find_one({"name":"last_tweet"})['tweet_id']
    print 'lastTweetId in databse is %s '%lastTweetId

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)

    # Nothing to see by displaying twitter_api except that it's now a
    # defined variable

    print twitter_api

    hillary_dict = {'Hillary':'Kween H',
    "-H":"-Kween H", 
    "are":"r",  
    "Hillary's":"Kween H's",  
    "#Hillary2016":"KweenH2016", 
    "\u2014Hillary":"\u2014KweenH", 
    "women":"womaaaaan", 
    "us":"ussss",
    "first":"frst", 
    "work":"wrk", 
    "gun":"gaaan",
    "people":"ppl", 
    "America":"dope america", 
    "must":"maast", 
    "help":"haaalp",
    "right":"rite",
    "Hillary.":"Kween H.", 
    "Hillary\u2019s":"KweenH\u2019s",
    "Americans":"dope americans", 
    "want":"fucking waant", 
    "What":"wat", 
    "good":"GOOOOOD",  
    "American":"dope american", 
    "fight":"fite", 
    "This":"dis",
    "support":"suprt", 
    "rights":"rits", 
    "equal":"=", 
    "Hillary:":"Hillary:", 
    "fighting":"fiting",
    "like":"lyk",
    "country":"cntry",
    "women's":"womennnn's", 
    "economy":"fking economy",
    "would":"wud",
    "stop":"staaap",
    "strong":"fucking strong", 
    "family":"fking family",
    "protect":"fking protect", 
    "never":"neva",  
    "keep":"fking keep",  
    "woman":"queen",
    "say":"fking say", 
    "great":"awsm", 
    "you.":"u", 
    "go":"fking go",
    "today.":"lik rite now.",
    "today":"lik rite now",
    "economic":"motherfking ecanaamy related",
    "big":"biiiiig",
    "You":"u",
    "official":"official(ugh)",  
    "-Hillary":"-KweenH",  
    "change":"fking change",
    "Iowa":"dope town Iowa", 
    "proud":"mad proud",  
    "affordable":"fking affordable",
    "pay":"pay",
    "President":"prezident", 
    "America.":"dope land america.",  
    "Republican":"lame ass republican",
    "Republicans":"lame ass republicans",
    "climate":"cuh-lie-mate",
    "team":"bitches",
    "business":"dope business", 
    "education":"fking education", 
    "ever":"eva", 
    "Hillary,":"Kween H,", 
    "economy.":"motherfking ecaanaamy.",
    "good":"awesome",
    "president":"prezident",
    "president.":"prezident.",
    "veterans":"dope veterans",
    "veterans,":"dope veterans,"}

    hillary_tweets= twitter_api.statuses.user_timeline(screen_name="HillaryClinton",count=1,exlude_replies='true',include_rts='false')
    currentTweetId = hillary_tweets[0]['id']
    print 'currentTweet id is %s : '%hillary_tweets[0]['id']

    millenialhillary_tweets= twitter_api.statuses.user_timeline(screen_name="KweenHillary",count=1,exlude_replies='true',include_rts='false')
    currentmillenialTweet = millenialhillary_tweets[0]['text']
    #print 'currentmillenialTweet is : %s'%currentmillenialTweet

    if currentTweetId == lastTweetId:
        print 'same tweet as last one. exiting...'
        sys.exit()

    #import emoji library and dict
    f = open('emoji_dict.txt')
    emoji_dict=[]
    emoji_dict_split=[]

    for row in f.readlines():
        if len(row) == 0:
            break
            
        emoji_dict.append(row.strip())
        
    f.close()

    for i in range(len(emoji_dict)):
        item=emoji_dict[i]
        result=item.split('_')
        emoji_dict_split.append(result)

    #print emoji_dict_split

    newTweets=[]
    temp_string=""

    print 'tweeting as millenialHillary now...'
    #dict replacement
    text = hillary_tweets[0]['text']
    tweetText=hillary_tweets[0]['text'].split()
    for word in tweetText:
        
        #if it's in the hillary_dict
        if word in hillary_dict:
            
            text = text.replace(word,hillary_dict[word])
            
        #if it's in the emoji dict
        if word in emoji_dict:           
            emoji_signal=":"+word+":"
            #print emoji.emojize(emoji_signal, use_aliases=True),
            text = text.replace(word,emoji.emojize(emoji_signal, use_aliases=True))
            
        #else:
            #print word,
                
    #print text  
    #text=text.encode('utf8')
    newTweets.append(text)
    #print newTweets
    #lower case
    newTweet = [x.lower() for x in newTweets]
    print "generated Tweet : %s"%newTweet
    #issue based substitution
    if newTweet == currentmillenialTweet:
        print 'same tweet as last'
        exit
    else:
        print 'tweeting finally'   
        #tweet it
        twitter_api.statuses.update(status=text)

    #adding lastTweet's Id to database
    client['heroku_980w3n73']['tweet'].update_one({
            'name':'last_tweet',
            },
            {
            '$set':{
                    'tweet_id':currentTweetId
                }
            }
        )