import tweepy
from datetime import datetime, date
import pytz
from dateutil.relativedelta import relativedelta
import re
import random
import credentials

class TwitterModel():
    """
    A class for interacting with the Twitter API and cleaning tweets.
    """
    
    def __init__(self):
        """
        Initialize the Twitter API object.
        """
        auth = tweepy.OAuthHandler(credentials.consumer_key,credentials.consumer_key_secret)
        auth.set_access_token(credentials.access_token, credentials.access_token_secret)
        self.api = tweepy.API(auth)

    def clean_text(self, string: str, punctuations=r'''!()-[]{};:'"\,<>./?@#$%^&*_~''',
                     stop_words=[]):
        """
        Clean the given string by removing hashtags, mentions, links, and specified punctuations and stop words.

        Parameters:
        - string (str): The string to be cleaned.
        - punctuations (str, optional): A string containing the punctuations to be removed. Default is all punctuations.
        - stop_words (list, optional): A list of stop words to be removed. Default is an empty list.
        
        Returns:
        - str: The cleaned string.
        """
        string = re.sub(r'<.*?>', '', string)
        string = re.sub("(@|#)[A-Za-z0-9_]+", "", string)
        string = re.sub(r'http\S+', '', string)
        #string = string.lower()

        #for x in string: 
        #   if x in punctuations: 
        #        string = string.replace(x, "") 

        # Removing stop words
        string = ' '.join([word for word in string.split() if word not in stop_words])
        # Cleaning the whitespaces
        string = re.sub("\s+", " ", string)

        return string  

    def get_tweets_last_year(self, account): 
        """
        Get the tweets of a user from the past year.

        Parameters:
        - account (str): The screen name of the user.

        Returns:
        - tuple: A tuple containing two lists:
            - The first list contains the cleaned tweets.
            - The second list contains the lengths of the original tweets (before cleaning).
        """
        text = []
        lentext = []
        utc = pytz.UTC
        date_now = utc.localize(datetime.now()- relativedelta(years=1))
        for status in tweepy.Cursor(self.api.user_timeline, screen_name=account, tweet_mode="extended").items():
            create_at = status.created_at
            if  (create_at > date_now):
                if status.full_text[:2] != 'RT':
                    lentext.append(len(status.full_text))
                utext = self.clean_text(status.full_text)
                text.append(utext)
            else:
                break
        return text, lentext
