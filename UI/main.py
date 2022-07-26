from tkinter import *

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

boolean_btn = Button(window, text = "Boolean")
boolean_btn.place(x=350, y=300)

tfidf_btn = Button(window, text = "Tf-Idf")
tfidf_btn.place(x=410, y=300)

fasttext_btn = Button(window, text = "Fasttext")
fasttext_btn.place(x=455, y=300)

transformer_btn = Button(window, text = "Transformer")
transformer_btn.place(x=510, y=300)

elastic_btn = Button(window, text = "Elastic search")
elastic_btn.place(x=590, y=300)

#Query Expansion
expansion_var = IntVar()
expansion_btn = Checkbutton(window, text="Query Expansion", variable=expansion_var, onvalue=1, offvalue=0, height=1, width=15)
expansion_btn.place(x=350, y=250)

# output.pack()
mainloop()