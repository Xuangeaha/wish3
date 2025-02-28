"""
祈愿 · 幸运观众：主窗口

Copyright © 2023-2025 XuangeAha(轩哥啊哈OvO)

"""

from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtCore import Qt, QTimer
import random

from RoundShadow import RoundShadow
from MovableWindow import MovableWindow
from SettingsWindow import SettingsWindow

from config import _short_ver, _ver, _vername, _iconpath, _base_numbers, _default_lang , _EVER_excluded_numbers

class WishWindow(MovableWindow):
    def __init__(self, parent=None):
        super(WishWindow, self).__init__(parent)
        self.numbers = []
        self.guarantee_mode = 0
        self.is_in_guarantee = False
        self.is_information_shown = False
        self.history_all, self.history_last_60 = [], []
        self.tie_list, self.separate_list, self.last_pick_tied = [], [], False

        try:  # 「自定义祈愿学号池」自定义祈愿学号解析加载
            with open('lucky.txt', 'r', encoding='utf-8') as file:
                get_content = [line.strip() for line in file][1]
                resolved_list = self.Resolver.resolve(get_content)
                if resolved_list in [[-1],[]]:
                    self.supportable_numbers = [_i for _i in _base_numbers if _i not in _EVER_excluded_numbers]
                    self.GUARANTEE = [8, 60]
                    if _default_lang == 0:
                        SettingsWindow.show_messagebox(self, f"「自定义祈愿学号池」中存在输入错误，请检查：\n\n        {get_content}\n\n  当前学号池及保底机制已重置为默认（学号1-40，8-60保底）。", lang=0, type=QMessageBox.Critical)
                    else:
                        SettingsWindow.show_messagebox(self, f"There are errors in the「Customed Lucky Number Pool」input, please check.\n\n        {get_content}\n\nThe current student number pool and guarantee mode have been reset to default (numbers 1-40, with 8-60 guarantee).", lang=1, type=QMessageBox.Critical)
                else:
                    if len(resolved_list) == 1:
                        if _default_lang == 0:
                            SettingsWindow.show_messagebox(self, f"「自定义祈愿学号池」中仅有一个学号： {resolved_list[0]}\n\n  这将导致祈愿的结果都为该学号。", lang=0)
                        else:
                            SettingsWindow.show_messagebox(self, f"There is only one student number in「Customed Lucky Number Pool」:  {resolved_list[0]}\n\n  This will result in all wishes being the same student number.", lang=1)
                    self.supportable_numbers = resolved_list
                    length = len(self.supportable_numbers)
                    self.GUARANTEE = [int(length/5 + 1) if length < 20 else 8, (int(length*1.5) // 10 + 1) * 10]
        except (FileNotFoundError, IndexError):
            self.supportable_numbers = [_i for _i in _base_numbers if _i not in _EVER_excluded_numbers]
            self.GUARANTEE = [8, 60]

        self.pick_num, self.pick_num_rest, self.last_pick, self.last_some_picks, self.lucky_rest = 0, self.GUARANTEE[1], 0, [], self.supportable_numbers.copy()
        self.information_list_zh = [
            f"当前保底机制：  · 每{self.GUARANTEE[1]}次祈愿内，所有学号必出至少一次。\n                                · 任意连续{self.GUARANTEE[0]}次祈愿内，相同学号至多出一次。",
            "当前保底机制：  无保底全随机"]
        self.information_list_en = [
            f"Current Mechanism of Guarantee: \n  Each student number is guaranteed to appear at least once within {self.GUARANTEE[1]} wishes.\n   The same student number can appear at most once within any consecutive {self.GUARANTEE[0]} wishes.",
            "Current Mechanism of Guarantee:    Completely random with no guarantee"]
        self.round_shadow = RoundShadow(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        _global_font = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(r'.wish\fonts\HYWH-85w Heavy.ttf'))[0]  

        self.root_settings = SettingsWindow(self)
        self.main_layout = QVBoxLayout(self)
        self.header_layout = QHBoxLayout()

        title = f'祈愿·幸运观众 {_short_ver}（{_vername}）{_ver}' if _vername != '正式版' else f'祈愿·幸运观众 {_short_ver}'  # 标题栏
        self.title_label = QLabel(title, self)
        self.title_label.setFont(QFont(_global_font, 11))

        self.information_button = QPushButton('∨祈愿详情∨', self)
        self.information_button.setFont(QFont(_global_font, 9))
        self.information_button.clicked.connect(self.toggle_information)
        self.set_widget_style(self.information_button, 'gray', 'white', 150, 26)

        self.minimize_button = QPushButton('', self)
        self.minimize_button.setIcon(QIcon(r'.wish\assets\icon\minimize.png'))
        self.minimize_button.clicked.connect(self.showMinimized)
        self.set_widget_style(self.minimize_button, 'blue', 'white', 30, 30)

        self.settings_button = QPushButton('', self)
        self.settings_button.setIcon(QIcon(r'.wish\assets\icon\settings.png'))
        self.settings_button.clicked.connect(self.root_settings.show)
        self.set_widget_style(self.settings_button, 'blue', 'white', 30, 30)

        self.close_button = QPushButton('', self)
        self.close_button.setIcon(QIcon(r'.wish\assets\icon\close.png'))
        self.close_button.clicked.connect(self.close) 
        self.set_widget_style(self.close_button, 'red', 'white', 30, 30)
        
        for _widget in [self.title_label, self.information_button, 1, self.minimize_button, self.settings_button, self.close_button]:  # 标题栏布局
            try: self.header_layout.addWidget(_widget)
            except TypeError: self.header_layout.addStretch(_widget)

        self.information = QLabel(self.information_list_zh[0], self)  # 信息
        self.information.setFont(QFont(_global_font, 12))
        self.information.setAlignment(Qt.AlignCenter)
        self.information.setFixedSize(1000, 100)
        self.information.setVisible(False)

        self.bottom_layout = QHBoxLayout()  # 底部栏

        self.label_number = QLabel('', self)
        self.label_number.setFont(QFont(_global_font, 19))
        self.label_number.setAlignment(Qt.AlignCenter)
        self.label_number.setFixedWidth(650)

        self.button_once = QPushButton('抽 1 次', self)
        self.button_once.setFont(QFont(_global_font, 13))
        self.button_once.clicked.connect(self.draw_once)
        self.button_once.setFixedSize(160, 60)

        self.button_ten = QPushButton('抽 10 次', self)
        self.button_ten.setFont(QFont(_global_font, 13))
        self.button_ten.clicked.connect(self.draw_ten)
        self.button_ten.setFixedSize(160, 60)

        for _widget in [self.label_number, self.button_once, self.button_ten]:
            self.bottom_layout.addWidget(_widget)

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addWidget(self.information)
        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.setContentsMargins(30, 25, 30, 25)

        self.setWindowTitle("祈愿 · 幸运观众")
        self.setWindowIcon(QIcon(_iconpath))
        self.setGeometry(100, 100, 950, 60)

        self.root_settings.toggle_language(self.root_settings.LANGUAGE_INDEX)

    def set_widget_style(self, widget, background_color, color, sizex, sizey):  # 元件格式包装
        widget.setFixedSize(sizex, sizey)
        widget.setStyleSheet(f"""
            QPushButton:hover {{
                border-radius: 5px;
                background-color: {background_color};
                color: {color}; }} """)
        
    class Resolver:
        def resolve(input_str):
            result = []
            exclude_set = set()
            parts = input_str.split()
            try:
                for part in parts:
                    if part.startswith('-'):
                        exclude_set.update(map(int, part[1:].split('-')))
                    elif part.startswith('+'):
                        result.extend(map(int, part[1:].split('-')))
                    else:
                        start, end = map(int, part.split('-'))
                        result.extend(range(start, end + 1))
            except ValueError:
                result = [-1]
            result = list(set([num for num in result if num not in exclude_set]))
            return sorted(result)

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
            if len(self.last_some_picks) > self.GUARANTEE[0]:
                self.last_some_picks.remove(self.last_some_picks[0])
            self.is_in_guarantee = len(self.lucky_rest) >= self.pick_num_rest ####### 60抽保底
            while True:
                if len(self.supportable_numbers) == 1:
                    lucky_person = self.supportable_numbers[0]
                    break
                if self.is_in_guarantee:
                    lucky_person = random.choice(self.lucky_rest)
                else:
                    lucky_person = random.choice(self.supportable_numbers)
                if lucky_person not in self.last_some_picks: ######################### 8抽保底
                    break
            self.last_some_picks.append(lucky_person)
            if lucky_person not in self.history_last_60: 
                self.history_last_60.append(lucky_person)
                self.lucky_rest.remove(lucky_person)
            self.pick_num += 1
            self.pick_num_rest -= 1
        else: ##################################################################### 无保底模式 ##################
            lucky_person = random.choice(self.supportable_numbers)

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
                lucky_person = random.choice(self.supportable_numbers)

        self.history_all.append(lucky_person)
        self.last_pick = lucky_person
        return lucky_person
    ##############################################################################################################
    ##############################################################################################################
    ##############################################################################################################

    def reset_guarantee(self):  # 重置保底
        self.history_last_60 = []
        self.lucky_rest = self.supportable_numbers.copy()
        self.pick_num, self.pick_num_rest, self.is_in_guarantee = 0, 60, False

    def toggle_information(self):  # 信息显示及按钮文字切换
        visible = not self.information.isVisible()
        self.information.setVisible(visible)
        if self.root_settings.LANGUAGE_INDEX == 0:
            self.information_button.setText('∧祈愿详情∧' if visible else '∨祈愿详情∨')
        else:
            self.information_button.setText('∧Details∧' if visible else '∨Details∨')
        self.adjustSize()
    
    def draw_once(self):  # 抽 1 次
        self.label_number.setText(f'{self.get_lucky()}')
        self.label_number.setFixedWidth(650+(len(self.label_number.text())-30)*20 if len(self.label_number.text()) > 30 else 650)  # 过长抽取结果显示适应
        self.adjustSize()
        self.adjustSize()  # CPU算力限制 需再次调整

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
            self.label_number.setFixedWidth(650+(len(self.label_number.text())-30)*20 if len(self.label_number.text()) > 30 else 650)  # 过长抽取结果显示适应
            self.adjustSize()
        else:
            self.update_label_timer.stop()
