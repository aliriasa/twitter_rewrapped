import tweepy_class as tc
import apply_model as m
import drawPosts as dP
import tensorflow as tf
import tensorflow_hub as hub
import tweepy
import numpy as np
import re
import json
import credentials
import logging
import os.path as path
from shutil import copyfile
import os
from os import chdir, environ as env, makedirs
import os.path as path
import subprocess

# AWS Lambda code
tmp_dir = "/tmp/interview-scheduler"
token_path_txt = path.join(tmp_dir, 'tweet_ID.txt')
token_path_png = path.join(tmp_dir, 'tweet_ID_1.png')
token_path_1png = path.join(tmp_dir, 'tweet_ID_2.png')
token_path_2png = path.join(tmp_dir, 'tweet_ID_3.png')
token_path_3png = path.join(tmp_dir, 'tweet_ID_4.png')
token_path_N = path.join(tmp_dir, 'cloud.png')
token_model = path.join(tmp_dir, 'my_model.h5')
token_twitter = path.join(tmp_dir, 'twitter.jpg')
token_stopwrods = path.join(tmp_dir, 'stopwords.txt')

try:
    makedirs(tmp_dir)
    subprocess.run(["chmod", "775", str(tmp_dir)])
    copyfile('tweet_ID.txt', token_path_txt )
    copyfile('tweet_ID.png', token_path_png)
    copyfile('tweet_ID_1.png', token_path_1png)
    copyfile('tweet_ID_2.png', token_path_2png)
    copyfile('tweet_ID_3.png', token_path_3png)
    copyfile('tweet_ID_3.png', token_path_N)
    copyfile('my_model.h5', token_model)
    copyfile('twitter.jpg', token_twitter)
    copyfile('stopwords.txt', token_stopwrods)
    print("Created directory / copied file")
except:
    pass

chdir(tmp_dir)

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
model = tf.keras.models.load_model('model/my_model.h5', custom_objects={'embed': embed})

def main(event, context):
    respondToTweet()

def get_last_tweet(file):
        f = open(file, 'r')
        lastId = int(f.read().strip())
        f.close()
        return lastId

def put_last_tweet(file, Id):
        f = open(file, 'w')
        f.write(str(Id))
        f.close()
        return

def respondToTweet(file='tools/tweet_ID.txt'):
    """
    Respond to tweets that mention the user of the API.

    Parameters:
    - file (str, optional): The file where the ID of the last tweet that was processed is stored. 
                            Default is 'tools/tweet_ID.txt'.
    """
    twitter_api = tc.TwitterModel()

    last_id = get_last_tweet(file)
    print(last_id)
    mentions = twitter_api.api.mentions_timeline(since_id=last_id, tweet_mode = 'extended')
    
    if len(mentions) == 0:
        return

    new_id = 0

    for mention in reversed(mentions):
        account = mention.user.screen_name
        new_id = mention.id
        try:
            tweets, len_tweets = twitter_api.get_tweets_last_year(account)
        except:
            twitter_api.api.update_status(status="Error. Sent me a DM to solve the issue #" + str(mention.id), in_reply_to_status_id = mention.id)
        
        try: 
            if len(tweets) > 20 and len(len_tweets) > 10:
                model_class = m.ApplyModel(model)
                interests_from_user = model_class.top_interests(tweets)
                avg_size = np.mean(len_tweets)
                total_length = len(len_tweets)
                
                drawing = dP.DrawTwitterPosts(interests_from_user, account, avg_size, total_length)
                img_interests = drawing.draw_top_interests()
                
                if img_interests == None:
                    twitter_api.api.update_status(status="Not enough long Tweets #" + str(mention.id), in_reply_to_status_id = mention.id)
                else:
                    img_interests.save("tweet_photos/tweet_ID_1.png")
                    
                    model_class.word_cloud()
                    img_wordcloud = drawing.draw_cloud()
                    img_wordcloud.save("tweet_photos/tweet_ID_2.png")

                    img_aop = drawing.draw_aop()
                    img_aop.save("tweet_photos/tweet_ID_3.png")
                    
                    img_avg = drawing.draw_avg_size()
                    img_avg.save("tweet_photos/tweet_ID_4.png")
                    
                    filenames = ['tweet_photos/tweet_ID_1.png', 'tweet_photos/tweet_ID_2.png', 'tweet_photos/tweet_ID_3.png', 'tweet_photos/tweet_ID_4.png',]
                    media_ids = []
                    for filename in filenames:
                        res = twitter_api.api.media_upload(filename=filename)
                        media_ids.append(res.media_id)

                    twitter_api.api.update_status(status='@' + mention.user.screen_name + " #ReWrapped", media_ids=media_ids)

            else:
                twitter_api.api.update_status(status="Not enough Tweets #" + str(mention.id), in_reply_to_status_id = mention.id)
        except:
            twitter_api.api.update_status(status="Error. Sent me a DM to solve the issue #" + str(mention.id), in_reply_to_status_id = mention.id)
        
    put_last_tweet(file, new_id)

