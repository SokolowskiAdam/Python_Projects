"""
Simple Miles to Kilometers converter
"""

from tkinter import *

# Creating a new window and configurations
window = Tk()
window.title("Mile to Km Converter")
window.config(padx=20, pady=20)


def miles_to_km() -> None:
    miles = float(miles_input.get())
    kilometers = round(miles * 1.6093)
    km_result_label.config(text=kilometers)


# Entry
miles_input = Entry(width=7)
print(miles_input.get())
miles_input.grid(column=1, row=0)

# Miles label
miles_label = Label(text="Miles")
miles_label.grid(column=2, row=0)

# Equal to label
equal_label = Label(text="is equal to")
equal_label.grid(column=0, row=1)

# Km label
km_label = Label(text="Km")
km_label.grid(column=2, row=1)

# Km number label
km_result_label = Label(text="0")
km_result_label.grid(column=1, row=1)

# Button
button = Button(text='Calculate', command=miles_to_km)
button.grid(column=1, row=2)


window.mainloop()
