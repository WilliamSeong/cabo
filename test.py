import random
import main

class TestGame(Game):
    def test_game(self, player1, player2, deck):
        self.players = [player1, player2]
        self.deck = deck
        self.active = []
        self.cabo = -1

    

