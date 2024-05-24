from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        
        # Basic layout
        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)
        self.setCentralWidget(self.cw)
        
        # Title
        self.setWindowTitle('Calculator')
        
    def adjustFixedSize(self):
        
        # Last thing to adjust 
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
        
    def addWidgetToVLayout(self, widget:QWidget):
        self.vLayout.addWidget(widget)
# Message box        
    def makeMsgBox(self):
        return QMessageBox(self)