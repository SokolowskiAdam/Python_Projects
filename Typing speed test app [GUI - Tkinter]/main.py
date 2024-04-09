from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import messagebox


class TestText:
    def __init__(self):
        self.sample_text = (
            "Trying to make a wise, good choice when thinking about what kinds of careers might be best for you is a "
            "hard thing to do. Your future may very well depend on the ways you go about finding the best job "
            "openings for you in the world of work. Some people will feel that there is one and only one job in the "
            "world for them. Hard thinking and a lot of hard work will help them find the one job that is best for "
            "them. Jobs are there for those with skills and a good work ethic. Many new young artists in the upper "
            "New England states are famous around the world as leaders in new American art."
        )
        self.word_number = 0
        self.text_list = self.sample_text.split()
        self.word_end = 0
        self.correct_words = 0
        self.incorrect_words = 0
        self.timer = None
        self.timer_sec = 60


def highlight_word(event=None):
    if text.text_list:
        # Looking for index of word in sample_text, starting from end of the previous word
        word_start = text.sample_text.index(text.text_list[0], text.word_end)
        text.word_end = word_start + len(text.text_list[0])

        # Check if the word input was correct and highlight with proper color
        if words_entry.get().strip() == text.text_list[0].strip():
            text_field.tag_add("correct", f"1.{word_start}", f"1.{text.word_end}")
            text_field.tag_config("correct", background="green", foreground="white")
            text.correct_words += 1
            score_label.config(
                text=f"Correct: {text.correct_words}   Not correct: {text.incorrect_words}"
            )
            words_entry.delete(0, END)  # clears word input
        else:
            text_field.tag_add("not_correct", f"1.{word_start}", f"1.{text.word_end}")
            text_field.tag_config("not_correct", background="red", foreground="white")
            text.incorrect_words += 1
            score_label.config(
                text=f"Correct: {text.correct_words}   Not correct: {text.incorrect_words}"
            )
            words_entry.delete(0, END)  # clears word input

        # Removes inputted word from the list
        text.text_list.remove(text.text_list[text.word_number])

    else:
        messagebox.showinfo(
            title="All words written",
            message=f"Good job! You have managed to write all words!\nYour score:\n\nCorrect words: {text.correct_words}"
            f"\nNot correct: {text.incorrect_words}\nAll words: {text.correct_words + text.incorrect_words}",
        )


def timer(count):
    # Update text in label
    timer_label["text"] = f"Timer: {count}s"

    if count > 0:
        # call countdown again after 1000ms (1s)
        text.timer = window.after(1000, timer, count - 1)
    else:
        messagebox.showinfo(
            title="Time Up",
            message=f"Your score:\n\nCorrect words: {text.correct_words}\nNot correct: {text.incorrect_words}"
            f"\nAll words: {text.correct_words + text.incorrect_words}",
        )


def start_test():
    # New test - fresh statistics
    global text
    text = TestText()

    # Start countdown
    timer(text.timer_sec)

    words_entry.delete(0, END)
    words_entry.bind("<space>", highlight_word)  # Space button approves input
    score_label.config(text=f"Correct: 0  |  Not correct: 0")  # Reset displayed scores

    # Remove existing tags from text:
    for tag in text_field.tag_names():
        text_field.tag_delete(tag)


# ----- GUI -----
text = TestText()

window = Tk()
window.title("Typing Speed Test")
window.config(padx=50, pady=50)

score_label = Label(
    text=f"Correct: {text.correct_words}  |  Not correct: {text.correct_words}"
)
score_label.grid(column=1, row=0, sticky=E)
score_label.config(pady=10)

timer_label = Label(text=f"Timer: {text.timer_sec}s")
timer_label.grid(column=0, row=0, sticky=W)
timer_label.config(pady=10)

text_field = Text(height=12, width=60, wrap=WORD)
text_field.insert(INSERT, text.sample_text)
text_field.grid(column=0, row=1, columnspan=2)
text_field.config(padx=20, pady=20)

words_entry = Entry(width=50, bg="#9bdeac")
words_entry.insert(END, string="Type words here, press SPACE to approve word.")
words_entry.grid(column=0, row=2, columnspan=2, padx=20, pady=20)

start_button = Button(
    text="Start Test",
    font=("Arial", 12, "bold"),
    command=start_test,
    padx=20,
    pady=30,
    borderwidth=1,
)
start_button.grid(column=0, row=3, columnspan=2)


window.mainloop()
