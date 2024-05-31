import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QFrame, QLineEdit
from PyQt5.QtWidgets import  QLabel, QSizePolicy, QGraphicsDropShadowEffect, QHBoxLayout, QPushButton
from PyQt5.QtGui import QColor, QPixmap, QIcon
from PyQt5.QtCore import   Qt, QSize, QFileSystemWatcher
from utils import collect, action
from utils.ui_componenet import FolderBrowser, animeToggleButton, IconLineEdit
import json, os


# testing purpose



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setProperty("mainwidget", True)
        self.centralwidget.setObjectName("centralwidget")
        self.vboxlayout = QVBoxLayout(self.centralwidget)
        self.vboxlayout.setObjectName("vboxlayout") 
        self.frame_widgets = []
        self.app_lables = []
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
        self.USER, self.HOME = collect.get_current_user_info()

        with open("database/app_info.json", "r") as file:
            app_info = json.load(file)
        with open(f"database/{self.USER}-startup_onned.json", "r") as file:
            startup_apps = json.load(file)
        with open(f"database/{self.USER}-added_sh.json", 'r') as file:
            script_files = json.load(file)
        self.script_files = script_files

    
        # self.searchbar = IconLineEdit('database/icon/search-icon.svg', QSize(20, 20))
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search")
        # self.searchbar.addAction(QIcon("database/icon/search-icon.svg"), QLineEdit.LeadingPosition)
        self.searchbar.setProperty("searchbar",True)
        self.searchbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.searchbar.setFixedHeight(90)  # Set fixed height
        self.searchbar.setMaximumWidth(1000)
        self.searchbar.textChanged.connect(self.display_frame_update)
        self.boxlayout.addWidget(self.searchbar)



        self.script_card = {}
        self.script_card[0] = {}
        self.script_card[0]['frame'] =  QFrame()
        self.script_card[0]['frame'].setProperty("framecontainer", True)
        self.script_card[0]['frame'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.script_card[0]['frame'].setFixedHeight(100)  # Set fixed height
        self.script_card[0]['frame'].setMaximumWidth(1000)
        self.script_card[0]['frame'].setFrameShape(QFrame.StyledPanel)
        self.script_card[0]['fileDialog'] = FolderBrowser()

        layout = QHBoxLayout(self.script_card[0]['frame'])
        layout.addStretch()
        layout.addWidget(self.script_card[0]['fileDialog'])
        layout.addStretch()

        self.boxlayout.addWidget(self.script_card[0]['frame'])
        self.loadScriptCards()

        
        action.setattr_needEmpty0()
        self.watcher = QFileSystemWatcher()
        file_path = "database/needEmpty.txt"
        self.watcher.addPath(file_path)
        self.watcher.fileChanged.connect(self.insert_sh_frame)


        self.app_cards = {}
        added_item = self.add_Sartup_apps_first(startup_apps, app_info)

        for i in range(len(app_info)):
            i = str(i)
            if "icon_path" not in app_info[i]:
                continue
            if "NoDisplay" in app_info[i] and app_info[i]['NoDisplay']=='true':
                continue
            if i in added_item:
                continue
            self.app_cards[i] = {}
            self.app_cards[i]['frame'] = QFrame()
            self.app_cards[i]['frame'].setProperty("framecontainer", True)
            self.app_cards[i]['frame'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.app_cards[i]['frame'].setFixedHeight(100)  # Set fixed height
            self.app_cards[i]['frame'].setMaximumWidth(1000)
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

            self.app_lables.append(self.app_cards[i]['label_2'].text().lower())
            self.frame_widgets.append(self.app_cards[i]['frame'])

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


    def add_Sartup_apps_first(self, startup_apps, app_info):
        already_added_items = []
        for i in range(len(app_info)):
            i = str(i)
            if app_info[i]["file_name"] in startup_apps and startup_apps[app_info[i]["file_name"]]==True:
                self.app_cards[i] = {}
                self.app_cards[i]['frame'] = QFrame()
                self.app_cards[i]['frame'].setProperty("framecontainer", True)
                self.app_cards[i]['frame'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.app_cards[i]['frame'].setFixedHeight(100)  # Set fixed height
                self.app_cards[i]['frame'].setMaximumWidth(1000)
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
                
                self.app_lables.append(self.app_cards[i]['label_2'].text().lower())
                self.frame_widgets.append(self.app_cards[i]['frame'])

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


    def loadScriptCards(self):
        great = -1
        for i in self.script_card:
            if i>great:
                great = i
        i = great + 1
        for filename in self.script_files:
            self.script_card[i] = {}
            self.script_card[i]["filename"] = filename
            self.script_card_layout_setup(i)
            self.boxlayout.addWidget(self.script_card[i]['frame'])
            i+=1
    
    def Delete_card(self, index, filename=""):
        if filename:
            action.startup_delete_sh(filename)
        else:
            action.startup_delete_sh(self.script_card[index]["filename"])
        ind = self.frame_widgets.index(self.script_card[index]['frame'])
        self.frame_widgets.pop(ind)
        self.app_lables.pop(ind)
        self.script_card[index]['frame'].deleteLater()
        self.boxlayout.removeWidget(self.script_card[index]['frame'])
        del self.script_files[self.script_card[index]["filename"]] 

    def insert_sh_frame(self):
        great = -1
        for i in self.script_card:
            if i>great:
                great = i
        i = great + 1
        with open(f"database/{self.USER}-added_sh.json", 'r') as file:
            new_entry = json.load(file)
        for f in new_entry:
            if f not in self.script_files:
                self.script_card[i] = {}
                self.script_card[i]["filename"] = f
                self.script_card_layout_setup(i)
                self.boxlayout.insertWidget(2, self.script_card[i]['frame'])
                self.script_files[f] = False

    def script_card_layout_setup(self, i):
        self.script_card[i]['frame'] = QFrame()
        self.script_card[i]['frame'].setProperty("framecontainer", True)
        self.script_card[i]['frame'].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.script_card[i]['frame'].setFixedHeight(100)  # Set fixed height
        self.script_card[i]['frame'].setMaximumWidth(1000)
        self.script_card[i]['frame'].setFrameShape(QFrame.StyledPanel)
        self.script_card[i]['toggleButton'] = animeToggleButton(id=i, sh=True, filename=self.script_card[i]["filename"])
        self.script_card[i]['toggleButton'].setProperty("toggleButt", True)
        self.setToggleButtonState(self.script_card[i]['toggleButton'], self.script_card[i]["filename"], self.script_files)

        self.script_card[i]['DeleteButton'] = QPushButton()
        self.script_card[i]['DeleteButton'].setFixedHeight(30)
        self.script_card[i]['DeleteButton'].setFixedWidth(30)
        self.script_card[i]['DeleteButton'].setIcon(QIcon("database/icon/trash_bin.svg"))
        self.script_card[i]['DeleteButton'].setIconSize(QSize(30,30))
        self.script_card[i]['DeleteButton'].setStyleSheet("border-radius: 35px;\
                                background-color: rgb(40, 40, 40);")
        self.script_card[i]['DeleteButton'].clicked.connect(lambda _, index=i : self.Delete_card(index))

        self.script_card[i]['label'] = QLabel("TextLabel")
        self.script_card[i]['label'].setProperty("app_icon", True)
        self.script_card[i]['label'].setFixedHeight(80)
        self.script_card[i]['label'].setFixedWidth(80)
        self.script_card[i]['label'].setPixmap(QPixmap("database/icon/bash.png").scaled(self.script_card[i]['label'].width()-15, self.script_card[i]['label'].height()-15))
        self.script_card[i]['label'].setAlignment(Qt.AlignCenter)
        
        self.script_card[i]['label_2'] = QLabel(self.script_card[i]["filename"])
        self.script_card[i]['label_2'].setProperty("desktop_app_name", True)

        self.app_lables.append(self.script_card[i]['label_2'].text().lower())
        self.frame_widgets.append(self.script_card[i]['frame'])

        layout = QHBoxLayout(self.script_card[i]['frame']) 
        layout.addWidget(self.script_card[i]['label'])
        layout.addWidget(self.script_card[i]['label_2'])
        layout.addStretch()
        layout.addStretch()
        layout.addStretch()
        layout.addStretch()
        layout.addStretch()
        layout.addWidget(self.script_card[i]['DeleteButton'])
        layout.addWidget(self.script_card[i]['toggleButton'])


    def display_frame_update(self):
        text = self.searchbar.text().lower()
        for i in range(len(self.app_lables)):
            if text in self.app_lables[i]:
                wiz = self.frame_widgets.pop(i)
                self.boxlayout.removeWidget(wiz)
                self.boxlayout.insertWidget(2, wiz)
                self.frame_widgets.insert(0, wiz)
                label = self.app_lables.pop(i)
                self.app_lables.insert(0, label)

    def doNothing(self):
        pass

if __name__ == "__main__":
    collect.load_current_user_info()
    collect.Collect_app_info()
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    MainWindow.setWindowTitle("Linux startupApp Manager")
    MainWindow.setProperty("mainLinux", True)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    with open('stylesheet', 'r') as file:
        stylesheet = file.read()
    MainWindow.setStyleSheet(stylesheet)
    MainWindow.show()
    sys.exit(app.exec_())
