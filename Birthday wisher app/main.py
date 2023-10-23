"""
App which checks the current day and month and sends birthday wishes if the date is the same as somebody's birthday.
Data about the person's birthday is stored in csv file
"""
# ----------- IMPORTS -----------
import pandas as pd
import datetime as dt
import random
import smtplib

# ----------- FILES -----------
birthday_list = pd.read_csv("birthdays.csv")
birthday_list_dict = birthday_list.to_dict(orient="records")

# ----------- WISHER -----------
now = dt.datetime.now()
my_email = "test@gmail.com"
password = "abc123"

for person in birthday_list_dict:
    if person["month"] == now.month and person["day"] == now.day:
        with open(
            fr"C:\Users\falko\Git - Python\Data-Science\PycharmProjects\day-32-birthday wisher "
            fr"project\letter_templates\letter_{random.randint(1,3)}.txt",
            "r",
        ) as file:
            letter = file.readlines()
            personal_letter = "".join(letter).replace("[NAME]", person["name"])

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()  # TLS -> Transport Layer Security
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject:Happy Birthday!\n\n{personal_letter}",
            )
            print("Birthday wishes were sent")
