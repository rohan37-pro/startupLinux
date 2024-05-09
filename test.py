# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QFrame

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         # Create a layout to hold the frames
#         layout = QVBoxLayout()

#         # Create a scroll area
#         scroll_area = QScrollArea()
#         scroll_area.setWidgetResizable(True)  # Allow scroll area to resize widget

#         # Create a widget to contain the frames
#         scroll_widget = QWidget()
#         scroll_widget.setLayout(layout)
#         scroll_area.setWidget(scroll_widget)

#         # Add frames to the layout
#         for i in range(1):
#             frame = QFrame()
#             frame.setFixedSize(200, 200)
#             frame.setStyleSheet("background-color: #CCCCCC;")
#             layout.addWidget(frame)

#         # Set main window layout
#         main_layout = QVBoxLayout(self)
#         main_layout.addWidget(scroll_area)

#         self.setWindowTitle('Scroll Area Example')
#         self.setGeometry(100, 100, 300, 400)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())






import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QFrame, QRadioButton, QLabel, QSizePolicy, QGraphicsDropShadowEffect, QHBoxLayout
from PyQt5.QtCore import Qt

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vboxlayout = QVBoxLayout(self.centralwidget)
        self.vboxlayout.setObjectName("vboxlayout")

        boxlayout = QVBoxLayout()
        boxlayout.setContentsMargins(10, 10, 10, 50)
        boxlayout.setAlignment(Qt.AlignHCenter)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        scroll_widget = QWidget()
        scroll_widget.setLayout(boxlayout)
        self.scrollArea.setWidget(scroll_widget)
        shadow = QGraphicsDropShadowEffect()
        self.app_cards = {}
        for i in range(10):
            self.app_cards[i] = {}
            self.app_cards[i]['frame'] = QFrame()
            self.app_cards[i]['frame'].setContentsMargins(0, 5, 0, 5)
            self.app_cards[i]['frame'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.app_cards[i]['frame'].setFixedHeight(100)  # Set fixed height
            self.app_cards[i]['frame'].setMaximumWidth(800)
            self.app_cards[i]['frame'].setFrameShape(QFrame.StyledPanel)
            self.app_cards[i]['frame'].setFrameShadow(QFrame.Raised)
            # self.app_cards[i]['frame'].setStyleSheet(" background-color: white; border-radius: 5px; \
            #                                            border: 1px solid #bfbfbf; ")
    
            self.app_cards[i]['radioButton'] = QRadioButton()
            self.app_cards[i]['label'] = QLabel("TextLabel")
            self.app_cards[i]['label_2'] = QLabel("TextLabel")

            boxlayout.addWidget(self.app_cards[i]['frame'])

            layout = QHBoxLayout(self.app_cards[i]['frame'])
            layout.addStretch()
            layout.addWidget(self.app_cards[i]['label'])
            layout.addWidget(self.app_cards[i]['label_2'])
            layout.addStretch()
            layout.addStretch()
            layout.addStretch()
            layout.addStretch()
            layout.addStretch()
            layout.addStretch()
            layout.addWidget(self.app_cards[i]['radioButton'])
            layout.addStretch()



        self.vboxlayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")
        for i in range(1):
            self.app_cards[i]['radioButton'].setText("RadioButton")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
