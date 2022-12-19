from collections import Counter
from operator import le
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import random
from wordcloud import STOPWORDS
import numpy as np

class ApplyModel():
    """
    ApplyModel is a class that takes in a trained machine learning model and a list of tweets 
    and predicts the top three interests of the user based on the tweets. 
    It also generates a word cloud of the tweets.

    Attributes:
        model (object): a trained machine learning model
        model_tweets (list): a list of tweets to be used for prediction and word cloud generation
        categories (list): a list of categories available for analysis

    Methods:
        top_interests(tweets): predicts the top three interests of the user based on the tweets
        word_cloud(): generates a word cloud of the tweets
    """
    
    def __init__(self, model):
        """
        Initializes the ApplyModel class with a trained machine learning model.

        Args:
            model (object): a trained machine learning model
        """
        self.model = model
        self.model_tweets = None

    # categories available for analysis
    categories = ['automotive', 'beauty', 'books & literature', 'business',
       'careers', 'education', 'events', 'family & parenting', 'fashion',
       'finance', 'food & drinks', 'gaming', 'health', 'hobbies',
       'home & garden', 'law, government & politics',
       'movies & television', 'music & radio', 'pets', 'science',
       'sports', 'tech & computing', 'travel']

    def top_interests(self, tweets):
        """
        Predicts the top three interests of the user based on the tweets.

        Args:
            tweets (list): a list of tweets to be used for prediction

        Returns:
            dict_values.most_common(3) (tuple): a tuple of the top three interests and their frequency in the tweets
        """

        model_tweets = []
        for tweet in tweets:
            if len(tweet.split(' ')) > 7:
                model_tweets.append(tweet)

        self.model_tweets = model_tweets

        predicts = self.model.predict(self.model_tweets, batch_size=32)
        predict_logits = predicts.argmax(axis=1)

        array = []
        for pre in predict_logits:
            array.append(self.categories[pre])

        dict_values = Counter(array)

        if len(dict_values) == 0:
            return None
        else:
            return dict_values.most_common(3)

    def word_cloud(self):
        """
        Generates a word cloud of the tweets.
        """
        def white_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
            """
            Determines the style of the word cloud.
            """
            return "hsl(0, 100%%, 100%d%%)" % random.randint(60, 100)
        
        review_words = ""
        for sentence in self.model_tweets:
            review_words = review_words + " " + sentence
        
        tmask = np.array(Image.open("tools/twitter.jpg"))
        stopwords = open('tools/stopwords.txt').read().split()
        
        wc = WordCloud(stopwords= stopwords + list(STOPWORDS), 
                        normalize_plurals = True, 
                        color_func=white_color_func, 
                        background_color='#1c9cf4', 
                        max_words=90, 
                        mask=tmask,
                        width=500, height=500)
        wc.generate(review_words)
        wc.to_file('tools/cloud.png')