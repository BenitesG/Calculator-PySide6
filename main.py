import sys
from interface import WINDOW_ICON_PATH, Display, Info, ButtonsGrid
from PySide6.QtGui import QIcon
from configSetup import MainWindow
from styles import setupTheme
from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    
    # Creating the application
    app = QApplication(sys.argv)
    
    # Setup archive styles.py
    setup = setupTheme(app) 
    window = MainWindow()
    
    # Set the icon
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            u'CompanyName.ProductName.SubProduct.VersionInformation')
    
    # Info
    info = Info('Your account:')
    window.addWidgetToVLayout(info)
    
    # Display
    display = Display()
    window.addWidgetToVLayout(display)
    
    # Grid
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

    # Execute ALL
    window.adjustFixedSize()
    window.show()
    app.exec()
