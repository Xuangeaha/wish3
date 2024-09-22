"""
圆角阴影窗口框架

Copyright © 2024 XuangeAha(轩哥啊哈OvO)

"""

from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt

class RoundShadow(QWidget):
    def __init__(self, parent=None):
        super(RoundShadow, self).__init__(parent)
        self.border_width = 8
        self.background_color = QColor(Qt.white)
        self.setAttribute(Qt.WA_TranslucentBackground)

        shadow = QGraphicsDropShadowEffect(self)  # 底窗口阴影
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 127))
        self.setGraphicsEffect(shadow)

    def set_background_color(self, color):  # 底窗口背景颜色
        self.background_color = color
        self.update()

    def paintEvent(self, event):  # 绘制窗口
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.background_color)
        painter.setPen(Qt.transparent)

        radius, rect = 16, self.rect()
        rect.adjust(radius, radius, -radius, -radius)
        painter.drawRoundedRect(rect, radius, radius)