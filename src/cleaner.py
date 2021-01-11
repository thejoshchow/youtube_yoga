import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import numpy as np
import pandas as pd
import string
import re

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

class cleaner():
    def __init__(self):

        # punctuation and stopwords
        self.punctuation = set(string.punctuation)
        self.stop_words = stopwords.words('english')
        yoga_stopwords = ['yoga', 'music', 'minute', 'min', 'music', 'teach', 'practice', 'song', 'class', 'playlist', 'none', 'facebook', 'instagram', 'online', 'web', 'exercise', 'video', 'workout', 'free', 'program', 'body', 'full', 'day', 'sound', 'channel', 'pose', 'de', 'fitness', 'kid', 'teacher' ,'series', 'life']
        self.stop_words.extend(yoga_stopwords)

        # LDA
        self.lem = WordNetLemmatizer()

    def take_head(self, text):
        head = text.partition('\n\n')
        return head[0]

    def no_emojis(self, text):
        return text.encode('ascii', 'ignore').decode('ascii')

    def remove_hyperlinks(self, text):
        return re.sub(r'(https?:\/\/\S*)|(www.\S+)}', '', text)

    def remove_punctuation(self, text):
        return ''.join([char for char in text.lower() if char not in string.punctuation])

    def remove_numbers(self, text):
        return ''.join([char for char in text if not char.isdigit()])

    def remove_single_char(self, text):
        return ' '.join([word for word in text.split() if len(word) > 1])

    def remove_stopwords(self, text):
        return ' '.join([word for word in text.split() if word not in self.stop_words])

    def lemmatize_text(self, text):
        return ' '.join([self.lem.lemmatize(word) for word in text.split()])

    def clean_text(self, text):
        text = self.no_emojis(text)
        text = self.remove_hyperlinks(text)
        text = self.remove_punctuation(text)
        text = self.remove_numbers(text)
        text = self.remove_single_char(text)
        text = self.lemmatize_text(text)
        text = self.remove_stopwords(text)
        return text

if __name__ == '__main__':
    # df = pd.read_csv('../data/yoga.csv')
    # cleaner = cleaner()
    # df['description'].fillna('none', inplace=True)
    # df['description'].apply(cleaner.take_head)
    pass