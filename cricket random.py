import random

class RandomCricketGame:
    def __init__(self, players):
        self.players = players
        self.scores = {player: 0 for player in players}
        self.all_numbers = list(range(5, 21)) + ['bull']
        self.ticked_numbers = []
        self.generate_numbers()
        self.marks = {player: {number: 0 for number in self.all_numbers} for player in players}
        self.closed_numbers = {number: [] for number in self.all_numbers}
        self.current_player_index = 0

    def generate_numbers(self):
        available_numbers = [num for num in range(5, 21) if num not in self.ticked_numbers]
        num_to_select = min(6 - len(self.ticked_numbers), len(available_numbers))
        self.numbers = self.ticked_numbers + random.sample(available_numbers, num_to_select)
        if 'bull' not in self.numbers:
            self.numbers.append('bull')

    def mark_number(self, player, number, marks):
        if number not in self.all_numbers:
            return

        if len(self.closed_numbers[number]) == len(self.players):
            return

        if player in self.closed_numbers[number]:
            self.scores[player] += (25 if number == 'bull' else number) * marks
        else:
            self.marks[player][number] += marks
            if self.marks[player][number] >= 3:
                self.marks[player][number] = 3
                self.closed_numbers[number].append(player)
                if number not in self.ticked_numbers:
                    self.ticked_numbers.append(number)
                    self.generate_numbers()
                if len(self.closed_numbers[number]) < len(self.players):
                    over_marks = self.marks[player][number] - 3
                    self.scores[player] += over_marks * (25 if number == 'bull' else number)

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
            if all(self.marks[player][number] == 3 for number in self.ticked_numbers):
                other_scores = [self.scores[p] for p in self.players if p != player]
                if self.scores[player] > max(other_scores):
                    return player
        return None

    def display_marks(self, player):
        symbols = {0: '', 1: '/', 2: '×', 3: '⊗'}
        return {number: symbols[self.marks[player][number]] for number in self.numbers}

def main():
    num_players = int(input("Hoeveel spelers: "))
    players = [input(f"Naam {i + 1}: ") for i in range(num_players)]
    game = RandomCricketGame(players)

    while True:
        current_player = players[game.current_player_index]
        print(f"\n{current_player}'s beurt")
        print(f"Beschikbare nummers: {', '.join(str(num) for num in game.numbers)}")
        darts = []
        for _ in range(3):
            number = input("Nummer: ")
            if not number:
                continue
            if number == 'bull':
                number = 'bull'
            else:
                number = int(number)
                if number not in game.numbers:
                    print("Nummer niet beschikbaar.")
                    continue
            multiplier = input("multiplier (1, 2, 3): ")
            if not multiplier:
                continue
            multiplier = int(multiplier)
            darts.append((number, multiplier))

        game.play_round(current_player, darts)
        game.next_player()

        print("\nScores:")
        header = f"{'Speler':<10} {'Score':<5} " + ' '.join(f"{str(num):<5}" for num in game.numbers)
        print(header)
        for player in players:
            marks = game.display_marks(player)
            marks_display = ' '.join(f"{marks.get(num, ''):<5}" for num in game.numbers)
            print(f"{player:<10} {game.scores[player]:<5} {marks_display}")
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