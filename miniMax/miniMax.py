import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.player = "X"
        self.computer = "O"
        self.board = [" " for _ in range(9)]
        self.buttons = []

        self.player_wins = 0
        self.computer_wins = 0
        self.ties = 0
        self.total_ai_score = 0
        self.match_count = 1
        self.match_history = []

        self.scoreboard_window = None

        self.create_widgets()

    def create_widgets(self):
        self.root.configure(bg="#f0f0f0")
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(padx=10, pady=10)

        title_label = tk.Label(
            self.main_frame,
            text="Tic-Tac-Toe",
            font=("Helvetica", 24, "bold"),
            bg="#f0f0f0",
        )
        title_label.pack(pady=(0, 10))

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

        buttons_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        buttons_frame.pack(pady=10)

        self.restart_button = tk.Button(
            buttons_frame,
            text="Play Again",
            font=("Helvetica", 14),
            bg="#4CAF50",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.restart_game,
        )
        self.restart_button.grid(row=0, column=0, padx=10)

        self.scoreboard_button = tk.Button(
            buttons_frame,
            text="Show Scoreboard",
            font=("Helvetica", 14),
            bg="#0074D9",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.show_scoreboard,
        )
        self.scoreboard_button.grid(row=0, column=1, padx=10)

    def show_scoreboard(self):
        if not self.scoreboard_window or not self.scoreboard_window.winfo_exists():
            self.scoreboard_window = tk.Toplevel(self.root)
            self.scoreboard_window.title("Match History & Scoreboard")
            self.scoreboard_window.geometry("350x350")

            columns = ("match", "winner", "score")
            self.history_tree = ttk.Treeview(
                self.scoreboard_window, columns=columns, show="headings"
            )
            self.history_tree.heading("match", text="Match")
            self.history_tree.column("match", width=80, anchor="center")
            self.history_tree.heading("winner", text="Winner")
            self.history_tree.column("winner", width=120, anchor="center")
            self.history_tree.heading("score", text="AI Score")
            self.history_tree.column("score", width=80, anchor="center")
            self.history_tree.pack(fill="both", expand=True, padx=10, pady=10)

            summary_frame = tk.Frame(self.scoreboard_window)
            summary_frame.pack(pady=10)

            self.player_wins_label = tk.Label(summary_frame, font=("Helvetica", 12))
            self.player_wins_label.pack()
            self.computer_wins_label = tk.Label(summary_frame, font=("Helvetica", 12))
            self.computer_wins_label.pack()
            self.ties_label = tk.Label(summary_frame, font=("Helvetica", 12))
            self.ties_label.pack()

            self.total_ai_score_label = tk.Label(
                summary_frame, font=("Helvetica", 14, "bold"), pady=10
            )
            self.total_ai_score_label.pack()

        self.update_scoreboard_display()
        self.scoreboard_window.lift()

    def update_scoreboard_display(self):
        if not self.scoreboard_window or not self.scoreboard_window.winfo_exists():
            return

        self.history_tree.delete(*self.history_tree.get_children())
        for match in self.match_history:
            self.history_tree.insert("", "end", values=match)

        self.player_wins_label.config(text=f"Total Player Wins: {self.player_wins}")
        self.computer_wins_label.config(
            text=f"Total Computer Wins: {self.computer_wins}"
        )
        self.ties_label.config(text=f"Total Ties: {self.ties}")

        self.total_ai_score_label.config(text=f"Total AI Score: {self.total_ai_score}")

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
        return any(
            all(self.board[i] == player for i in combo) for combo in win_conditions
        )

    def update_board_ui(self, index, symbol):
        self.board[index] = symbol
        color = "#ff4136" if symbol == "O" else "#0074D9"
        self.buttons[index].config(text=symbol, fg=color, state=tk.DISABLED)

    def end_game(self, message):
        winner, score = None, 0
        if message == "You win!":
            self.player_wins += 1
            winner, score = "Player", -10
        elif message == "Computer wins!":
            self.computer_wins += 1
            winner, score = "Computer", 10
        else:
            self.ties += 1
            winner, score = "Tie", 0
        
        self.total_ai_score += score

        self.match_history.append((self.match_count, winner, score))
        self.update_scoreboard_display()

        self.match_count += 1
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
