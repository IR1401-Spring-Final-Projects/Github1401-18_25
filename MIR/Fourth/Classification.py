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
        preprocessed_code = [preprocess(code)]
        index = self.predict(preprocessed_code)[0]
        language = valid_languages[index]
        return language

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
    code = '''CODE'''
    classification = load_object(CLASSIFICATION_PATH)

    predicted_language = classification.predict_code(code)
    print(predicted_language)
