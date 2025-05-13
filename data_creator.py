from PyQt5.QtCore import QObject
import numpy as np 

# Класс для создания начального массива данных
class DataCreator(QObject):
    def __init__(self): 
        super().__init__() 
        self.arr = np.array([]) 
    # Создание массива заданного размера, заполненный нулями
    def create_data(self, row=1, col=4): 
        # +3 для доп. столбцов (выпадающий список, среднее, кумулятивная сумма)
        self.arr = np.zeros((row, col+3), dtype=np.float32) 
        return self.arr 
