"""
祈愿 · 幸运观众：更新说明窗口

Copyright © 2024 XuangeAha(轩哥啊哈OvO)

"""

from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QFont, QFontDatabase, QIcon, QPixmap
from PyQt5.QtCore import Qt

from RoundShadow import RoundShadow
from MovableWindow import MovableWindow

from config import _iconpath, _default_lang

class ProfilephotoUpdateWindow(MovableWindow):
    def __init__(self, parent=None):
        super(ProfilephotoUpdateWindow, self).__init__(parent)
        self.round_shadow = RoundShadow(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        _global_font = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(r'.wish\fonts\HYWH-85w Heavy.ttf'))[0]  

        self.pfpu_layout = QVBoxLayout(self)

        self.pfpu_header_layout = QHBoxLayout()  # 更新说明窗口：标题栏
        title_label = '祈愿 · 幸运观众头像自动更新提示' if _default_lang == 0 else 'Profilephoto Update Prompt'
        self.pfpu_title_label = QLabel(title_label, self)
        self.pfpu_title_label.setFont(QFont(_global_font, 11))
        self.pfpu_close_button = QPushButton('', self)
        self.pfpu_close_button.setIcon(QIcon(r'.wish\assets\icon\close.png'))
        self.pfpu_close_button.setFont(QFont(_global_font, 12))
        self.pfpu_close_button.clicked.connect(self.close)
        self.pfpu_close_button.setFixedSize(30, 30)
        self.pfpu_close_button.setStyleSheet("""
            QPushButton:hover {
                border-radius: 5px;
                background-color: red;
                color: white; }""")
        self.pfpu_header_layout.addWidget(self.pfpu_title_label)
        self.pfpu_header_layout.addStretch(1)
        self.pfpu_header_layout.addWidget(self.pfpu_close_button)

        self.pfpu_table = QGridLayout()  # 更新说明窗口：更新说明表格

        update_info_label = QLabel("    以下学号及命名空间对应头像已自动更新：\n", self)
        update_info_label.setFont(QFont(_global_font, 13))
        self.pfpu_table.addWidget(update_info_label, 0, 0, 1, 3)

        updates = [
            {"id": "8", "namespace": "@student.global.8"}
        ]

        for row, update in enumerate(updates, start=1):
            label = QLabel(f"{update['id']} ({update['namespace']})", self)
            label.setFont(QFont(_global_font, 13))  # 设置字体和字号
            label.setContentsMargins(30, 0, 0, 0)
            old_photo = QLabel(self)
            old_photo.setPixmap(QPixmap(f".wish\\profilephoto\\{update['id']}#old.jpg").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            old_photo.setContentsMargins(60, 0, 0, 0)
            arrow_label = QLabel("→", self)
            arrow_label.setFont(QFont(_global_font, 30))  # 设置箭头字体和字号
            arrow_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            new_photo = QLabel(self)
            new_photo.setPixmap(QPixmap(f".wish\\profilephoto\\{update['id']}.jpg").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            self.pfpu_table.addWidget(label, row * 2 - 1, 0, 1, 4)  # 添加文字标签，占据整行
            self.pfpu_table.addWidget(old_photo, row * 2, 0)  # 添加旧头像
            self.pfpu_table.addWidget(arrow_label, row * 2, 1)  # 添加箭头
            self.pfpu_table.addWidget(new_photo, row * 2, 2)  # 添加新头像

        new_info_label = QLabel("\n\n★3.4.4版本起，以下命名空间将加入常驻学号池：\n", self)
        new_info_label.setFont(QFont(_global_font, 13))
        self.pfpu_table.addWidget(new_info_label, row * 2 + 1, 0, 1, 3)

        new_updates = [
            {"id": "41", "namespace": "@undefined(141) → @student.global.41"},
        ]

        for row, update in enumerate(new_updates, start=row * 2 + 2):
            newlabel = QLabel(f"★{update['id']} ({update['namespace']})", self)
            newlabel.setFont(QFont(_global_font, 13))
            newlabel.setContentsMargins(30, 0, 0, 0)
            photo = QLabel(self)
            photo.setPixmap(QPixmap(f".wish\\profilephoto\\{update['id']}.jpg").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            photo.setContentsMargins(60, 0, 0, 0)

            self.pfpu_table.addWidget(newlabel, row * 2 - 1, 0, 1, 4)  # 添加文字标签，占据整行
            self.pfpu_table.addWidget(photo, row * 2, 0)  # 添加头像

        self.pfpu_table.setContentsMargins(20, 10, 30, 30)
        self.pfpu_layout.addLayout(self.pfpu_header_layout)  # 更新说明窗口布局
        self.pfpu_layout.addLayout(self.pfpu_table)
        self.pfpu_layout.setContentsMargins(30, 25, 30, 25)

        self.setWindowTitle("祈愿 · 幸运观众头像自动更新提示")
        self.setWindowIcon(QIcon(_iconpath))
        self.setGeometry(250, 250, 440, 250)
