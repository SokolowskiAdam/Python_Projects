"""
App for generating secure passwords and storing them in json file
"""

# ---------------------------- IMPORTS ---------------------------- #
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
DEFAULT_EMAIL = "test@test.com"  # User's default email address shown in app


def generate_password() -> None:
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)  # copy password to the clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save() -> None:
    website = website_entry.get()
    email_username = email_username_entry.get()
    password = password_entry.get()

    new_data = {
        website:
            {
                "email": email_username,
                "password": password,
            }
    }

    # Check if all fields were filled
    if len(website) == 0 or len(email_username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")

    else:
        try:
            with open("data.json", 'r') as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", 'w') as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            # Clean entries after saving website/password to file
            website_entry.delete(0, 'end')
            password_entry.delete(0, 'end')


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password() -> None:
    website = website_entry.get()
    # Check if website field was filled
    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave Website field empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)

            if website in data:
                message = f"Email: {data[website]['email']}\nPassword: {data[website]['password']}"
                messagebox.showinfo(title=website, message=message)
            else:
                messagebox.showinfo(title="Oops", message=f"{website} not found")

        except FileNotFoundError:
            messagebox.showinfo(title="Oops", message="No Data File Found")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_entry = Entry()
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()

email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)
email_username_entry = Entry()
email_username_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
email_username_entry.insert(0, DEFAULT_EMAIL)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_entry = Entry()
password_entry.grid(column=1, row=3, sticky="EW")

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3, sticky="EW")

add_button = Button(text="Add", width=35, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky="EW")

window.mainloop()
