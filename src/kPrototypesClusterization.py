# K-Prototypes Clusterization

from matplotlib import pyplot as plt
from typing import List, Union
from random import randint

from distance import Distance
from constants import *


class KPrototypesClusterization():
    players: List[List[str]] # список игроков
    k: int                   # количество кластеров
    clusterContents: List[List[int]] # массив, содержащий в себе k массивов c номерами элементов, принадлежащих соответствующему кластеру
    clusterCenters: List[List[Union[str, int]]] # массив, содержащий в себе k центров кластеров


    def __init__(self, players: List[List[str]], k: int, clusterContents: Union[List[List[int]], None]=None):
        self.players = players
        self.k = k
        self.clusterContents, self.clusterCenters = self.run(clusterContents)


    def generateClusterCenters(self) -> List[List[Union[str, int]]]:
        '''
        Возвращает массив с k центрами кластерами
        '''
        clusterCenters = []

        for _ in range(self.k):
            rating  = randint(MIN_RATING, MAX_RATING)
            country = self.players[randint(0, len(self.players) - 1)][COUNTRY_COLUMN_NUMBER]
            club    = self.players[randint(0, len(self.players) - 1)][CLUB_COLUMN_NUMBER]

            clusterCenters.append(["", rating, country, club])

        return clusterCenters
    
    
    def getAverageRating(self, clusterNumbers: List[int]) -> float:
        '''
        Возвращает средний рейтинг игроков, принадлежащих одному кластеру
        '''
        sumRating = 0
        for i in clusterNumbers:
            sumRating += int(self.players[i][RATING_COLUMN_NUMBER])
        
        return sumRating / len(clusterNumbers)
    

    def getMostPopularField(self, clusterNumbers: List[int], columnNumber) -> str:
        '''
        Возвращает самое встречаемое поле в столбце среди элементов кластера
        '''
        repetitions = {}
        for i in clusterNumbers:
            key = self.players[i][columnNumber]

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
    
        for i in range(self.k):
            if len(clusterContents[i]) > 0:
                rating  = self.getAverageRating(clusterContents[i])
                country = self.getMostPopularField(clusterContents[i], COUNTRY_COLUMN_NUMBER)
                club    = self.getMostPopularField(clusterContents[i], CLUB_COLUMN_NUMBER)
                
                clusterCenters.append(["", rating, country, club])
            else:
                # если кластер пуст
                clusterCenters.append(oldClusterCenters[i].copy())

        return clusterCenters
    
    
    def createMatrixDistances(self, clusterCenters: List[List[Union[str, float]]]) -> List[List[float]]:
        '''
        Возвращает матрицу растояний от элементов до центров кластеров
        '''
        numbObjects = len(self.players)
        matrix = [ [0] * self.k for _ in range(numbObjects) ]
        distance = Distance()

        for i in range(numbObjects):
            for j in range(self.k):
                matrix[i][j] = distance.goverDistance(self.players[i], clusterCenters[j])

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
    

    def findDistancesToClusterCenters(self):
        '''
        Нахождение расстояний между элементами кластеров и их центрами для построения графика
        '''
        distsToCenter = []
        centerNumbers = []
        matrixDists = self.createMatrixDistances(self.clusterCenters)

        for iCenter in range(self.k):
            for iElem in self.clusterContents[iCenter]:
                distsToCenter.append(matrixDists[iElem][iCenter])
                centerNumbers.append(iCenter)

        return distsToCenter, centerNumbers
    

    def buildGraph(self) -> None:
        distsToCenter, centerNumbers = self.findDistancesToClusterCenters()

        plt.figure(figsize=(10, 7))
        plt.plot(distsToCenter, centerNumbers, 'or', label = 'K-Prototypes Clusterization')
        plt.grid(True)
        plt.legend()
        plt.ylabel('Номер кластера')
        plt.xlabel('Расстояния до центра кластера')
        plt.show()
