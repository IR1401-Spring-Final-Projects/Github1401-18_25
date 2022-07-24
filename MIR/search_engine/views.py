from django.views.generic import FormView

from search_engine.forms import InputForm


class SearchEngine(FormView):
    form_class = InputForm
    template_name = 'search_engine.html'

    def form_valid(self, form):
        input = form.cleaned_data.get('input')

        if 'boolean' in self.request.POST:
            result = self.boolean_retrieval(input)
        if 'tfidf' in self.request.POST:
            result = self.tfidf_retrieval(input)
        if 'fasttext' in self.request.POST:
            result = self.fasttext_retrieval(input)
        if 'transformer' in self.request.POST:
            result = self.transformer_retrieval(input)
        if 'elasticsearch' in self.request.POST:
            result = self.elastic_retrieval(input)

        if 'clustering' in self.request.POST:
            result = self.clustering(input)
        if 'classification' in self.request.POST:
            result = self.classification(input)

        if 'page_rank' in self.request.POST:
            result = self.page_rank(input)
        if 'hits' in self.request.POST:
            result = self.hits(input)

        if 'query_expansion' in self.request.POST:
            result = self.query_expansion(input)

        context = self.get_context_data()
        context['result'] = result

        return self.render_to_response(context)

    @staticmethod
    def boolean_retrieval(input):
        pass

    @staticmethod
    def tfidf_retrieval(input):
        pass

    @staticmethod
    def fasttext_retrieval(input):
        pass

    @staticmethod
    def transformer_retrieval(input):
        pass

    @staticmethod
    def elastic_retrieval(input):
        pass

    @staticmethod
    def clustering(input):
        pass

    @staticmethod
    def classification(input):
        pass

    @staticmethod
    def page_rank(input):
        pass

    @staticmethod
    def hits(input):
        pass

    @staticmethod
    def query_expansion(input):
        pass
