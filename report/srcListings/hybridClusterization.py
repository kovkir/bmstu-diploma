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
    