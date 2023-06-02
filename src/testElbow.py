from matplotlib import pyplot as plt
from typing import List
from enum import Enum
from prettytable import PrettyTable
import numpy as np

from distance import Distance
from haClusterization import HAClusterization
from kPrototypesClusterization import KPrototypesClusterization
from hybridClusterization import HybridClusterization
from constants import *


class EventMethod(Enum):
    HA_CLUST     = 0
    KP_CLUST     = 1
    HYBRID_CLUST = 2


class TestElbow():
    def __init__(self, objects: List[List[str]], numberOfRuns: int):
        self.objects = objects
        self.numberOfRuns = numberOfRuns
        self.numberObjects = len(objects)
        self.dissimilarityMatrix = self.createDissimilarityMatrix()
    

    def createDissimilarityMatrix(self) -> List[List[float]]:
        '''
        Возвращает матрицу несходства
        '''
        distance = Distance()
        dissimilarityMatrix = distance.createDissimilarityMatrix(self.objects)

        return dissimilarityMatrix
    

    def calcAvgDistance(self, listObjectNumbers: List[int]) -> float:
        '''
        Возвращает среднее расстояние между элементами кластера
        '''
        sumDistances = 0
        countDistances = 0
        size = len(listObjectNumbers)

        for i in range(size - 1):
            for j in range(i + 1, size):
                sumDistances += self.dissimilarityMatrix[listObjectNumbers[i]][listObjectNumbers[j]]
                countDistances += 1

        return sumDistances / countDistances if countDistances else 0
    
    
    def calcAvgWithinСlusterDistance(self, clusterContents: List[List[int]]) -> float:
        '''
        Возвращает среднее расстояние в пределах кластера
        '''
        sumAvgDistances = 0
        countAvgDistances = 0

        for listObjectNumbers in clusterContents:
            # если кластер содержит элементы
            if len(listObjectNumbers) > 0:
                sumAvgDistances += self.calcAvgDistance(listObjectNumbers)
                countAvgDistances += 1

        return sumAvgDistances / countAvgDistances if countAvgDistances else 0


    def calcAvgWithinСlusterDistanceForMethod(self, method: EventMethod, numberClusters: int) -> float:
        '''
        Возвращает среднее расстояние в пределах кластера
        '''
        if method == method.KP_CLUST:
            sumAvgDistances = 0
            for _ in range(self.numberOfRuns):
                kPrototypesClusterization = KPrototypesClusterization(self.objects, numberClusters)
                sumAvgDistances += self.calcAvgWithinСlusterDistance(kPrototypesClusterization.clusterContents)

            avgWithinСlusterDistance = sumAvgDistances / self.numberOfRuns

        elif method == method.HA_CLUST:
            haClusterization = HAClusterization(self.dissimilarityMatrix.copy(), numberClusters)
            # получение списка номеров объектов, входящих в каждый кластер
            clusterContents = [node.listClusterNumbers for node in haClusterization.nodes]
            avgWithinСlusterDistance = self.calcAvgWithinСlusterDistance(clusterContents)
        else:
            hybridClusterization = HybridClusterization(self.objects, numberClusters)
            avgWithinСlusterDistance = self.calcAvgWithinСlusterDistance(hybridClusterization.clusterContents)

        return avgWithinСlusterDistance


    def comparisonMethods(self) -> None:
        '''
        Сравнение методов разбиения
        '''
        listAvgDistanceHA = []
        listAvgDistanceKP = []
        listAvgDistanceHybrid = []

        print()
        for k in range(1, self.numberObjects + 1):
            listAvgDistanceHA.append(self.calcAvgWithinСlusterDistanceForMethod(EventMethod.HA_CLUST, k))
            listAvgDistanceKP.append(self.calcAvgWithinСlusterDistanceForMethod(EventMethod.KP_CLUST, k))
            listAvgDistanceHybrid.append(self.calcAvgWithinСlusterDistanceForMethod(EventMethod.HYBRID_CLUST, k))

            print("Проведено сравнение {:d} кластеров из {:d}".format(k, self.numberObjects))

        listСlusterNumbers = [i for i in range(1, self.numberObjects + 1)]

        self.printAvgDistanceTable(
            listСlusterNumbers, listAvgDistanceHA,
            listAvgDistanceKP, listAvgDistanceHybrid)
        
        self.buildGraph(
            listСlusterNumbers, listAvgDistanceHA,
            listAvgDistanceKP, listAvgDistanceHybrid)


    @staticmethod
    def printAvgDistanceTable(
            listСlusterNumbers: List[int], 
            listAvgDistanceHA: List[float],
            listAvgDistanceKP: List[float], 
            listAvgDistanceHybrid: List[float]) -> None:
        '''
        Построение таблицы со средними расстояниями в пределах кластера
        '''
        tableHeader = ["Кол-во кластеров", "Иерархический", "K-прототипов", "Гибридный"]
        table = PrettyTable(tableHeader)

        for i in range(len(listСlusterNumbers)):
            table.add_row([
                listСlusterNumbers[i], 
                round(listAvgDistanceHA[i], 3),
                round(listAvgDistanceKP[i], 3), 
                round(listAvgDistanceHybrid[i], 3)
            ])
        print("\n  --- Таблица со средними расстояниями в пределах кластера ---")
        print(table)


    @staticmethod
    def buildGraph( 
            listСlusterNumbers: List[int], 
            listAvgDistanceHA: List[float],
            listAvgDistanceKP: List[float], 
            listAvgDistanceHybrid: List[float]) -> None:
        '''
        Построение графика зависимости среднего расстояния в пределах кластера от кол-ва кластеров
        '''
        plt.figure(figsize=(13, 7))
        plt.title("Метод локтя")
        plt.plot(listСlusterNumbers, listAvgDistanceHA, '-.', label = 'Иерархический метод кластеризации')
        plt.plot(listСlusterNumbers, listAvgDistanceKP, '--', label = 'Метод кластеризации K-прототипов')
        plt.plot(listСlusterNumbers, listAvgDistanceHybrid, '-', label = 'Гибридный метод кластеризации')
        plt.grid(True)
        plt.legend()
        plt.ylabel('Среднее расстояние в пределах кластера')
        plt.xlabel('Кол-во кластеров, шт.')
        plt.show()
