from tkinter import *
import funcs
# import Third.boolean.BooleanRetrival
# import Third.preprocess.tokens_df

from ..Third.boolean import BooleanRetrival
from ..Third.preprocess import tokens_df

window = Tk()
window.title("Advanced Information Retrieval Project")
window.geometry("1000x572")

#Background
bg = PhotoImage(file="assets/background.png")
canvas1 = Canvas(window, width=1000, height=572)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")

#Search Box
input_label = Label(text = "Enter an input:").place(x = 350, y = 120)

def Take_input():
    inp = input.get("1.0", "end-1c")

input = Text(window, height = 8, width = 60, bg = "gray").place(x=350, y=150)

output = Text(window, height=8, width=60, bg="white").place(x=350, y=400)

#Buttons

boolean_btn = Button(window, text = "Boolean", command=funcs.onclick_boolean()).place(x=350, y=350)

# tfidf_btn = Button(window, text = "Tf-Idf", command=funcs.onclick_tfidf()).place(x=410, y=350)
#
# fasttext_btn = Button(window, text = "Fasttext", command=funcs.onclick_fasttext()).place(x=455, y=350)
#
# transformer_btn = Button(window, text = "Transformer", command=funcs.onclick_transformer()).place(x=510, y=350)
#
# elastic_btn = Button(window, text = "Elastic search", command=funcs.onclick_elastic()).place(x=590, y=350)
#
# pagerank_btn = Button(window, text = "Page Rank", command=funcs.onclick_pagerank()).place(x=675, y=350)
#
# classification_btn = Button(window, text = "Classification", command=funcs.onclick_classification()).place(x=350, y=400)
#
# clustering_btn = Button(window, text = "Clustering", command=funcs.onclick_clustering()).place(x=435, y=400)

#Query Expansion

expansion_var = IntVar()
model = BooleanRetrival(tokens_df)

def is_checked():
    if expansion_var.get() == 1:
        result = model.expand_query('Hardware cores OR Arduino AND API')
        output.insert(END, result)
    else:
        result = model.process_query('Hardware cores OR Arduino AND API')
        output.insert(END, result)
expansion_btn = Checkbutton(window, text="Query Expansion", variable=expansion_var, onvalue=1, offvalue=0, height=1, width=15, command=is_checked()).place(x=350, y=300)

# output.pack()
mainloop()