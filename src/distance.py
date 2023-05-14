from typing import List

from constants import *


class Distance():
    def __init__(self):
        self.ratingСolumnNumber = RATING_COLUMN_NUMBER
        self.ratingRange = RATING_RANGE


    def goverDistance(self, elem1: List[str], elem2: List[str]) -> float:
        '''
        Возвращает расстояние Говера между двумя элементами
        '''
        sumCoeffDiff = 0
        
        for i in range(1, len(elem1)):
            if i == self.ratingСolumnNumber:
                coeffDiff = abs(int(elem1[i]) - int(elem2[i])) / self.ratingRange
            elif elem1[i] == elem2[i]:
                coeffDiff = 0
            else:
                coeffDiff = 1

            sumCoeffDiff += coeffDiff

        return sumCoeffDiff / (len(elem1) - 1)


    def createDissimilarityMatrix(self, arr: List[List[str]]) -> List[List[float]]:
        '''
        Построение матрицы несходств с помощью расстояния Говера
        '''
        size = len(arr)
        matrix = [ [0] * size for _ in range(size) ]

        for i in range(size - 1):
            for j in range(i + 1, size):
                matrix[i][j] = self.goverDistance(arr[i], arr[j])
                matrix[j][i] = matrix[i][j]

        return matrix
    