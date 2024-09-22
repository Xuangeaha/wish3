from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox, QMessageBox, QApplication, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QFont, QIcon, QPainter
from PyQt5.QtCore import QPoint, Qt, QTimer

from RoundShadow import RoundShadow
from MovableWindow import MovableWindow

from config import _global_font, _iconpath

class LogWindow(MovableWindow):
    """
    祈愿 · 幸运观众：更新说明窗口
    
    Copyright © 2024 XuangeAha(轩哥啊哈OvO)
    
    """
    def __init__(self, parent=None):
        super(LogWindow, self).__init__(parent)
        self.round_shadow = RoundShadow(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.log_layout = QVBoxLayout(self)

        self.log_header_layout = QHBoxLayout()  # 更新说明窗口：标题栏
        self.log_title_label = QLabel('更新说明', self)
        self.log_title_label.setFont(QFont(_global_font, 11))
        self.log_close_button = QPushButton('', self)
        self.log_close_button.setIcon(QIcon(r'.wish\assets\icon\close.png'))
        self.log_close_button.setFont(QFont(_global_font, 12))
        self.log_close_button.clicked.connect(self.close)
        self.log_close_button.setFixedSize(30, 30)
        self.log_close_button.setStyleSheet("""
            QPushButton:hover {
                border-radius: 5px;
                background-color: red;
                color: white; }""")
        self.log_header_layout.addWidget(self.log_title_label)
        self.log_header_layout.addStretch(1)
        self.log_header_layout.addWidget(self.log_close_button)

        self.log_table = QGridLayout()  # 更新说明窗口：更新说明表格

        with open('CHANGELOG.txt', 'r', encoding='utf-8') as file:  # 更新说明文档读取
            content_list = [line.strip() for line in file]

        for x in range(1, int(len(content_list)/3+1)):
            log_column1 = QLabel(content_list[x*3-3].split("    ")[0]+"    ", self)
            log_column1.setFont(QFont(_global_font, 12))
            log_column2 = QLabel(content_list[x*3-3].split("    ")[1], self)
            log_column2.setFont(QFont(_global_font, 12))
            log_column3 = QLabel(content_list[x*3-2]+"    ", self)
            log_column3.setFont(QFont(_global_font, 12))
            self.log_table.addWidget(log_column1, x, 1)
            self.log_table.addWidget(log_column3, x, 2)
            self.log_table.addWidget(log_column2, x, 3)

        self.log_table.setContentsMargins(35, 5, 35, 10)

        self.log_layout.addLayout(self.log_header_layout)  # 更新说明窗口布局
        self.log_layout.addLayout(self.log_table)
        self.log_layout.setContentsMargins(30, 25, 30, 25)

        self.setWindowTitle("祈愿 · 幸运观众 - 更新说明")
        self.setWindowIcon(QIcon(_iconpath))
        self.setGeometry(300, 300, 400, 400)