import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QFrame, QCheckBox
from PyQt5.QtWidgets import QRadioButton, QLabel, QSizePolicy, QGraphicsDropShadowEffect, QHBoxLayout
from PyQt5.QtGui import QColor, QPaintEvent, QPainter, QBrush, QPen, QPixmap
from PyQt5.QtCore import   QPoint, Qt, QRect
from utils import collect
from utils import action
import json


# testing purpose




class animeToggleButton(QCheckBox):
    def __init__(
            self,
            width=60,
            bgcolor='#777',
            circle_color='#DDD',
            active_color='#00d5ff',
            id = None
    ):
        QCheckBox.__init__(self)
        self.setFixedSize(width, 28)
        self.setCursor(Qt.PointingHandCursor)
        
        self._bgcolor= bgcolor
        self._circle_color = circle_color
        self._active_color = active_color
        self.id = id

        self.stateChanged.connect(lambda state : action.startup_on_off(self.id, self.isChecked()))
   
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
        MainWindow.resize(700, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setProperty("mainwidget", True)
        self.centralwidget.setObjectName("centralwidget")
        self.vboxlayout = QVBoxLayout(self.centralwidget)
        self.vboxlayout.setObjectName("vboxlayout") 

        self.boxlayout = QVBoxLayout()
        self.boxlayout.setContentsMargins(10, 10, 10, 50)
        self.boxlayout.setAlignment(Qt.AlignHCenter)
        self.scrollArea = QScrollArea()
        self.scrollArea.setProperty("mainscrollarea", True)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.boxlayout)
        self.scrollArea.setWidget(scroll_widget)


        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(3, 3)
        self.shadow.setColor(QColor(0, 0, 0, 50))


        with open("database/app_info.json", "r") as file:
            app_info = json.load(file)
        with open("database/startup_onned.json", "r") as file:
            startup_apps = json.load(file)

        self.script_card = {}
        self.script_card[0] = {}
        self.script_card[0]['frame'] =  QFrame()
        self.script_card[0]['frame'].setProperty("framecontainer", True)
        self.script_card[0]['frame'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.script_card[0]['frame'].setFixedHeight(100)  # Set fixed height
        self.script_card[0]['frame'].setMaximumWidth(800)
        self.script_card[0]['frame'].setFrameShape(QFrame.StyledPanel)
        self.boxlayout.addWidget(self.script_card[0]['frame'])


        self.app_cards = {}
        added_item = self.add_Sartup_apps_first(startup_apps, app_info)

        for i in app_info:
            if "icon_path" not in app_info[i]:
                continue
            if i in added_item:
                continue
            self.app_cards[i] = {}
            self.app_cards[i]['frame'] = QFrame()
            self.app_cards[i]['frame'].setProperty("framecontainer", True)
            self.app_cards[i]['frame'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.app_cards[i]['frame'].setFixedHeight(100)  # Set fixed height
            self.app_cards[i]['frame'].setMaximumWidth(800)
            self.app_cards[i]['frame'].setFrameShape(QFrame.StyledPanel)

            self.app_cards[i]['toggleButton'] = animeToggleButton(id=i)
            self.app_cards[i]['toggleButton'].setProperty("toggleButt", True)
            self.setToggleButtonState(self.app_cards[i]['toggleButton'], app_info[i]['file_name'], startup_apps)

            self.app_cards[i]['label'] = QLabel("TextLabel")
            self.app_cards[i]['label'].setProperty("app_icon", True)
            self.app_cards[i]['label'].setFixedHeight(80)
            self.app_cards[i]['label'].setFixedWidth(80)

            self.app_cards[i]['label'].setPixmap(QPixmap(app_info[i]['icon_path']).scaled(self.app_cards[i]['label'].width()-15, self.app_cards[i]['label'].height()-15))
            self.app_cards[i]['label'].setAlignment(Qt.AlignCenter)
            if "GenericName" in app_info[i] :
                name = app_info[i]['Name'] + ", "+ app_info[i]['GenericName']
                self.app_cards[i]['label_2'] = QLabel(name)
            else:
                self.app_cards[i]['label_2'] = QLabel(app_info[i]['Name'])
            self.app_cards[i]['label_2'].setProperty("desktop_app_name", True)

            layout = QHBoxLayout(self.app_cards[i]['frame']) 
            layout.addWidget(self.app_cards[i]['label'])
            layout.addWidget(self.app_cards[i]['label_2'])
            layout.addStretch()
            layout.addStretch()
            layout.addStretch()
            layout.addStretch()
            layout.addStretch()
            layout.addWidget(self.app_cards[i]['toggleButton'])

            self.boxlayout.addWidget(self.app_cards[i]['frame'])
        self.vboxlayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)



    def setToggleButtonState(self, button, file_name, startup_apps):
        if file_name in startup_apps and startup_apps[file_name]==True:
            button.blockSignals(True)
            button.setCheckState(Qt.Checked)
            button.blockSignals(False)
        if button.isChecked():
            print(f"{file_name}=True")
    


    def add_Sartup_apps_first(self, startup_apps, app_info):
        already_added_items = []
        for i in app_info:
            if app_info[i]["file_name"] in startup_apps and startup_apps[app_info[i]["file_name"]]==True:
                self.app_cards[i] = {}
                self.app_cards[i]['frame'] = QFrame()
                self.app_cards[i]['frame'].setProperty("framecontainer", True)
                self.app_cards[i]['frame'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.app_cards[i]['frame'].setFixedHeight(100)  # Set fixed height
                self.app_cards[i]['frame'].setMaximumWidth(800)
                self.app_cards[i]['frame'].setFrameShape(QFrame.StyledPanel)

                self.app_cards[i]['toggleButton'] = animeToggleButton(id=i)
                self.app_cards[i]['toggleButton'].setProperty("toggleButt", True)
                self.app_cards[i]['toggleButton'].blockSignals(True)
                self.app_cards[i]['toggleButton'].setCheckState(Qt.Checked)
                self.app_cards[i]['toggleButton'].blockSignals(False)

                self.app_cards[i]['label'] = QLabel("TextLabel")
                self.app_cards[i]['label'].setProperty("app_icon", True)
                self.app_cards[i]['label'].setFixedHeight(80)
                self.app_cards[i]['label'].setFixedWidth(80)

                self.app_cards[i]['label'].setPixmap(QPixmap(app_info[i]['icon_path']).scaled(self.app_cards[i]['label'].width()-15, self.app_cards[i]['label'].height()-15))
                self.app_cards[i]['label'].setAlignment(Qt.AlignCenter)
                if "GenericName" in app_info[i] :
                    name = app_info[i]['Name'] + ", "+ app_info[i]['GenericName']
                    self.app_cards[i]['label_2'] = QLabel(name)
                else:
                    self.app_cards[i]['label_2'] = QLabel(app_info[i]['Name'])
                self.app_cards[i]['label_2'].setProperty("desktop_app_name", True)

                layout = QHBoxLayout(self.app_cards[i]['frame']) 
                layout.addWidget(self.app_cards[i]['label'])
                layout.addWidget(self.app_cards[i]['label_2'])
                layout.addStretch()
                layout.addStretch()
                layout.addStretch()
                layout.addStretch()
                layout.addStretch()
                layout.addWidget(self.app_cards[i]['toggleButton'])

                self.boxlayout.addWidget(self.app_cards[i]['frame'])
                already_added_items.append(i)
        return already_added_items



if __name__ == "__main__":
    # collect.Collect_app_info()
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
