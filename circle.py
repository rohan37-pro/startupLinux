import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor


#################################################################
############ oval and cirle paintings ###########################
#####################################################3
# class MyWidget(QWidget):
#     def __init__(self):
#         super().__init__()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setPen(QColor(255, 0, 0))  # Set pen color to red
#         painter.setBrush(QColor(0, 0, 255))  # Set brush color to blue

#         # Draw an ellipse (oval)
#         painter.drawEllipse(50, 50, 200, 100)

#         # Draw a circle
#         painter.drawEllipse(300, 50, 100, 100)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     widget = MyWidget()
#     widget.setGeometry(100, 100, 500, 200)  # Set widget position and size
#     widget.setWindowTitle('Ovals and Circles')
#     widget.show()
#     sys.exit(app.exec_())



######################################################################
####################### toggle button ###############################
#####################################################################
import sys
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import QTimer, QRect, Qt
from PyQt5.QtGui import QPainter, QColor

class AnimatedToggleButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setChecked(False)
        self.animationTimer = QTimer(self)
        self.animationTimer.timeout.connect(self.animate)
        self.animationStep = 0
        self.animationDuration = 200  # in milliseconds
        self.animationTotalSteps = 10
        self.animationTimer.setInterval(self.animationDuration // self.animationTotalSteps)

    def animate(self):
        self.animationStep += 1
        if self.animationStep > self.animationTotalSteps:
            self.animationTimer.stop()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.isChecked():
            # Background color when toggled on
            background_color = QColor(0, 255, 0)
        else:
            # Background color when toggled off
            background_color = QColor(255, 0, 0)

        painter.setBrush(background_color)

        # Calculate oval dimensions based on animation step
        diameter = self.height()
        x = (self.width() - diameter) * self.animationStep / self.animationTotalSteps
        oval_rect = QRect(x, 0, diameter, diameter)

        # Draw oval shape
        painter.drawEllipse(oval_rect)

    def toggle(self):
        if self.isChecked():
            self.animationStep = self.animationTotalSteps
            self.animationTimer.start()
        else:
            self.animationStep = 0
            self.animationTimer.start()
        self.setChecked(not self.isChecked())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    toggle_button = AnimatedToggleButton()
    toggle_button.setGeometry(100, 100, 100, 50)  # Set button position and size
    toggle_button.setText("Toggle")
    toggle_button.show()
    sys.exit(app.exec_())
