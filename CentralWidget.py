from PyQt6.QtCore import QTime, pyqtSlot, QTimer  # Importiert Zeitklassen und Timer-Funktionalität
from PyQt6.QtGui import QPixmap  # Importiert Pixmap, um Bilder zu laden (wird im Layout erwähnt)
from PyQt6.QtWidgets import (QWidget, QGridLayout, QLabel, QTextBrowser, QLineEdit, QPushButton, QTimeEdit, QLCDNumber,
                             QRadioButton)  # Importiert verschiedene Widgets für das GUI

# Haupt-Widget, das alle Elemente des Layouts enthält
class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)  # Konstruktor der Elternklasse aufrufen

        # Timer initialisieren (wird verwendet, um jede Sekunde Aktionen auszuführen)
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.decrease_sec)  # Verbinde Timer mit der Funktion, die jede Sekunde aufgerufen wird

        self.__time_left = QTime()  # Variable zur Speicherung der verbleibenden Zeit

        # Eingabefeld für den Blindwert (z. B. "50.00 €")
        self.__line_edit_blind_euro = QLineEdit("50.00")

        # Zeitfeld zur Festlegung der Zeit für Erhöhungen (z. B. 5 Sekunden)
        self.__time_edit = QTimeEdit(QTime(0, 0, 5))  # Standardzeit: 5 Sekunden
        self.__time_edit.setDisplayFormat("hh:mm:ss")  # Format der Zeitdarstellung

        # Eingabefeld für die Erhöhung in Prozent
        self.__line_edit_raise_percent = QLineEdit("15.3")

        # Eingabefeld für die Erhöhung in Euro
        self.__line_edit_raise_euro = QLineEdit("10.00")

        # Start-/Stopp-Button
        self.__push_button = QPushButton("Start")
        self.__push_button.released.connect(self.timer_start)  # Verbinde den Button mit der Startfunktion

        # Anzeige für die aktuelle Zeit (z. B. Countdown)
        self.__lcd_number = QLCDNumber()
        self.__lcd_number.display(self.__time_edit.time().toString("hh:mm:ss"))  # Setzt die anfängliche Zeit

        # Radiobuttons zur Auswahl, ob die Erhöhung in Prozent oder Euro erfolgen soll
        self.__radio_button_percent = QRadioButton("Raise in %")
        self.__radio_button_euro = QRadioButton("Raise in €")

        # Textbrowser für Status-Updates und Meldungen
        self.__text_browser = QTextBrowser()

        # Layout erstellen (Gitterlayout für klare Anordnung)
        grid_layout = QGridLayout()

        # Beschriftungen und Eingabefelder hinzufügen
        grid_layout.addWidget(QLabel("Blind in €"), 1, 1)
        grid_layout.addWidget(QLabel("Raise Time"), 2, 1)
        grid_layout.addWidget(self.__radio_button_percent, 3, 1)
        grid_layout.addWidget(self.__radio_button_euro, 4, 1)

        # Eingabefelder und andere Widgets hinzufügen
        grid_layout.addWidget(self.__line_edit_blind_euro, 1, 2)
        grid_layout.addWidget(self.__time_edit, 2, 2)
        grid_layout.addWidget(self.__line_edit_raise_percent, 3, 2)
        grid_layout.addWidget(self.__line_edit_raise_euro, 4, 2)

        # Button, LCD-Anzeige und Bild hinzufügen
        grid_layout.addWidget(self.__push_button, 1, 3)
        grid_layout.addWidget(self.__lcd_number, 2, 3)
        grid_layout.addWidget(QLabel("chip.jpg"), 3, 3, 1, 2)  # Platzhalter für ein Bild

        # Textbrowser hinzufügen, der über mehrere Spalten geht
        grid_layout.addWidget(self.__text_browser, 5, 1, 1, 4)

        # Layout setzen
        self.setLayout(grid_layout)

        # Initiale Nachricht in den Textbrowser schreiben
        self.__text_browser.append("Ready")

    # Startet den Timer
    @pyqtSlot()
    def timer_start(self):
        # Button-Text ändern und neue Funktion mit dem Button verbinden
        self.__push_button.setText("Stopp")
        self.__push_button.released.disconnect(self.timer_start)  # Verbindung zur Startfunktion trennen
        self.__push_button.released.connect(self.timer_stop)  # Verbindung zur Stoppfunktion herstellen

        # Eingabefelder und Radiobuttons deaktivieren (während der Timer läuft)
        self.__line_edit_blind_euro.setDisabled(True)
        self.__time_edit.setDisabled(True)
        self.__line_edit_raise_percent.setDisabled(True)
        self.__line_edit_raise_euro.setDisabled(True)
        self.__radio_button_euro.setDisabled(True)
        self.__radio_button_percent.setDisabled(True)

        # Verbleibende Zeit auf die Zeit aus dem Zeitfeld setzen
        self.__time_left = self.__time_edit.time()

        # Timer starten (Intervall: 1 Sekunde)
        self.__timer.start(1 * 1000)

    # Stoppt den Timer
    @pyqtSlot()
    def timer_stop(self):
        # Button-Text ändern und neue Funktion mit dem Button verbinden
        self.__push_button.setText("Start")
        self.__push_button.released.disconnect(self.timer_stop)  # Verbindung zur Stoppfunktion trennen
        self.__push_button.released.connect(self.timer_start)  # Verbindung zur Startfunktion herstellen

        # Eingabefelder und Radiobuttons wieder aktivieren
        self.__line_edit_blind_euro.setEnabled(True)
        self.__time_edit.setEnabled(True)
        self.__line_edit_raise_percent.setEnabled(True)
        self.__line_edit_raise_euro.setEnabled(True)
        self.__radio_button_euro.setEnabled(True)
        self.__radio_button_percent.setEnabled(True)

        # LCD-Anzeige zurücksetzen
        self.__lcd_number.display(self.__time_edit.time().toString("hh:mm:ss"))

        # Timer stoppen
        self.__timer.stop()

    # Reduziert die verbleibende Zeit jede Sekunde
    @pyqtSlot()
    def decrease_sec(self):
        if self.__time_left == QTime(0, 0, 0):  # Wenn der Countdown abgelaufen ist
            self.__time_left = self.__time_edit.time()  # Countdown zurücksetzen
            self.__text_browser.append("Blind raised.")  # Nachricht in den Textbrowser schreiben

        # Reduziert die verbleibende Zeit um eine Sekunde
        self.__time_left = self.__time_left.addSecs(-1)
        print(self.__time_left)  # Debug-Ausgabe der verbleibenden Zeit

        # Aktualisiert die Anzeige der verbleibenden Zeit
        self.__lcd_number.display(self.__time_left.toString("hh:mm:ss"))
