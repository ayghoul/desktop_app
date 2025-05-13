from PyQt5.QtCore import Qt
import pyqtgraph as pg

# Класс для работы с графиком        
class PlotGraphManager:
    def __init__(self):
        # Настройка стиля
        self.pen = pg.mkPen(color=(0, 0, 0), width=5, style=Qt.SolidLine) 
        self.plot_graph = pg.PlotWidget()
        self.graph = self.plot_graph.plot()
        self.plot_graph.setBackground("w") 
        self.plot_graph.showGrid(x=True, y=True) 
    
    # Создание системы координат
    def create_plot(self):
        return self.plot_graph

    # Обновление графика
    def update_plot(self, arr,  col1, col2): 
        self.plot_graph.setLabel("left", f"Столбец №{col2+1}") 
        self.plot_graph.setLabel("bottom", f"Столбец №{col1+1}") 
        self.plot_graph.addLegend() 
        self.plot_graph.setTitle(f"Зависимость столбца №{col2+1} от столбца №{col1+1}") 
        self.graph.setData(arr[:, col1], arr[:, col2], pen=self.pen, symbol="o") 
        return self.graph
