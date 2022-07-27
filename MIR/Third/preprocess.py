import os
from pathlib import Path
import nltk
import string
import json

import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


class Preprocess:

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()

    def remove_emoji(self, string):
        b'\\U0001f923'
        emoj = re.compile("["
                          u"\U0001F600-\U0001F64F"  # emoticons
                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          u"\U00002500-\U00002BEF"  # chinese char
                          u"\U00002702-\U000027B0"
                          u"\U00002702-\U000027B0"
                          u"\U000024C2-\U0001F251"
                          u"\U0001f926-\U0001f937"
                          u"\U00010000-\U0010ffff"
                          u"\u2640-\u2642"
                          u"\u2600-\u2B55"
                          u"\u200d"
                          u"\u23cf"
                          u"\u23e9"
                          u"\u231a"
                          u"\ufe0f"  # dingbats
                          u"\u3030"
                          "]+", re.UNICODE)
        return emoj.sub(r'', string)

    def normalize_tokens(self, tokens, remove_stopword, stopwords_domain=['https']):

        # Remove stopwords
        if remove_stopword:
            stopwords = [x.lower()
                         for x in nltk.corpus.stopwords.words('english')]
            normalized_tokens = [word for word in tokens if (
                word.lower() not in stopwords_domain + stopwords)]
        else:
            normalized_tokens = tokens

        # remove links
        normalized_tokens = [
            word for word in normalized_tokens if not re.match(r'^//.*(/?)$', word)]

        # Remove punctuations
        normalized_tokens = [
            word for word in normalized_tokens if word not in string.punctuation]

        # Convert everything to lowercase
        normalized_tokens = [word.lower() for word in normalized_tokens]

        normalized_tokens = [
            word for word in normalized_tokens if len(word) > 1]

        # Convert numbers to "Number" token
        normalized_tokens = [word if not re.match(
            r'(^| )\d+(\.\d+)*($| )', word) else 'NUMBER' for word in normalized_tokens]

        return normalized_tokens

    def isEnglish(self, s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    def non_english(self, text):
        t_list = word_tokenize(text)
        res = []
        for i in t_list:
            if self.isEnglish(i):
                res.append(i)
        return ' '.join(res)

    def preprocess(self, text, lemmatize=True, remove_stopword=True, token=True, re_sub_domain='\'|`|-'):

        # remove non enlish
        text = self.non_english(text)

        # replace sub_domain with space
        text = re.sub(re_sub_domain, ' ', text)

        # remove emoji
        text = self.remove_emoji(text)

        tokens = word_tokenize(text)

        # normalization
        tokens = self.normalize_tokens(tokens, remove_stopword)

        # lemmatization
        if lemmatize:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]

        if token:
            return tokens
        else:
            return ' '.join(tokens)

    def get_preprocessed_token(self, file_path='readmes.json'):
        data = json.loads(Path(file_path).read_text())
        docs = []
        for row in data:
            text = row['readme_html']
            preprocessed_tokens = []
            for paragraph in text:
                preprocessed_tokens += self.preprocess(paragraph)
            docs.append({'url': row['url'], 'text': preprocessed_tokens})
        Path('token.json').write_text(json.dumps(docs))

    def get_preprocessed_str(self, file_path='readmes.json'):
        data = json.loads(Path(file_path).read_text())
        docs = []
        for row in data:
            text = row['readme_html']
            preprocessed_paragraphs = []
            for paragraph in text:
                preprocessed_paragraphs.append(self.preprocess(
                    paragraph, lemmatize=False, remove_stopword=False, token=False))
            docs.append({'url': row['url'], 'text': preprocessed_paragraphs})
        Path('string.json').write_text(json.dumps(docs))


print(os.getcwd())
readmes_df = pd.read_json('Third/readmes.json', orient='records')
tokens_df = pd.read_json('Third/token.json', orient='records')
paragraph_df = pd.read_json('Third/string.json', orient='records')
