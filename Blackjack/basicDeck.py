from __future__ import annotations
import pygame
import random
from Blackjack.card import Card
from Blackjack.cardSuits import CardSuits
from Blackjack.cardValues import CardValues
from abc import ABC, abstractmethod
from typing import List


class BasicDeck(ABC):
    @property
    def AmountInDiscard(self) -> int:
        return len(self._discard)

    @property
    def height(self) -> int:
        return self.__topCard.height

    @property
    def newAmopunt(self) -> bool:
        if self.__lastAmout != len(self._cards):
            self.__lastAmout = len(self._cards)
            return True
        else:
            return False

    @property
    def Rect(self) -> pygame._common._RectValue:
        return self.__deckRect

    def __init__(
        self, surface: pygame.Surface, width: int, position: pygame._common._Coordinate
    ):
        self._sruface = surface
        self._width = width
        self._cards: List[Card] = []
        self._discard: List[Card] = []
        self.__drawSurf = pygame.Surface((width, width * 1.4), pygame.SRCALPHA)
        self.__topCard = Card(
            self.__drawSurf, CardSuits.Clubs, CardValues.Ace, self._width
        )
        self.__deckRect = pygame.Rect(position[0], position[1], self.__topCard.width, self.__topCard.height)
        self.__lastAmout = 0
        self.__position = position
        self.createDeck()

    @abstractmethod
    def createDeck(self):
        ...

    def discardCard(self, card: Card):
        card.flip()
        self._discard.append(card)

    def shuffleDiscard(self):
        random.shuffle(self._discard)
        self._cards = self._discard.copy()
        self._discard: List[Card] = []

    def getCard(self) -> Card:
        if len(self._cards) < 1:
            self.shuffleDiscard()
        return self._cards.pop()

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
            for i in range(len(self._cards)):
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
            self.__deckRect = self.__getDeckRect(len(self._cards))
            pygame.draw.rect(
                self.__drawSurf,
                self.__topCard.color,
                pygame.Rect(
                    len(self._cards) + self.__topCard.border,
                    int(len(self._cards) / 2) + self.__topCard.border,
                    self.__topCard.width - self.__topCard.border * 2,
                    self.__topCard.height - self.__topCard.border * 2,
                ),
                0,
                self.__topCard.radius,
            )
        self._sruface.blit(self.__drawSurf, self.__position)
