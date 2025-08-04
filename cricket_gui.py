import tkinter as tk
from tkinter import messagebox

class CricketGame:
    def __init__(self, players):
        self.players = players
        self.scores = {player: 0 for player in players}
        self.marks = {player: {20: 0, 19: 0, 18: 0, 17: 0, 16: 0, 15: 0, 'bull': 0} for player in players}
        self.closed_numbers = {20: [], 19: [], 18: [], 17: [], 16: [], 15: [], 'bull': []}
        self.current_player_index = 0

    def mark_number(self, player, number, marks):
        if number not in self.closed_numbers:
            return
        if len(self.closed_numbers[number]) == len(self.players):
            return
        if player in self.closed_numbers[number]:
            self.scores[player] += (25 if number == 'bull' else number) * marks
        else:
            self.marks[player][number] += marks
            if self.marks[player][number] >= 3:
                self.closed_numbers[number].append(player)
                if len(self.closed_numbers[number]) < len(self.players):
                    self.scores[player] += (self.marks[player][number] - 3) * (25 if number == 'bull' else number)
                self.marks[player][number] = 3

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def is_overkill(self, player):
        min_score = min(self.scores.values())
        return self.scores[player] - min_score >= 200

    def play_round(self, player, darts):
        for dart in darts:
            number, multiplier = dart
            if self.is_overkill(player):
                continue
            self.mark_number(player, number, multiplier)

    def check_winner(self):
        for player in self.players:
            if all(self.marks[player][number] == 3 for number in self.marks[player]):
                if all(
                    self.scores[player] > self.scores[other]
                    for other in self.players
                    if other != player
                ):
                    return player
        return None

    def display_marks(self, player):
        symbols = {0: '', 1: '/', 2: '×', 3: '⊗'}
        return {number: symbols[self.marks[player][number]] for number in self.marks[player]}


class CricketGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cricket Darts")
        self.setup_start_screen()

    def setup_start_screen(self):
        self.start_frame = tk.Frame(self.root)
        self.start_frame.pack(padx=10, pady=10)
        tk.Label(self.start_frame, text="Player names (comma separated):").pack()
        self.names_entry = tk.Entry(self.start_frame)
        self.names_entry.pack()
        tk.Button(self.start_frame, text="Start Game", command=self.start_game).pack(pady=5)

    def start_game(self):
        names_text = self.names_entry.get().strip()
        players = [n.strip() for n in names_text.split(',') if n.strip()]
        if not players:
            messagebox.showwarning("Invalid input", "Please enter at least one player name.")
            return
        self.game = CricketGame(players)
        self.players = players
        self.start_frame.destroy()
        self.setup_game_screen()

    def setup_game_screen(self):
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(padx=10, pady=10)
        self.current_player_label = tk.Label(self.game_frame, text="")
        self.current_player_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

        tk.Label(self.game_frame, text="Number").grid(row=1, column=0)
        self.number_var = tk.StringVar(value="20")
        numbers = ["20", "19", "18", "17", "16", "15", "bull"]
        tk.OptionMenu(self.game_frame, self.number_var, *numbers).grid(row=1, column=1)

        tk.Label(self.game_frame, text="Multiplier").grid(row=1, column=2)
        self.mult_var = tk.StringVar(value="1")
        tk.OptionMenu(self.game_frame, self.mult_var, "1", "2", "3").grid(row=1, column=3)

        tk.Button(self.game_frame, text="Add Dart", command=self.add_dart).grid(row=2, column=0, columnspan=4, pady=5)

        self.score_text = tk.Text(self.game_frame, width=60, height=10, state="disabled")
        self.score_text.grid(row=3, column=0, columnspan=4, pady=(10, 0))

        self.darts_thrown = 0
        self.update_current_player()
        self.update_scores()

    def add_dart(self):
        number_str = self.number_var.get()
        number = 'bull' if number_str == 'bull' else int(number_str)
        multiplier = int(self.mult_var.get())
        current_player = self.players[self.game.current_player_index]
        self.game.play_round(current_player, [(number, multiplier)])
        self.darts_thrown += 1
        if self.darts_thrown >= 3:
            self.darts_thrown = 0
            winner = self.game.check_winner()
            if winner:
                messagebox.showinfo("Game Over", f"{winner} wint!")
                self.game_frame.destroy()
                self.setup_start_screen()
                return
            self.game.next_player()
        self.update_current_player()
        self.update_scores()

    def update_current_player(self):
        player = self.players[self.game.current_player_index]
        self.current_player_label.config(text=f"{player}'s beurt")

    def update_scores(self):
        self.score_text.configure(state="normal")
        self.score_text.delete("1.0", tk.END)
        header = f"{'Speler':<10} {'Score':<5} {'20':<3} {'19':<3} {'18':<3} {'17':<3} {'16':<3} {'15':<3} {'Bull':<3}\n"
        self.score_text.insert(tk.END, header)
        for player in self.players:
            marks = self.game.display_marks(player)
            line = f"{player:<10} {self.game.scores[player]:<5} {marks[20]:<3} {marks[19]:<3} {marks[18]:<3} {marks[17]:<3} {marks[16]:<3} {marks[15]:<3} {marks['bull']:<3}\n"
            self.score_text.insert(tk.END, line)
        self.score_text.configure(state="disabled")


def main():
    root = tk.Tk()
    CricketGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
