# Hierarchical Agglomerative Clusterization

from scipy.cluster.hierarchy import dendrogram
from matplotlib import pyplot as plt
from typing import List, Union


class Node():
    def __init__(self, clusterNumber: int, listClusterNumbers: List[int], avgDistance: float, left=None, right=None):
        self.clusterNumber = clusterNumber           # номер кластера
        self.listClusterNumbers = listClusterNumbers # список номеров кластеров, входящих в текщий кластер
        self.avgDistance = avgDistance               # среднее расстояние между элементами класстера

        self.left  = left
        self.right = right


class HAClusterization():
    dissimilarityMatrix: List[List[float]] # матрица несходства
    nodes: List[Node]                      # список узлов дерева
    tree: Union[Node, None]                # корень дерева

    matrixInfo: List[List[float]]                         # для построения dendrogram
    listAvgDistance: List[Union[List[int], List[float]]]  # список для графика


    def __init__(self, dissimilarityMatrix: List[List[float]], numberClusters: int=1):
        self.dissimilarityMatrix = dissimilarityMatrix
        self.nodes = []
        self.addNodes()
        self.matrixInfo = []
        self.listAvgDistance = [[], []]
        self.tree = self.buildTree(numberClusters)


    def addNodes(self) -> None:
        for i in range(len(self.dissimilarityMatrix)):
            self.nodes.append(Node(i, [i], 0))


    def nodeClusterNumber(self, nodeIndex: int) -> int:
        return self.nodes[nodeIndex].clusterNumber


    def getClusterNumbersWithMinDistance(self) -> List[int]:
        # индексы узлов, содержащих номера кластеров с минимальным растояние между ними
        iMinDistance = 0
        jMinDistance = 1
        
        for i in range(len(self.nodes) - 1):
            for j in range(i + 1, len(self.nodes)):
                if self.dissimilarityMatrix[self.nodeClusterNumber(i)][self.nodeClusterNumber(j)] < \
                   self.dissimilarityMatrix[self.nodeClusterNumber(iMinDistance)][self.nodeClusterNumber(jMinDistance)]:
                    iMinDistance = i
                    jMinDistance = j

        return iMinDistance, jMinDistance
    

    def calcAvgDistance(self, listClusterNumbers: List[int]) -> float:
        # вычисление среднего расстояния между элементами класстера
        sumDistances = 0
        countDistances = 0

        for i in range(len(listClusterNumbers) - 1):
            for j in range(i + 1, len(listClusterNumbers)):
                sumDistances += self.dissimilarityMatrix[listClusterNumbers[i]][listClusterNumbers[j]]
                countDistances += 1

        return sumDistances / countDistances if countDistances != 0 else 0
    
    
    def calcAvgWithinСlusterDistance(self) -> float:
        # вычисление среднего расстояния в пределах класстера
        sumAvgDistances = 0
        countAvgDistances = 0

        for node in self.nodes:
            sumAvgDistances += node.avgDistance
            countAvgDistances += 1

        return sumAvgDistances / countAvgDistances if countAvgDistances != 0 else 0


    def updateDissimilarityMatrix(self, clusterNumber1: int, clusterNumber2: int) -> None:
        # добавление столбца с расстояниями до нового кластера в матрицу несходства
        for i in range(len(self.dissimilarityMatrix)):
            # расстояние между двумя кластерами -- самое длинное расстояние между двумя точками в каждом кластере (полная связь)
            maxDistance = max(self.dissimilarityMatrix[i][clusterNumber1],
                              self.dissimilarityMatrix[i][clusterNumber2])

            self.dissimilarityMatrix[i].append(maxDistance)

        # добавление строки, симметричной добавленому столбцу
        self.dissimilarityMatrix.append([self.dissimilarityMatrix[i][-1] for i in range(len(self.dissimilarityMatrix))])
        self.dissimilarityMatrix[-1].append(0)


    def buildTree(self, numberClusters: int) -> Node:
        self.listAvgDistance[0].append(len(self.nodes))
        self.listAvgDistance[1].append(0)
        
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

            self.listAvgDistance[0].append(len(self.nodes))
            self.listAvgDistance[1].append(self.calcAvgWithinСlusterDistance())

            self.matrixInfo.append(
                [
                    firstNode.clusterNumber, 
                    secondNode.clusterNumber, 
                    self.dissimilarityMatrix[firstNode.clusterNumber][secondNode.clusterNumber], 
                    len(listClusterNumbers)
                ]
            )
            
            self.updateDissimilarityMatrix(firstNode.clusterNumber, secondNode.clusterNumber)

        return self.nodes[0] if numberClusters == 1 else None 
    

    def printMatrixInfo(self) -> None:
        print("\n     --- MatrixInfo ---\n")

        for i in range(len(self.matrixInfo)):
            print("{:5.0f} {:5.0f} {:>7.3f} {:5.0f}".format(
                self.matrixInfo[i][0], self.matrixInfo[i][1], self.matrixInfo[i][2], self.matrixInfo[i][3]))


    def printListAvgDistance(self) -> None:
        print("\n --- ListAvgDistance ---\n")

        for i in range(len(self.listAvgDistance[0])):
            print("{:5d} {:>7.3f}".format(
                self.listAvgDistance[0][i], self.listAvgDistance[1][i]))


    def buildDendrogram(self) -> None:
        self.printMatrixInfo()

        plt.figure(figsize=(15, 8))
        plt.title("Hybrid Clusterization")
        dendrogram(self.matrixInfo)
        plt.show()
