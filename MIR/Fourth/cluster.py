import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
from Fourth.main import *
from Fourth.preprocess import preprocess


def purity_score(y_true, y_pred):
    y_voted_labels = np.zeros(y_true.shape)
    labels = np.unique(y_true)
    ordered_labels = np.arange(labels.shape[0])
    for k in range(labels.shape[0]):
        y_true[y_true == labels[k]] = ordered_labels[k]
    labels = np.unique(y_true)
    bins = np.concatenate((labels, [np.max(labels)+1]), axis=0)

    for cluster in np.unique(y_pred):
        hist, _ = np.histogram(y_true[y_pred == cluster], bins=bins)
        winner = np.argmax(hist)
        y_voted_labels[y_pred == cluster] = winner
    return accuracy_score(y_true, y_voted_labels)


class Cluster:

    def __init__(self, load=False):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_df=0.9,
            min_df=0.008,
            stop_words=None,
            norm='l2'
        )

    def train(self, X_train, y_train):
        self.y_train = y_train
        self.doc_term_mat = self.vectorizer.fit_transform(X_train)
        self.kmeans = KMeans(n_clusters=len(valid_languages), init='k-means++',
                             n_init=50, random_state=None).fit(self.doc_term_mat)

    def predict(self, X):
        vectorize_X = self.get_vectorized(X)
        return self.kmeans.predict(vectorize_X)

    def predict_code(self, code):
        preprocessed_code = [preprocess(code)]
        index = self.predict(preprocessed_code)[0]
        return index

    def get_purity_score(self, X=None, y=None, train=False):
        if train:
            return purity_score(self.y_train, self.kmeans.labels_)
        else:
            return purity_score(y, self.predict(X))

    def get_RSS(self):
        return self.kmeans.inertia_

    def get_vectorized(self, X):
        vectorize_X = self.vectorizer.transform(X)
        return vectorize_X


if __name__ == '__main__':
    code = '''CODE'''
    cluster = load_object(CLUSTER_PATH)
    cluster_number = cluster.predict_code(code)
    print(cluster_number)
