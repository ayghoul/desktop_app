import traceback
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
import numpy as np
import h5py 

# Класс для работы с файлами (сохранение/загрузка)         
class FileManager(QWidget):
    array_loaded = pyqtSignal(np.ndarray)
     # Сохранение файла с помощью h5py в формате hdf5 
    def save_array(self, arr): 
        save_file, _ = QFileDialog.getSaveFileName(self, "Сохранить массив в формате hdf", "", "HDF5 Files (*.hdf5);;All Files (*)") 
         
        # Если пользователь отменил выбор, никакой ошибки не случится 
        if not save_file: 
                    return   
         
        try: 
            # Создание HDF5 файла и запись данных 
            with h5py.File(save_file, "w") as data_file:   
                data_file.create_dataset("array", data=arr) 
                QMessageBox.information(self, 'Сохранение', 'Массив сохранен') 
        # В случае какой-либо ошибки, ошибка выведется в окно 
        except Exception as e: 
            QMessageBox.critical(self, 'Ошибка', f'Ошибка при сохранении: {str(e)}') 
 
    # Загрузка массива из hdf файла 
    def load_array(self, arr): 
        load_file, _ = QFileDialog.getOpenFileName(self, "Загрузить массив в формате hdf", "", "HDF5 Files (*.hdf5);;All Files (*)") 
        if not load_file: 
                    return   
        try: 
            # Чтение и редактирование HDF5 файла  
            with h5py.File(load_file, "r+") as data_file:   
                datasets = list(data_file.keys()) 
                if not datasets: 
                    QMessageBox.warning(self, 'Ошибка', 'Файл не содержит датасетов!') 
                    return 
                 
                dataset_name = datasets[0] 
                dataset = data_file[dataset_name] 
                 
                # Проверяем что это массив 
                if not isinstance(dataset, h5py.Dataset): 
                    QMessageBox.warning(self, 'Ошибка', 'Выбранный объект не является датасетом!') 
                    return 

                # Конвертируем в numpy массив 
                arr = np.array(dataset) 
                self.array_loaded.emit(arr)
                 
                QMessageBox.information(self, 'Загрузка файла', 'Успешно загружено, данные обновлены') 
        except Exception as e: 
            print(traceback.format_exc()) 
            QMessageBox.critical(self, 'Ошибка', f'Ошибка при загрузке: {str(e)}') 
