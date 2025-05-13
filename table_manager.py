from PyQt5 import QtGui
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import numpy as np

# Класс для управления таблицей
class TableManager(QObject): 
    table_size_changed = pyqtSignal(np.ndarray)
    add_combobox_signal = pyqtSignal(QTableWidget, np.ndarray, int)

    # Создание таблицы с указанными размерами
    def create_table(self, table, row, col):  
        table.setRowCount(row) 
        table.setColumnCount(col) 
        return table 
    
    def fill_table_cell(self, table, arr, row, col): 
        
        return table 
    def add_table_column(self, table, adding_col_quantity=1):
        for i in range(table.columnCount(),  table.columnCount()+adding_col_quantity): 
            table.insertColumn(i) 
        return table
    def add_table_row(self, table, adding_row_quantity=1):
        for i in range(table.rowCount(), table.rowCount()+adding_row_quantity): 
            table.insertRow(i) 
        return table
    def remove_table_column(self, table, removing_col_quantity=1): 
        for i in range(table.columnCount(), table.columnCount()-removing_col_quantity-1, -1): 
            table.removeColumn(i) 
        return table 
        
    def remove_table_row(self, table, removing_row_quantity=1):
        for i in range(table.rowCount(), table.rowCount()-removing_row_quantity-1, -1): 
            table.removeRow(i) 
        return table
        
    def change_table_size(self, table, arr):
        row_size = len(arr); col_size = len(arr[0])
        table_row = table.rowCount(); table_col = table.columnCount()
        if row_size > table_row:
            table = self.add_table_row(table, row_size - table_row)
        elif row_size < table_row:
            table = self.remove_table_row(table, table_row - row_size)
        if col_size > table_col:
            table = self.add_table_column(table, col_size - table_col)
        elif col_size < table_col:
            table = self.remove_table_column(table, table_col - col_size)
        
        self.add_combobox_signal.emit(table, arr, table_row)
        self.table_size_changed.emit(arr)
   
    def change_bg_color(self, table, arr, row): 
        if arr[row][len(arr[0])-2] > 0: 
            table.item(row, len(arr[0])-2).setBackground(QtGui.QColor(0,128,0)) 
        else: 
            table.item(row, len(arr[0])-2).setBackground(QtGui.QColor(128,0,0)) 
        return table
    
    # Заполнение ячеек таблицы данными из массива
    def fill_table(self, table, arr):
        for row_index in range(len(arr)):
            # Метод вызывается дважды при изменении размера массива, после при изменении размера таблицы
            # в первом случае размер таблицы еще не совпадает с размером массива из-за чего происходит ошибка
            # 'NoneType' object has no attribute ...
            # на работоспособность не влияет, поэтому ошибка игнорируется - pass
            try:
                for col_index in range(len(arr[0])): 
                    item = QTableWidgetItem(str(round(arr[row_index][col_index], 2))) 
                    table.setItem(row_index, col_index, item) 
                    table.item(row_index, col_index).setTextAlignment(Qt.AlignCenter)
                
                table = self.change_bg_color(table, arr, row_index) 
            except:
                pass
        return table