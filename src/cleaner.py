import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import numpy as np
import pandas as pd
import string
import re

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

from collections import defaultdict
from gensim import corpora
import gensim

class cleaner():
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)

        # punctuation and stopwords
        self.punctuation = set(string.punctuation)
        self.stop_words = stopwords.words('english')

        # LDA
        self.dictionary = corpora.Dictionary()
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

    def main(self):
        self.df['description'].apply(self.take_head)
        self.df['description'].fillna('none', inplace=True)
        self.df['tags'].fillna('none', inplace=True)
        channel_stop = list(self.df['channelTitle'].unique())
        self.stop_words.extend(channel_stop)
        columns = ['title', 'description', 'tags']
        for column in columns:
            self.df[column] = self.df[column].apply(self.clean_text)
        self.df['text'] = self.df['title'].apply(str.split) + self.df['description'].apply(str.split) + self.df['tags'].apply(str.split)

if __name__ == '__main__':
    pass