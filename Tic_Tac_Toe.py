import tkinter as tk
from tkinter import messagebox
import random
import abc


class Player(abc.ABC):
    def __init__(self, symbol):
        self._symbol = symbol

    @property
    def symbol(self):
        return self._symbol

    @abc.abstractmethod
    def make_move(self, board, row=None, col=None):
        pass


class HumanPlayer(Player):
    def make_move(self, board, row, col):
        return board.make_move(row, col, self.symbol)


class HardAIPlayer(Player):
    def __init__(self, symbol, opponent_symbol):
        super().__init__(symbol)
        self._opponent_symbol = opponent_symbol

    def make_move(self, board, row=None, col=None):
        for r in range(board.size):
            for c in range(board.size):
                if board.make_move(r, c, self.symbol):
                    if board.check_winner() == self.symbol:
                        return True
                    board.undo_move(r, c)

        for r in range(board.size):
            for c in range(board.size):
                if board.make_move(r, c, self._opponent_symbol):
                    if board.check_winner() == self._opponent_symbol:
                        board.undo_move(r, c)
                        board.make_move(r, c, self.symbol)
                        return True
                    board.undo_move(r, c)

        empty = board.get_empty_cells()
        if empty:
            r, c = random.choice(empty)
            board.make_move(r, c, self.symbol)
            return True
        return False


class PlayerFactory:
    @staticmethod
    def create_player(player_type, symbol, opponent_symbol="X"):
        if player_type == "human":
            return HumanPlayer(symbol)
        elif player_type == "AI":
            return HardAIPlayer(symbol, opponent_symbol)
        else:
            raise ValueError("Unknown player type")


class Board:
    def __init__(self, size=3, win_length=3):
        self._size = size
        self._win_length = win_length
        self._board = [[" " for _ in range(size)] for _ in range(size)]

    @property
    def size(self):
        return self._size

    def make_move(self, row, col, symbol):
        if self._board[row][col] == " ":
            self._board[row][col] = symbol
            return True
        return False

    def undo_move(self, row, col):
        self._board[row][col] = " "

    def check_winner(self):
        lines = []
        for i in range(self._size):
            lines.append(self._board[i])
            lines.append([self._board[j][i] for j in range(self._size)])

        lines.append([self._board[i][i] for i in range(self._size)])
        lines.append(
            [self._board[i][self._size - 1 - i] for i in range(self._size)]
        )

        for line in lines:
            if line.count(line[0]) == self._win_length and line[0] != " ":
                return line[0]
        return None

    def is_full(self):
        return all(cell != " " for row in self._board for cell in row)

    def get_empty_cells(self):
        return [
            (r, c)
            for r in range(self._size)
            for c in range(self._size)
            if self._board[r][c] == " "
        ]

    @property
    def board(self):
        return self._board


class Game:
    def __init__(self, players, board, gui):
        self._players = players
        self._board = board
        self._gui = gui
        self._current = 0
        self._is_ai_turn = False

    def make_move(self, row, col):
        if self._is_ai_turn:
            return

        player = self._players[self._current]

        if isinstance(player, HumanPlayer):
            move_made = player.make_move(self._board, row, col)

            if move_made:
                self._gui.update_buttons()
                winner = self._board.check_winner()
                if winner:
                    self._gui.show_winner(winner)
                    return
                if self._board.is_full():
                    self._gui.show_draw()
                    return

                self._current = (self._current + 1) % len(self._players)

                if isinstance(self._players[self._current], HardAIPlayer):
                    self._is_ai_turn = True
                    self._gui.window.after(500, self.ai_move)

    def ai_move(self):
        player = self._players[self._current]

        if isinstance(player, HardAIPlayer):
            player.make_move(self._board)
            self._gui.update_buttons()
            winner = self._board.check_winner()
            if winner:
                self._gui.show_winner(winner)
                return
            if self._board.is_full():
                self._gui.show_draw()
                return

            self._current = (self._current + 1) % len(self._players)
            self._is_ai_turn = False


class GameGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe 3x3")
        self.window.geometry("600x600+450+100")
        self.window.configure(bg="#E6E6FA")
        self.setup_screen()

    def save_result(self, winner):
        with open("results.txt", "a", encoding="utf-8") as file:
            if winner:
                file.write(f"Winner: {winner}\n")
            else:
                file.write("Draw\n")

    def load_results(self):
        try:
            with open("results.txt", "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return "No previous results."
            return content
        except FileNotFoundError:
            return "No previous results."

    def setup_screen(self):
        self.clear_screen()
        frame = tk.Frame(self.window, bg="#E6E6FA")
        frame.pack(expand=True)

        tk.Label(
            frame,
            text="Tic Tac Toe",
            font=("Arial", 24, "bold"),
            bg="#E6E6FA"
        ).pack(pady=(30, 10))

        results_label = tk.Label(
            frame,
            text=f"Previous results:\n{self.load_results()}",
            font=("Arial", 10),
            bg="#E6E6FA",
            justify="left"
        )
        results_label.pack(pady=10)

        tk.Label(
            frame,
            text="Choose Player 2:",
            font=("Arial", 14),
            bg="#E6E6FA"
        ).pack()
        self.player2_type = tk.StringVar(value="human")
        tk.OptionMenu(frame, self.player2_type, "human", "AI").pack(pady=10)

        tk.Label(
            frame,
            text="Choose Player 2 symbol:",
            font=("Arial", 14),
            bg="#E6E6FA"
        ).pack()
        self.player2_symbol = tk.StringVar(value="O")
        tk.OptionMenu(frame, self.player2_symbol, "X", "O").pack(pady=10)

        self.start_button = tk.Button(
            frame,
            text="Start Game",
            font=("Arial", 14),
            command=self.start_game
        )
        self.start_button.pack(pady=20)

    def start_game(self):
        players = []
        player2_symbol = self.player2_symbol.get()
        player1_symbol = "O" if player2_symbol == "X" else "X"

        players.append(PlayerFactory.create_player("human", player1_symbol))
        players.append(
            PlayerFactory.create_player(
                self.player2_type.get(),
                player2_symbol,
                player1_symbol
            )
        )

        self.board = Board()

        if players[0].symbol == "X":
            starting_index = 0
        else:
            starting_index = 1

        self.game = Game(players, self.board, self)
        self.game._current = starting_index

        self.show_board()

        if isinstance(players[starting_index], HardAIPlayer):
            self.window.after(500, self.game.ai_move)

    def show_board(self):
        self.clear_screen()
        self.buttons = []

        frame = tk.Frame(self.window, bg="#E6E6FA")
        frame.pack(expand=True)

        for r in range(3):
            row = []
            for c in range(3):
                button = tk.Button(
                    frame,
                    text="",
                    width=3,
                    height=1,
                    font=("Arial", 36, "bold"),
                    bg="white",
                    fg="black",
                    relief="raised",
                    bd=3,
                    command=lambda r=r, c=c: self.game.make_move(r, c)
                )
                button.grid(
                    row=r,
                    column=c,
                    padx=15,
                    pady=15,
                    ipadx=20,
                    ipady=20
                )
                row.append(button)
            self.buttons.append(row)

    def update_buttons(self):
        for r in range(3):
            for c in range(3):
                symbol = self.board.board[r][c]
                btn = self.buttons[r][c]
                btn['text'] = symbol

                if symbol == "X":
                    btn['fg'] = "red"
                elif symbol == "O":
                    btn['fg'] = "blue"

    def show_winner(self, winner):
        self.save_result(winner)
        if messagebox.askyesno(
            "Winner",
            f"Player {winner} wins!\nDo you want to play again?"
        ):
            self.setup_screen()
        else:
            self.window.quit()

    def show_draw(self):
        self.save_result(None)
        if messagebox.askyesno(
            "Draw",
            "The game ended in a draw!\nDo you want to play again?"
        ):
            self.setup_screen()
        else:
            self.window.quit()

    def clear_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = GameGUI()
    gui.run()
