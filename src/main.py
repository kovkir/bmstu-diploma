from typing import List
from random import shuffle

from window import Window
from constants import *


def readFile(nameFile: str) -> List[List[str]]:
    '''
    Возвращает перемешанный список объектов из файла
    '''
    file = open(nameFile, 'r')
    objects = file.read().split("\n")
    file.close()

    for i in range(len(objects)):
        objects[i] = objects[i].split(",")

    # перемешать список
    # shuffle(objects)
    return objects


def backupFile(nameFile: str, objects) -> List[List[str]]:
    '''
    Сохраняет список перемешанных объектов в файл
    '''
    file = open(nameFile, 'w')

    for obj in objects:
        for i in range(len(obj)):
            file.write(obj[i])

            if i == len(obj) - 1:
                file.write("\n")
            else:
                file.write(",")

    file.close()


def main(): 
    objects = readFile(FILE_NAME)
    # backupFile(BACKUP_FILE_NAME, objects)

    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, objects)
    window.run()


if __name__ == "__main__":
    main()
