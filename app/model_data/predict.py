import pickle
import numpy as np
import pandas as pd
import os

from gensim import models, similarities

class predict():
    def __init__(self, query):
        self.df = pd.read_csv('model_data/yoga.csv')
        with open('model_data/dictionary', 'rb') as fp:
            self.dictionary = pickle.load(fp)
        with open('model_data/corpus', 'rb') as fp:
            self.corpus = pickle.load(fp)
        self.index = similarities.MatrixSimilarity.load('model_data/index')
        self.lda = models.LdaModel.load('model_data/lda_model')
        self.query = query
        self.vec_bows = self.dictionary.doc2bow(self.query.lower().split())
        self.vec_lda = self.lda[self.vec_bows]
        self.query_vector = self.lda[self.vec_bows]
        
    def get_similarities(self):
        sims = self.index[self.query_vector]
        return sims

    # def vid_embed(self):
    #     sims = self.get_similarities()
    #     sims = sorted(enumerate(sims), key=lambda item: -item[1])
    #     ids = [(doc_position, doc_score) for doc_position, doc_score in sims[0:9]]
    #     vid_ids = [self.df.iloc[index[0]]['id'] for index in ids]
    #     links = [f'https://www.youtube.com/watch?v={id}' for id in vid_ids]
    #     return embed_table

    def vid_table(self):
        sims = self.get_similarities()
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        ids = [(doc_position, doc_score) for doc_position, doc_score in sims[0:10]]
        # vid_ids = [self.df.iloc[index[0]]['id'] for index in ids]
        to_html = pd.DataFrame(columns=self.df.columns)
        for id in ids:
            to_html = to_html.append(self.df.iloc[id[0]])
        heading = ['title', 'description', 'id']
        for i in to_html.columns:
            if i not in heading:
                to_html.drop(columns=i, inplace=True)
        to_html['id'] = to_html['id'].apply(lambda x: f'https://www.youtube.com/watch?v={x}')
        return to_html

def main():
    query = input('what type of yoga are you looking for? ')
    out = predict(query)
    print(out.vid_table())
        

if __name__ == '__main__':
    main()