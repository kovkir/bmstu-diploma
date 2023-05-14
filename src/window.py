from typing import List, Union
from tkinter import Tk, Label, Entry, Radiobutton, IntVar, \
                    Button, messagebox, DISABLED, END

from haClusterization import HAClusterization
from kPrototypesClusterization import KPrototypesClusterization
from hybridClusterization import HybridClusterization
from distance import Distance
from test import Test
from constants import *
from color import *


class Window():
    window: Tk
    numberClusters: Entry
    maxNumberClusters: Entry
    numberRuns: Entry
    methodVar: IntVar
    comparisonVar: IntVar
    players: List[List[str]]

    
    def __init__(self, windowWidth: int, windowHeight: int, players: List[List[str]]):
        self.window = self.createWindow(windowWidth, windowHeight)
        self.createInterface(windowWidth, windowHeight)
        self.players = players


    def createWindow(self, windowWidth: int, windowHeight: int):
        window = Tk()
        window.title("Выпускная квалификационная работа (Ковалец Кирилл ИУ7-83Б)")
        window.geometry("{0}x{1}".format(windowWidth, windowHeight))
        window.resizable(False, False)
        window["bg"] = PURPLE_LIGHT

        return window


    def createInterface(self, windowWidth: int, windowHeight: int):
        Label(text = "ПАРАМЕТРЫ", 
              font = ("Arial", 16, "bold"), bg = PURPLE_DARK, fg = "white")\
            .place(width = windowWidth, height = 30, x = 0 , y = 10)

        Label(text = "Количество итоговых кластеров", 
              font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK)\
            .place(width = windowWidth * 0.5, height = 30, x = windowWidth * 0.1, y = 50)

        self.numberClusters = Entry(font = ("Arial", 17))
        self.numberClusters.place(width = windowWidth * 0.3, height = 30, x = windowWidth * 0.6, y = 50)

        Label(text = "Максимальное количество кластеров", 
              font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK)\
            .place(width = windowWidth * 0.5, height = 30, x = windowWidth * 0.1, y = 90)

        self.maxNumberClusters = Entry(font = ("Arial", 17))
        self.maxNumberClusters.place(width = windowWidth * 0.3, height = 30, x = windowWidth * 0.6, y = 90)

        Label(text = "Количество прогонов для K-прототипов\nпри сравнении методов", 
              font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK)\
            .place(width = windowWidth * 0.5, height = 30, x = windowWidth * 0.1, y = 130)

        self.numberRuns = Entry(font = ("Arial", 17))
        self.numberRuns.place(width = windowWidth * 0.3, height = 30, x = windowWidth * 0.6, y = 130)


        Label(text = "ВЫБОР МЕТОДА РАЗБИЕНИЯ ДАННЫХ",
              font = ("Arial", 16, "bold"), bg = PURPLE_DARK, fg = "white")\
            .place(width = windowWidth, height = 30, x = 0 , y = 170)

        self.methodVar = IntVar()
        self.methodVar.set(HYBRID)

        Radiobutton(
            text = "Агломеративный подход иерархической кластеризации", 
            variable = self.methodVar, value = HA,
            font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK,
            anchor = "w")\
            .place(width = windowWidth * 0.7, height = 30, x = windowWidth  * 0.15, y = 210)
        
        Radiobutton(
            text = "Метод кластеризации центроидного типа K-прототипов", 
            variable = self.methodVar, value = K_PROTOTYPES,
            font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK,
            anchor = "w")\
            .place(width = windowWidth * 0.7, height = 30, x = windowWidth  * 0.15, y = 250)
        
        Radiobutton(
            text = "Реализованный гибридный метод кластеризации", 
            variable = self.methodVar, value = HYBRID,
            font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK,
            anchor = "w")\
            .place(width = windowWidth * 0.7, height = 30, x = windowWidth  * 0.15, y = 290)

        # вместо границы кнопки
        Button(highlightbackground = PURPLE_DARK, highlightthickness = 30, 
               fg = PURPLE_LIGHT, state = DISABLED)\
            .place(width = windowWidth * 0.8, height = 40, x = windowWidth * 0.1, y = 330)

        Button(
            text = "Кластеризировать данные", 
            font = ("Arial", 16), fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE, highlightthickness = 30,
            command = lambda: self.doClustering())\
            .place(width = windowWidth * 0.8 - 4, height = 36, x = windowWidth * 0.1 + 2, y = 332)


        Label(text = "МЕТОДЫ ОЦЕНКИ КАЧЕСТВА КЛАСТЕРИЗАЦИИ",
              font = ("Arial", 16, "bold"), bg = PURPLE_DARK, fg = "white")\
            .place(width = windowWidth, height = 30, x = 0 , y = 380)
        
        self.comparisonVar = IntVar()
        self.comparisonVar.set(ELBOW)

        Radiobutton(
            text = "Метод оценки силуэтов", 
            variable = self.comparisonVar, value = EVALUATION_SILHOUETTES,
            font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK,
            anchor = "w")\
            .place(width = windowWidth * 0.35, height = 30, x = windowWidth  * 0.15, y = 420)
        
        Radiobutton(
            text = "Метод локтя", 
            variable = self.comparisonVar, value = ELBOW,
            font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK,
            anchor = "w")\
            .place(width = windowWidth * 0.35, height = 30, x = windowWidth  * 0.6, y = 420)

        Button(highlightbackground = PURPLE_DARK, highlightthickness = 30, 
               fg = PURPLE_LIGHT, state = DISABLED)\
            .place(width = windowWidth * 0.8, height = 40, x = windowWidth * 0.1, y = 460)

        Button(
            text = "Сравнить методы разбиения", 
            font = ("Arial", 16), fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE, highlightthickness = 30,
            command = lambda: self.doComparison())\
            .place(width = windowWidth * 0.8 - 4, height = 36, x = windowWidth * 0.1 + 2, y = 462)
        

        Label(text = "О ПРОГРАММЕ", font = ("Arial", 16, "bold"), bg = PURPLE_DARK,
            fg = "white").place(width = windowWidth, height = 30, x = 0 , y = windowHeight - 90)

        Button(highlightbackground = PURPLE_DARK, highlightthickness = 30, 
               fg = PURPLE_LIGHT, state = DISABLED)\
            .place(width = windowWidth * 0.8, height = 40, x = windowWidth * 0.1, y = windowHeight - 50)

        Button(
            text = "Информация о программе", 
            font = ("Arial", 16), fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE, highlightthickness = 30, 
            command = lambda: self.aboutProgram())\
            .place(width = windowWidth * 0.8 - 4, height = 36, x = windowWidth * 0.1 + 2, y = windowHeight - 48)
    

    def getMaxNumberClusters(self) -> Union[int, None]:
        try:
            maxNumberClusters = int(self.maxNumberClusters.get())
        except:
            maxNumberClusters = None
        
        if maxNumberClusters == None or maxNumberClusters < 1:
            messagebox.showwarning("Ошибка",
                "Невозможное значение максимального количества кластеров!\n"
                "Ожидался ввод натурального числа.")
            return
        
        return maxNumberClusters
    

    def getNumberClusters(self, maxNumberClusters: int) -> Union[int, None]:
        try:
            numberClusters = int(self.numberClusters.get())
        except:
            numberClusters = None
        
        if numberClusters == None or \
           numberClusters < 1 or numberClusters > maxNumberClusters:
            messagebox.showwarning("Ошибка",
                "Невозможное значение количества кластеров!\n"
                "Ожидался ввод натурального числа.\n"
                "Также количество кластеров должно быть не больше "
                "максимального количества.")
            return
        
        return numberClusters
    
    
    def getNumberRuns(self) -> Union[int, None]:
        try:
            numberRuns = int(self.numberRuns.get())
        except:
            numberRuns = None
        
        if numberRuns == None or numberRuns < 1:
            messagebox.showwarning("Ошибка",
                "Невозможное значение количества прогонов!\n"
                "Ожидался ввод натурального числа.")
            return
        
        return numberRuns
    

    def doClustering(self):
        maxNumberClusters = self.getMaxNumberClusters()
        if maxNumberClusters == None:
            return

        numberClusters = self.getNumberClusters(maxNumberClusters)
        if numberClusters == None:
            return
        
        players = self.players[:maxNumberClusters]

        if self.methodVar.get() == HA:
            distance = Distance()
            dissimilarityMatrix = distance.createDissimilarityMatrix(players)

            haClusterization = HAClusterization(dissimilarityMatrix)
            haClusterization.buildDendrogram()

        elif self.methodVar.get() == K_PROTOTYPES:
            kPrototypesClusterization = KPrototypesClusterization(players, numberClusters)
            kPrototypesClusterization.buildGraph()

        elif self.methodVar.get() == HYBRID:
            hybridClusterization = HybridClusterization(players, numberClusters)
            hybridClusterization.buildGraph()


    def doComparison(self):
        maxNumberClusters = self.getMaxNumberClusters()
        if maxNumberClusters == None:
            return

        numberRuns = self.getNumberRuns()
        if numberRuns == None:
            return
        
        players = self.players[:maxNumberClusters]

        if self.comparisonVar.get() == ELBOW:
            test = Test(players, numberRuns)
            test.comparisonMethods()

        elif self.comparisonVar.get() == EVALUATION_SILHOUETTES:
           return


    def aboutProgram(self):
        messagebox.showinfo("О программе",
            ""
            "\n\nКовалец Кирилл ИУ7-83Б (2023)")

     
    def run(self):
        self.numberClusters.insert(0, CLUSTER_NUMBERS)
        self.maxNumberClusters.insert(0, MAX_CLUSTER_NUMBERS)
        self.numberRuns.insert(0, NUMBER_OF_RUNS)

        self.window.mainloop()
