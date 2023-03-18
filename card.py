import pygame

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.image = pygame.image.load(f"data/cards/{self.value}_of_{self.suit}.png")

    def __repr__(self):
        return f"{self.value} of {self.suit}"

    def __str__(self):
        return f"{self.value} of {self.suit}"
    
    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value
    
    def get_suit(self):
        return self.suit
    
    def get_value(self):
        return self.value
    
    def get_image(self):
        return self.image
    
    def set_suit(self, suit):
        self.suit = suit

    def set_value(self, value):
        self.value = value

    def set_image(self, image):
        self.image = image