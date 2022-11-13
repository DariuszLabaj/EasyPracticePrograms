from enum import Enum, auto
from typing import List, Tuple

import pygame

from Blackjack.card import Card
from Blackjack.blackjackDeck import BlackjackDeck
import Blackjack.Texts as Texts
import GraphicEngine

MAX_CARDS = 14
CPU_SCORE_PASS = 17
START_AMOUNT = 5000


class GameState(Enum):
    Introduction = auto()
    Bet = auto()
    Game = auto()
    ChooseWiner = auto()
    OpponentTurn = auto()


class Window(GraphicEngine.PygameGFX):
    gameState = GameState.Introduction
    wallet = START_AMOUNT
    bet = 0
    lastWin = 0

    def Setup(self):
        self.initValues()
        self.setFont("Arial", 16)
        self.deck = BlackjackDeck(self.DisplaySurface, 120, (10, 10))
        self.createButtons()

    def createButtons(self):
        self.startButton = Window.Button(
            surface=self.DisplaySurface,
            rect=pygame.Rect(self.Width / 2 - 75, self.Height - 75, 150, 50),
            command=self.StartBet,
            label="Play",
            font=pygame.font.SysFont("ArialBold", 24),
        )
        self.passButton = Window.Button(
            surface=self.DisplaySurface,
            rect=pygame.Rect(20, self.Height / 2, 150, 50),
            command=self.StartOpponentTurn,
            label="Stand",
            font=pygame.font.SysFont("ArialBold", 24),
        )
        self.betButton = Window.Button(
            surface=self.DisplaySurface,
            rect=pygame.Rect(self.Width / 2 - 75, self.Height - 75, 150, 50),
            command=self.StartGame,
            label="Bet",
            font=pygame.font.SysFont("ArialBold", 24),
        )
        self.increaseButton = Window.Button(
            surface=self.DisplaySurface,
            rect=pygame.Rect(self.Width / 3 - 25, self.Height / 2 - 25, 50, 50),
            command=self.increaseBet,
            label="+",
            font=pygame.font.SysFont("ArialBold", 24),
        )
        self.decreaseButton = Window.Button(
            surface=self.DisplaySurface,
            rect=pygame.Rect(2 * self.Width / 3 - 25, self.Height / 2 - 25, 50, 50),
            command=self.decreaseBet,
            label="-",
            font=pygame.font.SysFont("ArialBold", 24),
        )

    def increaseBet(self):
        if self.bet + 10 <= self.wallet:
            self.bet += 10

    def decreaseBet(self):
        if self.bet - 10 >= 0:
            self.bet -= 10

    def initValues(self):
        self.playerScore = 0
        self.cpuScore = 0
        self.player: List[Card] = []
        self.cpu: List[Card] = []
        self.endscreenDelay = 1

    def StartBet(self):
        # init values
        for card in self.player:
            self.deck.discardCard(card)
        for card in self.cpu:
            self.deck.discardCard(card)
        if self.bet > self.wallet:
            self.bet = self.wallet
        self.wallet += self.lastWin
        self.initValues()
        self.gameState = GameState.Bet

    def DealCards(self):
        for _ in range(2):
            self.player.append(self.deck.getCard())
            self.cpu.append(self.deck.getCard())

    def StartGame(self):
        if self.bet <= 0 or self.wallet <= 0:
            return
        self.wallet -= self.bet
        self.DealCards()
        self.gameState = GameState.Game

    def StartOpponentTurn(self):
        self.gameState = GameState.OpponentTurn
        self.FilpCards(self.cpu, [])

    def StartChooseWiner(self):
        self.gameState = GameState.ChooseWiner
        self.FilpCards(self.cpu, [])

    def mouseReleased(self):
        if (
            self.deck
            and self.deck.Rect.collidepoint(self.mousePosition)
            and self.playerScore < 21
        ):
            self.player.append(self.deck.getCard())

    def FilpCards(self, hand: List[Card], skip: List[int]):
        for i, card in enumerate(hand):
            if i not in skip:
                if not card.flipped:
                    card.flip()
                    break

    def ShowCards(self, hand: List[Card], pos: Tuple[int, int]):
        for i, card in enumerate(hand):
            posx = (
                pos[0] + (card.width + 10) * i
                if i < MAX_CARDS / 2
                else pos[0] + 5 + (card.width + 10) * (i - int(MAX_CARDS / 2))
            )
            posy = pos[1] if i < MAX_CARDS / 2 else pos[1] + self.deck.height / 4
            card.show((posx, posy))

    @staticmethod
    def CalculateScore(hand: List[Card]) -> int:
        score = 0
        aces = 0
        for card in hand:
            cardScore = card.value
            if cardScore > 10:
                cardScore = 10
            elif cardScore == 1:
                aces += 1
            score += cardScore
        for _ in range(aces):
            if score + 10 <= 21:
                score += 10
        return score

    def drawTable(self):
        self.background((0x04, 0x61, 0x34))
        self.ShowCards(self.cpu, (190, 10))
        self.ShowCards(self.player, (100, 330))
        self.FilpCards(self.player, [])
        self.FilpCards(self.cpu, [0])

    def drawIntroduction(self):
        self.background(51)
        self.drawText(Texts.RULES, (255, 255, 255), (10, 10))
        self.startButton.update()
        self.startButton.show()

    def drawBet(self):
        self.background(51)
        nextline = self.drawText(
            f"How much you want to bet : {self.bet}",
            (255, 255, 255),
            (self.Width / 2 - 110, self.Height / 2 - 20),
        )
        self.drawText(
            f"You have in you wallet: {self.wallet}",
            (255, 255, 255),
            (self.Width / 2 - 110, nextline + 10),
        )
        self.betButton.update()
        self.betButton.show()
        self.increaseButton.update()
        self.increaseButton.show()
        self.decreaseButton.update()
        self.decreaseButton.show()

    def drawGame(self):
        self.playerScore = self.CalculateScore(self.player)
        self.drawTable()
        self.drawText(f"Your Score : {self.playerScore}", (255, 255, 255), (10, 300))
        self.deck.show()
        self.passButton.update()
        self.passButton.show()
        if self.playerScore >= 21:
            self.endscreenDelay += 1
        if self.endscreenDelay % 60 == 0:
            self.StartOpponentTurn()

    def drawOpponentTurn(self):
        self.drawTable()
        self.deck.show()
        self.cpuScore = self.CalculateScore(self.cpu)
        if self.endscreenDelay % 60 == 0:
            if self.cpuScore < self.playerScore and self.playerScore <= 21:
                self.cpu.append(self.deck.getCard())
            elif self.cpuScore == self.playerScore and self.cpuScore < CPU_SCORE_PASS:
                self.cpu.append(self.deck.getCard())
            else:
                self.StartChooseWiner()
        self.endscreenDelay += 1

    def drawChooseWiner(self):
        self.drawTable()
        if self.playerScore > 21 or (
            self.cpuScore > self.playerScore and self.cpuScore <= 21
        ):
            nextLine = self.drawText(
                f"You Lost with score : {self.playerScore}",
                (255, 255, 255),
                (10, 250),
            )
            nextLine = self.drawText(
                f"Your Opponent had : {self.cpuScore}",
                (255, 255, 255),
                (10, nextLine + 10),
            )
            self.drawText("Want to try again?", (255, 255, 255), (10, nextLine + 10))
            self.lastWin = 0
        elif self.playerScore > self.cpuScore or self.cpuScore > 21:
            nextLine = self.drawText(
                f"You Win with score : {self.playerScore}",
                (255, 255, 255),
                (10, 10),
            )
            nextLine = self.drawText(
                f"Your Opponent had : {self.cpuScore}",
                (255, 255, 255),
                (10, nextLine + 10),
            )
            self.drawText("Want to try again?", (255, 255, 255), (10, nextLine + 10))
            if self.playerScore == 21 and len(self.player) == 2:
                self.lastWin = self.bet + self.bet * 1.5
            else:
                self.lastWin = self.bet * 2
        else:
            nextLine = self.drawText(
                f"Its a draw, with score : {self.playerScore}",
                (255, 255, 255),
                (10, 10),
            )
            self.drawText("Want to try again?", (255, 255, 255), (10, nextLine + 10))
            self.lastWin = self.bet
        self.startButton.update()
        self.startButton.show()

    def Draw(self):
        match self.gameState:
            case GameState.Introduction:
                self.drawIntroduction()
            case GameState.Bet:
                self.drawBet()
            case GameState.Game:
                self.drawGame()
            case GameState.OpponentTurn:
                self.drawOpponentTurn()
            case GameState.ChooseWiner:
                self.drawChooseWiner()
