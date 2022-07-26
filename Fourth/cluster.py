import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
import pickle
from preprocess import preprocess

CLUSTER_PATH = 'Cluster.pkl'


def save_object(obj, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)


def load_object(file_name):
    with open(file_name, 'rb') as file:
        return pickle.load(file)


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


class Cluster():

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
        self.kmeans = KMeans(n_clusters=5, init='k-means++',
                             n_init=50, random_state=None).fit(self.doc_term_mat)

    def predict(self, X):
        vectorize_X = self.get_vectorized(X)
        return self.kmeans.predict(vectorize_X)

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
    # valid_languages = ['Java', 'Python', 'Shell', 'C++', 'Go']

    cluster = load_object(CLUSTER_PATH)

    code = ''''''
    code = [preprocess(code)]
    prediction = cluster.predict(code)[0]
    print(prediction)
