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
        # initialisation des variables
        # conserver le winner, vide si pas de winner
        winner = ""
        # variable utilisee pour la boucle while
        line = 5
        # variable qui sert a arret si on trouve le winner
        stop = False
        # raisonnement similaire, plus performant qu'un parcours traditionnel
        # on boucle tant qu'on n'a pas atteint (la line) 0 et que l'on a pas de winner
        # le while nous permet de nous deplacer dans les lines de bas en haut (line 5 --> line 0)
        while line >= 0 and stop == False:
            for column in range(4):  # ca nous permet deplacer dans les columns
                # pourquoi 4 ? 4 possibilites de gagner dans une line
                # on determine le winner en fonction des valeurs definies dans les 4 columns (que l'on decale grace a la variable column) que l'on regarde pour la line donnee i
                if self.board[line][column] + self.board[line][column + 1] + self.board[line][column + 2] + \
                        self.board[line][column + 3] == GameBoard.YELLOW_WIN:  # gamer jaune gagne
                    # on affecte le winner (car on a nom nombre de points)
                    winner = "jaune"
                    print(winner)
                    # vu qu'on a gagne on arrete les parcours
                    stop = True
                if self.board[line][column] + self.board[line][column + 1] + self.board[line][column + 2] + \
                        self.board[line][column + 3] == GameBoard.RED_WIN:  # gamer rouge gagne
                    winner = "rouge"
                    print(winner)
                    stop = True
            # on remonte la line
            line = line - 1
        # retourne la variable winner
        return winner

    def get_vertical_winner(self):
        winner = ""
        # on regarde chaque column
        for column in range(7):
            # on descend les lines pour la column concernee, pour verifier s'il y a un winner
            # tant que la line est strictement superieur a 2
            # 5 YELLOW_WINNER 3 en baissant de -1 (3eme parametre du for)
            # c'est plus concis que ce qu'on a au-dessous
            for line in range(5, 2, -1):
                if self.board[line][column] + self.board[line - 1][column] + self.board[line - 2][column] + \
                        self.board[line - 3][column] == GameBoard.YELLOW_WIN:
                    winner = "jaune"
                if self.board[line][column] + self.board[line - 1][column] + self.board[line - 2][column] + \
                        self.board[line - 3][column] == GameBoard.RED_WIN:
                    winner = "rouge"
        return winner

    def get_diagonals_winner(self):
        winner = ""
        # on va diagonale d'en haut a gauche vers en bas a droite
        # on avance dans les lines
        for line in range(3):
            # on avance dans les columns
            for column in range(4):
                # vu que c'est en meme on avance en diagonale
                if self.board[line][column] + self.board[line + 1][column + 1] + self.board[line + 2][column + 2] + \
                        self.board[line + 3][column + 3] == GameBoard.YELLOW_WIN:
                    winner = "jaune"
                if self.board[line][column] + self.board[line + 1][column + 1] + self.board[line + 2][column + 2] + \
                        self.board[line + 3][column + 3] == GameBoard.RED_WIN:
                    winner = "rouge"
        # on va diagonale d'en haut a droite vers en bas a gauche
        for line in range(3):
            # 0 1 2 3, la line a laquelle on commence
            for column in range(3, 7):
                # 3 4 5 6, on commence a la column 3 pour aller vers la 6
                if self.board[line][column] + self.board[line + 1][column - 1] + self.board[line + 2][column - 2] + \
                        self.board[line + 3][column - 3] == GameBoard.YELLOW_WIN:
                    winner = "jaune"
                if self.board[line][column] + self.board[line + 1][column - 1] + self.board[line + 2][column - 2] + \
                        self.board[line + 3][column - 3] == GameBoard.RED_WIN:
                    winner = "rouge"
        return winner

    def get_winner(self):
        # on verifie q'il winner d'abord horizontalement
        gamer = self.get_horizontal_winner()
        # s'il y a un winner, je n'ai pas besoin de verifier les autres cas
        # s'il n'y pas de winner je vais pas sur le return donc je peux continuer les autres etapes de la verification
        if gamer != "":
            return gamer
        gamer = self.get_vertical_winner()
        if gamer != "":
            return gamer
        gamer = self.get_diagonals_winner()
        if gamer != "":
            return gamer

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
