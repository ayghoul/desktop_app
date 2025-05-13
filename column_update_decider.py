from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np

# Класс для проверки необходимости добавления служебных столбцов при загрузке файла (load_file)
class ColumnUpdateDecider(QObject): 
        column_is_needed = pyqtSignal(bool, np.ndarray)
        # Проверка столбца "среднее"
        # если столбец существует в загруженном файле, то пропадает необходимость 
        # добавления доп. столбцов 
        def is_column_addition_needed(self, arr): 
            for row in arr: 
                if row[-2] != round(np.mean(row[:-2]), 2): 
                    self.column_is_needed.emit(True, arr) 
            else: 
                self.column_is_needed.emit(False, arr) 