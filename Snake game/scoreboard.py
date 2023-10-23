from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")


def read_high_score() -> int:
    with open("data.txt", mode="r") as file:
        high_score = file.read()

    return int(high_score)


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = read_high_score()
        self.color("white")
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self) -> None:
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align=ALIGNMENT, font=FONT)

    def reset(self) -> None:
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.score = 0
        self.update_scoreboard()

    def increase_score(self) -> None:
        self.score += 1
        self.update_scoreboard()

    def save_high_score(self) -> None:
        with open("data.txt", mode="w") as file:
            file.write(f"{self.high_score}")
