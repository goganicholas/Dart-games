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
            return  # Geen punten meer 

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
            number = input("Welk nummer heb je gegooid? (20, 19, 18, 17, 16, 15, bull): ")
            if not number:
                continue
            if number == 'bull':
                number = 'bull'
            else:
                number = int(number)
            multiplier = input("multiplier (1, 2, 3): ")
            if not multiplier:
                continue
            multiplier = int(multiplier)
            darts.append((number, multiplier))

        game.play_round(current_player, darts)
        game.next_player()

        print("\nScores :")
        print(f"{'Speler':<10} {'Score':<5} {'20':<3} {'19':<3} {'18':<3} {'17':<3} {'16':<3} {'15':<3} {'Bull':<8}")
        for player in players:
            marks = game.display_marks(player)
            print(f"{player:<10} {game.scores[player]:<5} {marks[20]:<3} {marks[19]:<3} {marks[18]:<3} {marks[17]:<3} {marks[16]:<3} {marks[15]:<3} {marks['bull']:<8}")
        winner = game.check_winner()
        if winner:
            print(f"\n {winner} wint!")
            break
        else:
            print("\n speel verder")

    while True:
        exit_input = input("typ 'exit': ")
        if exit_input.lower() == 'exit':
            break

if __name__ == "__main__":
    main()
