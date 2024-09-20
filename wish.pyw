"""
祈愿·幸运观众 3.0 (Wish3: Who's the Luckiest Dog?)

Copyright © 2023-2024 XuangeAha(轩哥啊哈OvO)
All rights reserved. | MIT License

"""

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox, QMessageBox, QApplication, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QFont, QIcon, QPainter
from PyQt5.QtCore import QPoint, Qt, QTimer
import re
import sys
import random
import webbrowser

_ver = '3.1-dev0951'
_global_font = '汉仪文黑-85w'

class RoundShadow(QWidget):
    """
    圆角阴影窗口框架
    
    Copyright © 2024 XuangeAha(轩哥啊哈OvO)

    """
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


class MovableWindow(QWidget):
    """
    可拖动鼠标窗口框架

    Copyright © 2024 XuangeAha(轩哥啊哈OvO)

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


class AboutWindow(MovableWindow):
    """
    祈愿 · 幸运观众 3.0：关于窗口
    
    Copyright © 2024 XuangeAha(轩哥啊哈OvO)
    
    """
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.round_shadow = RoundShadow(self)

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

        self.wish_title = QLabel('祈愿·幸运观众 3.0', self)  # 关于窗口：祈愿·幸运观众标题
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
        self.call_csdn = QPushButton('CSDN(轩哥啊哈OvO) ↗', self)
        self.call_csdn.setFont(QFont('等线', 10))
        self.call_github.clicked.connect(self.call_github_broser)
        self.call_csdn.clicked.connect(self.call_csdn_broser)

        self.about_layout.addLayout(self.about_header_layout)  # 关于窗口布局
        self.about_layout.addStretch(1)
        self.about_layout.addWidget(self.wish_icon)
        self.about_layout.addWidget(self.wish_title)
        self.about_layout.addWidget(self.wish_subtitle)
        self.about_layout.addStretch(1)
        self.about_layout.addWidget(self.wish_copyright)
        self.about_layout.addWidget(self.call_github)
        self.about_layout.addWidget(self.call_csdn)
        self.about_layout.setContentsMargins(30, 25, 30, 25)

        self.setGeometry(300, 300, 400, 400)

    def call_github_broser(self):  # 外链调用
        webbrowser.open('https://www.github.com/xuangeaha')

    def call_csdn_broser(self):
        webbrowser.open('https://xuangeaha.blog.csdn.net/')


class LogWindow(MovableWindow):
    """
    祈愿 · 幸运观众 3.0：更新说明窗口
    
    Copyright © 2024 XuangeAha(轩哥啊哈OvO)
    
    """
    def __init__(self, parent=None):
        super(LogWindow, self).__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.round_shadow = RoundShadow(self)

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

        self.log_table.setContentsMargins(35, 5, 35, 10)  # 更新说明窗口布局
        self.log_layout.addLayout(self.log_header_layout)
        self.log_layout.addLayout(self.log_table)
        self.log_layout.setContentsMargins(30, 25, 30, 25)

        self.setGeometry(300, 300, 400, 400)


class SettingsWindow(MovableWindow):
    """
    祈愿 · 幸运观众 3.0：设置窗口
    
    Copyright © 2024 XuangeAha(轩哥啊哈OvO)
    
    """
    def __init__(self, wish_window, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.root_log = LogWindow(self)
        self.root_about = AboutWindow(self)
        self.wish_window = wish_window
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.round_shadow = RoundShadow(self)

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
        self.theme_combo.addItem("默认")
        self.theme_combo.addItem("轴月")
        self.theme_combo.addItem("谢不开朗鸡罗")
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
        self.tie_lineedit.setToolTip("「心之捆绑」：强制使两学号在两次连续祈愿中依次抽出。通过该方式祈愿获得的学号不计入保底。示例：“5-32 23-24”")

        self.separate_label = QLabel('「心之隔离」：', self)  # 设置窗口：4 「心之隔离」
        self.separate_label.setFont(QFont(_global_font, 12))
        self.separate_lineedit = QLineEdit(self)
        self.separate_lineedit.setFixedWidth(180)
        self.separate_lineedit.setFont(QFont(_global_font, 12))
        self.separate_lineedit.setText(''.join([str(item) + '|' if index % 2 == 0 else str(item) + ' ' for index, item in enumerate(self.wish_window.separate_list)]))
        self.separate_lineedit.setToolTip("「心之隔离」：限制两学号不得在两次连续祈愿中依次抽出。为满足该机制而进行强制插入的学号不计入保底。示例：“5|32 23|24”")

        self.apply_tie_separate_button = QPushButton('应用', self)  # 设置窗口底栏
        self.apply_tie_separate_button.setFont(QFont(_global_font, 12))
        self.apply_tie_separate_button.setFixedWidth(80)
        self.apply_tie_separate_button.clicked.connect(self.apply_tie_separate)

        self.settings_main_layout.addWidget(self.theme_label, 0, 0)  # 设置窗口中心布局
        self.settings_main_layout.addWidget(self.theme_combo, 0, 1)
        self.settings_main_layout.addWidget(self.guarantee_label, 1, 0)
        self.settings_main_layout.addWidget(self.guarantee_combo, 1, 1)
        self.settings_main_layout.addWidget(self.tie_label, 3, 0)
        self.settings_main_layout.addWidget(self.tie_lineedit, 3, 1)
        self.settings_main_layout.addWidget(self.separate_label, 4, 0)
        self.settings_main_layout.addWidget(self.separate_lineedit, 4, 1)
        self.settings_main_layout.addWidget(self.apply_tie_separate_button, 5, 1)
        self.settings_main_layout.setContentsMargins(30, 0, 30, 0)

        self.settings_bottom_layout = QHBoxLayout()

        self.about_button = QPushButton('关于..', self)  # 设置窗口底栏
        self.about_button.setFont(QFont(_global_font, 10))
        self.about_button.clicked.connect(self.call_about_window)
        self.about_button.setFixedSize(150, 30)
        self.about_button.setToolTip('关于')

        self.log_button = QPushButton('更新说明..', self)
        self.log_button.setFont(QFont(_global_font, 10))
        self.log_button.clicked.connect(self.call_log_window)
        self.log_button.setFixedSize(150, 30)
        self.log_button.setToolTip('更新说明')

        self.settings_bottom_layout.addWidget(self.about_button)
        self.settings_bottom_layout.addWidget(self.log_button)

        self.settings_layout.addLayout(self.settings_header_layout)  # 设置窗口布局
        self.settings_layout.addStretch(10)
        self.settings_layout.addLayout(self.settings_main_layout)
        self.settings_layout.addStretch(10)
        self.settings_layout.addLayout(self.settings_bottom_layout)
        self.settings_layout.setContentsMargins(30, 25, 30, 25)
        
        self.setGeometry(100, 100, 320, 350)
        
    def apply_tie_separate(self):
        def show_messagebox(message, type):
            msg = QMessageBox()  
            msg.setIcon(type)  
            msg.setWindowTitle("祈愿 · 幸运观众")
            msg.setText(message)
            msg.exec_()  

        while True:
            try:
                new_tie_list = [int(item) for item in filter(None, re.split(r'[- ]+', self.tie_lineedit.text()))] 
            except ValueError:
                show_messagebox("「心之捆绑」存在错误输入，请检查。", QMessageBox.Critical); break
            if len(new_tie_list) % 2 != 0:
                show_messagebox("「心之捆绑」存在输入格式错误，请检查。", QMessageBox.Critical); break
            is_unsupported_number = False
            for items in new_tie_list:
                if not (1 <= items <= 40):
                    is_unsupported_number = True
            if is_unsupported_number:
                show_messagebox("「心之捆绑」存在不支持的学号，请检查。", QMessageBox.Critical); break

            try:
                new_separate_list = [int(item) for item in filter(None, re.split(r'[| ]+', self.separate_lineedit.text()))] 
            except ValueError:
                show_messagebox("「心之隔离」存在存在错误输入，请检查。", QMessageBox.Critical); break
            if len(new_separate_list) % 2 != 0:
                show_messagebox("「心之隔离」存在输入格式错误，请检查。", QMessageBox.Critical); break
            is_unsupported_number = False
            for items in new_separate_list:
                if not (1 <= items <= 40):
                    is_unsupported_number = True
            if is_unsupported_number:
                show_messagebox("「心之捆绑」存在不支持的学号，请检查。", QMessageBox.Critical); break
            
            self.wish_window.tie_list = new_tie_list
            self.wish_window.separate_list = new_separate_list
            show_messagebox("「心之隔离」与「心之捆绑」已更新。", QMessageBox.Information)
            print(self.wish_window.tie_list, self.wish_window.separate_list)
            break

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
        toggle_size = [60, 40]
        self.wish_window.guarantee_mode = index
        self.wish_window.information.setText(self.wish_window.information_list[index])
        self.wish_window.information.setFixedSize(950, toggle_size[index])
        self.wish_window.adjustSize()

    def call_about_window(self):  # 关于窗口/更新说明窗口调取
        self.root_about.show()

    def call_log_window(self):
        self.root_log.show()


class WishWindow(MovableWindow):
    """
    祈愿 · 幸运观众 3.0：主窗口
    
    Copyright © 2024 XuangeAha(轩哥啊哈OvO)
    
    """
    def __init__(self, parent=None):
        super(WishWindow, self).__init__(parent)
        self.numbers = []
        self.guarantee_mode = 0
        self.history_all = []
        self.history_last_60 = []
        self.pick_num = 0
        self.pick_num_rest = 60
        self.last_pick = 0
        self.last_8_picks = []
        self.last_pick_tied = False
        self.is_information_shown = False
        self.is_in_guarantee: bool = False
        self.lucky_rest = list(range(1, 41))
        self.information_list = [
            "当前保底机制：  · 每60次祈愿内，所有学号必出至少一次。\n                                · 任意连续8次祈愿内，相同学号至多出一次。",
            "当前保底机制：  无保底全随机"]

        self.tie_list = []
        self.separate_list = []
        self.root_settings = SettingsWindow(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.round_shadow = RoundShadow(self)

        self.main_layout = QVBoxLayout(self)

        self.header_layout = QHBoxLayout()  # 标题栏

        self.title_label = QLabel('祈愿·幸运观众 3.1（早期开发）'+_ver, self)
        self.title_label.setFont(QFont(_global_font, 11))

        self.information_button = QPushButton('∨祈愿详情∨', self)
        self.information_button.setFont(QFont(_global_font, 10))
        self.information_button.clicked.connect(self.toggle_information)
        self.set_widget_style(self.information_button, 'gray', 'black', 150, 26, '祈愿详情')

        self.minimize_button = QPushButton('', self)
        self.minimize_button.setIcon(QIcon(r'.wish\assets\icon\minimize.png'))
        self.minimize_button.clicked.connect(self.showMinimized)
        self.set_widget_style(self.minimize_button, 'blue', 'white', 30, 30, '最小化')

        self.settings_button = QPushButton('', self)
        self.settings_button.setIcon(QIcon(r'.wish\assets\icon\settings.png'))
        self.settings_button.clicked.connect(self.call_settings_window)
        self.set_widget_style(self.settings_button, 'blue', 'white', 30, 30, '设置')

        self.close_button = QPushButton('', self)
        self.close_button.setIcon(QIcon(r'.wish\assets\icon\close.png'))
        self.close_button.clicked.connect(self.close) 
        self.set_widget_style(self.close_button, 'blue', 'white', 30, 30, '关闭')

        self.header_layout.addWidget(self.title_label)  # 标题栏布局
        self.header_layout.addWidget(self.information_button)
        self.header_layout.addStretch(1)
        self.header_layout.addWidget(self.minimize_button)
        self.header_layout.addWidget(self.settings_button)
        self.header_layout.addWidget(self.close_button)

        self.information = QLabel(self.information_list[0], self)  # 信息
        self.information.setFont(QFont(_global_font, 14))
        self.information.setAlignment(Qt.AlignCenter)
        self.information.setFixedSize(950, 60)
        self.information.setVisible(False)

        self.bottom_layout = QHBoxLayout()  # 底部栏

        self.label_number = QLabel('', self)
        self.label_number.setFont(QFont(_global_font, 19))
        self.label_number.setAlignment(Qt.AlignCenter)
        self.label_number.setFixedWidth(650)

        self.button_once = QPushButton('抽 1 次', self)
        self.button_once.setFont(QFont(_global_font, 14))
        self.button_once.clicked.connect(self.draw_once)
        self.button_once.setFixedSize(150, 60)

        self.button_ten = QPushButton('抽 10 次', self)
        self.button_ten.setFont(QFont(_global_font, 14))
        self.button_ten.clicked.connect(self.draw_ten)
        self.button_ten.setFixedSize(150, 60)

        self.bottom_layout.addWidget(self.label_number)
        self.bottom_layout.addWidget(self.button_once)
        self.bottom_layout.addWidget(self.button_ten)

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addWidget(self.information)
        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.setContentsMargins(30, 25, 30, 25)

        self.setWindowTitle("祈愿 · 幸运观众 3.0")
        self.setWindowIcon(QIcon(r'.wish\assets\wish\wish.png'))
        self.setGeometry(100, 100, 950, 60)

    def set_widget_style(self, widget, background_color, color, sizex, sizey, tooltip):  # 元件格式包装
        widget.setFixedSize(sizex, sizey)
        widget.setToolTip(tooltip)
        widget.setStyleSheet(f"""
            QPushButton:hover {{
                border-radius: 5px;
                background-color: {background_color};
                color: {color}; }} """)

    def call_settings_window(self):
        self.root_settings.show()

    ##############################################################################################################
    ############################################## 抽学号逻辑核心 #################################################
    ##############################################################################################################
    def get_lucky(self):  
        """
        祈愿 · 幸运观众：抽学号逻辑核心
        
        Copyright © 2023-2024 XuangeAha(轩哥啊哈OvO)

        """
        if self.guarantee_mode == 0: ############################################## 8-60保底模式 ###############
            if self.pick_num_rest == 0:
                self.reset_guarantee()
            if len(self.last_8_picks) > 7:
                self.last_8_picks.remove(self.last_8_picks[0])
            self.is_in_guarantee = len(self.lucky_rest) >= self.pick_num_rest ##### 60抽保底
            while True:
                if self.is_in_guarantee:
                    lucky_person = random.choice(self.lucky_rest)
                else:
                    lucky_person = random.randint(1, 40)
                if lucky_person not in self.last_8_picks: ######################### 8抽保底
                    break
            self.last_8_picks.append(lucky_person)
            if lucky_person not in self.history_last_60: 
                self.history_last_60.append(lucky_person)
                self.lucky_rest.remove(lucky_person)
            self.pick_num += 1
            self.pick_num_rest -= 1
        else: ##################################################################### 无保底模式 ##################
            self.reset_guarantee()
            lucky_person = random.randint(1, 40)

        if not self.last_pick_tied: ###############################################「心之捆绑」###################
            if self.last_pick in self.tie_list:
                index = self.tie_list.index(self.last_pick)
                if index % 2 == 0:
                    lucky_person = self.tie_list[index+1]
                else:
                    lucky_person = self.tie_list[index-1]
                self.last_pick_tied = True
        else:
            self.last_pick_tied = False

        ###########################################################################「心之隔离」###################
        if self.last_pick in self.separate_list:
            index = self.separate_list.index(self.last_pick)
            if index % 2 == 0:
                separate_person = self.separate_list[index+1]
            else:
                separate_person = self.separate_list[index-1]
            if lucky_person == separate_person:
                lucky_person = random.randint(1, 40)

        self.history_all.append(lucky_person)
        self.last_pick = lucky_person
        return lucky_person
    ##############################################################################################################
    ##############################################################################################################
    ##############################################################################################################

    def reset_guarantee(self):  # 重置保底
        self.history_last_60 = []
        self.lucky_rest = list(range(1, 41))
        self.pick_num, self.pick_num_rest, self.is_in_guarantee = 0, 60, False

    def toggle_information(self):  # 信息显示及按钮文字切换
        visible = not self.information.isVisible()
        self.information.setVisible(visible)
        self.information_button.setText('∧祈愿详情∧' if visible else '∨祈愿详情∨')
        self.adjustSize()

    def draw_once(self):  # 抽 1 次
        self.clear_label()
        self.label_number.setText(f'{self.get_lucky()}')

    def draw_ten(self):  # 抽 10 次
        self.clear_label()
        self.update_label_index = 0
        self.update_label_timer = QTimer(self)
        self.numbers = [self.get_lucky() for _ in range(10)]
        self.update_label_timer.timeout.connect(self.update_label)
        self.update_label_timer.start(50)

    def update_label(self):  # 学号显示动画
        if self.update_label_index < len(self.numbers):
            self.label_number.setText(' '.join(f'{num}' for num in self.numbers[:self.update_label_index + 1]))
            self.update_label_index += 1
        else:
            self.update_label_timer.stop()

    def clear_label(self):  # 清除学号
        self.label_number.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    root = WishWindow()
    root.show()
    app.exec_()
