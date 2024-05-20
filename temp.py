import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QFrame, QLabel, QHBoxLayout
import sip

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.box = QVBoxLayout()
        self.setLayout(self.box)

        self.frame = {}
        button1 = QPushButton('Button 1')
        button1.clicked.connect(self.addFrame)

        self.box.addWidget(button1)
        

        # Remove the widget at index 1

        self.show()
    def addFrame(self):
        great = 0
        for i in self.frame:
            if i> great:
                great = i 
        i = great+1
        self.frame[i] = {}
        self.frame[i]['frame'] = QFrame()
        self.frame[i]['frame'].setFixedHeight(100)
        self.frame[i]['frame'].setFixedWidth(300)
        self.frame[i]['lable'] = QLabel(f"label {i}")
        self.frame[i]['delete'] = QPushButton(f"delete{i}")
        self.frame[i]['delete'].clicked.connect(lambda _, index=i: self.delete_frame(index))

        layout = QHBoxLayout()
        self.frame[i]['frame'].setLayout(layout)
        layout.addWidget(self.frame[i]['lable'])
        layout.addWidget(self.frame[i]['delete'])
        self.box.addWidget(self.frame[i]['frame'])
        print(f"frame added at index {i}")

    def delete_frame(self, index):
        print("index at delete_frame",index)
        # sip.delete(self.frame[index]['frame'])
        self.frame[index]['frame'].deleteLater()
        self.box.removeWidget(self.frame[index]['frame'])
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())