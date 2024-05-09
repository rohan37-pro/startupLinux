import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QFrame
from PyQt5.QtWidgets import QRadioButton, QLabel, QSizePolicy, QGraphicsDropShadowEffect, QHBoxLayout
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setProperty("mainwidget", True)
        self.centralwidget.setObjectName("centralwidget")
        self.vboxlayout = QVBoxLayout(self.centralwidget)
        self.vboxlayout.setObjectName("vboxlayout") 

        boxlayout = QVBoxLayout()
        boxlayout.setContentsMargins(10, 10, 10, 50)
        boxlayout.setAlignment(Qt.AlignHCenter)
        self.scrollArea = QScrollArea()
        self.scrollArea.setProperty("mainscrollarea", True)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        scroll_widget = QWidget()
        scroll_widget.setLayout(boxlayout)
        self.scrollArea.setWidget(scroll_widget)


        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(3, 3)
        self.shadow.setColor(QColor(0, 0, 0, 50))


        self.app_cards = {}
        for i in range(10):
            self.app_cards[i] = {}
            self.app_cards[i]['frame'] = QFrame()
            self.app_cards[i]['frame'].setProperty("framecontainer", True)
            self.app_cards[i]['frame'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.app_cards[i]['frame'].setFixedHeight(100)  # Set fixed height
            self.app_cards[i]['frame'].setMaximumWidth(800)
            self.app_cards[i]['frame'].setFrameShape(QFrame.StyledPanel)


            self.app_cards[i]['radioButton'] = QRadioButton()
            self.app_cards[i]['radioButton'].setProperty("radiobutt", True)
            self.app_cards[i]['radioButton'].setStyleSheet(";")
            self.app_cards[i]['label'] = QLabel("TextLabel")
            self.app_cards[i]['label_2'] = QLabel("hello there this is my area, don't interfere")

            layout = QHBoxLayout(self.app_cards[i]['frame']) 
            
            layout.addStretch()
            layout.addWidget(self.app_cards[i]['label'])
            layout.addWidget(self.app_cards[i]['label_2'])
            layout.addStretch()
            layout.addStretch()
            layout.addStretch()
            layout.addStretch()
            layout.addStretch()
            layout.addWidget(self.app_cards[i]['radioButton'])
            layout.addStretch()


            boxlayout.addWidget(self.app_cards[i]['frame'])

        self.vboxlayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")
        for i in range(10):
            self.app_cards[i]['radioButton'].setText("OFF")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    MainWindow.setProperty("mainLinux", True)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    with open('stylesheet', 'r') as file:
        stylesheet = file.read()
    MainWindow.setStyleSheet(stylesheet)
    MainWindow.show()
    sys.exit(app.exec_())
