from PyQt5.QtCore import QObject, QSignalMapper, pyqtSignal
from PyQt5.QtWidgets import QComboBox
import numpy as np

# Класс для управления выпадающим списком в первом столбце
class ComboboxManager(QObject):
    array_changed = pyqtSignal(np.ndarray)
    combo_created = pyqtSignal(np.ndarray)
    to_update_plot = pyqtSignal()

    def __init__(self):
        super().__init__() 
        self.mapper = QSignalMapper()  

    # Создание выпадающих списков в первом столбце
    def create_combobox(self, table, arr, added_rows_index=0):
        if added_rows_index == 0:
            self.mapper = QSignalMapper()

        for i in range(added_rows_index, table.rowCount()):
            self.combobox = QComboBox()
            self.combobox.addItems(['1', '2', '3', '4', '5'])
            table.setCellWidget(i, 0, self.combobox)
            arr[i][0] = 1
            # Настройка сигналов, чтобы при изменении ячейки с выпадающим списком
            # менялся и массив
            self.mapper.setMapping(self.combobox,i)
            self.combobox.currentIndexChanged.connect(self.mapper.map)   
        self.mapper.mapped[int].connect(lambda: self.get_item_combobox(table, arr))
        self.combo_created.emit(arr)
        return (table, arr)
    
    # Метод забирающий значение из ячейки таблицы в массив
    def get_item_combobox(self, table, arr):
        arr[table.currentRow()][0] = int(table.cellWidget(table.currentRow(), 0).currentText()) 
        self.array_changed.emit(arr)
        self.to_update_plot.emit()
     