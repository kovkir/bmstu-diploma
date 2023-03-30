from typing import List
from random import shuffle

from haClusterization import HAClusterization
from kPrototypesClusterization import KPrototypesClusterization
from hybridClusterization import HybridClusterization
from distance import Distance
from test import Test
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


def createDissimilarityMatrix(arr: List[List[str]], size: int) -> List[List[float]]:
    '''
    Построение матрицы несходств с помощью расстояния Говера
    '''
    matrix = [ [0] * size for _ in range(size) ]
    distance = Distance()

    for i in range(size - 1):
        for j in range(i + 1, size):
            matrix[i][j] = distance.goverDistance(arr[i], arr[j])
            matrix[j][i] = matrix[i][j]

    return matrix


def main():
    players = readFile(FILE_NAME)
    dissimilarityMatrix = createDissimilarityMatrix(players, MAX_CLUSTER_NUMBERS)

    # haClusterization = HAClusterization(dissimilarityMatrix.copy())
    # haClusterization.buildDendrogram()
    # haClusterization.buildGraph()

    # kPrototypesClusterization = KPrototypesClusterization(players, CLUSTER_NUMBERS)
    # hybridClusterization = HybridClusterization(players, dissimilarityMatrix.copy(), CLUSTER_NUMBERS)

    test = Test(players, dissimilarityMatrix)
    test.comparisonMethods()


if __name__ == "__main__":
    main()
