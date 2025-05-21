"""
祈愿 · 幸运观众：主窗口

Copyright © 2023-2025 XuangeAha(轩哥啊哈OvO)

"""

from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QGraphicsOpacityEffect, QMenu
from PyQt5.QtGui import QFont, QFontDatabase, QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
import time
import random
import pyperclip

from RoundShadow import RoundShadow
from MovableWindow import MovableWindow
from SettingsWindow import SettingsWindow
import MessageBox

from config import _ver_short, _ver, _ver_type, _iconpath, _base_numbers, _default_lang , _EVER_excluded_numbers, _morning_newspaper, _is_special_wish_on, _is_debug_on

class WishWindow(MovableWindow):
    def __init__(self, parent=None):
        super(WishWindow, self).__init__(parent)
        self.numbers = []
        self.guarantee_mode = 0
        self.is_in_guarantee = False
        self.is_information_shown = False
        self.is_avatar_shown = True
        self.history_all, self.history_last = [], []
        self.tie_list, self.separate_list, self.last_pick_tied = [], [], False

        try:  # 「自定义祈愿学号池」自定义祈愿学号解析加载
            with open('lucky.txt', 'r', encoding='utf-8') as file:
                get_content = [line.strip() for line in file][1]
                resolved_list = self.Resolver.resolve(get_content)
                if resolved_list in [[-1],[]]:
                    self.supportable_numbers = [_i for _i in _base_numbers if _i not in _EVER_excluded_numbers]
                    self.GUARANTEE = [8, 60]
                    if _default_lang == 0:
                        SettingsWindow.show_dialoguebox(self, f"「自定义祈愿学号池」中存在输入错误，请检查：\n\n        {get_content}\n\n  当前学号池及保底机制已重置为默认（学号1-41，8-60保底）。", lang=0, type=QMessageBox.Critical)
                    else:
                        SettingsWindow.show_dialoguebox(self, f"There are errors in the「Customed Lucky Number Pool」input, please check.\n\n        {get_content}\n\nThe current student number pool and guarantee mode have been reset to default (numbers 1-41, with 8-60 guarantee).", lang=1, type=QMessageBox.Critical)
                else:
                    if len(resolved_list) == 1:
                        if _default_lang == 0:
                            SettingsWindow.show_dialoguebox(self, f"「自定义祈愿学号池」中仅有一个学号： {resolved_list[0]}\n\n  这将导致祈愿的结果都为该学号。", lang=0)
                        else:
                            SettingsWindow.show_dialoguebox(self, f"There is only one student number in「Customed Lucky Number Pool」:  {resolved_list[0]}\n\n  This will result in all wishes being the same student number.", lang=1)
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
            f"Current Mechanism of Guarantee: \n  Each number is guaranteed to appear at least once within {self.GUARANTEE[1]} wishes.\n   The same number can appear at most once within any consecutive {self.GUARANTEE[0]} wishes.",
            "Current Mechanism of Guarantee:    Completely random with no guarantee"]
        self.round_shadow = RoundShadow(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        _global_font = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(r'.wish\fonts\HYWH-85w Heavy.ttf'))[0]  

        self.root_settings = SettingsWindow(self)
        self.main_layout = QVBoxLayout(self)

        self.header_layout = QHBoxLayout()  # 标题栏

        self.title = f'祈愿·幸运观众 {_ver_short}（{_ver_type}）{_ver}' if _ver_type != '正式版' else f'祈愿·幸运观众 {_ver_short}'  # 标题
        self.title_label = QLabel(self.title, self)
        self.title_label.setFont(QFont(_global_font, 11))

        self.information_button = QPushButton('∨祈愿详情∨', self)  # 祈愿详情按钮
        self.information_button.setFont(QFont(_global_font, 9))
        self.information_button.clicked.connect(self.toggle_information)
        self.set_widget_style(self.information_button, 'gray', 'white', 150, 26)

        self.newspaper = QLabel('', self)  # 动态信息报纸
        self.newspaper.setFont(QFont(_global_font, 11))

        self.history_button = QPushButton('', self)  # 历史记录按钮
        self.history_button.setIcon(QIcon(r'.wish\assets\icon\history.png'))
        self.history_button.clicked.connect(self.show_history)
        self.set_widget_style(self.history_button, 'gray', 'white', 30, 30)

        self.minimize_button = QPushButton('', self)  # 最小化按钮
        self.minimize_button.setIcon(QIcon(r'.wish\assets\icon\minimize.png'))
        self.minimize_button.clicked.connect(self.showMinimized)
        self.set_widget_style(self.minimize_button, 'gray', 'white', 30, 30)

        self.settings_button = QPushButton('', self)  # 设置按钮
        self.settings_button.setIcon(QIcon(r'.wish\assets\icon\settings.png'))
        self.settings_button.clicked.connect(self.root_settings.show)
        self.set_widget_style(self.settings_button, 'gray', 'white', 30, 30)

        self.close_button = QPushButton('', self)  # 关闭按钮
        self.close_button.setIcon(QIcon(r'.wish\assets\icon\close.png'))
        self.close_button.clicked.connect(self.close) 
        self.set_widget_style(self.close_button, 'red', 'white', 30, 30)
        
        for _widget in [self.title_label, self.information_button, 1, self.newspaper, 1, self.history_button, self.minimize_button, self.settings_button, self.close_button]:  # 标题栏布局
            try: self.header_layout.addWidget(_widget)
            except TypeError: self.header_layout.addStretch(_widget)

        self.information = QLabel(self.information_list_zh[0], self)  # 祈愿详情信息
        self.information.setFont(QFont(_global_font, 12))
        self.information.setAlignment(Qt.AlignCenter)
        self.information.setWordWrap(True)
        self.information.setVisible(False)

        self.bottom_layout = QHBoxLayout()  # 底部栏

        self.label_number_layout = QHBoxLayout()  # 头像+学号显示
        self.label_number_avatar = QLabel(self)  # 头像显示
        self.label_number_avatar.setFixedWidth(310)
        self.label_number_avatar.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_number_text = QLabel('', self)  # 学号显示
        self.label_number_text.setFont(QFont(_global_font, 19))
        self.label_number_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label_number_text.setFixedWidth(310)
        self.label_number_layout.addWidget(self.label_number_avatar)
        self.label_number_layout.addWidget(self.label_number_text)

        self.button_once = QPushButton('抽 1 次', self)  # 抽 1 次按钮
        self.button_once.setFont(QFont(_global_font, 13))
        self.button_once.clicked.connect(self.pick_once)
        self.button_once.setFixedSize(160, 60)

        self.button_ten = QPushButton('抽 10 次', self)  # 抽 10 次按钮
        self.button_ten.setFont(QFont(_global_font, 13))
        self.button_ten.clicked.connect(self.pick_ten)
        self.button_ten.setFixedSize(160, 60)

        self.bottom_layout.addLayout(self.label_number_layout)  # 底部栏布局
        self.bottom_layout.addWidget(self.button_once)
        self.bottom_layout.addWidget(self.button_ten)

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addWidget(self.information)
        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.setContentsMargins(30, 25, 30, 25)

        self.setContextMenuPolicy(Qt.CustomContextMenu)  # 右键菜单
        self.customContextMenuRequested.connect(self.context_menu)

        self.setWindowTitle("祈愿 · 幸运观众")
        self.setWindowIcon(QIcon(_iconpath))
        self.setGeometry(100, 100, 900, 600)

        self.root_settings.toggle_language(self.root_settings.LANGUAGE_INDEX)

        self.send_newspaper(_morning_newspaper, show_time=10000)  # 晨报

    @staticmethod
    def set_widget_style(widget, background_color:str, color:str, sizex:int, sizey:int):  # 元件格式包装
        widget.setFixedSize(sizex, sizey)
        widget.setStyleSheet(f"""
            QPushButton:hover {{
                border-radius: 5px;
                background-color: {background_color};
                color: {color}; }} """)

    ##############################################################################################################
    ############################################## 抽学号逻辑核心 #################################################
    ##############################################################################################################
    def get_lucky(self) -> int:  # 抽学号逻辑核心
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
                    if self.root_settings.LANGUAGE_INDEX == 0:
                        self.send_newspaper('保底生效中..')
                    else:
                        self.send_newspaper('Guarantee is activated..')
                else:
                    lucky_person = random.choice(self.supportable_numbers)
                if lucky_person not in self.last_some_picks: ######################### 8抽保底
                    break

                if lucky_person == 41 and self.pick_num < 4:
                    continue # 41号学号在4抽内不可抽到

            if _is_special_wish_on:
                if self.pick_num == 4:
                    lucky_person = 41 # 41号学号在5抽时必出

            self.last_some_picks.append(lucky_person)
            if lucky_person not in self.history_last: 
                self.history_last.append(lucky_person)
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
                if self.root_settings.LANGUAGE_INDEX == 0:
                    self.send_newspaper('「心之捆绑」生效中..')
                else:
                    self.send_newspaper('「The Tied」is activated..')
        else:
            self.last_pick_tied = False

        if self.last_pick in self.separate_list: ##################################「心之隔离」####################
            index = self.separate_list.index(self.last_pick)
            separate_person = self.separate_list[index+1] if index % 2 == 0 else self.separate_list[index-1]
            if lucky_person == separate_person:
                lucky_person = random.choice(self.supportable_numbers)
                if self.root_settings.LANGUAGE_INDEX == 0:
                    self.send_newspaper('「心之隔离」生效中..')
                else:
                    self.send_newspaper('「The Separated」is activated..')

        self.history_all.append(lucky_person)
        self.last_pick = lucky_person

        if _is_debug_on:
            print(f'''本次祈愿: {lucky_person} 距保底剩余抽数: {self.pick_num_rest} 最近小保底抽: {self.last_some_picks} 本轮保底已抽到: {self.history_last} 本轮保底未抽到: {self.lucky_rest}''')  # 调试信息
        
        return lucky_person
    ##############################################################################################################
    ##############################################################################################################
    ##############################################################################################################
    
    def pick_once(self):  # 抽 1 次
        if hasattr(self, 'update_label_timer') and self.update_label_timer.isActive(): # 避免10抽1抽连续抽取
            return
        
        lucky_one = self.get_lucky()  # 抽学号
        
        profile_photo_path = f'.wish/profilephoto/{lucky_one}.jpg'  # 头像处理
        
        if self.is_avatar_shown and QPixmap(profile_photo_path).isNull() is False:  # 显示头像且头像存在
            pixmap = QPixmap(profile_photo_path).scaled(55, 55, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_number_avatar.setFixedWidth(310)
            self.label_number_avatar.setPixmap(pixmap)
            self.label_number_text.setFixedWidth(310)
            self.label_number_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.label_number_text.setText(" "+str(lucky_one))
        else:  # 不显示头像或头像不存在
            self.label_number_avatar.setFixedWidth(0)
            self.label_number_avatar.clear()
            self.label_number_text.setFixedWidth(620)
            self.label_number_text.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.label_number_text.setText(str(lucky_one))

        self.adjustSize()
        self.adjustSize()

    def pick_ten(self):  # 抽 10 次
        self.label_number_avatar.setFixedWidth(0)
        self.label_number_avatar.clear()
        self.label_number_text.setFixedWidth(620)
        self.label_number_text.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.update_label_index = 0
        self.update_label_timer = QTimer(self)
        self.numbers = [self.get_lucky() for _ in range(10)]
        self.update_label_timer.timeout.connect(self.update_label)
        self.update_label_timer.start(50)

    def update_label(self):  # 学号显示动画
        if self.update_label_index < len(self.numbers):
            self.label_number_text.setText(' '.join(f'{num}' for num in self.numbers[:self.update_label_index + 1]))
            self.update_label_index += 1
            self.label_number_text.setFixedWidth(620+(len(self.label_number_text.text())-30)*20 if len(self.label_number_text.text()) > 30 else 620)  # 过长抽取结果显示适应
            self.adjustSize()
        else:
            self.update_label_timer.stop()

    def reset_guarantee(self):  # 重置保底
        self.history_last = []
        self.lucky_rest = self.supportable_numbers.copy()
        self.pick_num, self.pick_num_rest, self.is_in_guarantee = 0, self.GUARANTEE[1], False
        if self.root_settings.LANGUAGE_INDEX == 0:
            self.send_newspaper('保底已重置..')
        else:
            self.send_newspaper('Guarantee reset..')

    class Resolver:  # 「自定义祈愿学号池」学号解析器
        def resolve(input_str:str) -> list:
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

    def toggle_information(self):  # 信息显示及按钮文字切换
        visible = not self.information.isVisible()
        
        if self.root_settings.LANGUAGE_INDEX == 0:
            self.information_button.setText('∧祈愿详情∧' if visible else '∨祈愿详情∨')
        else:
            self.information_button.setText('∧Details∧' if visible else '∨Details∨')

        def _on_value_changed(value):  # 动画每一帧都调整窗口大小
            self.information.setMinimumHeight(value)
            self.adjustSize()

        def _on_anim_finished():  # 动画结束时隐藏information
            self.information.setVisible(False)

        self.anim = QPropertyAnimation(self.information, b"maximumHeight")  # 祈愿详情展开/收回动画
        self.anim.setDuration(300)

        if visible:  # 展开
            self.information.setFixedHeight(0)  # 显示information但初始高度为0
            self.information.setVisible(True)
            self.information.setFixedHeight(16777215)  # 获取完整展开时的高度
            full_height = self.information.sizeHint().height() + 20
            self.information.setFixedHeight(0)
            self.anim.setStartValue(0)
            self.anim.setEndValue(full_height)
        else:  # 收回
            self.anim.setStartValue(self.information.height())
            self.anim.setEndValue(0)
            self.anim.finished.connect(_on_anim_finished)
        
        self.anim.setEasingCurve(QEasingCurve.OutQuad)  # 使用缓出动画曲线
        self.anim.valueChanged.connect(_on_value_changed)
        self.anim.start()
        
    def send_newspaper(self, news:str, show_time:int=5000):  # 发报纸
        if news != self.newspaper.text():
            self.newspaper.setText(news)
            self.newspaper.setVisible(True)
            self.adjustSize()
            
            if hasattr(self, 'fade_timer') and self.fade_timer.isActive():
                self.fade_timer.stop()
            
            self.fade_timer = QTimer(self)
            self.fade_timer.setSingleShot(True)
            self.fade_timer.timeout.connect(self.fade_out_newspaper)
            self.fade_timer.start(show_time)  # 报纸显示时间

    def fade_out_newspaper(self):  # 渐隐报纸
        self.opacity_effect = QGraphicsOpacityEffect(self.newspaper)
        self.newspaper.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(500)  # 报纸淡出时间
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.hide_newspaper)
        self.animation.start()

    def hide_newspaper(self):  # 隐藏报纸
        self.newspaper.setVisible(False)
        self.newspaper.setGraphicsEffect(None)

    def show_history(self):  # 历史记录
        ticktime = time.asctime(time.localtime(time.time()))
        if self.root_settings.LANGUAGE_INDEX == 0:
            pyperclip.copy(f'{self.history_all}（祈愿记录导出于 {ticktime}）')
            MessageBox.show_messagebox(f"祈愿历史记录已复制到剪贴板。", duration=3)
            if len(self.history_all) < 500:
                SettingsWindow.show_dialoguebox(self, f"祈愿历史记录（{ticktime}）共 {len(self.history_all)} 次祈愿：\n\n{self.history_all}", lang=0, type=QMessageBox.Information)
            else:
                SettingsWindow.show_dialoguebox(self, f"祈愿历史记录（{ticktime}）共 {len(self.history_all)} 次祈愿，最近 500 次祈愿：\n\n...{self.history_all[-500:]}", lang=0, type=QMessageBox.Information)
        else:
            pyperclip.copy(f'{self.history_all}（Wish record exported at {ticktime}）')
            MessageBox.show_messagebox(f"Wish record copied to clipboard.", duration=3)
            if len(self.history_all) < 500:
                SettingsWindow.show_dialoguebox(self, f"Wish History ({ticktime}) Total {len(self.history_all)} wishes: \n\n{self.history_all}", lang=1, type=QMessageBox.Information)
            else:
                SettingsWindow.show_dialoguebox(self, f"Wish History ({ticktime}) Total {len(self.history_all)} wishes, recent 500 wishes: \n\n...{self.history_all[-500:]}", lang=1, type=QMessageBox.Information)

    def context_menu(self, pos):  # 右键菜单
        context_menu = QMenu(self)
        context_menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                padding: 8px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 3px 18px;
                margin: 1px 1px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: gray;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                margin: 4px 0;
            }
        """)
        
        context_menu_pick_once = context_menu.addAction("抽 1 次" if self.root_settings.LANGUAGE_INDEX == 0 else "Pick Once")
        context_menu_pick_once.triggered.connect(self.pick_once)

        context_menu_pick_ten = context_menu.addAction("抽 10 次" if self.root_settings.LANGUAGE_INDEX == 0 else "Pick Ten Times")
        context_menu_pick_ten.triggered.connect(self.pick_ten)

        context_menu.addSeparator()

        context_menu_open_settings_window = context_menu.addAction("设置" if self.root_settings.LANGUAGE_INDEX == 0 else "Settings")
        context_menu_open_settings_window.triggered.connect(self.root_settings.show)

        context_menu.exec_(self.mapToGlobal(pos))
