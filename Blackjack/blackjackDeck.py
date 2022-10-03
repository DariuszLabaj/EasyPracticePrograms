from __future__ import annotations
import pygame
import random
from Blackjack.card import Card
from Blackjack.cardSuits import CardSuits
from Blackjack.cardValues import CardValues
from Blackjack.basicDeck import BasicDeck
from typing import List


class BlackjackDeck(BasicDeck):
    def __init__(
        self, surface: pygame.Surface, width: int, position: pygame._common._Coordinate
    ):
        super(BlackjackDeck, self).__init__(surface, width, position)

    def createDeck(self):
        self._cards: List[Card] = []
        self._discard: List[Card] = []
        for suit in CardSuits:
            for card in CardValues:
                if card != CardValues.Joker:
                    self._cards.append(Card(self._sruface, suit, card, self._width))
        random.shuffle(self._cards)
