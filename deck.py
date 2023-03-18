import card
import random

class Deck:
    def __init__(self):
        self.cards = []

    def build(self):
        for suit in ["hearts", "diamonds", "clubs", "spades"]:
            for value in ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]:
                self.cards.append(card.Card(suit, value))

    def get_cards(self):
        return self.cards

    def show(self):
        for card in self.cards:
            print(card)

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            rand = random.randint(0, i)
            self.cards[i], self.cards[rand] = self.cards[rand], self.cards[i]

    def draw_card(self):
        return self.cards.pop()
    
    def add_card(self, card):
        self.cards.append(card)

    def value(self):
        value = [0]
        ace_count = 0
        for card in self.cards:
            if card.get_value() == "ace":
                ace_count += 1
                value[0] += 11
            elif card.get_value() == "jack" or card.get_value() == "queen" or card.get_value() == "king":
                value[0] += 10
            else:
                value[0] += int(card.get_value())
        for i in range(ace_count):
            value.append(value[0] - 10)
        return value
    
    def best_value(self):
        value = self.value()
        for i in range(len(value)):
            if value[i] > 21:
                value[i] = 0
        return max(value)