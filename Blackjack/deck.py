from __future__ import annotations
from operator import pos
import pygame
import random
from Blackjack.card import Card
from Blackjack.cardSuits import CardSuits
from Blackjack.cardValues import CardValues
from typing import List


class Deck:
    @property
    def AmountInDiscard(self) -> int:
        return len(self.__discard)

    @property
    def height(self) -> int:
        return self.__topCard.height

    @property
    def newAmopunt(self) -> bool:
        if self.__lastAmout != len(self.__cards):
            self.__lastAmout = len(self.__cards)
            return True
        else:
            return False

    @property
    def Rect(self) -> pygame._common._RectValue:
        return self.__deckRect

    def __init__(
        self, surface: pygame.Surface, width: int, position: pygame._common._Coordinate
    ):
        self.__sruface = surface
        self.__width = width
        self.__cards: List[Card] = []
        self.__discard: List[Card] = []
        self.__drawSurf = pygame.Surface((width, width * 1.4), pygame.SRCALPHA)
        self.__topCard = Card(
            self.__drawSurf, CardSuits.Clubs, CardValues.Ace, self.__width
        )
        self.__deckRect = pygame.Rect(position[0], position[1], self.__topCard.width, self.__topCard.height)
        self.__lastAmout = 0
        self.__position = position
        self.createDeck()

    def createDeck(self):
        self.__cards: List[Card] = []
        self.__discard: List[Card] = []
        for suit in CardSuits:
            for card in CardValues:
                if card != CardValues.Joker:
                    self.__cards.append(Card(self.__sruface, suit, card, self.__width))
        random.shuffle(self.__cards)

    def discardCard(self, card: Card):
        card.flip()
        self.__discard.append(card)

    def shuffleDiscard(self):
        random.shuffle(self.__discard)
        self.__cards = self.__discard.copy()
        self.__discard: List[Card] = []

    def getCard(self) -> Card:
        if not self.__cards:
            self.shuffleDiscard()
        return self.__cards.pop()

    def __createSurface(self):
        rect = pygame.Rect(
            0,
            0,
            int(self.__topCard.width + self.__lastAmout),
            int(self.__topCard.height + (self.__lastAmout / 2)),
        )
        self.__drawSurf = pygame.Surface(rect.size, pygame.SRCALPHA)

    def __getDeckRect(self, cardNo: int) -> pygame._common._RectValue:
        return pygame.Rect(
            cardNo, cardNo / 2, self.__topCard.width, self.__topCard.height
        )

    def show(self):
        if self.newAmopunt:
            self.__createSurface()
            for i in range(len(self.__cards)):
                if i % 2 == 0:
                    color = (128, 128, 128)
                else:
                    color = (255, 255, 255)
                pygame.draw.rect(
                    self.__drawSurf,
                    color,
                    self.__getDeckRect(i),
                    0,
                    self.__topCard.radius,
                )
            self.__deckRect = self.__getDeckRect(len(self.__cards))
            pygame.draw.rect(
                self.__drawSurf,
                self.__topCard.color,
                pygame.Rect(
                    len(self.__cards) + self.__topCard.border,
                    int(len(self.__cards) / 2) + self.__topCard.border,
                    self.__topCard.width - self.__topCard.border * 2,
                    self.__topCard.height - self.__topCard.border * 2,
                ),
                0,
                self.__topCard.radius,
            )
        self.__sruface.blit(self.__drawSurf, self.__position)
