# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 17:41:27 2026

@author: akaal
"""

import math
import tkinter as tk
from tkinter import messagebox


class TicTacToeGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI (Minimax)")
        self.root.resizable(False, False)

        # Board representation: 3x3 list
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.human = "O"
        self.ai = "X"
        self.game_over = False

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()

    def create_widgets(self):
        # Header Label
        self.status_label = tk.Label(
            self.root,
            text="Your Turn (O)",
            font=("Helvetica", 14, "bold"),
            pady=10,
        )
        self.status_label.grid(row=0, column=0, columnspan=3)

        # Grid Buttons
        for r in range(3):
            for c in range(3):
                btn = tk.Button(
                    self.root,
                    text=" ",
                    font=("Helvetica", 24, "bold"),
                    width=5,
                    height=2,
                    bg="#f0f0f0",
                    command=lambda row=r, col=c: self.human_move(row, col),
                )
                btn.grid(row=r + 1, column=c, padx=5, pady=5)
                self.buttons[r][c] = btn

        # Reset Button
        reset_btn = tk.Button(
            self.root,
            text="Reset Game",
            font=("Helvetica", 10, "bold"),
            bg="#d9d9d9",
            command=self.reset_game,
        )
        reset_btn.grid(row=4, column=0, columnspan=3, pady=10)

    # --- Game Logic Functions ---

    def check_winner(self, board):
        """Checks for a winner on the given board."""
        # Rows and Columns
        for i in range(3):
            if (
                board[i][0] == board[i][1] == board[i][2]
                and board[i][0] != " "
            ):
                return board[i][0]
            if (
                board[0][i] == board[1][i] == board[2][i]
                and board[0][i] != " "
            ):
                return board[0][i]

        # Diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
            return board[0][2]

        # Check for Draw
        for row in board:
            if " " in row:
                return None  # Game still ongoing

        return "Draw"

    # --- Minimax Algorithm with Alpha-Beta Pruning ---

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        """Recursively scores moves (+10 AI win, -10 Human win, 0 Draw)."""
        winner = self.check_winner(board)

        if winner == self.ai:
            return 10 - depth  # Prefer faster wins
        if winner == self.human:
            return depth - 10  # Prefer slower losses
        if winner == "Draw":
            return 0

        if is_maximizing:
            max_eval = -math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == " ":
                        board[r][c] = self.ai
                        eval_score = self.minimax(
                            board, depth + 1, False, alpha, beta
                        )
                        board[r][c] = " "  # Undo move
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break  # Alpha-Beta Pruning
            return max_eval
        else:
            min_eval = math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == " ":
                        board[r][c] = self.human
                        eval_score = self.minimax(
                            board, depth + 1, True, alpha, beta
                        )
                        board[r][c] = " "  # Undo move
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break  # Alpha-Beta Pruning
            return min_eval

    def best_move(self):
        """Determines the optimal move for the AI."""
        best_score = -math.inf
        move = None

        for r in range(3):
            for c in range(3):
                if self.board[r][c] == " ":
                    self.board[r][c] = self.ai
                    score = self.minimax(
                        self.board, 0, False, -math.inf, math.inf
                    )
                    self.board[r][c] = " "
                    if score > best_score:
                        best_score = score
                        move = (r, c)
        return move

    # --- Turn Controllers ---

    def human_move(self, r, c):
        if self.board[r][c] == " " and not self.game_over:
            self.make_move(r, c, self.human)

            if not self.game_over:
                self.status_label.config(text="AI Thinking...")
                self.root.update()
                self.ai_move()

    def ai_move(self):
        move = self.best_move()
        if move:
            self.make_move(move[0], move[1], self.ai)

    def make_move(self, r, c, player):
        self.board[r][c] = player
        color = "#2196F3" if player == "O" else "#F44336"
        self.buttons[r][c].config(text=player, state="disabled", fg=color)

        result = self.check_winner(self.board)
        if result:
            self.game_over = True
            if result == "Draw":
                self.status_label.config(text="It's a Draw!")
                messagebox.showinfo(
                    "Game Over", "The game ended in a draw! "
                )
            else:
                winner_text = "Human Wins!" if result == "O" else "AI Wins!"
                self.status_label.config(text=winner_text)
                messagebox.showinfo("Game Over", f"{winner_text} 🎉")
        else:
            next_turn = "Your Turn (O)" if player == self.ai else "AI Thinking..."
            self.status_label.config(text=next_turn)

    def reset_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.status_label.config(text="Your Turn (O)")

        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(
                    text=" ", state="normal", bg="#f0f0f0"
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()