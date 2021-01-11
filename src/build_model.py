import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import numpy as np
import pandas as pd
import string
import re
import pickle

from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities
import gensim

from cleaner import cleaner

class model():
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.cleaner = cleaner()
        self.cleaned_df = self.clean_df()
        self.dictionary, self.corpus = self.create_dictionary()
        self.lda = self.create_model()

    def clean_df(self):
        self.df['description'].fillna('none', inplace=True)
        self.df['tags'].fillna('none', inplace=True)
        self.df['description'].apply(self.cleaner.take_head)
        columns = ['title', 'description', 'tags']
        for column in columns:
            self.df[column] = self.df[column].apply(self.cleaner.clean_text)
        self.df['text'] = self.df['title'].apply(str.split) + self.df['description'].apply(str.split) + self.df['tags'].apply(str.split)
        return self.df

    def create_dictionary(self):
        frequency = defaultdict(int)
        for text in self.df['text']:
            for token in text:
                frequency[token] += 1

        texts = [
            [token for token in text if frequency[token] > 1]
            for text in self.df['text']
        ]
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        return dictionary, corpus

    def create_model(self):
        lda = models.LdaMulticore(self.corpus, id2word=self.dictionary, num_topics=12, passes=50)
        return lda

if __name__ == '__main__':
    data_path = '../data/yoga.csv'
    model = model(data_path)
    # Save resources
    model.lda.save('../app/model_data/lda_model')
    with open('../app/model_data/dictionary', 'wb') as fp:
        pickle.dump(model.dictionary, fp)
    with open('../app/model_data/corpus', 'wb') as fp:
        pickle.dump(model.corpus, fp)