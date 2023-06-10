# Hierarchical Agglomerative Clusterization

from scipy.cluster.hierarchy import dendrogram
from matplotlib import pyplot as plt
from typing import List, Union


class Node():
    def __init__(self, clusterNumber: int, listClusterNumbers: List[int], avgDistance: float, left=None, right=None):
        self.clusterNumber = clusterNumber           # номер кластера
        self.listClusterNumbers = listClusterNumbers # список номеров кластеров, входящих в текщий кластер
        self.avgDistance = avgDistance               # среднее расстояние между элементами кластера

        self.left  = left
        self.right = right


class HAClusterization():
    dissimilarityMatrix: List[List[float]] # матрица несходства
    nodes: List[Node]                      # список узлов дерева
    tree: Union[Node, None]                # корень дерева

    def __init__(self, dissimilarityMatrix: List[List[float]], numberClusters: int=1):
        self.dissimilarityMatrix = dissimilarityMatrix
        self.nodes = []
        self.addNodes()
        self.tree = self.buildTree(numberClusters)

    def addNodes(self) -> None:
        '''
        Размещение каждого объекта в отдельный кластер 
        '''
        for i in range(len(self.dissimilarityMatrix)):
            self.nodes.append(Node(i, [i], 0))

    def nodeClusterNumber(self, nodeIndex: int) -> int:
        '''
        Возвращает номер кластера узла
        '''
        return self.nodes[nodeIndex].clusterNumber

    def getClusterNumbersWithMinDistance(self) -> List[int]:
        '''
        Возвращает индексы узлов, содержащих номера кластеров 
        с минимальным растояние между ними
        '''
        iMinDistance = 0
        jMinDistance = 1
        
        for i in range(len(self.nodes) - 1):
            for j in range(i + 1, len(self.nodes)):
                if self.dissimilarityMatrix\
                    [self.nodeClusterNumber(i)]\
                    [self.nodeClusterNumber(j)] <\
                   self.dissimilarityMatrix\
                    [self.nodeClusterNumber(iMinDistance)]\
                    [self.nodeClusterNumber(jMinDistance)]:
                    
                    iMinDistance = i
                    jMinDistance = j

        return iMinDistance, jMinDistance
    
    def calcAvgDistance(self, listClusterNumbers: List[int]) -> float:
        '''
        Возвращает среднее расстояние между элементами кластера
        '''
        sumDistances = 0
        countDistances = 0
        size = len(listClusterNumbers)

        for i in range(size - 1):
            for j in range(i + 1, size):
                sumDistances += self.dissimilarityMatrix\
                    [listClusterNumbers[i]][listClusterNumbers[j]]
                countDistances += 1

        return sumDistances / countDistances if countDistances != 0 else 0
    
    def calcAvgWithinСlusterDistance(self) -> float:
        '''
        Возвращает среднее расстояние в пределах кластера
        '''
        sumAvgDistances = 0
        countAvgDistances = 0

        for node in self.nodes:
            sumAvgDistances += node.avgDistance
            countAvgDistances += 1

        return sumAvgDistances / countAvgDistances if countAvgDistances != 0 else 0

    def updateDissimilarityMatrix(self, clusterNumber1: int, clusterNumber2: int) -> None:
        '''
        Дополнение матрицы несходства
        '''
        # добавление столбца с расстояниями до нового кластера в матрицу несходства
        for i in range(len(self.dissimilarityMatrix)):
            # расстояние между двумя кластерами -- самое длинное расстояние между двумя точками в каждом кластере (полная связь)
            maxDistance = max(self.dissimilarityMatrix[i][clusterNumber1],
                              self.dissimilarityMatrix[i][clusterNumber2])

            self.dissimilarityMatrix[i].append(maxDistance)

        # добавление строки, симметричной добавленому столбцу
        self.dissimilarityMatrix.append([self.dissimilarityMatrix[i][-1] for i in range(len(self.dissimilarityMatrix))])
        self.dissimilarityMatrix[-1].append(0)

    def buildTree(self, numberClusters: int) -> Union[Node, None]:
        '''
        Построение бинарного дерева кластеров
        (если оно полное, то возвращается корень дерева)
        '''
        while len(self.nodes) > numberClusters:
            iMinDistance, jMinDistance = self.getClusterNumbersWithMinDistance()

            firstNode = self.nodes.pop(iMinDistance)
            secondNode = self.nodes.pop(jMinDistance - 1)

            listClusterNumbers = firstNode.listClusterNumbers
            listClusterNumbers.extend(secondNode.listClusterNumbers)

            self.nodes.append(
                Node(
                    len(self.dissimilarityMatrix),
                    listClusterNumbers,
                    self.calcAvgDistance(listClusterNumbers),
                    firstNode, 
                    secondNode
                )
            )

            self.updateDissimilarityMatrix(firstNode.clusterNumber, secondNode.clusterNumber)

        return self.nodes[0] if numberClusters == 1 else None 
    