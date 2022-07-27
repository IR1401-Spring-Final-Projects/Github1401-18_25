import numpy as npimport pandas as pdimport faissimport torchfrom sentence_transformers import SentenceTransformerimport scipy from operator import itemgetterfrom Third.preprocess import readmes_dffrom .rocchio import Rocchioclass TransformerModel:    def __init__(self, data, k = 10, load_data = True):        self.k = 10        self.model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')        if torch.cuda.is_available():            model = self.model.to(torch.device("cuda"))        self.data = data        self.list_to_string()        self.set_id()        if load_data:            self.embedding = np.load('bert_embedding.npy')        else:            self.embedding = self.get_data_embedding()        self.index = self.set_indexes()    def list_to_string(self):      #Change list of doc string to string        for i in range(0, len(self.data['readme_html'])):          self.data['readme_html'][i] = ' '.join(map(str, self.data['readme_html'][i]))    def get_data_embedding(self):        return self.model.encode(self.data['readme_html'].tolist(), show_progress_bar=True)    def vector_search(self, query, model, index, num_results=10):        vector = model.encode(list(query))        D, I = index.search(np.array(vector).astype("float32"), k=num_results)        return D, I    def set_id(self):        self.data['id'] = range(0, len(self.data))        def set_indexes(self):        embeddings = np.array([embedding for embedding in self.embedding]).astype("float32")        index = faiss.IndexFlatL2(embeddings.shape[1])        index = faiss.IndexIDMap(index)        index.add_with_ids(embeddings, self.data.id.values)        return index    def get_recommendation(self, user_query):        D, I = self.vector_search([user_query], self.model, self.index, num_results=10)        print(f'L2 distance: {D.flatten().tolist()}\n\nReadme IDs: {I.flatten().tolist()}')        return [self.data['url'][i] for i in I.flatten().tolist()]    def get_recommendation2(self, query, expand = False):        queries = [query]        query_embeddings = self.model.encode(queries)        if expand:            return self.expand_query(query_embeddings[0])        number_top_matches = 10        for query, query_embedding in zip(queries, query_embeddings):            distances = scipy.spatial.distance.cdist(query_embeddings, self.embedding, "cosine")[0]            results = zip(range(len(distances)), distances)            results = sorted(results, key=lambda x: x[1])            temp = []            for idx, distance in results[0:number_top_matches]:              temp.append(str(1-distance) + ' ' + readmes_df['url'][idx])            return temp    def expand_query(self,q_embedding ):        _, url, cos_sim = Rocchio().expand_query(self.embedding,q_embedding, np.array(readmes_df['url']))        print('212')        temp = []        for i in range(self.k):            temp.append(str(cos_sim[0][i]) + ' '+ url[0][i])        return temp