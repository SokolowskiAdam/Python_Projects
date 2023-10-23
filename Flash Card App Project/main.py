"""
App which can be used for learning French. It draws French word from the list of words stored in CSV file and shows
it -> next user chooses if he knows following word or not (tick or cross). If user knows the word, it is removed
from main file (with the words to learn), so user can always go back to the list of words he needs to learn.
"""
# ---------------------------- IMPORTS ------------------------------- #
from tkinter import *
import pandas as pd
import random
from tkinter import messagebox

# ---------------------------- WORDS ------------------------------- #
try:
    df_words = pd.read_csv(r"data/words_to_learn.csv")
    words_dicts = df_words.to_dict(orient="records")
except FileNotFoundError:
    df_words = pd.read_csv(r"data/french_words.csv")
    words_dicts = df_words.to_dict(orient="records")

word_number = None


def next_card() -> None:
    global word_number, flip_timer

    window.after_cancel(flip_timer)  # timer reset
    word_number = random.randint(0, len(words_dicts) - 1)
    random_french_word = words_dicts[word_number]["French"]

    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=random_french_word, fill="black")
    canvas.itemconfig(card_background, image=image_card_front)

    flip_timer = window.after(
        3000, flip_card
    )


def flip_card() -> None:
    random_english_word = words_dicts[word_number]["English"]
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=random_english_word, fill="white")
    canvas.itemconfig(card_background, image=image_card_back)


def is_known() -> None:
    if word_number is not None and (len(words_dicts) - 1) > 0:
        # Delete known word
        words_dicts.remove(words_dicts[word_number])
        # Save it to csv
        df_words_dicts = pd.DataFrame(data=words_dicts)
        df_words_dicts.to_csv("data/words_to_learn.csv", index=False)
        next_card()
    else:
        messagebox.showinfo(
            title="Congratulations",
            message="That was the last word.\nCongratulations. You know "
            "every word from the list!",
        )


# ---------------------------- UI SETUP ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"

# Window configuration
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

# Images
check_image = PhotoImage(file=r"images/right.png")
cross_image = PhotoImage(file=r"images/wrong.png")
image_card_front = PhotoImage(file=r"images/card_front.png")
image_card_back = PhotoImage(file=r"images/card_back.png")

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_background = canvas.create_image(400, 263, image=image_card_front)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
known_button = Button(
    image=check_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=is_known
)
known_button.grid(column=1, row=1)

unknown_button = Button(
    image=cross_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card
)
unknown_button.grid(column=0, row=1)

next_card()

window.mainloop()
