import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.player = "X"
        self.computer = "O"
        self.board = [" " for _ in range(9)]
        self.buttons = []

        # --- NEW: Initialize scores ---
        self.player_score = 0
        self.computer_score = 0

        self.create_widgets()

    def create_widgets(self):
        self.root.configure(bg="#f0f0f0")
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(padx=10, pady=10)

        title_label = tk.Label(
            self.main_frame,
            text="Tic-Tac-Toe AI",
            font=("Helvetica", 24, "bold"),
            bg="#f0f0f0",
        )
        title_label.pack(pady=(0, 10))

        # --- NEW: Scoreboard Frame ---
        self.score_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.score_frame.pack(pady=(0, 10))
        self.score_label = tk.Label(
            self.score_frame,
            text=f"You: {self.player_score}  -  Computer: {self.computer_score}",
            font=("Helvetica", 16),
        )
        self.score_label.pack()

        self.board_frame = tk.Frame(self.main_frame, bg="#333")
        self.board_frame.pack()

        for i in range(9):
            button = tk.Button(
                self.board_frame,
                text=" ",
                font=("Helvetica", 28, "bold"),
                height=2,
                width=5,
                bg="#fff",
                fg="#333",
                relief="flat",
                command=lambda i=i: self.player_move(i),
            )
            button.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(button)

        self.status_label = tk.Label(
            self.main_frame, text="Your turn (X)", font=("Helvetica", 16), bg="#f0f0f0"
        )
        self.status_label.pack(pady=20)

        self.restart_button = tk.Button(
            self.main_frame,
            text="Play Again",
            font=("Helvetica", 14),
            bg="#4CAF50",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.restart_game,
        )
        self.restart_button.pack(pady=10)

    def player_move(self, index):
        if self.board[index] == " ":
            self.update_board_ui(index, self.player)
            if self.check_winner(self.player):
                self.end_game("You win!")
            elif " " not in self.board:
                self.end_game("It's a tie!")
            else:
                self.status_label.config(text="Computer's turn (O)")
                self.root.after(500, self.computer_move)

    def computer_move(self):
        best_score = -float("inf")
        best_move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = self.computer
                score = self.minimax(self.board, 0, False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.update_board_ui(best_move, self.computer)
            if self.check_winner(self.computer):
                self.end_game("Computer wins!")
            elif " " not in self.board:
                self.end_game("It's a tie!")
            else:
                self.status_label.config(text="Your turn (X)")

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner(self.computer):
            return 10
        elif self.check_winner(self.player):
            return -10
        elif " " not in board:
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.computer
                    score = self.minimax(board, depth + 1, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.player
                    score = self.minimax(board, depth + 1, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        win_conditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                return True
        return False

    def update_board_ui(self, index, player_symbol):
        self.board[index] = player_symbol
        color = "#ff4136" if player_symbol == "O" else "#0074D9"
        self.buttons[index].config(text=player_symbol, fg=color, state=tk.DISABLED)

    def end_game(self, message):
        # --- NEW: Update scores on game end ---
        if message == "You win!":
            self.player_score += 1
        elif message == "Computer wins!":
            self.computer_score += 1

        # --- NEW: Refresh the score display ---
        self.score_label.config(
            text=f"You: {self.player_score}  -  Computer: {self.computer_score}"
        )

        for button in self.buttons:
            button.config(state=tk.DISABLED)
        self.status_label.config(text=message)
        messagebox.showinfo("Game Over", message)

    def restart_game(self):
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ", state=tk.NORMAL)
        self.status_label.config(text="Your turn (X)")


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
