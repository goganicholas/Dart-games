import random

class CricketGame:
    def __init__(self, players):
        self.players = players
        self.numbers = random.sample(range(5, 21), 6)
        self.numbers.sort(reverse=True)
        self.numbers.append('bull')
        self.scores = {player: 0 for player in players}
        self.marks = {player: {number: 0 for number in self.numbers} for player in players}
        self.closed_numbers = {number: [] for number in self.numbers}
        self.current_player_index = 0

    def mark_number(self, player, number, marks):
        if number not in self.closed_numbers:
            return

        if len(self.closed_numbers[number]) == len(self.players):
            return  # No more points

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

def main():
    num_players = int(input("Hoeveel spelers: "))
    players = [input(f"Naam {i + 1}: ") for i in range(num_players)]
    game = CricketGame(players)

    while True:
        current_player = players[game.current_player_index]
        print(f"\n{current_player}'s beurt")
        darts = []
        for _ in range(3):
            number = input(f"Welk nummer heb je gegooid? {game.numbers}: ")
            if not number:
                continue
            if number == 'bull':
                number = 'bull'
            else:
                try:
                    number = int(number)
                    if number not in game.numbers:
                        print("Ongeldig nummer.")
                        continue
                except ValueError:
                    print("Ongeldige invoer.")
                    continue
            multiplier = input("multiplier (1, 2, 3): ")
            if not multiplier:
                continue
            try:
                multiplier = int(multiplier)
                if multiplier not in [1, 2, 3]:
                    print("Ongeldige multiplier.")
                    continue
            except ValueError:
                print("Ongeldige invoer.")
                continue
            darts.append((number, multiplier))

        game.play_round(current_player, darts)
        game.next_player()

        print("\nScores :")
        header = f"{'Speler':<10} {'Score':<5} " + " ".join([f"{num:<3}" for num in game.numbers])
        print(header)
        for player in players:
            marks = game.display_marks(player)
            marks_str = " ".join([f"{marks[num]:<3}" for num in game.numbers])
            print(f"{player:<10} {game.scores[player]:<5} {marks_str}")

        winner = game.check_winner()
        if winner:
            print(f"\n{winner} wint!")
            break
        else:
            print("\nSpeel verder")

    while True:
        exit_input = input("Typ 'exit': ")
        if exit_input.lower() == 'exit':
            break

if __name__ == "__main__":
    main()
