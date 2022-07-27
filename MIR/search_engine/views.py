from django.views.generic import FormView

#from Fourth.cluster import load_object
from Third import boolean, preprocess, fasttext, tfidf, bert
from search_engine.forms import InputForm
import Fourth

from Fourth.cluster import load_object, Cluster


class SearchEngine(FormView):
    form_class = InputForm
    template_name = 'search_engine.html'

    def form_valid(self, form):
        input = form.cleaned_data.get('input')
        expansion = 'expansion' in self.request.POST
        type = 'third'
        if 'boolean' in self.request.POST:
            result = self.boolean_retrieval(input, expansion)
        elif 'tfidf' in self.request.POST:
            result = self.tfidf_retrieval(input, expansion)
        elif 'fasttext' in self.request.POST:
            result = self.fasttext_retrieval(input, expansion)
        elif 'transformer' in self.request.POST:
            result = self.transformer_retrieval(input, expansion)
        elif 'elasticsearch' in self.request.POST:
            result = self.elastic_retrieval(input)
        else:
            type = 'forth'
            result = False

        if 'clustering' in self.request.POST:
            result = self.clustering(input)
            result = "The input code belongs to cluster " + str(result)
        if 'classification' in self.request.POST:
            result = self.classification(input)
            result = 'The predicted language is ' + str(result)

        context = self.get_context_data()
        context['result'] = result
        context['type'] = type

        return self.render_to_response(context)

    @staticmethod
    def boolean_retrieval(input, expansion: bool):
        print(type(expansion))
        model = boolean.BooleanRetrival(preprocess.tokens_df)
        if expansion:
            result = model.expand_query(input)
        else:
            result = model.process_query(input)
            result = [x['url'] for x in result]
        return result

    @staticmethod
    def tfidf_retrieval(input, expansion):
        model = tfidf.Tfidf()
        if expansion:
            return model.print_results(input, expand=True)
        else:
            return model.print_results(input)

    @staticmethod
    def fasttext_retrieval(input, expansion):
        ft_model = fasttext.FastTextModel(
            preprocess.tokens_df, train=False, k=10)
        if expansion:
            return ft_model.search_query(input, expand=True)
        else:
            return ft_model.search_query(input)

    @staticmethod
    def transformer_retrieval(input, expansion):
        t_model = bert.TransformerModel(preprocess.readmes_df, load_data=True)
        if expansion:
            return t_model.get_recommendation2(input, expand=True)
        return t_model.get_recommendation2(input)

    @staticmethod
    def elastic_retrieval(input):
        from elasticsearch import Elasticsearch
        from elasticsearch_dsl import Q, Search
        result = []
        es = Elasticsearch("http://localhost:9200")
        query = Q('match', text=input)
        s = Search(using=es, index='my-index').query(query)
        response = s.execute()
        for hit in response:
            result.append(hit.url)
        return result

    @staticmethod
    def clustering(input):
        cluster = load_object('Fourth/Cluster.pkl')

        code = input
        code = [Fourth.preprocess.preprocess(code)]
        prediction = cluster.predict(code)[0]
        return prediction

    @staticmethod
    def classification(input):
        cluster = load_object('Fourth/Classification.pkl')
        code = input
        prediction = cluster.predict_code(code)
        return prediction
