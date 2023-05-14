from matplotlib import pyplot as plt
from typing import List, Union
from enum import Enum

from distance import Distance
from haClusterization import HAClusterization
from kPrototypesClusterization import KPrototypesClusterization
from hybridClusterization import HybridClusterization
from constants import *


class EventMethod(Enum):
    HA_CLUST     = 0
    KP_CLUST     = 1
    HYBRID_CLUST = 2


class Test():
    def __init__(self, players: List[List[str]], numberOfRuns: int):
        self.players = players
        self.numberOfRuns = numberOfRuns
        self.maxClusterNymbers = len(players)
        self.dissimilarityMatrix = self.createDissimilarityMatrix()
    

    def createDissimilarityMatrix(self):
        '''
        Возвращает матрицу несходства
        '''
        distance = Distance()
        dissimilarityMatrix = distance.createDissimilarityMatrix(self.players)

        return dissimilarityMatrix
    

    def calcAvgDistance(self, listClusterNumbers: List[int]) -> float:
        '''
        Возвращает среднее расстояние между элементами класстера
        '''
        sumDistances = 0
        countDistances = 0

        for i in range(len(listClusterNumbers) - 1):
            for j in range(i + 1, len(listClusterNumbers)):
                sumDistances += self.dissimilarityMatrix[listClusterNumbers[i]][listClusterNumbers[j]]
                countDistances += 1

        return sumDistances / countDistances if countDistances != 0 else 0
    
    
    def calcAvgWithinСlusterDistance(self, clusterContents: List[List[int]]) -> float:
        '''
        Возвращает среднее расстояние в пределах кластера
        '''
        sumAvgDistances = 0
        countAvgDistances = 0

        for listClusterNumbers in clusterContents:
            # если кластер содержит элементы
            if len(listClusterNumbers) > 0:
                sumAvgDistances += self.calcAvgDistance(listClusterNumbers)
                countAvgDistances += 1

        return sumAvgDistances / countAvgDistances if countAvgDistances != 0 else 0


    def calcAvgWithinСlusterDistanceForMethod(self, method: EventMethod, numberClusters: int) -> float:
        '''
        Возвращает среднее расстояние в пределах кластера
        '''
        if method == method.KP_CLUST:
            sumAvgDistances = 0
            for _ in range(self.numberOfRuns):
                kPrototypesClusterization = KPrototypesClusterization(self.players, numberClusters)
                sumAvgDistances += self.calcAvgWithinСlusterDistance(kPrototypesClusterization.clusterContents)

            avgWithinСlusterDistance = sumAvgDistances / self.numberOfRuns
        else:
            hybridClusterization = HybridClusterization(self.players, numberClusters)
            avgWithinСlusterDistance = self.calcAvgWithinСlusterDistance(hybridClusterization.clusterContents)

        return avgWithinСlusterDistance


    def comparisonMethods(self):
        listAvgDistanceKP = []
        listAvgDistanceHybrid = []

        for k in range(1, self.maxClusterNymbers + 1):
            listAvgDistanceKP.append(self.calcAvgWithinСlusterDistanceForMethod(EventMethod.KP_CLUST, k))
            listAvgDistanceHybrid.append(self.calcAvgWithinСlusterDistanceForMethod(EventMethod.HYBRID_CLUST, k))

            print("Проведено сравнение {:d} кластеров из {:d}".format(k, self.maxClusterNymbers))
            
        haClusterization = HAClusterization(self.dissimilarityMatrix.copy())

        listHAClust     = haClusterization.listAvgDistance
        listKPClust     = [[i for i in range(1, self.maxClusterNymbers + 1)], listAvgDistanceKP]
        listHybridClust = [[i for i in range(1, self.maxClusterNymbers + 1)], listAvgDistanceHybrid]

        self.buildGraph(listHAClust, listKPClust, listHybridClust)


    @staticmethod
    def buildGraph( 
            listHAClust: List[Union[List[int], List[float]]], 
            listKPClust: List[Union[List[int], List[float]]], 
            listHybridClust: List[Union[List[int], List[float]]]) -> None:
        '''
        Построения графика зависимости среднего расстояния в пределах кластера от кол-ва кластеров
        '''
        plt.figure(figsize=(15, 8))
        plt.plot(listHAClust[0], listHAClust[1], label = 'Hierarchical Agglomerative Clusterization')
        plt.plot(listKPClust[0], listKPClust[1], label = 'K-Prototypes Clusterization')
        plt.plot(listHybridClust[0], listHybridClust[1], label = 'Hybrid Clusterization')
        plt.grid(True)
        plt.legend()
        plt.ylabel('Среднее расстояние в пределах кластера')
        plt.xlabel('Кол-во кластеров')
        plt.show()
