from tkinter import *
from tkinter import messagebox
import re  # regex


class Application:
    def __init__(self):
        self.root = Tk()
        self.root.title("Disappear Text App")
        self._after_id = None  # job id - needed for tkinter "after" function
        self.wordcount = 0

        self.label = Label(
            text="Please write text below. If you stop writing, after 5 seconds whole text is going "
            "to disappear, have fun!",
            font=("Arial", 10),
        )
        self.label.grid(column=0, row=0, columnspan=2)
        self.label.config(padx=20, pady=10)

        self.word_label = Label(
            text=f"Words: 0",
            font=("Arial", 10, "bold"),
        )
        self.word_label.grid(column=0, row=1, columnspan=2)
        self.word_label.config(padx=20, pady=10)

        self.text_field = Text(height=16, width=80, wrap=WORD)
        self.text_field.grid(column=0, row=2, columnspan=2)
        self.text_field.config(padx=20, pady=20)
        self.text_field.bind("<Key>", self.handle_wait)  # Checks if user stopped typing
        self.text_field.focus()

    def handle_wait(self, event):
        # Cancel the old job
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)

        # Create new job
        self._after_id = self.root.after(5000, self.change_color)  # 5000ms = 5s

        # Count words - uses regex to find all words in text
        words = self.text_field.get("1.0", "end-1c")
        self.wordcount = len(re.findall("\w+", words))
        self.word_label.config(text=f"Words: {self.wordcount}")

    def change_color(self):
        self.text_field.delete(1.0, END)  # Clears whole text
        messagebox.showinfo(
            title="Time is up!",
            message=f"Good job! You have managed to write {self.wordcount} words!",
        )
        self.word_label.config(text=f"Words: 0")  # Reset displayed number of words


app = Application()
app.root.mainloop()
