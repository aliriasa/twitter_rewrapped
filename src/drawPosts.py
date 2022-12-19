import string
import scipy
import math
from PIL import Image, ImageDraw, ImageFont

class DrawTwitterPosts():
    """
    A class for drawing Twitter posts.
    """
    
    def __init__(self, 
            mostCommon,  account, avg_size, total_length,
            hashtag = '#ReWrapped', 
            width = 500, height = 500, 
            font = 'tools/Twitter.ttf'):
        """
        Initializes a DrawTwitterPosts object with the given parameters.

        mostCommon: a list of tuples, each representing the top 3 most common words 
                    in the user's tweets, in the form (word, count)
        account: the Twitter handle of the user
        avg_size: the average length of the user's tweets
        total_length: the total length of all the user's tweets
        hashtag: the hashtag to include in the image, default is '#ReWrapped'
        width: the width of the image, default is 500
        height: the height of the image, default is 500
        font: the font to use in the image, default is 'tools/Twitter.ttf'
        """
        self.topInterests = mostCommon
        self.avg_size = avg_size
        self.total_length = total_length
        self.account = account
        self.hashtag = hashtag
        self.width = width
        self.height = height
        self.font = font
        self.fontt = ImageFont.truetype(font, size=30)
        self.fonth = ImageFont.truetype(font, size=15)

    def get_cat_and_values(self):
        """
        Returns the top 3 most common words in the user's tweets and their respective counts.
        """
        dict = self.topInterests
        return dict[0][0], dict[1][0], dict[2][0], dict[0][1], dict[1][1], dict[2][1],

    def draw_cloud(self):
        """
        Draws an image representing a word cloud.
        """
        title = "#WordCloud"

        img = Image.open('tools/cloud.png', 'r')
        imgDraw = ImageDraw.Draw(img)

        imgDraw.text((165, 50), title, font=self.fontt, fill='white')
        imgDraw.text((165-1, 50-1), title, font=self.fontt, fill='white')
        imgDraw.text((165+1, 50-1), title, font=self.fontt, fill='white')

        imgDraw.text((500-100, 500-25), self.hashtag, font=self.fonth, fill='white')
        imgDraw.text((15, 500-25), "@" + self.account, font=self.fonth, fill='white')

        return img

    def draw_aop(self):
        """
        Draws an image representing whether the user is active or passive 
        on Twitter.
        """
        title = '#ActiveOrPassive?'
        percentile = int((scipy.stats.norm(100, 200).cdf(self.total_length)*100))
        if percentile == 100:
            percentile = 99
        per_day = float(self.total_length/365)

        if percentile < 50:
                label = "PASSIVE"
        else:
            label = "ACTIVE"

        text1 = "You seem to be..."
        text2 = "{:0.2f} tweets per day".format(per_day)
        text3 = str(percentile) + "th percentile"

        fontl = ImageFont.truetype(self.font, size=35)

        img = Image.new('RGB', (self.width, self.height), color='#1c9cf4')
        imgDraw = ImageDraw.Draw(img)

        imgDraw.text((120, 60), title, font=self.fontt, fill='white')
        imgDraw.text((120-1, 60-1), title, font=self.fontt, fill='white')
        imgDraw.text((120+1, 60-1), title, font=self.fontt, fill='white')

        imgDraw.text((500-100, 500-25), self.hashtag, font=self.fonth, fill='white')
        imgDraw.text((15, 500-25), "@" + self.account, font=self.fonth, fill='white')

        imgDraw.text((40, 150), text1, font=self.fontt, fill='white')

        imgDraw.text((110, 280), text2, font=self.fontt, fill='white')
        imgDraw.text((140, 335), text3, font=self.fontt, fill='white')

        imgDraw.text((320, 180), label, font=fontl, fill='white')
        imgDraw.text((320-1, 180-1), label, font=fontl, fill='white')
        imgDraw.text((320+1, 180+1), label, font=fontl, fill='white')

        return img

    def draw_avg_size(self):
        """
        This function generates an image with text displaying the user's 
        average number of characters per tweet.
        """
        title = '#DoYouNeedMoreCharacters?'
        text1 = "You use an average of"
        n = str(int(self.avg_size))
        text2 = "characters per tweet."

        img = Image.new('RGB', (self.width, self.height), color='#1c9cf4')
        imgDraw = ImageDraw.Draw(img)

        fontn = ImageFont.truetype(self.font, size=100)

        h = 210
        if len(n) == 2:
            w = 190
        else:
            w = 160

        imgDraw.text((50, 60), title, font=self.fontt, fill='white')
        imgDraw.text((50-1, 60-1), title, font=self.fontt, fill='white')
        imgDraw.text((50+1, 60-1), title, font=self.fontt, fill='white')

        imgDraw.text((w, h), n, font=fontn, fill='white')
        imgDraw.text((w-1, h-1), n, font=fontn, fill='white')
        imgDraw.text((w+1, h-1), n, font=fontn, fill='white')

        imgDraw.text((500-100, 500-25), self.hashtag, font=self.fonth, fill='white')
        imgDraw.text((15, 500-25), "@" + self.account, font=self.fonth, fill='white')

        imgDraw.text((40, 150), text1, font=self.fontt, fill='white')
        imgDraw.text((180, 360), text2, font=self.fontt, fill='white')

        return img
    
    def draw_top_interests(self):
        """
        This function generates an image with text displaying the user's top interests.
        """
        def font_size(value, total):
            """
            This helper function calculates the font size for a given 
            value based on its proportion to the total.
            """
            percentage = value/total
            return int(32) #int(30 + percentage*3)
        
        title = '#WhatDoYouTalkAbout?'

        img = Image.new('RGB', (self.width, self.height), color='#1c9cf4')
        imgDraw = ImageDraw.Draw(img)

        imgDraw.text((80, 60), title, font=self.fontt, fill='white')
        imgDraw.text((80-1, 60-1), title, font=self.fontt, fill='white')
        imgDraw.text((80+1, 60-1), title, font=self.fontt, fill='white')

        imgDraw.text((500-100, 500-25), self.hashtag, font=self.fonth, fill='white')
        imgDraw.text((15, 500-25), "@" + self.account, font=self.fonth, fill='white')

        if self.topInterests == None:
            return None
        elif len(self.topInterests) < 3:
            cat1 = self.topInterests[0][0]
            value1 = self.topInterests[0][1]

            value1 = font_size(value1, value1)
            font1 = ImageFont.truetype(self.font, size=value1)

            imgDraw.text((30, 255), "1 | " + cat2, font=font2, fill='white')
        else:
            cat1, cat2, cat3, value1, value2, value3 = self.get_cat_and_values()
            total = value1 + value2 + value3

            value1 = font_size(value1, total)
            value2 = font_size(value2, total)
            value3 = font_size(value3, total)

            font1 = ImageFont.truetype(self.font, size=value1)
            font2 = ImageFont.truetype(self.font, size=value2)
            font3 = ImageFont.truetype(self.font, size=value3)

            imgDraw.text((30, 150), "1 | " + cat1, font=font1, fill='white')
            imgDraw.text((30, 255), "2 | " + cat2, font=font2, fill='white')
            imgDraw.text((30, 360), "3 | " + cat3, font=font3, fill='white')

        return img


