from __future__ import annotations
from functools import cached_property
import pygame
from Blackjack.cardSuits import CardSuits
from Blackjack.cardValues import CardValues


class Card:
    heightRatio: float = 1.4
    border = 5
    radius = 10

    @cached_property
    def __backRect(self) -> pygame._common._RectValue:
        return pygame.Rect(
            self.border,
            self.border,
            self.__rect.width - self.border * 2,
            self.__rect.height - self.border * 2,
        )

    @cached_property
    def value(self) -> int:
        return self.__cardValue.value

    @property
    def Rect(self) -> pygame._common._RectValue:
        return self.__rect

    @property
    def flipped(self) -> bool:
        return not self.__revers

    @cached_property
    def width(self) -> int:
        return self.__rect.width

    @cached_property
    def height(self) -> int:
        return self.__rect.height

    @property
    def __cardFilpped(self) -> bool:
        if self.__lastState != self.__revers:
            self.__lastState = self.__revers
            return True
        else:
            return False

    def __init__(
        self,
        surface: pygame.Surface,
        suit: CardSuits,
        cardValue: CardValues,
        width: int,
    ):
        self.__sruface = surface
        self.__suit = suit
        self.__cardValue = cardValue
        self.__rect = pygame.Rect(0, 0, width, width * 1.4)
        self.__font = pygame.font.SysFont("Arial", size=int(self.__rect.height / 6))
        self.__charFont = pygame.font.SysFont("Arial", size=int(self.__rect.height / 4))
        self.__suitChar = ""
        self.__vlaChar = ""
        self.__revers = True
        self.__lastState = False
        self.__textColor = (0xE1, 0x13, 0x16)
        self.color = (0xE1, 0x13, 0x16)
        self.__createSurface()
        match self.__suit:
            case CardSuits.Clubs:
                self.__suitChar = "♣"
                self.__textColor = (0x00, 0x00, 0x00)
            case CardSuits.Diamonds:
                self.__suitChar = "♦"
                self.__textColor = (0xE1, 0x13, 0x16)
            case CardSuits.Hearts:
                self.__suitChar = "♥"
                self.__textColor = (0xE1, 0x13, 0x16)
            case CardSuits.Spades:
                self.__suitChar = "♠"
                self.__textColor = (0x00, 0x00, 0x00)
        match self.__cardValue:
            case CardValues.Ace:
                self.__vlaChar = "A"
            case CardValues.two:
                self.__vlaChar = "2"
            case CardValues.three:
                self.__vlaChar = "3"
            case CardValues.four:
                self.__vlaChar = "4"
            case CardValues.five:
                self.__vlaChar = "5"
            case CardValues.six:
                self.__vlaChar = "6"
            case CardValues.seven:
                self.__vlaChar = "7"
            case CardValues.eight:
                self.__vlaChar = "8"
            case CardValues.nine:
                self.__vlaChar = "9"
            case CardValues.ten:
                self.__vlaChar = "10"
            case CardValues.Jack:
                self.__vlaChar = "J"
            case CardValues.Queen:
                self.__vlaChar = "Q"
            case CardValues.King:
                self.__vlaChar = "K"
            case CardValues.Joker:
                self.__vlaChar = "JOKER"

    def __createSurface(self):
        self.__drawSurf = pygame.Surface(self.__rect.size, pygame.SRCALPHA)

    def __prepareValueText(self, top: bool):
        labelWidth, labelHeihgt = self.__font.size(
            self.__vlaChar + " " + self.__suitChar
        )
        if top:
            textX = self.border
            textY = self.border
        else:
            textX = self.__rect.width - labelWidth - self.border
            textY = self.__rect.height - labelHeihgt - self.border
        return (
            self.__font.render(
                self.__vlaChar + " " + self.__suitChar, True, self.__textColor
            ),
            textX,
            textY,
        )

    def __prepareSuiteText(self):
        labelWidth, labelHeihgt = self.__charFont.size(self.__suitChar)
        textX = self.__rect.centerx - labelWidth / 2
        textY = self.__rect.centery - labelHeihgt / 2
        return (
            self.__charFont.render(self.__suitChar, True, self.__textColor),
            textX,
            textY,
        )

    def flip(self):
        self.__revers = not self.__revers

    def show(self, position: pygame._common._Coordinate):
        if self.__cardFilpped:
            self.__createSurface()
            pygame.draw.rect(
                self.__drawSurf, (255, 255, 255), self.__rect, 0, self.radius
            )
            pygame.draw.rect(
                self.__drawSurf, (0, 0, 0), self.__rect, 1, self.radius
            )
            if self.__revers:
                pygame.draw.rect(
                    self.__drawSurf, self.color, self.__backRect, 0, self.radius
                )
            else:
                text, textX, textY = self.__prepareValueText(True)
                self.__drawSurf.blit(text, (textX, textY))
                text, textX, textY = self.__prepareValueText(False)
                self.__drawSurf.blit(text, (textX, textY))
                text, textX, textY = self.__prepareSuiteText()
                self.__drawSurf.blit(text, (textX, textY))
        self.__sruface.blit(self.__drawSurf, position)
