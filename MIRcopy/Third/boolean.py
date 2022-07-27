import json 
import random
from copy import deepcopy
from gensim.models import FastText

import Third.preprocess as preprocess

class BooleanRetrival:

    def __init__(self, docs, k = 10):
        self.inverted_index = {}
        self.docs = docs
        self.query_keywords = ['NOT', 'ORNOT', 'OR', 'AND']
        self.k = k 
        self.create_inverted_index()
    
    def create_inverted_index(self):
        for i, row in self.docs.iterrows():
            tokens = row['text']
            url = row['url']
            for word in tokens:
                if word in self.inverted_index.keys():
                    self.inverted_index[word].add(url)
                else:
                    self.inverted_index.update({word:{url}})
    
    def dump_dict_json(self):
        with open('inverted_index.json', 'w') as f:
            f.write(json.dumps(self.inverted_index))

    def add_and_to_query(self, query):
        temp_query = deepcopy(query)
        changed_count = 0 
        for i in range(len(query)-1):
            if query[i] not in self.query_keywords and query[i+1] not in self.query_keywords:
                temp_query.insert(i+1 + changed_count,'AND')
                changed_count +=1 
        return temp_query
    
    def normalize_query(self, query):
        result = []
        for text in query:
            if text not in self.query_keywords:
                result.append(preprocess.Preprocess().preprocess(text, token = False))
            else:
                result.append(text)
        return result
        
    def tokenize_query(self, query):
        query = query.replace('OR NOT', 'ORNOT')
        query = query.split(' ')
        query = self.add_and_to_query(query)
        query = self.normalize_query(query)
        return query
    
    def process_query(self, query, query_expansion = False):
        if not query_expansion:
            query = self.tokenize_query(query)
        if not query[0] in self.inverted_index.keys():
            result = set(self.docs.loc[:,"url"])
        else:
            result = set(self.inverted_index[query[0]])
        i = 1
        while i < len(query):
            result = self.handle_operation(result,query[i+1], query[i])
            i += 2
        res = []
        for i in result:
            res.append({'score':1.0, 'url': i})
        if query_expansion:
            return result
        return res
    
    def handle_operation(self, result:set, second_word:str, operation:str):
        if not second_word in self.inverted_index.keys():
            return result
        second_list = self.inverted_index[second_word]
        if operation == 'AND':
            return result.intersection(second_list)
        elif operation=='OR':
            return result.union(second_list)
        elif operation == 'ORNOT' :
            all_urls = self.docs.loc[:,"url"]
            return result.union((set(preprocess.tokens_df.loc[:,'url'])) - self.inverted_index[second_word])
        elif operation == 'NOT':
            return result - second_list

    def expand_query(self, query):
        ft_model = FastText.load('_fasttext.model')
        query = self.tokenize_query(query)
        all_queries = [query]
        for i in range(5):
            indexes = {}
            for index, part in enumerate(query):
                if part in ['ORNOT', 'NOT', 'OR', 'AND']:
                    continue
                similars = [word for word, percentage in ft_model.most_similar([part]) if percentage>0.85]
                indexes.update({index: similars})
            temp, query = self.generate_queries(indexes, query)
            all_queries.extend(temp)
            all_queries.append(query)
        res = set()
        for query in all_queries:
            res.update(self.process_query(query, True))
        return res
            


    def generate_queries(self, indexes, query):
        final_query = deepcopy(query)
        new_queries = []
        for index, similars in indexes.items():
            if similars:
                final_query[index] = random.choice(similars)
                q = deepcopy(query)
                q[index] = random.choice(similars)
                new_queries.append(q)
        return new_queries, final_query


