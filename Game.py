import sys
import time

from GameInterface import *


class Game:
    NUMBER_OF_CHIPS = 42

    def __init__(self):
        self.gamer = 1
        self.playedChips = 0
        self.potentialWinner = False
        self.gameInterface = GameInterface()

    def get_gamer(self):
        # Cette fonction retourne le numero du joueur qui doit jouer
        if self.playedChips % 2 == 0:
            gamer_id = GameBoard.YELLOW_CHIP
        else:
            gamer_id = GameBoard.RED_CHIP
        return gamer_id

    def display_winner(self):
        if self.gamer == "" or self.gamer is None:
            return "personne n'a gagne"
        else:
            return self.gamer + " a gagne"

    def start(self):
        while self.potentialWinner != "jaune" \
                and self.potentialWinner != "rouge" \
                and self.playedChips < Game.NUMBER_OF_CHIPS:
            time.sleep(0.05)
            # Le joueur joue
            for event in self.gameInterface.pyGame.event.get():

                self.gameInterface.gameBoard.display()

                if event.type == self.gameInterface.pyGame.MOUSEBUTTONUP:
                    x, y = self.gameInterface.pyGame.mouse.get_pos()
                    gamer = self.get_gamer()
                    column = self.gameInterface.determine_column(x)
                    # On modifie les variables pour tenir compte du jeton depose.
                    self.gameInterface.gameBoard.put_chip(column, gamer)
                    self.playedChips = self.playedChips + 1
                    self.potentialWinner = self.gameInterface.gameBoard.get_winner()
                    print("GAGNANT ? : " + str(self.potentialWinner))
                    self.gameInterface.render()
                    self.gameInterface.pyGame.display.flip()

                if event.type == self.gameInterface.pyGame.QUIT:
                    sys.exit(0)