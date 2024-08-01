#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import random

from GameView import *


class Game:
    NUMBER_OF_CHIPS = 42

    def __init__(self):
        self.gamer = 1
        self.playedChips = 0
        self.potentialWinner = False
        self.gameView = GameView()

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
            gamer = self.get_gamer()
            if gamer == GameBoard.RED_CHIP:
                self.random_move(gamer)
            else: 
                for event in self.gameView.pyGame.event.get():

                    self.gameView.gameBoard.display()

                    if event.type == self.gameView.pyGame.MOUSEBUTTONUP:
                        x, y = self.gameView.pyGame.mouse.get_pos()
                        gamer = self.get_gamer()
                        column = self.gameView.determine_column(x)
                        self.make_move(column, gamer)

                    if event.type == self.gameView.pyGame.QUIT:
                        sys.exit(0)

    def random_move(self, gamer):
        available_columns = [i for i in range(7) if self.gameView.gameBoard.is_column_available(i)]
        if available_columns: 
            column = random.choice(available_columns)
            self.make_move(column, gamer)

    def make_move(self, column, gamer):
        self.gameView.gameBoard.put_chip(column, gamer)
        self.playedChips += 1
        self.potentialWinner = self.gameView.gameBoard.get_winner()
        print("Gagnant ? : " + str(self.potentialWinner))
        self.gameView.render()
        self.gameView.pyGame.display.flip()