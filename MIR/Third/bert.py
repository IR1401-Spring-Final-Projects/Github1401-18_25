import numpy as np
import torch
from sentence_transformers import SentenceTransformer
import scipy
from Third.preprocess import readmes_df

from .rocchio import Rocchio


class TransformerModel:

    def __init__(self, data, k=10, load_data=True):
        self.k = k
        self.model = SentenceTransformer(
            'distilbert-base-nli-stsb-mean-tokens')
        if torch.cuda.is_available():
            self.model = self.model.to(torch.device("cuda"))
        self.data = data
        self.list_to_string()
        self.set_id()
        if load_data:
            self.embedding = np.load('bert_embedding.npy')
        else:
            self.embedding = self.get_data_embedding()

    def list_to_string(self):
        # Change list of doc string to string
        for i in range(0, len(self.data['readme_html'])):
            self.data['readme_html'][i] = ' '.join(
                map(str, self.data['readme_html'][i]))

    def get_data_embedding(self):
        return self.model.encode(self.data['readme_html'].tolist(), show_progress_bar=True)

    def set_id(self):
        self.data['id'] = range(0, len(self.data))

    def get_recommendation2(self, query, expand=False):
        queries = [query]
        query_embeddings = self.model.encode(queries)
        if expand:
            return self.expand_query(query_embeddings[0])
        number_top_matches = 10
        for query, query_embedding in zip(queries, query_embeddings):
            distances = scipy.spatial.distance.cdist(
                query_embeddings, self.embedding, "cosine")[0]
            results = zip(range(len(distances)), distances)
            results = sorted(results, key=lambda x: x[1])
            temp = []
            for idx, distance in results[0:number_top_matches]:
                temp.append(readmes_df['url'][idx])
            return temp

    def expand_query(self, q_embedding):
        _, url, cos_sim = Rocchio().expand_query(
            self.embedding, q_embedding, np.array(readmes_df['url']))
        temp = []
        for i in range(self.k):
            temp.append(url[0][i])
        return temp[0:self.k]
