from gensim.models.fasttext import FastText
import numpy as np
import pandas as pd
import scipy

from Third.rocchio import Rocchio
from .preprocess import Preprocess


class FastTextModel:

    def __init__(self, data, train=False, k=-1):
        self.data = data
        if train:
            self.ft_model = self.train()
        else:
            self.ft_model = FastText.load('Third/_fasttext.model')
        self.data_embedding = self.get_data_embedding_avg()
        self.k = k

    def get_words(self, doc):
        words = []
        for sent in doc:
            words.extend(sent.split(' '))
        return words

    def get_tok_text(self):
        tok_text = []
        for doc in self.data['readme_html']:
            tok_text.append(self.get_words(doc))
        return tok_text

    def train(self):
        ft_model = FastText(sg=1, size=100, window=10,
                            min_count=2, negative=15, min_n=2, max_n=5)
        tok_text = list(self.data.loc[:, 'text'])
        ft_model.build_vocab(tok_text)
        ft_model.train(
            tok_text,
            epochs=6,
            total_examples=ft_model.corpus_count,
            total_words=ft_model.corpus_total_words)
        ft_model.save('_fasttext.model')  # save
        return ft_model

    def get_data_embedding_avg(self) -> dict:
        '''

        :return: a dict: the keys are the urls of data and the value is the embedding average
        '''
        docs_avg = dict()
        for index, row in self.data.iterrows():
            words = row['text']
            url = row['url']
            docs_avg[url] = np.mean([self.ft_model.wv[word]
                                    for word in words], axis=0)
        return docs_avg

    def get_query_embedding(self, query_tokens):
        return np.mean([self.ft_model.wv[word] for word in query_tokens], axis=0)

    def tokenize_query(self, query: str):
        query = Preprocess().preprocess(query, token=True)
        return query

    def search_query(self, query, expand=False):
        tokens = self.tokenize_query(query)
        q_embedding = self.get_query_embedding(tokens)
        if expand:
            return self.expand_query(q_embedding)
        cosine_sim_values = {}
        for url, embedding_value in self.data_embedding.items():
            cosine_sim_values.update(
                {url: self.cosine_sim(embedding_value, q_embedding)})
        if not expand:
            return self.calculate_best_k(cosine_sim_values)

    def calculate_best_k(self, cosine_sim_values: dict):
        res = sorted(cosine_sim_values.items(),
                     key=lambda x: x[1], reverse=True)[0: self.k]
        final_res = []
        for i, j in res:
            final_res.append(i)
        return final_res

    def cosine_sim(self, x, y):
        return 1 - scipy.spatial.distance.cosine(x, y)

    def expand_query(self, q_embedding):
        _, url, cos_sim = Rocchio().expand_query([x for u, x in self.data_embedding.items(
        )], q_embedding, [u for u, x in self.data_embedding.items()])
        return url[0:self.k]
