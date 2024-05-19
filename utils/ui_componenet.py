from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QFileDialog, QCheckBox
from PyQt5.QtCore import   QPoint, Qt, QRect
from PyQt5.QtGui import QPainter, QColor
from utils import action



class FolderBrowser(QDialog):
    def __init__(self, object, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Browse Folder")

        self.button = QPushButton("Browse")
        self.button.clicked.connect(self.browse_folder)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def browse_folder(self):
        # options = QFileDialog.Options()
        file_filter = "Shell scripts (*.sh);;All files (*)"
        filename, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_filter)
        if filename:
            print("Selected file:", filename)





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
