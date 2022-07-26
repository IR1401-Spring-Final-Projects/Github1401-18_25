from tkinter import *
import funcs

window = Tk()
window.title("Advanced Information Retrieval Project")
window.geometry("1000x572")

#Background
bg = PhotoImage(file="asset/background.png")
canvas1 = Canvas(window, width=1000, height=572)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")

#Search Box
def Take_input():
    inp = input.get("1.0", "end-1c")
    print(inp)
    # if isinstance(inp, not str):
    #     output.insert(END, "Wrong input format")

input = Text(window, height = 8, width = 60, bg = "white")
input.place(x=350, y=100)

#Buttons

boolean_btn = Button(window, text = "Boolean", command=funcs.onclick_boolean())
boolean_btn.place(x=350, y=300)

tfidf_btn = Button(window, text = "Tf-Idf", command=funcs.onclick_tfidf())
tfidf_btn.place(x=410, y=300)

fasttext_btn = Button(window, text = "Fasttext", command=funcs.onclick_fasttext())
fasttext_btn.place(x=455, y=300)

transformer_btn = Button(window, text = "Transformer", command=funcs.onclick_transformer())
transformer_btn.place(x=510, y=300)

elastic_btn = Button(window, text = "Elastic search", command=funcs.onclick_elastic())
elastic_btn.place(x=590, y=300)

pagerank_btn = Button(window, text = "Page Rank", command=funcs.onclick_pagerank())
pagerank_btn.place(x=675, y=300)

classification_btn = Button(window, text = "Classification", command=funcs.onclick_classification())
classification_btn.place(x=350, y=350)

clustering_btn = Button(window, text = "Clustering", command=funcs.onclick_clustering())
clustering_btn.place(x=435, y=350)

#Query Expansion

expansion_var = IntVar()
def is_checked():
    if expansion_var.get() == 1:
        #using query expansion
        pass
    else:
        pass
expansion_btn = Checkbutton(window, text="Query Expansion", variable=expansion_var, onvalue=1, offvalue=0, height=1, width=15, command=is_checked())
expansion_btn.place(x=350, y=250)


# output.pack()
mainloop()