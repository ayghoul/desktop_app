import numpy as np 
from PyQt5.QtWidgets import (QMessageBox, QWidget, QTableWidget,  
 QLineEdit, QPushButton, QVBoxLayout,  
QHBoxLayout, QLabel) 
from PyQt5.QtCore import Qt, QSize, pyqtSignal 
from PyQt5 import QtGui 


# Импорт классов из файлов с той же директории
from data_creator import DataCreator
from column_update_decider import ColumnUpdateDecider
from data_manager import DataManager
from table_manager import TableManager
from combobox_manager import ComboboxManager
from plotgraph_manager import PlotGraphManager
from file_manager import FileManager

# Основной класс приложения, связывающий все части между собой
class DesktopApp(QWidget):
    selected_column_signal = pyqtSignal(np.ndarray, int, int) 
    is_empty_signal = pyqtSignal(QTableWidget, np.ndarray, int, int)
    def __init__(self): 
        super().__init__() 
        # Инициализация всех компонентов
        self.data_creator = DataCreator() 
        self.data_manager = DataManager() 
        self.table_manager = TableManager() 
        self.plotgraph_manager = PlotGraphManager()
        self.combobox_manager = ComboboxManager()
        self.file_manager = FileManager()
        self.add_column_decider = ColumnUpdateDecider()


        # Создание вспомогательных переменных
        self.last_selected_column = None
        self.column1 = None
        self.column2 = None

        # Создание таблицы, графика и массива размером 3х2 (3х5 с учетом доп столбцов)
        self.plot_graph = self.plotgraph_manager.create_plot()
        self.arr = self.data_creator.create_data(3, 2) 
        self.table = QTableWidget() 
        self.table = self.table_manager.create_table(self.table, len(self.arr), len(self.arr[0])) 
        self.table, self.arr = self.combobox_manager.create_combobox(self.table, self.arr)
        
        # Сигналы
        self.table.itemSelectionChanged.connect(self.check_selection)
        self.selected_column_signal.connect(self.plotgraph_manager.update_plot)
        self.table.itemChanged.connect(self.change_array_item)
        self.data_manager.array_changed.connect(self.update_table)
        self.data_manager.array_changed.connect(self.update_arr)
        self.data_manager.array_size_changed.connect(self.table_manager.change_table_size)
        self.table_manager.add_combobox_signal.connect(self.combobox_manager.create_combobox)
        self.data_manager.array_changed.connect(lambda: self.combobox_manager.create_combobox(self.table, self.arr))
        self.combobox_manager.to_update_plot.connect(self.update_plot)
        self.combobox_manager.array_changed.connect(self.update_table)
        self.table_manager.table_size_changed.connect(self.update_table)
        self.combobox_manager.combo_created.connect(self.update_arr)
        self.file_manager.array_loaded.connect(self.update_arr)
        self.file_manager.array_loaded.connect(self.add_column_decider.is_column_addition_needed)
        self.add_column_decider.column_is_needed.connect(self.add_calculation_columns)
        self.is_empty_signal.connect(self.data_manager.change_arr_size)
        # Обновление таблицы с учетом всех вычислений
        self.update_table(self.arr)

        # Настройка интерфейса приложения
        self.setup_ui(self.table) 

    # Метод добавляет доп. столбцы если получил сигнал True от класса "ColumnUpdateDecider"
    def add_calculation_columns(self, flag, arr):
        if flag:
            self.table = self.table_manager.add_table_column(self.table, 3)
            arr = self.data_manager.add_columns(arr)
            self.update_arr(self.arr)
        else:
            # если получен сигнал False, то таблица обновляется
            self.update_arr(self.arr)
            if len(self.arr) == self.table.rowCount() and len(self.arr[0]) == self.table.columnCount():
                self.update_table(self.arr)
            else:
                self.table_manager.change_table_size(self.table, self.arr)
    
    # Метод для обновления графика
    def update_plot(self):
        if self.column1 is not None and self.column2 is not None :
            self.plotgraph_manager.update_plot(self.arr, self.column1, self.column2)

    # Обновление массива при его изменении
    def update_arr(self, arr):
        self.arr = arr

    # Обновление таблицы при изменении данных массива
    def update_table(self, arr):
        # отключение сигнала itemChanged для избежания зацикливания
        if self.table.receivers(self.table.itemChanged) > 0:
            self.table.itemChanged.disconnect(self.change_array_item) 
        for i in range(len(arr)):
            arr = self.data_manager.calculate_mean(arr, i)
        arr = self.data_manager.calculate_cumsum(arr)
        self.table = self.table_manager.fill_table(self.table, arr)
        self.arr = arr
        if self.table.receivers(self.table.itemChanged) <= 0:
            self.table.itemChanged.connect(self.change_array_item)
        self.update_plot() 
        
    # Изменение значения в ячейке массива, при изменении таблицы
    def change_array_item(self):
        row = self.table.currentRow(); col = self.table.currentColumn()
        self.arr[row][col] = float(self.table.item(row, col).text()) 
        self.update_table(self.arr)

    # Обработка выбора столбцов для графика
    def check_selection(self):

        # Если не выбрано ничего, то последнему выбранному столбцу присваивается значение None
        if not self.table.selectedItems():
            self.last_selected_column = None
            return

        # Если выбрана ячейка, а не столбец, также присваивается None
        if len(self.table.selectedItems()) < len(self.arr) - 1:
            if (self.table.selectedItems()[0].column() != 0):
                self.last_selected_column = None
            return

        # при прохождении проверок, выбранный столбец остается в памяти
        col_checking = self.table.selectedItems()[0].column()

        # если это первый выбранный столбец, то он присвается в переменную
        # как последний выбранный до следующего 
        if self.last_selected_column == None:
            self.last_selected_column = col_checking

        # если выбраны 2 неодинаковых столбца, посылается сигнал
        # строится график
        if self.last_selected_column != col_checking:
            self.selected_column_signal.emit(self.arr, self.last_selected_column, col_checking)
            self.column1 = self.last_selected_column
            self.column2 = col_checking
            self.table.clearSelection()
            return
        
    # Проверка пустые ли ячейки для ввода размера массива 
    def is_empty(self, row, col):
        if row and not col:
            QMessageBox.information(self, "Внимание", "Небходимо ввести количество столбцов")
            return
        if col and not row:
            QMessageBox.information(self, "Внимание", "Небходимо ввести количество строк")
            return
        if row and col:
            self.is_empty_signal.emit(self.table, self.arr, int(row), int(col)+3)
        else:
            QMessageBox.information(self, "Внимание", "Небходимо ввести размер массива")
            return

    # Настройка GUI
    def setup_ui(self, table): 
        self.setMinimumSize(QSize(1000, 700))       
        self.setWindowTitle("DesktopApp")  

        # Кнопки управления
        self.fill_button = QPushButton("Заполнить рандомно", self) # 
        self.change_size_button = QPushButton("Изменить размер массива", self) 
        self.load_array_button = QPushButton("Загрузить массив", self) 
        self.save_array_button = QPushButton("Сохранить массив", self) 

        # Слоты для ввода размера массива
        self.le_row_size = QLineEdit(self) 
        self.le_col_size = QLineEdit(self) 
         
        self.row = len(self.arr)
        self.col = len(self.arr[0]) 
        
        self.lbl_row_size = QLabel("Количество строк") 
        self.lbl_col_size = QLabel("Количество столбцов") 
        self.le_row_size.setValidator(QtGui.QIntValidator(1, 999, self)) 
        self.le_col_size.setValidator(QtGui.QIntValidator(1, 999, self)) 

        # Настройка слоев
        layout = QHBoxLayout() 

        layout_vertical = QVBoxLayout() 
        layout_vertical.addWidget(table) 
        layout_vertical.addWidget(self.plot_graph) 

        layout_input_lines = QHBoxLayout() 
        layout_input_lines.addWidget(self.le_row_size) 
        layout_input_lines.addWidget(self.le_col_size)

        layout_input_labels = QHBoxLayout() 
        layout_input_labels.addWidget(self.lbl_row_size) 
        layout_input_labels.addWidget(self.lbl_col_size) 

        layout_buttons = QVBoxLayout() 
        layout_buttons.addWidget(self.fill_button) 
        layout_buttons.addLayout(layout_input_labels) 
        layout_buttons.addLayout(layout_input_lines) 
        layout_buttons.addWidget(self.change_size_button) 
        layout_buttons.addWidget(self.load_array_button) 
        layout_buttons.addWidget(self.save_array_button) 
        layout_buttons.setAlignment(Qt.AlignTop) 
        
        layout.addLayout(layout_vertical, stretch=1) 
        layout.addLayout(layout_buttons) 
        self.setLayout(layout)

        
        # Соединение кнопок с методами реализующими их функционал
        self.save_array_button.clicked.connect(lambda: self.file_manager.save_array(self.arr))
        self.load_array_button.clicked.connect(lambda: self.file_manager.load_array(self.arr))
        self.change_size_button.clicked.connect(lambda: self.is_empty(self.le_row_size.text(), self.le_col_size.text()))
        self.fill_button.clicked.connect(lambda: self.data_manager.fill_array_random(self.arr))



