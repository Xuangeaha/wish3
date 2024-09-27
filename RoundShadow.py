"""
圆角阴影窗口框架

Copyright © 2024 XuangeAha(轩哥啊哈OvO)

"""

from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect  
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor    
from PyQt5.QtCore import Qt  

class RoundShadow(QWidget):
    def __init__(self, parent=None):
        super(RoundShadow, self).__init__(parent)
        self.border_width = 8
        self.pixmap = QPixmap('')  # 加载图片  
        self.background_brush = QBrush(self.pixmap)  # 创建画刷 
        self.background_colour = QColor(Qt.white)
        self.setAttribute(Qt.WA_TranslucentBackground) 
        self.toggle_colour_picture = 0

        shadow = QGraphicsDropShadowEffect(self)  # 底窗口阴影
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 127))
        self.setGraphicsEffect(shadow)

    def set_background(self, colour=None, picture=None):  # 底窗口背景颜色
        if colour != None:
            self.background_colour = colour
            self.toggle_colour_picture = 0
        if picture != None:
            self.background_brush = QBrush(QPixmap(picture))
            self.toggle_colour_picture = 1
        self.update()

    def paintEvent(self, event):  # 绘制窗口
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.toggle_colour_picture == 0:
            painter.setBrush(self.background_colour) 
        elif self.toggle_colour_picture == 1:
            painter.setBrush(self.background_brush) 
        painter.setPen(Qt.transparent)  

        radius, rect = 16, self.rect()
        rect.adjust(radius, radius, -radius, -radius)
        painter.drawRoundedRect(rect, radius, radius)
        