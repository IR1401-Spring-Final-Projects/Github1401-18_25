from django.views.generic import FormView

from Fourth.cluster import load_object
from Third import boolean, preprocess, fasttext, tfidf, bert
from search_engine.forms import InputForm
import Fourth


class SearchEngine(FormView):
    form_class = InputForm
    template_name = 'search_engine.html'

    def form_valid(self, form):
        input = form.cleaned_data.get('input')
        expansion = self.request.POST['expansion'] == 'true'
        if 'boolean' in self.request.POST:
            result = self.boolean_retrieval(input, expansion)
        if 'tfidf' in self.request.POST:
            result = self.tfidf_retrieval(input, expansion)
        if 'fasttext' in self.request.POST:
            result = self.fasttext_retrieval(input, expansion)
        if 'transformer' in self.request.POST:
            result = self.transformer_retrieval(input, expansion)
        if 'elasticsearch' in self.request.POST:
            result = self.elastic_retrieval(input)

        if 'clustering' in self.request.POST:
            result = self.clustering(input)
        if 'classification' in self.request.POST:
            result = self.classification(input)

        context = self.get_context_data()
        context['result'] = result

        return self.render_to_response(context)

    @staticmethod
    def boolean_retrieval(input, expansion: bool):
        print(type(expansion))
        model = boolean.BooleanRetrival(preprocess.tokens_df)
        if expansion:
            result = model.expand_query(input)
        else:
            result = model.process_query(input)
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
        ft_model = fasttext.FastTextModel(preprocess.tokens_df, train=False, k=10)
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
        cluster = load_object('.Fourth/Cluster.pkl')

        code = input
        code = [Fourth.preprocess.preprocess(code)]
        prediction = cluster.predict(code)[0]
        return prediction

    @staticmethod
    def classification(input):
        pass
