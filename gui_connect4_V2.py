import tkinter as tk
from tkinter import messagebox
import random

ROWS = 6
COLS = 7
CELL_SIZE = 100
PADDING = 12


class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4 — Enhanced Edition")

        # Scoreboard values (kept across all games)
        self.score_p1 = 0
        self.score_p2 = 0
        self.score_draw = 0

        # Game mode: 1 = PvP, 2 = vs AI
        self.game_mode = None

        # Start at the main menu
        self.show_main_menu()

   
    # /////// MAIN MENU SCREEN
    
    def show_main_menu(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="#003366", padx=50, pady=50)
        frame.pack(expand=True)

        tk.Label(
            frame,
            text="CONNECT 4",
            font=("Arial", 40, "bold"),
            bg="#003366",
            fg="white"
        ).pack(pady=25)

        # Classic Player vs Player mode
        tk.Button(
            frame, text="Play vs Player", font=("Arial", 20),
            command=lambda: self.start_game(mode=1),
            width=20
        ).pack(pady=10)

        # AI button (only easy mode in this version)
        tk.Button(
            frame, text="Play vs AI (Easy)", font=("Arial", 20),
            command=lambda: self.start_game(mode=2),
            width=20
        ).pack(pady=10)

        tk.Button(
            frame, text="Scoreboard", font=("Arial", 20),
            command=self.show_scoreboard,
            width=20
        ).pack(pady=10)

        tk.Button(
            frame, text="Exit", font=("Arial", 20),
            command=self.root.quit,
            width=20
        ).pack(pady=10)

    
    # ////// SCOREBOARD SCREEN
    
    def show_scoreboard(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="#222", padx=40, pady=40)
        frame.pack(expand=True)

        tk.Label(frame, text="Scoreboard", font=("Arial", 32),
                 bg="#222", fg="white").pack(pady=20)

        tk.Label(frame, text=f"Player 1 Wins: {self.score_p1}",
                 font=("Arial", 20), bg="#222", fg="white").pack(pady=5)

        tk.Label(frame, text=f"Player 2 / AI Wins: {self.score_p2}",
                 font=("Arial", 20), bg="#222", fg="white").pack(pady=5)

        tk.Label(frame, text=f"Draws: {self.score_draw}",
                 font=("Arial", 20), bg="#222", fg="white").pack(pady=5)

        tk.Button(frame, text="Back to Menu", font=("Arial", 20),
                  command=self.show_main_menu).pack(pady=20)

    
    #  /////////// GAME INITIALIZATION
    
    def start_game(self, mode):
        self.game_mode = mode
        self.board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = 0  # Player 1 starts

        self.clear_window()

        # Main game canvas (drawing the board)
        self.canvas = tk.Canvas(
            self.root,
            width=COLS * CELL_SIZE,
            height=ROWS * CELL_SIZE,
            bg="#0047ab",
            highlightthickness=0
        )
        self.canvas.pack()

        # Clicking inside the board places a piece
        self.canvas.bind("<Button-1>", self.on_click)

        # --- BACK TO MENU BUTTON (new feature) ---
        back_btn = tk.Button(
            self.root,
            text="Back to Main Menu",
            font=("Arial", 14),
            bg="#222",
            fg="white",
            command=self.show_main_menu
        )
        back_btn.pack(pady=10)

        # Draw the empty board at startup
        self.draw_board()

    # Clears every widget on screen (used by menu + scoreboard)
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    
    # ///// DRAWING THE GAME BOARD
    
    def draw_board(self):
        self.canvas.delete("all")

        # Loop over every cell and draw a circle
        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * CELL_SIZE + PADDING
                y1 = r * CELL_SIZE + PADDING
                x2 = x1 + (CELL_SIZE - PADDING * 2)
                y2 = y1 + (CELL_SIZE - PADDING * 2)

                # Default slot color
                fill = "#e0e0e0"

                # Put actual colors if a piece exists
                if self.board[r][c] == "orange":
                    fill = "#ff3b30"   # Red piece
                elif self.board[r][c] == "yellow":
                    fill = "#ffcc00"   # Yellow piece

                self.canvas.create_oval(
                    x1, y1, x2, y2,
                    fill=fill, outline="black", width=2
                )

   
    # //////// validity of col and epty places
    
    def is_valid_move(self, col):
        #/////// column is valid only if the top cell is empty
        return self.board[0][col] == " "

    def get_next_row(self, col):
        #//////// Find the lowest empty row in the selected column
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == " ":
                return r

    def drop(self, row, col, piece):
        #////////  place the piece inside the board matrix
        self.board[row][col] = piece

    def winning(self, piece):
        #/////// Check all win conditions: horizontal, vertical, diagonal

        # Horizontal check
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.board[r][c + i] == piece for i in range(4)):
                    return True

        # Vertical check
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(self.board[r + i][c] == piece for i in range(4)):
                    return True

        # Diagonal /
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.board[r - i][c + i] == piece for i in range(4)):
                    return True

        # Diagonal \
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.board[r + i][c + i] == piece for i in range(4)):
                    return True

        return False

    def board_full(self):
        return all(self.board[0][c] != " " for c in range(COLS))

   
    # ////////// AI LOGIC
    
    def ai_move(self):
        # Simple AI: just picks a random valid column
        valid_cols = [c for c in range(COLS) if self.is_valid_move(c)]
        return random.choice(valid_cols)

   
    #  ////////////  PLAYER CLICK HANDLING
   
    def on_click(self, event):
        col = event.x // CELL_SIZE

        # ////////Stop invalid clicks
        if col < 0 or col >= COLS or not self.is_valid_move(col):
            return

        # /////////Get the correct row + decide which piece to drop
        row = self.get_next_row(col)
        piece = "orange" if self.turn == 0 else "yellow"
        self.drop(row, col, piece)

        self.draw_board()

        # ////////Check win or draw after every move
        if self.winning(piece):
            if piece == "orange":
                self.score_p1 += 1
            else:
                self.score_p2 += 1
            messagebox.showinfo("Game Over", f"Player {self.turn + 1} ({piece}) wins!")
            self.start_game(self.game_mode)
            return

        if self.board_full():
            self.score_draw += 1
            messagebox.showinfo("Game Over", "Draw!")
            self.start_game(self.game_mode)
            return

        # /////Switch turn
        self.turn = 1 - self.turn

        # /////AI turn if playing vs computer
        if self.game_mode == 2 and self.turn == 1:
            self.root.after(300, self.ai_turn)

    
    #////////AI TURN HANDLER//
   
    def ai_turn(self):
        col = self.ai_move()
        row = self.get_next_row(col)
        piece = "yellow"

        self.drop(row, col, piece)
        self.draw_board()

        if self.winning(piece):
            self.score_p2 += 1
            messagebox.showinfo("Game Over", "AI Wins!")
            self.start_game(self.game_mode)
            return

        if self.board_full():
            self.score_draw += 1
            messagebox.showinfo("Game Over", "Draw!")
            self.start_game(self.game_mode)
            return

        # //////Back to player's turn
        self.turn = 0



#  //  START THE APPLICATION//

root = tk.Tk()
game = Connect4GUI(root)
root.mainloop()
