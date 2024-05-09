import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QFrame, QRadioButton, QLabel, QSizePolicy
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

class StyledFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the background with rounded corners
        painter.setBrush(QColor(25, 100, 100, 80))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 5, 5)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vboxlayout = QVBoxLayout(self.centralwidget)
        self.vboxlayout.setObjectName("vboxlayout")

        boxlayout = QVBoxLayout()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        scroll_widget = QWidget()
        scroll_widget.setLayout(boxlayout)
        self.scrollArea.setWidget(scroll_widget)

        self.app_cards = {}
        for i in range(10):
            self.app_cards[i] = {}
            self.app_cards[i]['frame'] = StyledFrame()
            self.app_cards[i]['frame'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.app_cards[i]['frame'].setFixedHeight(100)  # Set fixed height

            self.app_cards[i]['radioButton'] = QRadioButton()
            self.app_cards[i]['label'] = QLabel("TextLabel")
            self.app_cards[i]['label_2'] = QLabel("TextLabel")

            layout = QVBoxLayout(self.app_cards[i]['frame'])
            layout.addWidget(self.app_cards[i]['label'])
            layout.addWidget(self.app_cards[i]['label_2'])
            layout.addWidget(self.app_cards[i]['radioButton'])

            boxlayout.addWidget(self.app_cards[i]['frame'])

        self.vboxlayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")
        for i in range(10):
            self.app_cards[i]['radioButton'].setText("RadioButton")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
