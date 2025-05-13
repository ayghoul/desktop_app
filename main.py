import sys
from PyQt5.QtWidgets import QApplication
from desktop_app import DesktopApp

# Запуск приложения

if __name__ == "__main__": 
    app = QApplication(sys.argv) 
    window = DesktopApp() 
    window.show() 
    sys.exit(app.exec_()) 