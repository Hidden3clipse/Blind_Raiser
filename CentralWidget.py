from PyQt6.QtWidgets import QWidget, QPushButton, QTextBrowser, QLabel, QGridLayout, QRadioButton, QCheckBox, QLineEdit, \
    QTimeEdit, QLCDNumber
from PyQt6.QtCore import Qt, pyqtSlot
import sys


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        layout = QGridLayout()

        #First Row
        self.blind_in_euro = QLabel("Blind in €")
        layout.addWidget(self.blind_in_euro, 0, 0)

        start_amount_input = QLineEdit()
        start_amount_input.setInputMask("9999")
        layout.addWidget(start_amount_input, 0, 1)

        self.start_stop = QPushButton("Start/Stop")
        self.start_stop.pressed.connect(self.choose_drink)
        layout.addWidget(self.start_stop, 0, 2)

        #Second Row
        self.raise_time = QLabel("Raise-Time")
        layout.addWidget(self.raise_time, 1, 0)
        time_settings = QTimeEdit()
        layout.addWidget(time_settings, 1, 1)
        lcd_timer = QLCDNumber()
        layout.addWidget(lcd_timer, 1, 2)

        #Third Row
        self.raise_in_percent = QLabel("Raise in %")
        layout.addWidget(self.raise_in_percent, 2, 0)
        in_percent = QLineEdit()
        in_percent.setInputMask("9999")
        layout.addWidget(in_percent, 2, 1)
        self.raise_in = QLabel("Raise in...")
        layout.addWidget(self.raise_in, 2, 2)

        #Fourth Row
        self.raise_in_euro = QLabel("Raise in €")
        layout.addWidget(self.raise_in_euro, 3, 0)
        in_euro = QLineEdit()
        in_euro.setInputMask("9999")
        layout.addWidget(in_euro, 3, 1)

        self.percent = QRadioButton("€")
        self.percent.clicked.connect(self.choose_euro)
        layout.addWidget(self.percent, 3, 2, Qt.AlignmentFlag.AlignRight)

        self.euro = QRadioButton("%")
        self.euro.clicked.connect(self.choose_percent)
        layout.addWidget(self.euro, 3, 3)

        self.text_browser = QTextBrowser()
        layout.addWidget(self.text_browser, 4, 0, 2, 4)

        self.setLayout(layout)

    @pyqtSlot()
    def choose_drink(self):
        print("Start/Stop gedrückt")

    @pyqtSlot()
    def choose_percent(self):
        print("Raise in %", )

    @pyqtSlot()
    def choose_euro(self):
        print("Raise in €")


