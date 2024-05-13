import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QFrame, QCheckBox
from PyQt5.QtWidgets import QRadioButton, QLabel, QSizePolicy, QGraphicsDropShadowEffect, QHBoxLayout
from PyQt5.QtGui import QColor, QPaintEvent, QPainter, QBrush, QPen, QPixmap
from PyQt5.QtCore import   QPoint, Qt, QRect
from utils import collect


class animeToggleButton(QCheckBox):
    def __init__(
            self,
            width=60,
            bgcolor='#777',
            circle_color='#DDD',
            active_color='#00d5ff',
    ):
        QCheckBox.__init__(self)
        self.setFixedSize(width, 28)
        self.setCursor(Qt.PointingHandCursor)
        
        self._bgcolor= bgcolor
        self._circle_color = circle_color
        self._active_color = active_color


        self.stateChanged.connect(self.debug)

   
    def debug(self):
        print(f"status : {self.isChecked()}")


    def hitButton(self, pos: QPoint) :
        return self.contentsRect().contains(pos)

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.setRenderHint(QPainter.Antialiasing)
        paint.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.width(), self.height())

        if not self.isChecked():
            paint.setBrush(QColor(self._bgcolor))
            paint.drawRoundedRect(0, 0, rect.width(), self.height(), self.height()/2, self.height()/2)
            
            # paint circle
            paint.setBrush(QColor(self._circle_color))
            paint.drawEllipse(3, 3, 22, 22)
        else:
            paint.setBrush(QColor(self._active_color))
            paint.drawRoundedRect(0, 0, rect.width(), self.height(), self.height()/2, self.height()/2)
            
            # paint circle
            paint.setBrush(QColor(self._circle_color))
            paint.drawEllipse(self.width()-26, 3, 22, 22)


        paint.end()

    


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


            self.app_cards[i]['toggleButton'] = animeToggleButton()
            self.app_cards[i]['toggleButton'].setProperty("toggleButt", True)
            self.app_cards[i]['toggleButton'].setStyleSheet(";")

            self.app_cards[i]['label'] = QLabel("TextLabel")
            self.app_cards[i]['label'].setProperty("app_icon", True)
            self.app_cards[i]['label'].setFixedHeight(80)
            self.app_cards[i]['label'].setFixedWidth(80)
            self.app_cards[i]['label'].setPixmap(QPixmap("/home/rohan/Pictures/swarnali.png").scaled(self.app_cards[i]['label'].width()-20, self.app_cards[i]['label'].height()-20))
            self.app_cards[i]['label'].setAlignment(Qt.AlignCenter)
            
            self.app_cards[i]['label_2'] = QLabel("hello there this is my area, don't interfere")
            self.app_cards[i]['label_2'].setProperty("desktop_app_name", True)



            layout = QHBoxLayout(self.app_cards[i]['frame']) 
        
            layout.addStretch()
            layout.addWidget(self.app_cards[i]['label'])
            layout.addWidget(self.app_cards[i]['label_2'])
            layout.addStretch()
            layout.addStretch()
            layout.addStretch()
            layout.addStretch()
            layout.addStretch()
            layout.addWidget(self.app_cards[i]['toggleButton'])
            layout.addStretch()


            boxlayout.addWidget(self.app_cards[i]['frame'])

        self.vboxlayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")
        for i in range(10):
            self.app_cards[i]['toggleButton'].setText("OFF")


if __name__ == "__main__":
    collect.Collect_app_info()
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
