import tkinter as tk
from tkinter import messagebox

ROWS = 6
COLS = 7
CELL_SIZE = 100
PADDING = 12

class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4 — Enhanced Edition")

        self.create_menu()

        self.board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = 0  # 0 = X (red), 1 = O (yellow)
        self.piece_colors = {"Orange": "#ff3b30", "Yellow": "#ffcc00"}  # Better vibrant colors

        self.canvas = tk.Canvas(
            root,
            width=COLS * CELL_SIZE,
            height=ROWS * CELL_SIZE,
            bg="#0047ab",  # Deep blue like real Connect 4 board
            highlightthickness=0
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()

    def create_menu(self):
        menubar = tk.Menu(self.root)

        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", command=self.reset_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)

        menubar.add_cascade(label="Game", menu=game_menu)
        self.root.config(menu=menubar)

    def draw_board(self):
        self.canvas.delete("all")

        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * CELL_SIZE + PADDING
                y1 = r * CELL_SIZE + PADDING
                x2 = x1 + (CELL_SIZE - PADDING * 2)
                y2 = y1 + (CELL_SIZE - PADDING * 2)

                # Empty slot color
                fill_color = "#e0e0e0"

                if self.board[r][c] != " ":
                    fill_color = self.piece_colors[self.board[r][c]]

                # Draw disc with nice visuals
                self.canvas.create_oval(
                    x1, y1, x2, y2,
                    fill=fill_color,
                    outline="black",
                    width=2
                )

    def is_valid_move(self, col):
        return self.board[0][col] == " "

    def get_next_open_row(self, col):
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == " ":
                return r
        return None

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def winning_move(self, piece):
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.board[r][c + i] == piece for i in range(4)):
                    return True

        # Vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(self.board[r + i][c] == piece for i in range(4)):
                    return True

        # Diagonal (/)
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.board[r - i][c + i] == piece for i in range(4)):
                    return True

        # Diagonal (\)
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.board[r + i][c + i] == piece for i in range(4)):
                    return True

        return False

    def board_full(self):
        return all(self.board[0][c] != " " for c in range(COLS))

    def on_click(self, event):
        col = event.x // CELL_SIZE

        if col < 0 or col >= COLS:
            return

        if self.is_valid_move(col):
            row = self.get_next_open_row(col)
            piece = "Orange" if self.turn == 0 else "Yellow"

            self.drop_piece(row, col, piece)
            self.draw_board()

            if self.winning_move(piece):
                messagebox.showinfo("Game Over", f"Player {self.turn + 1} ({piece}) wins!")
                self.reset_game()
                return

            if self.board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
                return

            self.turn = 1 - self.turn

    def reset_game(self):
        self.board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = 0
        self.draw_board()


# Run the game
root = tk.Tk()
game = Connect4GUI(root)
root.mainloop()
