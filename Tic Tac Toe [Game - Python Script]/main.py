class Player:
    def __init__(self, name, sign):
        self.name = name
        self.score = 0
        self.sign = sign


class Game:
    def __init__(self):
        self.map = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def show_board(self):
        print("\n" + " " + " | ".join(self.map[0]))
        print("-----------")
        print(" " + " | ".join(self.map[1]))
        print("-----------")
        print(" " + " | ".join(self.map[2]) + "\n")

    def update_board(self, row, place, player_sign):
        self.map[row][place] = player_sign

    # Horizontal fields check
    def h_fields_check(self, player_sign):
        for i in range(0, len(self.map)):
            if all(sign == player_sign for sign in self.map[i]):
                return True
            else:
                return False

    # Vertical fields check
    def v_fields_check(self, player_sign):
        # Vertical check - create list with signs - checked vertically by indexes
        v_column_ch = []
        for col_n in range(0, len(self.map)):
            for row_n in range(0, len(self.map)):
                v_column_ch.append(self.map[row_n][col_n])

        # Vertical checks
        if (
            all(sign == player_sign for sign in v_column_ch[:3])
            or all(sign == player_sign for sign in v_column_ch[3:6])
            or all(sign == player_sign for sign in v_column_ch[6:])
        ):
            return True
        # Diagonal signs - from top left corner and from top right corner
        elif all(
            sign == player_sign for sign in [v_column_ch[i] for i in [0, 4, 8]]
        ) or all(sign == player_sign for sign in [v_column_ch[i] for i in [2, 4, 6]]):
            return True
        else:
            return False

    def check_empty_fields(self):
        empty_fields = []
        for i in range(0, len(self.map)):
            for field in self.map[i]:
                if field == " ":
                    empty_fields.append(field)

        return len(empty_fields)


print("---- Welcome to Tic Tac Toe game ----\n")
p1_name = input("Player 1 (X) name: ")
p2_name = input("Player 2 (O) name: ")

game = Game()
player1 = Player(p1_name, sign="X")
player2 = Player(p2_name, sign="O")

game.show_board()

game_on = True
while game_on:
    for player in [player1, player2]:
        print(f"Your turn {player.name}")

        # Loop for inputs
        while True:
            try:
                row = int(
                    input(
                        f"{player.name}: Please provide ROW (0, 1, 2) where you would like to make your move: "
                    )
                )

                place = int(
                    input(
                        f"{player.name}: Please provide PLACE (0, 1, 2) where you would like to make your move: "
                    )
                )

                if row in (0, 1, 2) and place in (0, 1, 2):
                    if game.map[row][place] == " ":
                        game.update_board(row, place, player.sign)
                        break
                    else:
                        print(
                            f"{player.name}: Please choose other place to place your sign, this one is taken!"
                        )
                else:
                    print(f"{player.name}: Please provide number from 0 to 2.")

            except Exception as e:
                print(e)

        game.show_board()

        # Check if any player achieved 3 signs in a row or there are no empty fields left
        if game.h_fields_check(player.sign) or game.v_fields_check(player.sign):
            player.score += 1
            print(f"Congratulations {player.name} you won!")
            game_on = False
            break
        elif game.check_empty_fields() == 0:
            print(f"Draw - nobody won this time.")
            game_on = False
            break
