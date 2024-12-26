#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GameBoard:
    EMPTY_BOX = 0
    RED_CHIP = -1
    YELLOW_CHIP = 1
    YELLOW_WIN = 4
    RED_WIN = -4

    def __init__(self):
        self.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]

    def get_horizontal_winner(self):
        for line in range(6):
            for column in range(4):
                if self.board[line][column] == self.board[line][column + 1] == self.board[line][column + 2] == self.board[line][column + 3] != GameBoard.EMPTY_BOX:
                    return self.board[line][column]
        return GameBoard.EMPTY_BOX

    def get_vertical_winner(self):
        for column in range(7):
            for line in range(3):
                if self.board[line][column] == self.board[line + 1][column] == self.board[line + 2][column] == self.board[line + 3][column] != GameBoard.EMPTY_BOX:
                    return self.board[line][column]
        return GameBoard.EMPTY_BOX

    def get_diagonals_winner(self):
        for line in range(3):
            for column in range(4):
                if self.board[line][column] == self.board[line + 1][column + 1] == self.board[line + 2][column + 2] == self.board[line + 3][column + 3] != GameBoard.EMPTY_BOX:
                    return self.board[line][column]
                if self.board[line + 3][column] == self.board[line + 2][column + 1] == self.board[line + 1][column + 2] == self.board[line][column + 3] != GameBoard.EMPTY_BOX:
                    return self.board[line + 3][column]
        return GameBoard.EMPTY_BOX

    def get_winner(self):
        winner = self.get_horizontal_winner()
        if winner != GameBoard.EMPTY_BOX:
            return winner
        winner = self.get_vertical_winner()
        if winner != GameBoard.EMPTY_BOX:
            return winner
        winner = self.get_diagonals_winner()
        if winner != GameBoard.EMPTY_BOX:
            return winner
        return GameBoard.EMPTY_BOX

    def put_chip(self, column, gamer):
        # boucle sur les lines de bas en haut
        line = 5  # par le bas 5 4 3 2 1 0
        #  ATTENTION CECI est different de l'encodage des pions. peut on utiliser true or false
        # False je continue, truej'arrete
        stop = False
        while line >= 0 and stop == False:
            # si j'ai une case vide pour la column concernee
            if self.board[line][column] == GameBoard.EMPTY_BOX:
                if gamer == GameBoard.YELLOW_CHIP:
                    # je mets mon pion jaune
                    self.board[line][column] = GameBoard.YELLOW_CHIP
                    # vu que je viens de placer mon pion, je ne vais pas en placer d'autres.
                    stop = True
                else:
                    self.board[line][column] = GameBoard.RED_CHIP
                    stop = True
            # je remonte de bas en haut avec column fixee dans board
            line = line - 1  # faire le parcours de bas en haut, parce que c'est plus performant (condition arret atteinte plus tot)

    def remove_chip(self, column):
        for line in range(6):
            if self.board[line][column] != GameBoard.EMPTY_BOX:
                self.board[line][column] = GameBoard.EMPTY_BOX
                break

    # Methode purement technique d'aide a la representation
    def reverse_game_board(self):
        # par exemple la ligne d'en bas se retrouve en haut
        reversed_game_board = []
        for row in range(5, -1, -1):
            reversed_game_board.append(self.board[row])
        return reversed_game_board

    def display(self):
        print("\n")
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j], end=' ')
            print()
        print("\n")

    def is_column_available(self, column):
        return self.board[0][column] == GameBoard.EMPTY_BOX
