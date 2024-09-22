from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox, QMessageBox, QApplication, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QFont, QIcon, QPainter
from PyQt5.QtCore import QPoint, Qt, QTimer

from RoundShadow import RoundShadow
from MovableWindow import MovableWindow
from LogWindow import LogWindow
from AboutWindow import AboutWindow

import re

from config import _global_font, _iconpath

class SettingsWindow(MovableWindow):
    """
    祈愿 · 幸运观众：设置窗口
    
    """
    def __init__(self, wish_window, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.root_log = LogWindow(self)
        self.root_about = AboutWindow(self)
        self.wish_window = wish_window

        self.round_shadow = RoundShadow(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.settings_layout = QVBoxLayout(self)

        self.settings_header_layout = QHBoxLayout()  # 设置窗口：标题栏
        self.settings_title_label = QLabel('设置', self)
        self.settings_title_label.setFont(QFont(_global_font, 11))
        self.settings_close_button = QPushButton('', self)
        self.settings_close_button.setIcon(QIcon(r'.wish\assets\icon\close.png'))
        self.settings_close_button.setFont(QFont(_global_font, 12))
        self.settings_close_button.clicked.connect(self.close)
        self.settings_close_button.setFixedSize(30, 30)
        self.settings_close_button.setStyleSheet("""
            QPushButton:hover {
                border-radius: 5px;
                background-color: red;
                color: white; }""")
        self.settings_header_layout.addWidget(self.settings_title_label)
        self.settings_header_layout.addStretch(1)
        self.settings_header_layout.addWidget(self.settings_close_button)

        self.settings_main_layout = QGridLayout()

        self.theme_label = QLabel('主题配色：', self)  # 设置窗口：1 主题配色设置
        self.theme_label.setFont(QFont(_global_font, 12))
        self.theme_combo = QComboBox(self)
        self.theme_combo.setFont(QFont(_global_font, 12))
        for _item in ["默认", "轴月", "谢不开朗鸡罗"]:
            self.theme_combo.addItem(_item)
        self.theme_combo.currentIndexChanged.connect(self.toggle_theme)

        self.guarantee_label = QLabel('保底机制：', self)  # 设置窗口：2 保底机制
        self.guarantee_label.setFont(QFont(_global_font, 12))
        self.guarantee_combo = QComboBox(self)
        self.guarantee_combo.setFont(QFont(_global_font, 12))
        self.guarantee_combo.addItem("8-60保底")
        self.guarantee_combo.addItem("无保底")
        self.guarantee_combo.currentIndexChanged.connect(self.toggle_guarantee)

        self.tie_label = QLabel('「心之捆绑」：', self)  # 设置窗口：3 「心之捆绑」
        self.tie_label.setFont(QFont(_global_font, 12))
        self.tie_lineedit = QLineEdit(self)
        self.tie_lineedit.setFixedWidth(180)
        self.tie_lineedit.setFont(QFont(_global_font, 12))
        self.tie_lineedit.setText(''.join([str(item) + '-' if index % 2 == 0 else str(item) + ' ' for index, item in enumerate(self.wish_window.tie_list)]))
        self.tie_lineedit.setToolTip("强制使两学号在两次连续祈愿中依次抽出。通过该方式祈愿获得的学号不计入保底。示例：“5-32 23-24”")

        self.separate_label = QLabel('「心之隔离」：', self)  # 设置窗口：4 「心之隔离」
        self.separate_label.setFont(QFont(_global_font, 12))
        self.separate_lineedit = QLineEdit(self)
        self.separate_lineedit.setFixedWidth(180)
        self.separate_lineedit.setFont(QFont(_global_font, 12))
        self.separate_lineedit.setText(''.join([str(item) + '|' if index % 2 == 0 else str(item) + ' ' for index, item in enumerate(self.wish_window.separate_list)]))
        self.separate_lineedit.setToolTip("限制两学号不得在两次连续祈愿中依次抽出。为满足该机制而进行强制插入的学号不计入保底。示例：“5|32 23|24”")

        self.apply_tie_separate_button = QPushButton('应用', self)  # 设置窗口底栏
        self.apply_tie_separate_button.setFont(QFont(_global_font, 12))
        self.apply_tie_separate_button.setFixedWidth(80)
        self.apply_tie_separate_button.clicked.connect(self.apply_tie_separate)

        for _widget in [[self.theme_label, 0, 0], [self.theme_combo, 0, 1],  # 设置窗口中心布局
                        [self.guarantee_label, 1, 0], [self.guarantee_combo, 1, 1], 
                        [self.tie_label, 3, 0], [self.tie_lineedit, 3, 1],
                        [self.separate_label, 4, 0], [self.separate_lineedit, 4, 1], 
                        [self.apply_tie_separate_button, 5, 1]]:
            self.settings_main_layout.addWidget(_widget[0], _widget[1], _widget[2])

        self.settings_main_layout.setContentsMargins(30, 0, 30, 0)

        self.settings_bottom_layout = QHBoxLayout()

        self.about_button = QPushButton('关于..', self)  # 设置窗口底栏
        self.about_button.setFont(QFont(_global_font, 10))
        self.about_button.clicked.connect(self.root_about.show)
        self.about_button.setFixedSize(150, 30)
        self.about_button.setToolTip('关于')

        self.log_button = QPushButton('更新说明..', self)
        self.log_button.setFont(QFont(_global_font, 10))
        self.log_button.clicked.connect(self.root_log.show)
        self.log_button.setFixedSize(150, 30)
        self.log_button.setToolTip('更新说明')

        self.settings_bottom_layout.addWidget(self.about_button)
        self.settings_bottom_layout.addWidget(self.log_button)

        for _layout in [self.settings_header_layout, 10, self.settings_main_layout, 10, self.settings_bottom_layout]:  # 设置窗口布局
            try: self.settings_layout.addLayout(_layout)
            except TypeError: self.settings_layout.addStretch(_layout)
        self.settings_layout.setContentsMargins(30, 25, 30, 25)
        
        self.setWindowTitle("祈愿 · 幸运观众 - 设置")
        self.setWindowIcon(QIcon(_iconpath))
        self.setGeometry(100, 100, 320, 350)
 
    def toggle_theme(self, index):  # 1 主题配色切换
        if index == 1:
            color = QColor(0, 165, 0)
            stylesheet = "QWidget {background-color: #00a500; color: white}"
        elif index == 2:
            color = QColor(255, 184, 198)
            stylesheet = "QWidget {background-color: #ffb8c6; color: white}"
        else:
            color = Qt.white
            stylesheet = "QWidget {background-color: white; color: black}"
        self.wish_window.round_shadow.set_background_color(color)
        self.wish_window.setStyleSheet(stylesheet)

    def toggle_guarantee(self, index):  # 2 保底机制切换
        self.wish_window.reset_guarantee()
        self.wish_window.guarantee_mode = index
        self.wish_window.information.setText(self.wish_window.information_list[index])
        self.wish_window.information.setFixedSize(950, [60, 40][index])
        self.wish_window.adjustSize()
   
    def apply_tie_separate(self):  # 3 / 4「心之捆绑」与「心之隔离」应用 
        def show_messagebox(message, type):
            msg = QMessageBox()  
            msg.setIcon(type)  
            msg.setWindowTitle("祈愿 · 幸运观众")
            msg.setText(message)
            msg.exec_() 

        def check_list(lineedit, message_prefix): 
            try:  
                new_list = [int(item) for item in filter(None, re.split(r'[-| ]+', lineedit.text()))]  
            except ValueError:  
                show_messagebox(f"「{message_prefix}」存在错误输入，请检查。", QMessageBox.Critical); return None  
            if len(new_list) % 2 != 0:  
                show_messagebox(f"「{message_prefix}」存在输入格式错误，请检查。", QMessageBox.Critical); return None  
            is_unsupported_number = False  
            for number in new_list:  
                if not (1 <= number <= 40):  
                    is_unsupported_number = True  
            if is_unsupported_number:  
                show_messagebox(f"「{message_prefix}」存在不支持的学号，请检查。", QMessageBox.Warning); return None  
            return new_list
            
        while True:  
            new_tie_list = check_list(self.tie_lineedit, "心之捆绑")  
            new_separate_list = check_list(self.separate_lineedit, "心之隔离") 
            if new_tie_list is None or new_separate_list is None: break  
            self.wish_window.tie_list, self.wish_window.separate_list = new_tie_list, new_separate_list
            show_messagebox("「心之隔离」与「心之捆绑」已更新。", QMessageBox.Information)
            break
