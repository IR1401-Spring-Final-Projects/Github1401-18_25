import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
import pickle
from preprocess import preprocess
from main import *


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
        self.kmeans = KMeans(n_clusters=len(valid_languages), init='k-means++',
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
    code = '''#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-02-09 11:28:52

import re

# NOTE: When get/get_all/check_update from database with default fields,
#       all following fields should be included in output dict.
{
    'project': {
        'name': str,
        'group': str,
        'status': str,
        'script': str,
        # 'config': str,
        'comments': str,
        # 'priority': int,
        'rate': int,
        'burst': int,
        'updatetime': int,
    }
}


class ProjectDB(object):
    status_str = [
        'TODO',
        'STOP',
        'CHECKING',
        'DEBUG',
        'RUNNING',
    ]

    def insert(self, name, obj={}):
        raise NotImplementedError

    def update(self, name, obj={}, **kwargs):
        raise NotImplementedError

    def get_all(self, fields=None):
        raise NotImplementedError

    def get(self, name, fields):
        raise NotImplementedError

    def drop(self, name):
        raise NotImplementedError

    def check_update(self, timestamp, fields=None):
        raise NotImplementedError

    def split_group(self, group, lower=True):
        if lower:
            return re.split("\W+", (group or '').lower())
        else:
            return re.split("\W+", group or '')

    def verify_project_name(self, name):
        if len(name) > 64:
            return False
        if re.search(r"[^\w]", name):
            return False
        return True

    def copy(self):
        \'\'\'
        database should be able to copy itself to create new connection

        it's implemented automatically by pyspider.database.connect_database
        if you are not create database connection via connect_database method,
        you should implement this
        \'\'\'
        raise NotImplementedError
'''
    code = [preprocess(code)]
    cluster = load_object(CLUSTER_PATH)
    t = cluster.predict(code)[0]
    print(valid_languages[t], t)
