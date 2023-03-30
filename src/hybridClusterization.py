# Hybrid Clusterization

from typing import List

from haClusterization import HAClusterization
from kPrototypesClusterization import KPrototypesClusterization


class HybridClusterization():
    players: List[List[str]]               # список игроков
    dissimilarityMatrix: List[List[float]] # матрица несходства
    
    numberClusters: int              # количество кластеров
    clusterContents: List[List[int]] # массив, содержащий в себе k массивов c номерами элементов, принадлежащих соответствующему кластеру


    def __init__(self, players: List[List[str]], dissimilarityMatrix: List[List[float]], numberClusters: int):
        self.dissimilarityMatrix = dissimilarityMatrix
        self.players = players
        self.numberClusters = numberClusters
        self.clusterContents = self.run()


    def run(self) -> List[List[int]]:
        haClusterization = HAClusterization(self.dissimilarityMatrix.copy(), self.numberClusters)

        clusterContents = [node.listClusterNumbers for node in haClusterization.nodes]
        kPrototypesClusterization = KPrototypesClusterization(self.players, self.numberClusters, clusterContents)

        return kPrototypesClusterization.clusterContents
