import tkinter as tk
from tkinter import messagebox

class CricketGame:
    def __init__(self, players):
        self.players = players
        self.scores = {player: 0 for player in players}
        self.marks = {player: {20: 0, 19: 0, 18: 0, 17: 0, 16: 0, 15: 0, 'bull': 0} for player in players}
        self.closed_numbers = {20: [], 19: [], 18: [], 17: [], 16: [], 15: [], 'bull': []}

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
        self.root.geometry("500x500")
        self.root.configure(bg="#013220")
        self.setup_start_screen()

    def setup_start_screen(self):
        self.start_frame = tk.Frame(self.root, bg="#013220")
        self.start_frame.pack(padx=10, pady=10, fill="both", expand=True)
        tk.Label(self.start_frame, text="Player names (comma separated):", fg="white", bg="#013220").pack(pady=(100,5))
        self.names_entry = tk.Entry(self.start_frame, justify="center")
        self.names_entry.pack()
        tk.Button(self.start_frame, text="Start Game", command=self.start_game).pack(pady=20)

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
        self.game_frame = tk.Frame(self.root, bg="#013220")
        self.game_frame.pack(fill="both", expand=True)

        control_frame = tk.Frame(self.game_frame, bg="#013220")
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Player", fg="white", bg="#013220").pack(side="left")
        self.current_player_var = tk.StringVar(value=self.players[0])
        player_menu = tk.OptionMenu(control_frame, self.current_player_var, *self.players)
        player_menu.config(bg="#013220", fg="white", highlightthickness=0)
        player_menu['menu'].config(bg="#013220", fg="white")
        player_menu.pack(side="left", padx=5)

        tk.Label(control_frame, text="Multiplier", fg="white", bg="#013220").pack(side="left", padx=(10,0))
        self.mult_var = tk.IntVar(value=1)
        for val in [1,2,3]:
            tk.Radiobutton(control_frame, text=str(val), variable=self.mult_var, value=val,
                           bg="#013220", fg="white", selectcolor="#02511f").pack(side="left")

        numbers_frame = tk.Frame(self.game_frame, bg="#013220")
        numbers_frame.pack(side="left", padx=10, pady=10)

        for number in [20,19,18,17,16,15,'BULL']:
            btn = tk.Button(numbers_frame, text=str(number).upper(), font=("Helvetica", 18),
                             width=10, height=1, bg="#013220", fg="white",
                             activebackground="#02511f",
                             command=lambda n=number: self.record_throw(n))
            btn.pack(pady=5, fill="x")

        score_frame = tk.Frame(self.game_frame, bg="#013220")
        score_frame.pack(side="left", padx=10, pady=10)
        self.score_labels = {}
        self.mark_labels = {}
        for player in self.players:
            player_col = tk.Frame(score_frame, bg="#013220")
            player_col.pack(side="left", padx=10)

            tk.Label(player_col, text=player, font=("Helvetica", 18, "bold"),
                     fg="white", bg="#013220").pack()

            info_frame = tk.Frame(player_col, bg="#013220")
            info_frame.pack()

            score_lbl = tk.Label(info_frame, text="0", font=("Helvetica", 18),
                                 fg="white", bg="#013220")
            score_lbl.pack(side="left", padx=(0,10))

            marks_frame = tk.Frame(info_frame, bg="#013220")
            marks_frame.pack(side="left")

            marks_lbls = {}
            for num in [20,19,18,17,16,15,'bull']:
                lbl = tk.Label(marks_frame, text="", font=("Helvetica", 18),
                               fg="white", bg="#013220")
                lbl.pack()
                marks_lbls[num] = lbl

            self.score_labels[player] = score_lbl
            self.mark_labels[player] = marks_lbls

        self.update_scores()

    def record_throw(self, number):
        player = self.current_player_var.get()
        mult = self.mult_var.get()
        dart_number = 'bull' if str(number).lower() == 'bull' else int(number)
        self.game.play_round(player, [(dart_number, mult)])
        winner = self.game.check_winner()
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.game_frame.destroy()
            self.setup_start_screen()
            return
        self.update_scores()

    def update_scores(self):
        for player in self.players:
            self.score_labels[player].configure(text=str(self.game.scores[player]))
            marks = self.game.display_marks(player)
            for num, symbol in marks.items():
                self.mark_labels[player][num].configure(text=symbol)


def main():
    root = tk.Tk()
    CricketGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
