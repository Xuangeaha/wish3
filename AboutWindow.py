from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox, QMessageBox, QApplication, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QFont, QIcon, QPainter
from PyQt5.QtCore import QPoint, Qt, QTimer

import webbrowser
from RoundShadow import RoundShadow
from MovableWindow import MovableWindow


from config import _short_ver, _ver, _global_font, _iconpath

class AboutWindow(MovableWindow):
    """
    祈愿 · 幸运观众：关于窗口
    
    """
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.round_shadow = RoundShadow(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.about_layout = QVBoxLayout(self)

        self.about_header_layout = QHBoxLayout()  # 关于窗口标题栏
        self.about_title_label = QLabel('关于 祈愿·幸运观众', self)
        self.about_title_label.setFont(QFont(_global_font, 11))
        self.about_close_button = QPushButton('', self)
        self.about_close_button.setIcon(QIcon(r'.wish\assets\icon\close.png'))
        self.about_close_button.setFont(QFont(_global_font, 12))
        self.about_close_button.clicked.connect(self.close)
        self.about_close_button.setFixedSize(30, 30)
        self.about_close_button.setStyleSheet("""
            QPushButton:hover {
                border-radius: 5px;
                background-color: red;
                color: white; }""")
        self.about_header_layout.addWidget(self.about_title_label)
        self.about_header_layout.addStretch(1)
        self.about_header_layout.addWidget(self.about_close_button)

        self.wish_icon = QLabel(self)  # 关于窗口：祈愿·幸运观众图标
        self.wish_icon.setPixmap(QIcon(r'.wish\assets\wish\wish.png').pixmap(100, 100))
        self.wish_icon.setAlignment(Qt.AlignCenter)

        self.wish_title = QLabel('祈愿·幸运观众 '+_short_ver, self)  # 关于窗口：祈愿·幸运观众标题
        self.wish_title.setFont(QFont(_global_font, 18))
        self.wish_title.setAlignment(Qt.AlignCenter)
        self.wish_subtitle = QLabel(_ver, self)
        self.wish_subtitle.setFont(QFont(_global_font, 12))
        self.wish_subtitle.setAlignment(Qt.AlignCenter)
        self.wish_copyright = QLabel('Copyright © 2023-2024 XuangeAha(轩哥啊哈OvO), \nAll rights reserved. | MIT License', self)
        self.wish_copyright.setFont(QFont('Arial', 10))
        self.wish_copyright.setAlignment(Qt.AlignCenter)

        self.call_github = QPushButton('Github(Xuangeaha) ↗', self)  # 关于窗口：外链按钮
        self.call_github.setFont(QFont('等线', 10))
        self.call_wishsite = QPushButton('祈愿·幸运观众 官方网站 ↗', self)
        self.call_wishsite.setFont(QFont('等线', 10))
        self.call_github.clicked.connect(self.call_github_broser)
        self.call_wishsite.clicked.connect(self.call_wishsite_broser)
        
        self.about_layout.addLayout(self.about_header_layout)  # 关于窗口布局
        for _widget in [1, self.wish_icon, self.wish_title, self.wish_subtitle, 1, self.wish_copyright, self.call_github, self.call_wishsite]:
            try: self.about_layout.addWidget(_widget)
            except TypeError: self.about_layout.addStretch(_widget)
        self.about_layout.setContentsMargins(30, 25, 30, 25)

        self.setWindowTitle("祈愿 · 幸运观众 - 关于")
        self.setWindowIcon(QIcon(_iconpath))
        self.setGeometry(300, 300, 400, 400)

    def call_github_broser(self): webbrowser.open('https://www.github.com/xuangeaha')  # 外链调用
    def call_wishsite_broser(self): webbrowser.open('https://xuangeaha.github.io/wishsite')