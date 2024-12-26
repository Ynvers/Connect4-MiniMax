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
        while self.potentialWinner != GameBoard.YELLOW_CHIP \
                and self.potentialWinner != GameBoard.RED_CHIP \
                and self.playedChips < Game.NUMBER_OF_CHIPS:
            time.sleep(0.05)
            # Le joueur joue
            gamer = self.get_gamer()
            print(f"Joueur actuel : {gamer}")  # Debug
            if gamer == GameBoard.RED_CHIP:
                print("L'IA joue...")  # Debug
                self.minimax_move(gamer, True)
            else:
                print("Le joueur humain joue...")  # Debug
                for event in self.gameView.pyGame.event.get():
                    self.gameView.gameBoard.display()
                    if event.type == self.gameView.pyGame.MOUSEBUTTONUP:
                        x, y = self.gameView.pyGame.mouse.get_pos()
                        print(f"Clic détecté à la position : ({x}, {y})")  # Debug
                        column = self.gameView.determine_column(x)
                        print(f"Colonne déterminée : {column}")  # Debug
                        self.make_move(column, gamer)
                    if event.type == self.gameView.pyGame.QUIT:
                        sys.exit(0)
            
            self.gamer = GameBoard.YELLOW_CHIP if self.gamer == GameBoard.RED_CHIP else GameBoard.RED_CHIP


    def random_move(self, gamer):
        available_columns = [i for i in range(7) if self.gameView.gameBoard.is_column_available(i)]
        if available_columns:
            column = random.choice(available_columns)
            self.make_move(column, gamer)

    def minimax_move(self, gamer, is_maximizing):
        best_move = None
        best_value = -float('inf') if is_maximizing else float('inf')
        for column in range(7):
            if self.gameView.gameBoard.is_column_available(column):
                self.gameView.gameBoard.put_chip(column, gamer)
                self.playedChips += 1
                move_value = self.minimax(3, not is_maximizing, -float('inf'), float('inf'))
                self.gameView.gameBoard.remove_chip(column)
                self.playedChips -= 1
                if is_maximizing:
                    if move_value > best_value:
                        best_value = move_value
                        best_move = column
                else:
                    if move_value < best_value:
                        best_value = move_value
                        best_move = column
        if best_move is not None:
            self.make_move(best_move, gamer)

    def minimax(self, depth, is_maximizing, alpha, beta):
        winner = self.gameView.gameBoard.get_winner()
        if winner == "rouge":
            return 1000000000
        elif winner == "jaune":
            return -1000000000
        elif self.playedChips == Game.NUMBER_OF_CHIPS:
            return 0

        if depth == 0:
            return self.evaluate_board()

        if is_maximizing:
            max_eval = -float('inf')
            for column in range(7):
                if self.gameView.gameBoard.is_column_available(column):
                    self.gameView.gameBoard.put_chip(column, GameBoard.RED_CHIP)
                    self.playedChips += 1
                    eval = self.minimax(depth - 1, False, alpha, beta)
                    self.gameView.gameBoard.remove_chip(column)
                    self.playedChips -= 1
                    max_eval = max(eval, max_eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for column in range(7):
                if self.gameView.gameBoard.is_column_available(column):
                    self.gameView.gameBoard.put_chip(column, GameBoard.YELLOW_CHIP)
                    self.playedChips += 1
                    eval = self.minimax(depth - 1, True, alpha, beta)
                    self.gameView.gameBoard.remove_chip(column)
                    self.playedChips -= 1
                    min_eval = min(eval, min_eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def evaluate_board(self):
        score = 0

        def evaluate_line(line):
            yellow_count = line.count(GameBoard.YELLOW_CHIP)
            red_count = line.count(GameBoard.RED_CHIP)
            if yellow_count > 0 and red_count > 0:
                return 0
            elif yellow_count == 4:
                return -1000000
            elif red_count == 4:
                return 1000000
            elif yellow_count == 3:
                return -100
            elif red_count == 3:
                return 100
            elif yellow_count == 2:
                return -10
            elif red_count == 2:
                return 10
            return 0

        for row in range(6):
            for col in range(4):
                line = [self.gameView.gameBoard.board[row][col + i] for i in range(4)]
                score += evaluate_line(line)

        # Check vertical lines
        for col in range(7):
            for row in range(3):
                line = [self.gameView.gameBoard.board[row + i][col] for i in range(4)]
                score += evaluate_line(line)

        # Check positively sloped diagonals
        for row in range(3):
            for col in range(4):
                line = [self.gameView.gameBoard.board[row + i][col + i] for i in range(4)]
                score += evaluate_line(line)

        # Check negatively sloped diagonals
        for row in range(3):
            for col in range(4):
                line = [self.gameView.gameBoard.board[row + 3 - i][col + i] for i in range(4)]
                score += evaluate_line(line)

        return score

    def make_move(self, column, gamer):
        if self.gameView.gameBoard.is_column_available(column):
            self.gameView.gameBoard.put_chip(column, gamer)
            self.playedChips += 1
            self.potentialWinner = self.gameView.gameBoard.get_winner()
            print("Gagnant ? : " + str(self.potentialWinner))  # Debug
            self.gameView.render()
            self.gameView.pyGame.display.flip()
