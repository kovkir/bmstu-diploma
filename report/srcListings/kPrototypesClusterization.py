# K-Prototypes Clusterization

from matplotlib import pyplot as plt
from typing import List, Union
from random import randint

from distance import Distance
from constants import *


class KPrototypesClusterization():
    objects: List[List[str]] # список объектов
    k: int                   # количество кластеров
    clusterContents: List[List[int]] # массив, содержащий в себе k массивов c номерами элементов, принадлежащих соответствующему кластеру
    clusterCenters: List[List[Union[str, int]]] # массив, содержащий в себе k центров кластеров

    def __init__(self, objects: List[List[str]], k: int, clusterContents: Union[List[List[int]], None]=None):
        self.objects = objects
        self.k = k
        self.clusterContents, self.clusterCenters = self.run(clusterContents)

    def generateClusterCenters(self) -> List[List[Union[str, int]]]:
        '''
        Возвращает массив с k центрами кластерами
        '''
        clusterCenters = []
        numbObjects = len(self.objects)
        numberColumns = len(self.objects[0])

        for _ in range(self.k):
            clusterCenter = []
            for columnNumber in range(numberColumns):
                field = self.objects[randint(0, numbObjects - 1)][columnNumber]
                clusterCenter.append(field)

            clusterCenters.append(clusterCenter)

        return clusterCenters
    
    def getAverageField(self, clusterNumbers: List[int], columnNumber: int) -> float:
        '''
        Возвращает среднее значение поля в столбце среди элементов кластера
        '''
        sumValue = 0
        for i in clusterNumbers:
            sumValue += int(self.objects[i][columnNumber])
        
        return sumValue / len(clusterNumbers)

    def getMostPopularField(self, clusterNumbers: List[int], columnNumber: int) -> str:
        '''
        Возвращает самое встречаемое поле в столбце среди элементов кластера
        '''
        repetitions = {}
        for i in clusterNumbers:
            key = self.objects[i][columnNumber]

            if key in repetitions.keys():
                repetitions[key] += 1
            else:
                repetitions[key] = 1

        maxRep = max(repetitions.values())
        for key, value in repetitions.items():
            if value == maxRep:
                return key 

    def recalculateClusterCenters(self, 
            oldClusterCenters: List[List[Union[str, float]]], 
            clusterContents: List[List[int]]) -> List[List[Union[str, float]]]:
        '''
        Возвращает массив с k центрами кластерами
        '''
        clusterCenters = []
        numberColumns = len(self.objects[0])
    
        for i in range(self.k):
            if len(clusterContents[i]) > 0:
                clusterCenter = []
                for columnNumber in range(numberColumns):
                    if columnNumber in NUMERIC_COLUMNS:
                        field = self.getAverageField(clusterContents[i], columnNumber)
                    else:
                        field = self.getMostPopularField(clusterContents[i], columnNumber)

                    clusterCenter.append(field)
                clusterCenters.append(clusterCenter)
            else:
                # если кластер пуст
                clusterCenters.append(oldClusterCenters[i].copy())

        return clusterCenters
    
    def createMatrixDistances(self, clusterCenters: List[List[Union[str, float]]]) -> List[List[float]]:
        '''
        Возвращает матрицу растояний от элементов до центров кластеров
        '''
        numbObjects = len(self.objects)
        matrix = [ [0] * self.k for _ in range(numbObjects) ]
        distance = Distance()

        for i in range(numbObjects):
            for j in range(self.k):
                matrix[i][j] = distance.goverDistance(self.objects[i], clusterCenters[j])

        return matrix

    def distributeElemsIntoClusters(self, clusterCenters: List[List[Union[str, float]]]) -> List[List[int]]:
        '''
        Возвращает массив, содержащий в себе k массивов c номерами элементов, принадлежащих соответствующему кластеру
        '''
        clusterContents = [ [] for _ in range(self.k) ]
        matrixDistances = self.createMatrixDistances(clusterCenters)

        for i in range(len(matrixDistances)):
            jMin = 0
            minDistr = matrixDistances[i][jMin]
            
            for j in range(1, self.k):
                if matrixDistances[i][j] < minDistr:
                    jMin = j
                    minDistr = matrixDistances[i][jMin]

            clusterContents[jMin].append(i)

        return clusterContents
    
    def run(self, clusterContents: Union[List[List[int]], None]) -> List[List[int]]:
        if clusterContents == None:
            clusterCenters = self.generateClusterCenters()
        else:
            clusterCenters = self.recalculateClusterCenters([], clusterContents)

        while(True):
            prevСlusterCenters = clusterCenters.copy()
            clusterContents = self.distributeElemsIntoClusters(clusterCenters)

            clusterCenters = self.recalculateClusterCenters(prevСlusterCenters, clusterContents)
            if prevСlusterCenters == clusterCenters:
                break
        
        return clusterContents, clusterCenters
    