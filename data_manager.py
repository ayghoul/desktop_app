from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QTableWidget
import numpy as np


# Основной класс для управления данными и вычислений
class DataManager(QObject):
    array_changed = pyqtSignal(np.ndarray)
    array_size_changed = pyqtSignal(QTableWidget, np.ndarray)
    calculate_mean_signal = pyqtSignal(float)
    calculate_cumsum_signal = pyqtSignal(np.ndarray)

    # Методы для изменения размера массива

    # добавить колонку слева (для вып. списка)
    def add_left_column(self, arr, adding_col_quantity=1): 
        arr = np.append(np.ones((len(arr), adding_col_quantity)), arr, axis=1)
        self.array_changed.emit(arr)
        return arr 
    
    # добавить колонку или несколько справа
    def add_right_column(self, arr, adding_col_quantity=1): 
        arr = np.append(arr, np.zeros((len(arr), adding_col_quantity)), axis=1)
        self.array_changed.emit(arr)
        return arr 
    
    # добавить строки
    def add_bottom_row(self, arr, adding_row_quantity=1): 
        arr = np.append(arr, np.zeros((adding_row_quantity, len(arr[0]))), axis=0) 
        self.array_changed.emit(arr)
        return arr 
    
    # удалить колонки
    def remove_column(self, arr, removing_col_quantity=1): 
        arr = np.delete(arr, [-i for i in range(1, removing_col_quantity+1)], axis=1) 
        return arr 
    
    # удалить строки
    def remove_row(self, arr, removing_row_quantity=1): 
        arr = np.delete(arr, [-i for i in range(1, removing_row_quantity+1)], axis=0) 
        return arr 
    
    # Метод для изменения размера массива, связан с кнопкой "Изменить размер"
    # проверяет, как именно необходимо изменить размер: увеличить или уменьшить
    # кидает сигнал для изменения таблицы
    def change_arr_size(self, table, arr, row_size, col_size):
        

        if row_size == len(arr) and col_size == len(arr[0]):
            return
        elif row_size == 0:
            return
        elif col_size < 1:
            return
        else:
            if row_size > len(arr):
                arr = self.add_bottom_row(arr, row_size - len(arr))
            elif row_size < len(arr):
                arr = self.remove_row(arr, len(arr) - row_size)
            if col_size > len(arr[0]):
                arr = self.add_right_column(arr, col_size - len(arr[0]))
            elif col_size < len(arr[0]):
                arr = self.remove_column(arr, len(arr[0]) - col_size)
        self.array_size_changed.emit(table, arr)

    # Вычисление среднего значения для строки, есть сигнал
    def calculate_mean(self, arr, row_index): 
        arr[row_index][-2] = np.mean(arr[row_index][:-2]) 
        self.calculate_mean_signal.emit(np.mean(arr[row_index][:-2]))
        return arr 
    
    # Вычисление кумулятивной суммы, есть сигнал
    def calculate_cumsum(self, arr): 
        arr[:, -1] = np.cumsum(arr[:,-2], axis=0) 
        self.calculate_cumsum_signal.emit(np.cumsum(arr[:,-2], axis=0)) 
        return arr 
    # Заполнение массива радномными числами от -100 до 100
    # первая колонка под выпадающий список заполняется единицами
    def fill_array_random(self, arr): 
        arr = np.random.randint(-100, 100, (len(arr), len(arr[0])-1)) 
        arr = np.append(np.ones((len(arr), 1)), arr, axis=1)
        self.array_changed.emit(arr)
    
    # Метод для добавления доп.столбцов при загрузке файла
    def add_columns(self, arr):
        arr = self.add_left_column(arr)
        arr = self.add_right_column(arr, 2)
        self.array_changed.emit(arr)