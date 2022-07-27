import os
from tkinter import *
from tkHyperLinkManager import HyperlinkManager

from Third import preprocess
from Third import boolean
from functools import partial
import webbrowser


window = Tk()
window.title("Advanced Information Retrieval Project")
window.geometry("1000x572")

#Background
print(os.getcwd())
bg = PhotoImage(file="assets\\background.png")
canvas1 = Canvas(window, width=1000, height=572)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")

#Search Box
input_label = Label(text = "Enter an input:").place(x = 350, y = 50)
input = Text(window, height = 5, width = 60, bg = "gray")
input.place(x=350, y=70)
output = Text(window, height=8, width=60, bg="white")
output.place(x=350, y=310)


def get_input():
    global input
    string = input.get(1.0, "end-1c")
    return string

expansion_var = IntVar()
expansion_btn = Checkbutton(window, text="Query Expansion", variable=expansion_var, onvalue=1, offvalue=0, height=1, width=15).place(x=350, y=170)

#Models-----------------------------------------------------

bool_model = boolean.BooleanRetrival(preprocess.tokens_df)
# tfidf_model = model = Tfidf()
# ft_model = FastTextModel(tokens_df, train=False, k=10)


#Boolean----------------------------------------------

def onclick_boolean():
    if expansion_var.get() == 1:
        result = bool_model.expand_query(get_input())
    else:
        result = bool_model.process_query(get_input())

        result = [x['url'] for x in result]
    output.delete("1.0", "end")
    output.insert(END, "Results:\n ")
    hyperlink = HyperlinkManager(output)
    for i in range(len(result)):
        output.insert(END, f'{i+1}. ')
        output.insert(END,
                result[i], hyperlink.add(partial(webbrowser.open, result[i])))
        output.insert(END, '\n')

boolean_btn = Button(window, text = "Boolean", command=onclick_boolean).place(x=350, y=210)

#Tf-Idf---------------------------------------------
#
# def onclick_tfidf():
#     if expansion_var.get() == 1:
#         result = tfidf_model.print_results(query = get_input(), expand = True)
#         output.insert(END, result)
#     else:
#         result = tfidf_model.print_results(query = get_input())
#         output.insert(END, result)
#
# tfidf_btn = Button(window, text = "Tf-Idf", command=onclick_tfidf).place(x=410, y=210)
#
# #Fasttext---------------------------------------------------------
#
# def onclick_fasttext():
#     if expansion_var.get() == 1:
#         result = ft_model.print_results(query=get_input(), expand=True)
#         output.insert(END, result)
#     else:
#         result = ft_model.print_results(query=get_input())
#         output.insert(END, result)
#
# fasttext_btn = Button(window, text = "Fasttext", command=onclick_fasttext).place(x=455, y=210)

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


#
#
transformer_btn = Button(window, text = "Transformer", command=onclick_transformer).place(x=510, y=210)

elastic_btn = Button(window, text = "Elastic search", command=onclick_elastic).place(x=590, y=210)

pagerank_btn = Button(window, text = "Page Rank", command=onclick_pagerank).place(x=675, y=210)

classification_btn = Button(window, text = "Classification", command=onclick_classification).place(x=350, y=250)

clustering_btn = Button(window, text = "Clustering", command=onclick_clustering).place(x=435, y=250)

mainloop()