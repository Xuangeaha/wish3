"""
祈愿 · 幸运观众：主窗口

Copyright © 2023-2024 XuangeAha(轩哥啊哈OvO)

"""

from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer
import random

from RoundShadow import RoundShadow
from MovableWindow import MovableWindow
from SettingsWindow import SettingsWindow

from config import _short_ver, _ver, _vername, _global_font, _iconpath

class WishWindow(MovableWindow):
    def __init__(self, parent=None):
        super(WishWindow, self).__init__(parent)
        self.numbers = []
        self.guarantee_mode = 0
        self.is_in_guarantee = False
        self.is_information_shown = False
        self.history_all, self.history_last_60 = [], []
        self.tie_list, self.separate_list, self.last_pick_tied = [], [], False
        self.pick_num, self.pick_num_rest, self.last_pick, self.last_8_picks, self.lucky_rest = 0, 60, 0, [], list(range(1, 41))
        self.information_list = [
            "当前保底机制：  · 每60次祈愿内，所有学号必出至少一次。\n                                · 任意连续8次祈愿内，相同学号至多出一次。",
            "当前保底机制：  无保底全随机"]

        self.round_shadow = RoundShadow(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.root_settings = SettingsWindow(self)
        self.main_layout = QVBoxLayout(self)
        self.header_layout = QHBoxLayout()  # 标题栏

        self.title_label = QLabel(f'祈愿·幸运观众 {_short_ver}（{_vername}）{_ver}', self)
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
        self.settings_button.clicked.connect(self.root_settings.show)
        self.set_widget_style(self.settings_button, 'blue', 'white', 30, 30, '设置')

        self.close_button = QPushButton('', self)
        self.close_button.setIcon(QIcon(r'.wish\assets\icon\close.png'))
        self.close_button.clicked.connect(self.close) 
        self.set_widget_style(self.close_button, 'blue', 'white', 30, 30, '关闭')
        
        for _widget in [self.title_label, self.information_button, 1, self.minimize_button, self.settings_button, self.close_button]:  # 标题栏布局
            try: self.header_layout.addWidget(_widget)
            except TypeError: self.header_layout.addStretch(_widget)

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

        for _widget in [self.label_number, self.button_once, self.button_ten]:
            self.bottom_layout.addWidget(_widget)

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addWidget(self.information)
        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.setContentsMargins(30, 25, 30, 25)

        self.setWindowTitle("祈愿 · 幸运观众")
        self.setWindowIcon(QIcon(_iconpath))
        self.setGeometry(100, 100, 950, 60)

    def set_widget_style(self, widget, background_color, color, sizex, sizey, tooltip):  # 元件格式包装
        widget.setFixedSize(sizex, sizey)
        widget.setToolTip(tooltip)
        widget.setStyleSheet(f"""
            QPushButton:hover {{
                border-radius: 5px;
                background-color: {background_color};
                color: {color}; }} """)

    ##############################################################################################################
    ############################################## 抽学号逻辑核心 #################################################
    ##############################################################################################################
    def get_lucky(self):  
        """
        祈愿 · 幸运观众：抽学号逻辑核心

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
            lucky_person = random.randint(1, 40)

        if not self.last_pick_tied: ###############################################「心之捆绑」###################
            if self.last_pick in self.tie_list:
                index = self.tie_list.index(self.last_pick)
                lucky_person = self.tie_list[index+1] if index % 2 == 0 else self.tie_list[index-1]
                self.last_pick_tied = True
        else:
            self.last_pick_tied = False

        ###########################################################################「心之隔离」###################
        if self.last_pick in self.separate_list:
            index = self.separate_list.index(self.last_pick)
            separate_person = self.separate_list[index+1] if index % 2 == 0 else self.separate_list[index-1]
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
        self.label_number.setText(f'{self.get_lucky()}')

    def draw_ten(self):  # 抽 10 次
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
            