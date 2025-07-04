from typing import List, Union
from tkinter import Tk, Label, Entry, Radiobutton, IntVar, \
                    Button, messagebox, DISABLED

from haClusterization import HAClusterization
from kPrototypesClusterization import KPrototypesClusterization
from hybridClusterization import HybridClusterization
from distance import Distance
from testElbow import TestElbow
from testSilhouettes import TestSilhouettes
from constants import *
from color import *


class Window():
    window: Tk
    numberClusters: Entry
    numberObjects: Entry
    numberRuns: Entry
    methodVar: IntVar
    comparisonVar: IntVar
    objects: List[List[str]]

    
    def __init__(self, windowWidth: int, windowHeight: int, objects: List[List[str]]):
        self.window = self.createWindow(windowWidth, windowHeight)
        self.createInterface(windowWidth, windowHeight)
        self.objects = objects


    def createWindow(self, windowWidth: int, windowHeight: int):
        window = Tk()
        window.title("Выпускная квалификационная работа (Ковалец Кирилл ИУ7-83Б)")
        window.geometry("{0}x{1}".format(windowWidth, windowHeight))
        window.resizable(False, False)
        window["bg"] = PURPLE_LIGHT

        return window


    def createInterface(self, windowWidth: int, windowHeight: int):
        Label(
            text = "ПАРАМЕТРЫ", 
            font = ("Arial", 16, "bold"), bg = PURPLE_DARK, fg = "white"
        ).place(
            width = windowWidth, height = 30, 
            x = 0 , y = 10)

        Label(
            text = "Количество итоговых кластеров", 
            font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK
        ).place(
            width = windowWidth * 0.5, height = 30, 
            x = windowWidth * 0.1, y = 50)

        self.numberClusters = Entry(font = ("Arial", 17))
        self.numberClusters.place(
            width = windowWidth * 0.3, height = 30, 
            x = windowWidth * 0.6, y = 50)

        Label(text = "Количество обрабатываемых объектов", 
              font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK)\
            .place(width = windowWidth * 0.5, height = 30, x = windowWidth * 0.1, y = 90)

        self.numberObjects = Entry(font = ("Arial", 17))
        self.numberObjects.place(
            width = windowWidth * 0.3, height = 30, 
            x = windowWidth * 0.6, y = 90)

        Label(
            text = "Количество прогонов для K-прототипов\nпри сравнении методов", 
            font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK
        ).place(
            width = windowWidth * 0.5, height = 30, 
            x = windowWidth * 0.1, y = 130)

        self.numberRuns = Entry(font = ("Arial", 17))
        self.numberRuns.place(
            width = windowWidth * 0.3, height = 30, 
            x = windowWidth * 0.6, y = 130)

        Label(
            text = "ВЫБОР МЕТОДА РАЗБИЕНИЯ ДАННЫХ",
            font = ("Arial", 16, "bold"), bg = PURPLE_DARK, fg = "white"
        ).place(
            width = windowWidth, height = 30, 
            x = 0 , y = 170)

        self.methodVar = IntVar()
        self.methodVar.set(HYBRID)

        Radiobutton(
            text = "Агломеративный подход иерархической кластеризации", 
            variable = self.methodVar, value = HA,
            font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK,
            anchor = "w"
        ).place(
            width = windowWidth * 0.7, height = 30, 
            x = windowWidth  * 0.15, y = 210)
        
        Radiobutton(
            text = "Метод кластеризации центроидного типа K-прототипов", 
            variable = self.methodVar, value = K_PROTOTYPES,
            font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK,
            anchor = "w"
        ).place(
            width = windowWidth * 0.7, height = 30, 
            x = windowWidth  * 0.15, y = 250)
        
        Radiobutton(
            text = "Гибридный метод кластеризации", 
            variable = self.methodVar, value = HYBRID,
            font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK,
            anchor = "w"
        ).place(
            width = windowWidth * 0.7, height = 30, 
            x = windowWidth  * 0.15, y = 290)

        # вместо границы кнопки
        Button(
            highlightbackground = PURPLE_DARK, highlightthickness = 30, 
            fg = PURPLE_LIGHT, state = DISABLED
        ).place(
            width = windowWidth * 0.8, height = 40, 
            x = windowWidth * 0.1, y = 330)
        Button(
            text = "Кластеризировать данные", 
            font = ("Arial", 16), fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE, highlightthickness = 30,
            command = lambda: self.doClustering()
        ).place(
            width = windowWidth * 0.8 - 4, height = 36, 
            x = windowWidth * 0.1 + 2, y = 332)

        Label(
            text = "МЕТОДЫ ОЦЕНКИ КАЧЕСТВА КЛАСТЕРИЗАЦИИ",
            font = ("Arial", 16, "bold"), bg = PURPLE_DARK, fg = "white"
        ).place(
            width = windowWidth, height = 30, 
            x = 0 , y = 380)
        
        self.comparisonVar = IntVar()
        self.comparisonVar.set(ELBOW)

        Radiobutton(
            text = "Метод оценки силуэтов", 
            variable = self.comparisonVar, value = EVALUATION_SILHOUETTES,
            font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK,
            anchor = "w"
        ).place(
            width = windowWidth * 0.35, height = 30, 
            x = windowWidth  * 0.15, y = 420)
        
        Radiobutton(
            text = "Метод локтя", 
            variable = self.comparisonVar, value = ELBOW,
            font = ("Arial", 16), bg = PURPLE_LIGHT, fg = PURPLE_SUPER_DARK,
            anchor = "w"
        ).place(
            width = windowWidth * 0.35, height = 30, 
            x = windowWidth  * 0.6, y = 420)

        Button(
            highlightbackground = PURPLE_DARK, highlightthickness = 30, 
            fg = PURPLE_LIGHT, state = DISABLED
        ).place(
            width = windowWidth * 0.8, height = 40, 
            x = windowWidth * 0.1, y = 460)
        Button(
            text = "Сравнить методы разбиения", 
            font = ("Arial", 16), fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE, highlightthickness = 30,
            command = lambda: self.doComparison()
        ).place(
            width = windowWidth * 0.8 - 4, height = 36, 
            x = windowWidth * 0.1 + 2, y = 462)
        
        Label(
            text = "О ПРОГРАММЕ", 
            font = ("Arial", 16, "bold"), bg = PURPLE_DARK, fg = "white"
        ).place(
            width = windowWidth, height = 30, 
            x = 0 , y = windowHeight - 90)

        Button(highlightbackground = PURPLE_DARK, highlightthickness = 30, 
               fg = PURPLE_LIGHT, state = DISABLED
        ).place(
            width = windowWidth * 0.8, height = 40, 
            x = windowWidth * 0.1, y = windowHeight - 50)
        Button(
            text = "Информация о программе", 
            font = ("Arial", 16), fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE, highlightthickness = 30, 
            command = lambda: self.aboutProgram()
        ).place(
            width = windowWidth * 0.8 - 4, height = 36, 
            x = windowWidth * 0.1 + 2, y = windowHeight - 48)
    

    def getNumberObjects(self) -> Union[int, None]:
        try:
            numberObjects = int(self.numberObjects.get())
        except:
            numberObjects = None
        
        if numberObjects == None or \
           numberObjects < 1 or numberObjects > NUMBER_OF_ROWS:
            messagebox.showwarning("Ошибка",
                "Невозможное значение количества обрабатываемых объектов!\n"
                "Ожидался ввод натурального числа.")
            return
        
        return numberObjects
    

    def getNumberClusters(self, numberObjects: int) -> Union[int, None]:
        try:
            numberClusters = int(self.numberClusters.get())
        except:
            numberClusters = None
        
        if numberClusters == None or \
           numberClusters < 1 or numberClusters > numberObjects:
            messagebox.showwarning("Ошибка",
                "Невозможное значение количества кластеров!\n"
                "Ожидался ввод натурального числа.\n"
                "Также количество кластеров должно быть не больше "
                "количества обрабатываемых объектов.")
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
        numberObjects = self.getNumberObjects()
        if numberObjects == None:
            return

        numberClusters = self.getNumberClusters(numberObjects)
        if numberClusters == None:
            return
        
        objects = self.objects[:numberObjects]

        if self.methodVar.get() == HA:
            distance = Distance()
            dissimilarityMatrix = distance.createDissimilarityMatrix(objects)

            haClusterization = HAClusterization(dissimilarityMatrix)
            haClusterization.buildDendrogram()

        elif self.methodVar.get() == K_PROTOTYPES:
            kPrototypesClusterization = KPrototypesClusterization(objects, numberClusters)
            kPrototypesClusterization.buildGraph()

        elif self.methodVar.get() == HYBRID:
            hybridClusterization = HybridClusterization(objects, numberClusters)
            hybridClusterization.buildGraph()


    def doComparison(self):
        numberObjects = self.getNumberObjects()
        if numberObjects == None:
            return

        numberRuns = self.getNumberRuns()
        if numberRuns == None:
            return
        
        objects = self.objects[:numberObjects]

        if self.comparisonVar.get() == ELBOW:
            test = TestElbow(objects, numberRuns)
            test.comparisonMethods()

        elif self.comparisonVar.get() == EVALUATION_SILHOUETTES:
            test = TestSilhouettes(objects, numberRuns)
            test.comparisonMethods()


    def aboutProgram(self):
        messagebox.showinfo("О программе",
            '''
            Реализация метода разбиения категориальных данных 
            на основе агломеративного подхода иерархической кластеризации
            \n\nКовалец Кирилл ИУ7-83Б (2023)
            ''')

     
    def run(self):
        self.numberClusters.insert(0, NUMBER_OF_CLUSTERS)
        self.numberObjects.insert(0, NUMBER_OF_OBJECTS)
        self.numberRuns.insert(0, NUMBER_OF_RUNS)

        self.window.mainloop()
