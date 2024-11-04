from PyQt6.QtWidgets import QWidget, QPushButton, QTextBrowser, QLabel, QGridLayout, QRadioButton, QCheckBox, QLineEdit, \
    QTimeEdit, QLCDNumber
from PyQt6.QtCore import Qt, pyqtSlot, QDateTime, QTimer
import sys


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        layout = QGridLayout()

        # First Row
        self.blind_in_euro = QLabel("Blind in €")
        layout.addWidget(self.blind_in_euro, 0, 0)

        self.start_amount_input = QLineEdit()
        self.start_amount_input.setInputMask("9999")
        layout.addWidget(self.start_amount_input, 0, 1)

        self.start_stop = QPushButton("Start/Stop")
        self.start_stop.pressed.connect(self.start_timer)
        layout.addWidget(self.start_stop, 0, 2)

        # Second Row
        self.raise_time = QLabel("Raise-Time")
        layout.addWidget(self.raise_time, 1, 0)

        self.time_settings = QTimeEdit()
        self.time_settings.setDisplayFormat("mm:ss")
        layout.addWidget(self.time_settings, 1, 1)

        self.lcd_timer = QLCDNumber()
        layout.addWidget(self.lcd_timer, 1, 2)

        # Third Row
        self.raise_in_percent = QLabel("Raise in %")
        layout.addWidget(self.raise_in_percent, 2, 0)

        self.in_percent = QLineEdit()
        self.in_percent.setInputMask("9999")
        layout.addWidget(self.in_percent, 2, 1)

        self.raise_in = QLabel("Raise in...")
        layout.addWidget(self.raise_in, 2, 2)

        # Fourth Row
        self.raise_in_euro = QLabel("Raise in €")
        layout.addWidget(self.raise_in_euro, 3, 0)

        self.in_euro = QLineEdit()
        self.in_euro.setInputMask("9999")
        layout.addWidget(self.in_euro, 3, 1)

        self.percent = QRadioButton("%")
        self.percent.clicked.connect(self.choose_percent)
        layout.addWidget(self.percent, 3, 2, Qt.AlignmentFlag.AlignRight)

        self.euro = QRadioButton("€")
        self.euro.clicked.connect(self.choose_euro)
        layout.addWidget(self.euro, 3, 3)

        # QTextBrowser für Ausgabe
        self.text_browser = QTextBrowser()
        layout.addWidget(self.text_browser, 4, 0, 2, 4)

        self.setLayout(layout)

        # Timer für Raise
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 0


    @pyqtSlot()
    def start_timer(self):
        raise_time = self.time_settings.time()
        self.time_left = raise_time.minute() * 60 + raise_time.second()
        self.lcd_timer.display(self.time_left)
        self.timer.start(1000)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.lcd_timer.display(self.time_left)
        else:
            self.timer.stop()
            self.calculate_raise()


    @pyqtSlot()
    def choose_percent(self):
        print("Raise in %")

    @pyqtSlot()
    def choose_euro(self):
        print("Raise in €")

