import math

from styles import BIG_FONT_SIZE, MEDIUM_FONT_SIZE, SMALL_FONT_SIZE, TEXT_MARGIN, MINIMUM_WIDTH
from PySide6.QtWidgets import QLineEdit, QLabel, QWidget, QPushButton, QGridLayout
from PySide6.QtGui import QKeyEvent
from configSetup import MainWindow
from PySide6.QtCore import Qt, Slot, Signal
from pathlib import Path
import re


# Diretory
ROOT_DIR = Path(__file__).parent
FILES_DIR = ROOT_DIR / 'files'
WINDOW_ICON_PATH = FILES_DIR / 'image_calculator.png'

# Utils
NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')

def isNumOrDot(string):
    return bool(NUM_OR_DOT_REGEX.search(string))

def convertToInt(string: str):
    number = float(string)
    if number.is_integer():
        number = int(number)

    return number

def isValidNumber(string:str):
    valid = False
    try:
        convertToInt(string)
        valid = True
    except ValueError:
        valid = False
    return valid
        
def isEmpty(string:str):
    return len(string) == 0

# Config Display
class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

        self.setReadOnly(True)
        
    def configStyle(self):
        self.setStyleSheet(f'Font-size:{BIG_FONT_SIZE}px;')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGIN for _ in range (4)])
        self.setMinimumWidth(MINIMUM_WIDTH)
  
# Disabling typing on the display and inserting keys
    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key
        
        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isEsc = key in [KEYS.Key_Escape]
        isOperator = key in [KEYS.Key_Minus, KEYS.Key_Plus, KEYS.Key_Slash, KEYS.Key_Asterisk, KEYS.Key_P]
        
        if isEnter:
            self.eqPressed.emit()
            return event.ignore()
        
        if isDelete:
            self.delPressed.emit()
            return event.ignore()
        
        if isEsc:
            self.clearPressed.emit()
            return event.ignore()
        
        if isOperator:
            self.operatorPressed.emit(text)
            if text.lower() == 'p':
                text = '^'
            return event.ignore()
        
        if isEmpty(text):
            return event.ignore()
        
        if isNumOrDot(text):
            self.inputPressed.emit(text)
            return event.ignore()
        
# Info showed        
class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        
# Buttons  
class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
        
    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)
    
class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow', *args, **kwargs ) -> None:
        super().__init__(*args, **kwargs)
 
        self._gridMask = [
            ['C', '⌫', '^', '/'],
            ['7', '8',     '9', '*'],
            ['4', '5',     '6', '-'],
            ['1', '2',     '3', '+'],
            ['N', '0', '.', '='],
        ]
        
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue = 'Your account'
        self._left = None
        self._right = None
        self._op = None
        
        self._makeGrid()
        
    @property
    def equation(self):
        return self._equation
        
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)
            
# Making Grid
    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)
        
        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)
                
                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)
                
                self.addWidget(button, i, j)
                    
                slot = self._makeSlot(self._insertToDisplay, buttonText) 
                self._connectButtonClicked(button, slot)

# Connecting and configuin the button          
    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)   

# Configuin Special buttons / Operators  
    def _configSpecialButton(self, button):
        text = button.text()
        
        if text == 'C':
            self._connectButtonClicked(button, self._clear)
            
        if text == '⌫':
            self._connectButtonClicked(button, self._backspace)      
                 
        if text == 'N':
            self._connectButtonClicked(button, self._invertNumber)           
            
        if text in '+-/*^':
            self._connectButtonClicked(button, self._makeSlot(self._configLeftOp, text))
            
        if text == '=':
            self._connectButtonClicked(button, self._eq)
            
    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

# Set numbers in display to negative form
    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()
        
        if not isValidNumber(displayText):
            return
        
        number = -convertToInt(displayText)    
        self.display.setText(str(number))
        self.display.setFocus()
        
# Insert the button  
    @Slot()     
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text
        
        if not isValidNumber(newDisplayValue):
            return
        
        self.display.insert(text)
        self.display.setFocus()
        
# Func to clear the display 
    @Slot()      
    def _clear(self):
        displayText = self.display.text() 
        
        if not isValidNumber(displayText) and self._left is None:
            self._showError("No numbers to clear")
            return
        
        self._left = None
        self._right = 0.0
        self._op = None
        self.display.clear()
        self.display.setFocus()
    
    @Slot()    
    def _configLeftOp(self, text):
        displayText = self.display.text()  # Number left
        self.display.clear()  # Clear the display
        self.display.setFocus()
        
        # If the people clicked in the operator without a method
        if not isValidNumber(displayText) and self._left is None:
            self._showError("You didn't select numbers")
            return

        # If have something in the left side
        # Don't do nothing. Will wait the number in the right side
        if self._left is None:
            self._left = convertToInt(displayText)

        self._op = text
        self.equation = f'{self._left} {self._op} ??'
    
    @Slot()
# Configuin equal    
    def _eq(self):
        displayText = self.display.text()
        
        if not isValidNumber(displayText):
            self._showError("You didn't select a number")
            return
        
        if self._left is None:
            self._showError("Select a operator")
            return
        
        self._right = convertToInt(displayText)

        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'Error'
        
        try:
            if '^' in self.equation and isinstance(self._left, float | int):
                result = math.pow(self._left, self._right) # type: ignore
                
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError('Undefined result')
         
        except OverflowError:
            self._showError('Pop')        
                           
        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._right = None
        self._left = result
        self.display.setFocus()
        
        if result == 'Error':
            self._left = None
    
    @Slot()
# Fixing backspace for windows users
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()
 
# Dialog Message box         
    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        self.display.setFocus()
        return msgBox
           
    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.setWindowTitle('Informational')
        msgBox.exec()
        self.display.setFocus()
        
    # def _showInfo(self, text):
    #     msgBox = self._makeDialog(text)
    #     msgBox.setIcon(msgBox.Icon.Information)
    #     msgBox.exec()
    
            