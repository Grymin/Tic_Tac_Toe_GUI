import random
import sys
import tkinter as tk
from tkinter import messagebox


class ClassTTT:

    font = ("COMIC SANS MS", 10)

    def __init__(self):
        """Initializing values and window"""
        self.players = {0: 'X', 1: 'O'}
        self.game_options = {1: "1 player", 2: "2 players"}
        self.chosen_game_option = 1
        self.player_symbol = "X"   # in case of game vs cpu
        self.turn = 0    # 0 -> 1 -> 0 -> 1...
        self.winner = None

        # initializing the board
        self.board = [[None for _ in range(3)] for _ in range(3)]

        # initialize the window
        self.root = tk.Tk()
        self.set_window_geometry()

        # Initialize and set upper text
        self.upper_text = tk.Label(self.root, font=ClassTTT.font)
        self.set_upper_text()
        self.upper_text.grid(row=0, column=1)

        # Initialize buttons - button_list (9 button in a list), button_pos (list of tuples with position)
        self.button_list = [[tk.Button(self.root) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.initialize_button(i, j)

        # Menu
        self.menubar = tk.Menu(self.root)
        self.menubar_set()

        # Main loop
        self.root.mainloop()

    def set_window_geometry(self):
        """Setting the sizes and position of the window"""
        self.root.geometry("250x250")
        self.root.title("Tic Tac Toe")

        # window middle of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        dx = 400
        dy = 400
        x0 = int((screen_width - dx) / 2)
        y0 = int((screen_height - dy) / 2)
        self.root.geometry(f"{dx}x{dy}+{x0}+{y0}")

    def menu_restart(self):
        """Restarts the game"""
        print("===============")
        self.turn = 0
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.winner = None
        self.set_upper_text()

        # Clear and polish the buttons
        for row in range(3):
            for col in range(3):
                self.button_list[row][col].config(text=" ")

        # If 2 players - disable symbol choice
        if self.chosen_game_option == 2:
            self.menubar.entryconfig(4, state=tk.DISABLED)
        else:
            self.menubar.entryconfig(4, state=tk.ACTIVE)

        # CPU turn?
        if self.chosen_game_option == 1 and self.players[self.turn] != self.player_symbol:
            print("cpu move at the beginning")
            print("   ", self.turn, self.players[self.turn], self.player_symbol)
            self.cpu_move()

    def menu_quit(self):
        """Closes app"""
        self.root.destroy()
        sys.exit()

    def choice_player(self, i):
        """Set game option: number of players"""
        self.chosen_game_option = i
        self.menu_restart()

    def choice_symbol(self, sym):
        """Set game option: symbol of the player"""
        print("player symbol:", self.player_symbol)
        self.player_symbol = sym
        self.menu_restart()

    def menubar_set(self):
        """ Setting the menu"""
        menubar_players = tk.Menu(self.menubar, tearoff=0)
        self.menubar_player_symbol = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_command(label="Restart", command=self.menu_restart)
        self.menubar.add_command(label="Quit", command=self.menu_quit)

        menubar_players.add_command(label="1player", command=lambda: self.choice_player(1))
        menubar_players.add_command(label="2players", command=lambda: self.choice_player(2))

        self.menubar_player_symbol.add_command(label="X", command=lambda: self.choice_symbol("X"))
        self.menubar_player_symbol.add_command(label="O", command=lambda: self.choice_symbol("O"))

        self.menubar.add_cascade(label="Players", menu=menubar_players)
        self.menubar.add_cascade(label="Symbol choice", menu=self.menubar_player_symbol)

        self.root.config(menu=self.menubar)

    def set_upper_text(self):
        """Change the upper text"""
        self.upper_text.config(text=f"PLAYER {self.turn+1}: '{self.players[self.turn]}'")

    def change_turn(self):
        """Changes turn of player (0/1)"""
        self.turn = (self.turn+1) % 2

    def end_screen(self):
        """Finished the game and asks what to do next"""
        if self.winner is not None:
            text = f"{self.winner} wins!"
        else:
            text = "This is a tie!"
        text += "\n\nDo you want to play agains?"
        answer = messagebox.askquestion("GAME FINISHED", text)
        if answer == "yes":
            self.menu_restart()
        else:
            self.menu_quit()

    def check_winner(self):
        """Checks if there is winner and initializes the end game screen if yes"""
        for player in self.players.values():
            for i in range(0, 3):
                if self.board[0][i] == self.board[1][i] == self.board[2][i] == player or \
                   self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                    self.winner = player
            if self.board[0][0] == self.board[1][1] == self.board[2][2] == player or \
               self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
                self.winner = player

    def check_tie(self):
        """Checks if the board is full"""
        if not any(el is None for line in self.board for el in line):
            self.end_screen()

    def move(self, i, j):
        """Changes board / buttos / chnges text and checks the results"""
        symbol = self.players.get(self.turn)
        color = "black" if symbol == "X" else "red"
        self.button_list[i][j].config(text=symbol, fg=color)
        self.board[i][j] = symbol
        self.set_upper_text()
        self.change_turn()
        self.check_winner()
        if self.winner is None:
            self.check_tie()
        else:
            self.end_screen()

    def cpu_move(self):
        """Random move of cpu"""
        possible_moves = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] is None]
        choice = random.choice(possible_moves)
        self.move(choice[0], choice[1])

    def click_button(self, i, j):
        """What to do after clcking"""
        if self.board[i][j] is None:
            self.move(i, j)
            if self.chosen_game_option == 1 and self.players[self.turn] != self.player_symbol:
                self.cpu_move()
        else:
            messagebox.showerror("Ups", "The field is already occupied")

    def initialize_button(self, i, j):
        """Initializing the buttons and defining what happens after clicking"""
        self.button_list[i][j].config(height=6, width=12, bg="white", font=ClassTTT.font,
                                      command=lambda: self.click_button(i, j))
        self.button_list[i][j].grid(row=i+1, column=j)


ClassTTT()
