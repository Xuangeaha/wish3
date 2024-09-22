from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox, QMessageBox, QApplication, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QFont, QIcon, QPainter
from PyQt5.QtCore import QPoint, Qt, QTimer

class MovableWindow(QWidget):
    """
    可拖动鼠标窗口框架

    """
    def __init__(self, parent=None):
        super(MovableWindow, self).__init__(parent)
        self.dragging = False
        self.dragPosition = None
        self.setAttribute(Qt.WA_TranslucentBackground)

    def mousePressEvent(self, event):  # 按下鼠标动作绑定
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.dragPosition = event.globalPos()

    def mouseMoveEvent(self, event):  # 移动鼠标动作绑定
        if self.dragging:
            delta = QPoint(event.globalPos() - self.dragPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.dragPosition = event.globalPos()

    def mouseReleaseEvent(self, event):  # 松开鼠标动作绑定
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def resizeEvent(self, event):  # 动态放缩调整
        self.round_shadow.resize(self.size())