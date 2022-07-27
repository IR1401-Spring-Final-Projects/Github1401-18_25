from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, confusion_matrix
from .preprocess import preprocess
from Fourth.main import *


class Classification:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_df=0.9,
            min_df=0.1,
            stop_words=None,
            norm='l2'
        )

    def train(self, X_train, y_train):
        self.y_train = y_train
        self.doc_term_mat = self.vectorizer.fit_transform(X_train)
        self.clf = LogisticRegression(random_state=0, multi_class='multinomial').fit(
            self.doc_term_mat, y_train)

    def predict(self, X):
        vectorize_X = self.get_vectorized(X)
        return self.clf.predict(vectorize_X)

    def predict_code(self, code):
        preprocessed = [preprocess(code)]
        index = self.predict(preprocessed)[0]
        return valid_languages[index]

    def get_vectorized(self, X):
        vectorize_X = self.vectorizer.transform(X)
        return vectorize_X

    def get_accuracy(self, X, y):
        vectorize_X = self.get_vectorized(X)
        return self.clf.score(vectorize_X, y)

    def get_f1_score(self, X, y, average):
        predicted = self.predict(X)
        return f1_score(y, predicted, average=average)

    def get_confusion_matrix(self, X, y):
        predicted = self.predict(X)
        return confusion_matrix(y, predicted, labels=list(range(len(valid_languages))))


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
        raise NotImplementedError'''
    classification = load_object(CLASSIFICATION_PATH)

    code = [preprocess(code)]
    t = classification.predict(code)[0]
    print(valid_languages[t], t)
