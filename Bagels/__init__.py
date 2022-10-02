from enum import Enum, auto
import random
from typing import List
import pygame
import GraphicEngine
import Bagels.Texts.Introduction as introduction


NUM_DIGITS = 3
MAX_GUESSES = 10


class GameState(Enum):
    Introduction = auto()
    Game = auto()
    Win = auto()
    Lost = auto()


class Window(GraphicEngine.PygameGFX):
    def Setup(self):
        self.background(51)
        self.gameStae = GameState.Introduction
        self.noOfTriesLeft = 10
        self.setFont("Arial", 16)
        self.font = pygame.font.SysFont("Arial", 16)
        nextlineY = self.drawText(introduction.INTRODUCTION, (255, 255, 255), (10, 10))
        for rule in introduction.RULES:
            nextlineY = self.drawText(rule, (255, 255, 255), (30, nextlineY + 10))
        nextlineY = self.drawText(
            introduction.EXAMPLE, (255, 255, 255), (10, nextlineY + 10)
        )
        self.button = Window.Button(
            surface=self.DisplaySurface,
            rect=pygame.Rect(self.Width / 2 - 75, self.Height - 75, 150, 50),
            command=self.ButtonPressed,
            label="Rozpocznij",
            font=pygame.font.SysFont("ArialBold", 24),
        )
        self.guesses: List[str] = []
        self.guess = ""
        self.guessDisplay = Window.TextInput(
            surface=self.DisplaySurface,
            rect=pygame.Rect(
                self.Width / 3, self.Height - self.Height / 3, self.Width / 3, 30
            ),
            text=self.guess,
            font=pygame.font.SysFont("Arial", 24),
        )

    @staticmethod
    def getSecretNum() -> str:
        numbers = list("0123456789")
        random.shuffle(numbers)
        secretNum = "".join(numbers[:NUM_DIGITS])
        return secretNum

    @staticmethod
    def getClues(guess: str, secretNum: str):
        clues: List[str] = []
        for i in range(len(guess)):
            if guess[i] == secretNum[i]:
                clues.append("Fermi")
            elif guess[i] in secretNum:
                clues.append("Pico")
        if clues:
            clues.sort()
            return " ".join(clues)
        else:
            return "Bagels"

    def keyReleased(self):
        keyCodeToByte = self.keyCode.to_bytes(4, "big", signed=False)
        try:
            text = keyCodeToByte.decode("utf-8").strip("\x00")
        except UnicodeDecodeError:
            text = ""
        if text.isdigit() and len(self.guess) < NUM_DIGITS and text not in self.guess:
            self.guess += text
        if len(self.guess) >= NUM_DIGITS:
            self.guessPlaced()

    def guessPlaced(self):
        clues = Window.getClues(self.guess, self.secretNum)
        self.guesses.append(f"Number: {self.guess} | {clues}")
        self.guess = ""
        if clues == ' '.join(["Fermi"]*NUM_DIGITS):
            self.gameStae = GameState.Win
        elif len(self.guesses) >= MAX_GUESSES:
            self.gameStae = GameState.Lost

    def ButtonPressed(self):
        self.gameStae = GameState.Game
        self.guesses: List[str] = []
        self.secretNum = self.getSecretNum()

    def Draw(self):
        match self.gameStae:
            case GameState.Introduction:
                self.button.update()
                self.button.show()
            case GameState.Game:
                self.background(51)
                nextlineY = self.drawText(
                    "I Have a number in mind...", (255, 255, 255), (10, 10)
                )
                nextlineY = self.drawText(
                    f"You Have {self.noOfTriesLeft} tries left to guess the number.",
                    (255, 255, 255),
                    (10, nextlineY + 10),
                )
                for i, guess in enumerate(self.guesses):
                    nextlineY = self.drawText(
                        f"Guess #{i+1}: {guess}",
                        (255, 255, 255),
                        (10, nextlineY + 10),
                    )
                self.guessDisplay.update(self.guess)
                self.guessDisplay.show()
            case GameState.Win:
                self.background(51)
                nextlineY = self.drawText(
                    f"Congratulations you Have Won. I was thinking of {self.secretNum}",
                    (255, 255, 255),
                    (10, 10),
                )
                self.button.update()
                self.button.show()
            case GameState.Lost:
                self.background(51)
                nextlineY = self.drawText(
                    f"What a shame. You Have Lost. I was thinking of {self.secretNum}",
                    (255, 255, 255),
                    (10, 10),
                )
                self.button.update()
                self.button.show()
