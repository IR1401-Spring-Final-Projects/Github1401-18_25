def onclick_boolean():
    if expansion_var.get() == 1:
        result = model.expand_query(string)
        output.insert(END, result)
    else:
        result = model.process_query(string)
        output.insert(END, result)


def onclick_tfidf():
    pass


def onclick_fasttext():
    pass


def onclick_transformer():
    pass


def onclick_elastic():
    pass


def onclick_pagerank():
    pass


def onclick_classification():
    pass


def onclick_clustering():
    pass
