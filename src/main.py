from typing import List
from random import shuffle

from window import Window
from constants import *


def readFile(nameFile: str) -> List[List[str]]:
    '''
    Возвращает перемешанный список игроков из файла
    '''
    file = open(nameFile, 'r')
    players = file.read().split("\n")
    file.close()

    for i in range(len(players)):
        players[i] = players[i].split(",")

    # перемешать список
    shuffle(players)
    return players


def main(): 
    players = readFile(FILE_NAME)
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, players)
    window.run()


if __name__ == "__main__":
    main()
