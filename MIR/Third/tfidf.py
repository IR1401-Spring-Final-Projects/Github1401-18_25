from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json
from pathlib import Path
from .preprocess import Preprocess
from .rocchio import Rocchio


class Tfidf:

    def __init__(self, file_name='Third/token.json', k=10):
        data = json.loads(Path(file_name).read_text())
        corpus = []
        self.urls = []
        for row in data:
            corpus.append(' '.join(row['text']))
            self.urls.append(row['url'])

        self.vectorizer = TfidfVectorizer(
            input='content',
            lowercase=False,
            analyzer='word',
            ngram_range=(1, 1),
            max_df=0.90,
            min_df=1,
            max_features=None,
            vocabulary=None,
            binary=False,
            norm='l2',
            use_idf=True,
            smooth_idf=True,
            sublinear_tf=True
        )
        self.k = k
        self.X = self.vectorizer.fit_transform(corpus)
        self.words = self.vectorizer.get_feature_names_out().tolist()

    def process_query(self, query, url_num=10, expand=False):
        query = ' '.join(Preprocess().preprocess(query))
        query_embedding = self.vectorizer.transform([query]).T
        if expand:
            return self.expand_query(query_embedding.T)
        score = self.X.dot(query_embedding).toarray()[:, 0]
        max_scores_docs = list(np.argsort(score))

        related_urls = []
        scores = []
        for doc in reversed(max_scores_docs):
            if self.urls[doc] not in related_urls:
                related_urls.append(self.urls[doc])
                scores.append(score[doc])
            if len(related_urls) == url_num:
                break

        return related_urls, scores

    def print_results(self, query, expand=False):
        result = []
        for url, score in zip(*self.process_query(query, expand=expand)):
            result.append(url)
        return result

    def expand_query(self, query):
        _, url, cos_sim = Rocchio().expand_query(
            self.X.toarray(), query.toarray()[0], self.urls)
        return url[0][0:self.k], cos_sim[0][0:self.k]
