"""
Following program uses Turtle library to create painting based on "Spots" painting created by Damien Hirst.
"""

from turtle import Turtle, Screen, colormode
import random

color_list = [(200, 167, 110), (144, 74, 52), (169, 152, 45), (58, 92, 119), (224, 203, 131), (136, 162, 180),
              (131, 34, 26), (51, 117, 89), (199, 94, 72), (143, 25, 30), (18, 97, 74), (69, 47, 40), (173, 146, 153),
              (150, 177, 152), (131, 70, 74), (56, 43, 46), (237, 174, 163), (184, 88, 94), (38, 58, 71), (28, 82, 89),
              (182, 204, 178), (242, 156, 160), (93, 144, 124), (20, 66, 57), (36, 65, 96), (108, 125, 154)]

tim = Turtle()
colormode(255)
tim.pensize(10)
tim.speed(6)

tp = tim.pos()
print(tp)

tim.penup()
y = -200
tim.setpos(-200, y)
tim.hideturtle()


def make_10_dots() -> None:
    for _ in range(10):
        tim.dot(20, random.choice(color_list))
        tim.fd(50)


for _ in range(10):
    make_10_dots()
    y += 50
    tim.setpos(-200, y)

screen = Screen()
screen.exitonclick()
