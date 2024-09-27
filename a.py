from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect  
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt  
  
class RoundShadow(QWidget):  
    def __init__(self, image_path, parent=None):  
        super(RoundShadow, self).__init__(parent)  
        self.border_width = 8  
        self.image_path = image_path  # 图片路径  
        self.pixmap = QPixmap(self.image_path)  # 加载图片  
        self.background_brush = QBrush(self.pixmap)  # 创建画刷  
  
        # 设置窗口透明背景  
        self.setAttribute(Qt.WA_TranslucentBackground)  
  
        # 设置阴影效果  
        shadow = QGraphicsDropShadowEffect(self)  
        shadow.setBlurRadius(20)  
        shadow.setOffset(0, 0)  
        shadow.setColor(QColor(0, 0, 0, 127))  
        self.setGraphicsEffect(shadow)  
  
        # 调整窗口大小以适应图片  
        self.resize(self.pixmap.size())  
  
    def paintEvent(self, event):  
        painter = QPainter(self)  
        painter.setRenderHint(QPainter.Antialiasing)  
  
        # 绘制圆角矩形并填充图片  
        radius = 16  
        rect = self.rect()  
        rect.adjust(radius, radius, -radius, -radius)  
        painter.setBrush(self.background_brush)  
        painter.setPen(Qt.NoPen)  # 使用无边框  
        painter.drawRoundedRect(rect, radius, radius)  
  
# 使用示例  
if __name__ == '__main__':  
    import sys  
    from PyQt5.QtWidgets import QApplication  
  
    app = QApplication(sys.argv)  
    window = RoundShadow(r'wish.ico')  # 替换为您的图片路径  
    window.show()  
    sys.exit(app.exec_())