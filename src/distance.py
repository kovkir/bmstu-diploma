from typing import List

from constants import *


class Distance():
    def __init__(self):
        self.numericColumns = NUMERIC_COLUMNS
        self.rangesList = RANGES_LIST


    def goverDistance(self, elem1: List[str], elem2: List[str]) -> float:
        '''
        Возвращает расстояние Говера между двумя элементами
        '''
        sumCoeffDiff = 0
        numberColumns = len(elem1)
        
        for columnNumber in range(1, numberColumns):
            # если столбец содержит числовые данные
            try:
                i = self.numericColumns.index(columnNumber)
                coeffDiff = abs(int(elem1[columnNumber]) - int(elem2[columnNumber])) \
                     / self.rangesList[i]
                
            # если столбец содержит категориальные данные
            except ValueError:
                if elem1[columnNumber] == elem2[columnNumber]:
                    coeffDiff = 0
                else:
                    coeffDiff = 1

            sumCoeffDiff += coeffDiff

        return sumCoeffDiff / (numberColumns - 1)


    def createDissimilarityMatrix(self, objects: List[List[str]]) -> List[List[float]]:
        '''
        Построение матрицы несходства с помощью расстояния Говера
        '''
        numbObjects = len(objects)
        matrix = [ [0] * numbObjects for _ in range(numbObjects) ]

        for i in range(numbObjects - 1):
            for j in range(i + 1, numbObjects):
                matrix[i][j] = self.goverDistance(objects[i], objects[j])
                matrix[j][i] = matrix[i][j]

        return matrix
    