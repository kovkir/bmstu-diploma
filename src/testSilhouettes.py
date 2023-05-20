from matplotlib import pyplot as plt
from typing import List, Union
from prettytable import PrettyTable

from distance import Distance
from haClusterization import HAClusterization
from kPrototypesClusterization import KPrototypesClusterization
from hybridClusterization import HybridClusterization
from testElbow import EventMethod
from constants import *


class TestSilhouettes():
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


    def calcAvgDistance(self, objectNumber: int, 
            listObjectNumbers: List[int], defaultValue: int=0) -> float:
        '''
        Возвращает среднее расстояние между объектом и переданными элементами
        '''
        sumDistances = 0
        countObjects = len(listObjectNumbers)

        for i in range(countObjects):
            sumDistances += self.dissimilarityMatrix[objectNumber][listObjectNumbers[i]]

        return sumDistances / countObjects if countObjects else defaultValue
    

    def calcMaxDistance(self, objectNumber: int, listObjectNumbers: List[int]) -> float:
        '''
        Возвращает максимальное расстояние между объектом и переданными элементами
        '''
        distance = 0
        countObjects = len(listObjectNumbers)

        for i in range(countObjects):
            distance = max(distance, self.dissimilarityMatrix[objectNumber][listObjectNumbers[i]])

        return distance if countObjects else 1
    

    def getNearestCluster(self, objectNumber: int, 
            clusterContents: List[List[int]]) -> List[int]:
        '''
        Возвращает список номеров объектов из ближайшего кластера
        '''
        minDistance = 1
        nearestCluster = clusterContents[0]

        for listObjectNumbers in clusterContents:
            # расстояние между двумя кластерами -- самое длинное расстояние между двумя точками в каждом кластере (полная связь)
            distance = self.calcMaxDistance(objectNumber, listObjectNumbers)
            if distance < minDistance:
                minDistance = distance
                nearestCluster = listObjectNumbers

        return nearestCluster

    
    def calcSumCoeffsOneCluster(self, 
            listObjectNumbers: List[int],
            clusterContents: List[List[int]]) -> float:
        '''
        Возвращает сумму значений коэффициента силуэта 
        для элементов текущего кластера
        '''
        sumCoeffs = 0
        
        for objectNumber in listObjectNumbers:
            # найдем список номеров объектов из ближайшего кластера
            nearestCluster = self.getNearestCluster(objectNumber, clusterContents)
            # создадим копию списка номеров элементов текущего кластера без с номера текущего объета
            otherNumbers = listObjectNumbers.copy()
            otherNumbers.remove(objectNumber)

            # среднее расстояние между текущим объектом и объектами из ближайшего кластера
            b = self.calcAvgDistance(objectNumber, nearestCluster, defaultValue=1)
            a = self.calcAvgDistance(objectNumber, otherNumbers, defaultValue=0)

            sumCoeffs += (b - a) / max(a, b)
        
        return sumCoeffs
    

    def calcAvgSilhouetteCoeff(self, clusterContents: List[List[int]]) -> float:
        '''
        Возвращает среднее значение коэффициента силуэта
        для всех объектов при заданном кол-ве кластеров
        '''
        sumCoeffs = 0
        countCoeffs = 0

        for i in range(len(clusterContents)):
            listObjectNumbers = clusterContents[i]
            # если кластер содержит элементы
            if len(listObjectNumbers) > 0:
                # создадим копию списка без массива с номерами элементов текущего кластера
                otherClusterContents = clusterContents.copy()
                otherClusterContents.pop(i)

                sumCoeffs += self.calcSumCoeffsOneCluster(listObjectNumbers, otherClusterContents)
                countCoeffs += len(listObjectNumbers)

        return sumCoeffs / countCoeffs if countCoeffs != 0 else 0


    def calcAvgSilhouetteCoeffForMethod(self, method: EventMethod, numberClusters: int) -> float:
        '''
        Возвращает среднее значение коэффициента силуэта 
        для всех объектов при заданном кол-ве кластеров
        '''
        if method == method.KP_CLUST:
            sumAvgCoeffs = 0
            for _ in range(self.numberOfRuns):
                kPrototypesClusterization = KPrototypesClusterization(self.objects, numberClusters)
                sumAvgCoeffs += self.calcAvgSilhouetteCoeff(kPrototypesClusterization.clusterContents)

            avgSilhouetteCoeff = sumAvgCoeffs / self.numberOfRuns

        elif method == method.HA_CLUST:
            haClusterization = HAClusterization(self.dissimilarityMatrix.copy(), numberClusters)
            # получение списка номеров объектов, входящих в каждый кластер
            clusterContents = [node.listClusterNumbers for node in haClusterization.nodes]
            avgSilhouetteCoeff = self.calcAvgSilhouetteCoeff(clusterContents)
        else:
            hybridClusterization = HybridClusterization(self.objects, numberClusters)
            avgSilhouetteCoeff = self.calcAvgSilhouetteCoeff(hybridClusterization.clusterContents)

        return avgSilhouetteCoeff


    def comparisonMethods(self) -> None:
        listSilhouetteCoeffHA = []
        listSilhouetteCoeffKP = []
        listSilhouetteCoeffHybrid = []
 
        for k in range(2, self.numberObjects + 1):
            listSilhouetteCoeffHA.append(self.calcAvgSilhouetteCoeffForMethod(EventMethod.HA_CLUST, k))
            listSilhouetteCoeffKP.append(self.calcAvgSilhouetteCoeffForMethod(EventMethod.KP_CLUST, k))
            listSilhouetteCoeffHybrid.append(self.calcAvgSilhouetteCoeffForMethod(EventMethod.HYBRID_CLUST, k))

            print("Проведено сравнение {:d} кластеров из {:d}".format(k, self.numberObjects))

        listСlusterNumbers = [i for i in range(2, self.numberObjects + 1)]

        self.printAvgDistanceTable(
            listСlusterNumbers, listSilhouetteCoeffHA,
            listSilhouetteCoeffKP, listSilhouetteCoeffHybrid)
        
        self.buildGraph(
            listСlusterNumbers, listSilhouetteCoeffHA,
            listSilhouetteCoeffKP, listSilhouetteCoeffHybrid)
        

    @staticmethod
    def printAvgDistanceTable(
            listСlusterNumbers: List[int], 
            listSilhouetteCoeffHA: List[float],
            listSilhouetteCoeffKP: List[float], 
            listSilhouetteCoeffHybrid: List[float]) -> None:
        '''
        Построение таблицы со средними значениями коэффициента силуэта
        '''
        tableHeader = ["Кол-во кластеров", "Hierarchical", "K-Prototypes", "Hybrid"]
        table = PrettyTable(tableHeader)

        for i in range(len(listСlusterNumbers)):
            table.add_row([
                listСlusterNumbers[i], 
                round(listSilhouetteCoeffHA[i], 3),
                round(listSilhouetteCoeffKP[i], 3), 
                round(listSilhouetteCoeffHybrid[i], 3)
            ])
        print(table)

        
    @staticmethod
    def buildGraph( 
            listСlusterNumbers: List[int], 
            listAvgDistanceHA: List[float],
            listAvgDistanceKP: List[float], 
            listAvgDistanceHybrid: List[float]) -> None:
        '''
        Построения графика зависимости среднего значения коэффициента силуэта от кол-ва кластеров
        '''
        plt.figure(figsize=(13, 7))
        plt.plot(listСlusterNumbers, listAvgDistanceHA, label = 'Hierarchical Agglomerative Clusterization')
        plt.plot(listСlusterNumbers, listAvgDistanceKP, label = 'K-Prototypes Clusterization')
        plt.plot(listСlusterNumbers, listAvgDistanceHybrid, label = 'Hybrid Clusterization')
        plt.grid(True)
        plt.legend()
        plt.ylabel('Среднее значение коэффициента силуэта')
        plt.xlabel('Кол-во кластеров')
        plt.show()
