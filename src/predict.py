import pickle
import numpy as np
import pandas as pd
import argparse

from gensim import models, similarities

class predict():
    def __init__(self, query):
        self.df = pd.read_csv('../data/yoga.csv')
        with open('../app/model_data/dictionary', 'rb') as fp:
            self.dictionary = pickle.load(fp)
        with open('../app/model_data/corpus', 'rb') as fp:
            self.corpus = pickle.load(fp)
        self.lda = models.LdaModel.load('../app/model_data/lda_model')
        self.query, self.duration = query
        self.vec_bows = self.dictionary.doc2bow(self.query.lower().split())
        self.vec_lda = self.lda[self.vec_bows]
        self.query_vector = self.lda[self.vec_bows]
        

    def get_query(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-q', '--query', dest='query')
        values = parser.parse_args()
        if (values.query):
            query = values.query
        return query

    def get_similarities(self):
        index = similarities.MatrixSimilarity(self.lda[self.corpus])
        sims = index[self.query_vector]
        return sims

    def vid_ids(self):
        sims = self.get_similarities()
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        top_10 = [(doc_position, doc_score) for doc_position, doc_score in sims[0:10]]
        vid_ids = [self.df.iloc[index[0]]['id'] for index in top_10]
        links = [f'https://www.youtube.com/watch?v={id}' for id in vid_ids]
        return sims

    def filter_duration(self):
        df

def main():
    query = (input('what type of yoga are you looking for? '), input('duration: ')
    out = predict(query)
    print(out.vid_ids())
        

if __name__ == '__main__':
    main()