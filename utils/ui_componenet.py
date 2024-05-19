from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QFileDialog, QCheckBox, QFrame
from PyQt5.QtWidgets import QSizePolicy, QLabel, QHBoxLayout
from PyQt5.QtCore import   QPoint, Qt, QRect, QSize
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap
from utils import action
import json, os



class FolderBrowser(QDialog):
    def __init__(self,  parent=None):
        super().__init__(parent)

        self.setWindowTitle("Browse Folder")

        self.button = QPushButton()
        self.button.setFixedHeight(70)
        self.button.setFixedWidth(70)
        self.button.setIcon(QIcon("database/icon/plus-circle-dotted-white.svg"))
        self.button.setIconSize(QSize(50,50))
        self.button.setStyleSheet("border: 2px solid rgb(35, 35, 35); \
                                  border-radius: 35px;\
                                  background-color: rgb(40, 40, 40);")
        self.button.clicked.connect(self.browse_folder)
        self.setStyleSheet("background-color: rgb(55, 55, 55);")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def browse_folder(self):
        # options = QFileDialog.Options()
        file_filter = "Shell scripts (*.sh);;All files (*)"
        filename, _ = QFileDialog.getOpenFileName(self, "Select File", os.path.expanduser("~"), file_filter)
        with open("database/added_sh.json", 'r') as file:
            added_sh = json.load(file)
        if filename=="" or filename in added_sh:
            return
        added_sh[f"{filename}"] = False
        with open("database/added_sh.json", 'w') as file:
            added_sh = json.dump(added_sh, file, indent=4)
        
        num = action.get_needEmptyNumber()
        os.rename(f"database/needEmpty.{num}.txt", f"database/needEmpty.{num+1}.txt")



class animeToggleButton(QCheckBox):
    def __init__(
            self,
            width=60,
            bgcolor='#777',
            circle_color='#DDD',
            active_color='#00d5ff',
            id = None,
            sh=False,
            filename = ""
    ):
        QCheckBox.__init__(self)
        self.setFixedSize(width, 28)
        self.setCursor(Qt.PointingHandCursor)
        
        self._bgcolor= bgcolor
        self._circle_color = circle_color
        self._active_color = active_color
        self.id = id
        self.sh = sh
        self.filename = filename

        if self.sh==False:
            self.stateChanged.connect(lambda state : action.startup_on_off(self.id, self.isChecked()))
        if self.sh==True and self.filename!="":
            self.stateChanged.connect(lambda state : action.startup_on_off_sh(self.filename, self.isChecked()))
   
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
