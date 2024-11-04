from PyQt6.QtCore import QTime, pyqtSlot, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QTextBrowser, QLineEdit, QPushButton, QTimeEdit, QLCDNumber, \
    QRadioButton


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.decrease_sec)

        self.__time_left = QTime()

        self.__line_edit_blind_euro = QLineEdit("50.00")

        self.__time_edit = QTimeEdit(QTime(0, 0, 5))
        self.__time_edit.setDisplayFormat("hh:mm:ss")

        self.__line_edit_raise_percent = QLineEdit("15.3")

        self.__line_edit_raise_euro = QLineEdit("10.00")

        self.__push_button = QPushButton("Start")
        self.__push_button.released.connect(self.timer_start)

        self.__lcd_number = QLCDNumber()
        self.__lcd_number.display(self.__time_edit.time().toString("hh:mm:ss"))

        self.__radio_button_percent = QRadioButton("Raise in %")

        self.__radio_button_euro = QRadioButton("Raise in €")

        self.__text_browser = QTextBrowser()

        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel("Blind in €"), 1, 1)
        grid_layout.addWidget(QLabel("Raise Time"), 2, 1)
        grid_layout.addWidget(self.__radio_button_percent, 3, 1)
        grid_layout.addWidget(self.__radio_button_euro, 4, 1)

        grid_layout.addWidget(self.__line_edit_blind_euro, 1, 2)
        grid_layout.addWidget(self.__time_edit, 2, 2)
        grid_layout.addWidget(self.__line_edit_raise_percent, 3, 2)
        grid_layout.addWidget(self.__line_edit_raise_euro, 4, 2)

        grid_layout.addWidget(self.__push_button, 1, 3)
        grid_layout.addWidget(self.__lcd_number, 2, 3)
        grid_layout.addWidget(QLabel("chip.jpg"), 3, 3, 1, 2)

        grid_layout.addWidget(self.__text_browser, 5, 1, 1, 4)

        self.setLayout(grid_layout)

        self.__text_browser.append("Ready")

    @pyqtSlot()
    def timer_start(self):
        self.__push_button.setText("Stopp")
        self.__push_button.released.disconnect(self.timer_start)
        self.__push_button.released.connect(self.timer_stop)

        self.__line_edit_blind_euro.setDisabled(True)
        self.__time_edit.setDisabled(True)
        self.__line_edit_raise_percent.setDisabled(True)
        self.__line_edit_raise_euro.setDisabled(True)

        self.__radio_button_euro.setDisabled(True)
        self.__radio_button_percent.setDisabled(True)

        self.__time_left = self.__time_edit.time()

        self.__timer.start(1 * 1000)

    @pyqtSlot()
    def timer_stop(self):
        self.__push_button.setText("Start")
        self.__push_button.released.disconnect(self.timer_stop)
        self.__push_button.released.connect(self.timer_start)

        self.__line_edit_blind_euro.setEnabled(True)
        self.__time_edit.setEnabled(True)
        self.__line_edit_raise_percent.setEnabled(True)
        self.__line_edit_raise_euro.setEnabled(True)

        self.__radio_button_euro.setEnabled(True)
        self.__radio_button_percent.setEnabled(True)

        self.__lcd_number.display(self.__time_edit.time().toString("hh:mm:ss"))

        self.__timer.stop()

    @pyqtSlot()
    def decrease_sec(self):
        if self.__time_left == QTime(0, 0, 0):
            self.__time_left = self.__time_edit.time()

            self.__text_browser.append("Blind raised.")

        self.__time_left = self.__time_left.addSecs(-1)
        print(self.__time_left)

        self.__lcd_number.display(self.__time_left.toString("hh:mm:ss"))
