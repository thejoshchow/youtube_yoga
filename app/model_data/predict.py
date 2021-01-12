import pickle
import numpy as np
import pandas as pd
import os

from gensim import models, similarities

class predict():
    def __init__(self, query):
        self.df = pd.read_csv('../../data/yoga.csv')
        with open('dictionary', 'rb') as fp:
            self.dictionary = pickle.load(fp)
        with open('corpus', 'rb') as fp:
            self.corpus = pickle.load(fp)
        self.index = similarities.MatrixSimilarity.load('index')
        self.lda = models.LdaModel.load('lda_model')
        self.query = query
        self.vec_bows = self.dictionary.doc2bow(self.query.lower().split())
        self.vec_lda = self.lda[self.vec_bows]
        self.query_vector = self.lda[self.vec_bows]
        
    def get_similarities(self):
        sims = self.index[self.query_vector]
        return sims

    def vid_ids(self):
        sims = self.get_similarities()
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        ids = [(doc_position, doc_score) for doc_position, doc_score in sims]
        vid_ids = [self.df.iloc[index[0]]['id'] for index in ids]
        links = [f'https://www.youtube.com/watch?v={id}' for id in vid_ids]
        return links

def main():
    query = input('what type of yoga are you looking for? ')
    out = predict(query)
    print(out.vid_ids())
        

if __name__ == '__main__':
    main()