import random
from tkinter import *
from tkinter.ttk import Combobox

import pandas

LANGUAGES = ['English', 'Spanish', 'Greek', 'Portuguese', 'German', 'Turkish', 'Vietnamese', 'Italian', 'Polish',
             'Russian', 'Japanese']
FONT_NAME = 'Arial'
BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Multi-Lingual Flash Card")
window.config(padx=50, pady=20, bg=BACKGROUND_COLOR)
window.geometry('+280+20')

language_choices = []


# ------------------------ DIALOG BOX SETUP ----------------------------------
def close_db():
    global language_choices
    language_choices = [lang1_var.get(), lang2_var.get()]
    top.destroy()


top = Toplevel(window)
top.title("Dialog Box")
top.config(padx=40, pady=30)
top.wm_transient(window)

# CENTERING DIALOG BOX ON SCREEN
w = 400
h = 185
sw = top.winfo_screenwidth()
sh = top.winfo_screenheight()
x = (sw - w) // 2
y = (sh - h) // 2
top.geometry(f'{w}x{h}+{x}+{y}')

lang1_lb = Label(top, text="Foreign Language:", font=(FONT_NAME, 11, 'normal'))
lang1_lb.grid(row=0, column=0, pady=10)
lang1_var = StringVar()
lang1_cb = Combobox(top, textvariable=lang1_var, state='readonly', font=(FONT_NAME, 11, 'italic'))
lang1_cb['values'] = LANGUAGES
lang1_cb.current(1)
lang1_cb.grid(row=0, column=1)

lang2_lb = Label(top, text=" Native Language:", font=(FONT_NAME, 11, 'normal'))
lang2_lb.grid(row=1, column=0, pady=10)
lang2_var = StringVar()
lang2_cb = Combobox(top, textvariable=lang2_var, font=(FONT_NAME, 11, 'italic'), state='readonly')
lang2_cb['values'] = LANGUAGES
lang2_cb.current(0)
lang2_cb.grid(row=1, column=1)

cont_btn = Button(top, text='Continue')
cont_btn.config(font=(FONT_NAME, 14, 'normal'), bg=BACKGROUND_COLOR, command=close_db)
cont_btn.grid(row=2, column=1, sticky='e')

# ----------------------------- CARD UI SETUP ----------------------------------
window.wait_window(top)

lang1 = language_choices[0]
lang2 = language_choices[1]

current_card = {}
words_to_learn = {}

try:
    data_file = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data_file = pandas.read_csv('data/flash_card_wordlist.csv')
    words_to_learn = original_data_file.to_dict(orient='records')
else:
    words_to_learn = data_file.to_dict(orient='records')


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn)
    canvas.itemconfig(card_cover, image=front_img)
    canvas.itemconfig(card_title, text=lang1, fill='black')
    canvas.itemconfig(card_word, text=current_card[lang1], fill='black')
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_cover, image=back_img)
    canvas.itemconfig(card_title, text=lang2, fill='white')
    canvas.itemconfig(card_word, text=current_card[lang2], fill='white')


def is_known():
    words_to_learn.remove(current_card)
    df = pandas.DataFrame(words_to_learn)
    df.to_csv(path_or_buf='data/words_to_learn.csv', index=False)
    next_card()


flip_timer = window.after(3000, flip_card)

front_img = PhotoImage(file='images/card_front.png')
back_img = PhotoImage(file='images/card_back.png')

canvas = Canvas(window, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_cover = canvas.create_image(400, 268, image=front_img)
card_title = canvas.create_text(400, 120, text='', font=(FONT_NAME, 50, 'bold'))
card_word = canvas.create_text(400, 300, text='', font=(FONT_NAME, 70, 'normal'))
canvas.grid(row=0, columnspan=2, column=0)

check_img = PhotoImage(file='images/right.png')
known_btn = Button(window, image=check_img)
known_btn.config(relief='flat', bg=BACKGROUND_COLOR, command=is_known)
known_btn.grid(row=1, column=1)

cross_img = PhotoImage(file='images/wrong.png')
un_known_btn = Button(window, image=cross_img)
un_known_btn.config(relief='flat', bg=BACKGROUND_COLOR, command=next_card)
un_known_btn.grid(row=1, column=0)

next_card()
window.mainloop()
