# Hybrid Clusterization

from matplotlib import pyplot as plt
from typing import List, Union

from haClusterization import HAClusterization
from kPrototypesClusterization import KPrototypesClusterization
from distance import Distance


class HybridClusterization():
    objects: List[List[str]] # список объектов
    numberClusters: int      # количество кластеров
    clusterContents: List[List[int]] # массив, содержащий в себе k массивов c номерами элементов, принадлежащих соответствующему кластеру
    clusterCenters: List[List[Union[str, int]]] # массив, содержащий в себе k центров кластеров


    def __init__(self, objects: List[List[str]], numberClusters: int):
        self.objects = objects
        self.numberClusters = numberClusters
        self.clusterContents, self.clusterCenters = self.run()


    def run(self) -> List[List[int]]:
        distance = Distance()
        # построение матрицы несходства
        dissimilarityMatrix = distance.createDissimilarityMatrix(self.objects)
        # иерархическая часть метода
        haClusterization = HAClusterization(dissimilarityMatrix, self.numberClusters)
        # получение списка номеров объектов, входящих в каждый кластер
        clusterContents = [node.listClusterNumbers for node in haClusterization.nodes]
        # уточнение принадлежности элементов кластерам с помощью метода кластеризации центроидного типа
        kPrototypesClusterization = \
            KPrototypesClusterization(self.objects, self.numberClusters, clusterContents)

        return kPrototypesClusterization.clusterContents, \
               kPrototypesClusterization.clusterCenters
    

    def createMatrixDistances(self, clusterCenters: List[List[Union[str, float]]]) -> List[List[float]]:
        '''
        Возвращает матрицу растояний от элементов до центров кластеров
        '''
        numbObjects = len(self.objects)
        matrix = [ [0] * self.numberClusters for _ in range(numbObjects) ]
        distance = Distance()

        for i in range(numbObjects):
            for j in range(self.numberClusters):
                matrix[i][j] = distance.goverDistance(self.objects[i], clusterCenters[j])

        return matrix


    def findDistancesToClusterCenters(self):
        '''
        Нахождение расстояний между элементами кластеров и их центрами для построения графика
        '''
        distsToCenter = []
        centerNumbers = []
        matrixDists = self.createMatrixDistances(self.clusterCenters)

        for iCenter in range(self.numberClusters):
            for iElem in self.clusterContents[iCenter]:
                distsToCenter.append(matrixDists[iElem][iCenter])
                centerNumbers.append(iCenter)

        return distsToCenter, centerNumbers
    

    def buildGraph(self) -> None:
        distsToCenter, centerNumbers = self.findDistancesToClusterCenters()

        plt.figure(figsize=(10, 7))
        plt.plot(distsToCenter, centerNumbers, 'o', label = 'Hybrid Clusterization')
        plt.grid(True)
        plt.legend()
        plt.ylabel('Номер кластера')
        plt.xlabel('Расстояния до центра кластера')
        plt.xlim([0, 1])
        plt.show()
