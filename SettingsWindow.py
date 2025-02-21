"""
祈愿 · 幸运观众：设置窗口

Copyright © 2024-2025 XuangeAha(轩哥啊哈OvO)

"""

from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox, QMessageBox, QFileDialog, QCheckBox
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QIcon
from PyQt5.QtCore import Qt
import re

from RoundShadow import RoundShadow
from MovableWindow import MovableWindow
from LogWindow import LogWindow
from AboutWindow import AboutWindow

from config import _short_ver, _ver, _vername, _iconpath
from i18n import STATIC_STRINGS

class SettingsWindow(MovableWindow):
    def __init__(self, wish_window, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.root_log = LogWindow(self)
        self.root_about = AboutWindow(self)
        self.wish_window = wish_window

        self.round_shadow = RoundShadow(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        _global_font = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(r'.wish\fonts\HYWH-85w Heavy.ttf'))[0] 

        self.LANGUAGE_INDEX = 0
        self.lang_text = STATIC_STRINGS[str(self.LANGUAGE_INDEX)]

        self.settings_layout = QVBoxLayout(self)

        self.settings_header_layout = QHBoxLayout()  # 设置窗口：标题栏
        self.settings_title_label = QLabel('设置', self)
        self.settings_title_label.setFont(QFont(_global_font, 11))
        self.settings_close_button = QPushButton('', self)
        self.settings_close_button.setIcon(QIcon(r'.wish\assets\icon\close.png'))
        self.settings_close_button.setFont(QFont(_global_font, 12))
        self.settings_close_button.clicked.connect(self.close)
        self.settings_close_button.setFixedSize(30, 30)
        self.settings_close_button.setStyleSheet("QPushButton:hover {border-radius: 5px; background-color: red; color: white; }")
        self.settings_header_layout.addWidget(self.settings_title_label)
        self.settings_header_layout.addStretch(1)
        self.settings_header_layout.addWidget(self.settings_close_button)

        self.settings_main_layout = QGridLayout()

        self.languages_label = QLabel('语言/Languages：', self)  # 设置窗口：1 语言
        self.languages_label.setFont(QFont(_global_font, 12))
        self.languages_combo = QComboBox(self)
        self.languages_combo.setFont(QFont(_global_font, 12))
        for _item in ["中文", "English"]:
            self.languages_combo.addItem(_item)
        self.languages_combo.setCurrentIndex(self.LANGUAGE_INDEX)
        self.languages_combo.currentIndexChanged.connect(self.toggle_language)

        self.theme_label = QLabel('主题配色：', self)  # 设置窗口：2 主题配色设置
        self.theme_label.setFont(QFont(_global_font, 12))
        self.theme_combo = QComboBox(self)
        self.theme_combo.setFont(QFont(_global_font, 12))
        self.example_theme_list_zh = ["默认", "轴月", "谢不开朗鸡罗", "（自定义图片）"]
        self.example_theme_list_en = ["Default", "AxisMoon", "Shaybuklangiro", "(Customed Image)"]
        for _item in self.example_theme_list_zh:
            self.theme_combo.addItem(_item)
        self.theme_combo.currentIndexChanged.connect(self.toggle_theme)

        self.guarantee_label = QLabel('保底机制：', self)  # 设置窗口：3 保底机制
        self.guarantee_label.setFont(QFont(_global_font, 12))
        self.guarantee_combo = QComboBox(self)
        self.guarantee_combo.setFont(QFont(_global_font, 12))
        self.guarantee_item_name_zh = "8-60保底" if wish_window.GUARANTEE == [8,60] else f"自适应保底（当前{wish_window.GUARANTEE[0]}-{wish_window.GUARANTEE[1]}）"
        self.guarantee_item_name_en = "8-60 Guarantee" if wish_window.GUARANTEE == [8,60] else f"Auto Adaptive Guarantee (Currently {wish_window.GUARANTEE[0]}-{wish_window.GUARANTEE[1]})"
        self.guarantee_combo.addItem(self.guarantee_item_name_zh)
        self.guarantee_combo.addItem("无保底")
        self.guarantee_combo.currentIndexChanged.connect(self.toggle_guarantee)

        self.tie_label = QLabel('「心之捆绑」：', self)  # 设置窗口：4.1 「心之捆绑」
        self.tie_label.setFont(QFont(_global_font, 12))
        self.tie_lineedit = QLineEdit(self)
        self.tie_lineedit.setFont(QFont(_global_font, 12))
        self.tie_lineedit.setText(''.join([str(item) + '-' if index % 2 == 0 else str(item) + ' ' for index, item in enumerate(self.wish_window.tie_list)]))

        self.separate_label = QLabel('「心之隔离」：', self)  # 设置窗口：4.2 「心之隔离」
        self.separate_label.setFont(QFont(_global_font, 12))
        self.separate_lineedit = QLineEdit(self)
        self.separate_lineedit.setFont(QFont(_global_font, 12))
        self.separate_lineedit.setText(''.join([str(item) + '|' if index % 2 == 0 else str(item) + ' ' for index, item in enumerate(self.wish_window.separate_list)]))

        self.apply_tie_separate_button = QPushButton('应用', self)
        self.apply_tie_separate_button.setFont(QFont(_global_font, 12))
        self.apply_tie_separate_button.setFixedWidth(100)
        self.apply_tie_separate_button.clicked.connect(self.apply_tie_separate)

        for _widget in [[self.languages_label, 0, 0], [self.languages_combo, 0, 1],  # 设置窗口中心布局
                        [self.theme_label, 1, 0], [self.theme_combo, 1, 1], 
                        [self.guarantee_label, 2, 0], [self.guarantee_combo, 2, 1], 
                        [self.tie_label, 4, 0], [self.tie_lineedit, 4, 1],
                        [self.separate_label, 5, 0], [self.separate_lineedit, 5, 1], 
                        [self.apply_tie_separate_button, 6, 1]]:
            self.settings_main_layout.addWidget(_widget[0], _widget[1], _widget[2])

        self.settings_main_layout.setContentsMargins(30, 0, 30, 0)

        self.settings_bottom_layout = QHBoxLayout()
        
        self.onfront_label = QLabel('窗口始终置顶：', self)  # 窗口置顶设置
        self.onfront_label.setFont(QFont(_global_font, 12))
        self.onfront_checkbox = QCheckBox('', self)
        self.onfront_checkbox.stateChanged.connect(self.toggle_onfront)

        self.about_button = QPushButton('关于..', self)  # 设置窗口底栏
        self.about_button.setFont(QFont(_global_font, 10))
        self.about_button.clicked.connect(self.root_about.show)
        self.about_button.setFixedSize(120, 30)

        self.log_button = QPushButton('更新说明..', self)
        self.log_button.setFont(QFont(_global_font, 10))
        self.log_button.clicked.connect(self.root_log.show)
        self.log_button.setFixedSize(120, 30)

        self.settings_bottom_layout.addWidget(self.onfront_label)
        self.settings_bottom_layout.addWidget(self.onfront_checkbox)
        self.settings_bottom_layout.addStretch(1)
        self.settings_bottom_layout.addWidget(self.about_button)
        self.settings_bottom_layout.addWidget(self.log_button)

        for _layout in [self.settings_header_layout, 10, self.settings_main_layout, 10, self.settings_bottom_layout]:  # 设置窗口布局
            try: self.settings_layout.addLayout(_layout)
            except TypeError: self.settings_layout.addStretch(_layout)
        self.settings_layout.setContentsMargins(30, 25, 30, 25)
        
        self.setWindowTitle("祈愿 · 幸运观众 - 设置")
        self.setWindowIcon(QIcon(_iconpath))
        self.setGeometry(200, 200, 360, 350)
    
    def show_messagebox(self, message, type=QMessageBox.Warning):  # 弹出消息框
        msg = QMessageBox()  
        msg.setIcon(type)
        msg.setWindowIcon(QIcon(_iconpath))
        messagebox_title = "祈愿 · 幸运观众" if self.LANGUAGE_INDEX == 0 else "Wish3: Who's the Luckiest Dog?"
        msg.setWindowTitle(messagebox_title)
        msg.setText(message)
        msg.exec_() 

    def toggle_language(self, index):  # 1 语言切换
        self.LANGUAGE_INDEX = index
        self.lang_text = STATIC_STRINGS[str(self.LANGUAGE_INDEX)]
        self.wish_window.setWindowTitle(self.lang_text['title'])
        newtitle = f'{self.lang_text["title"]} {_short_ver}（{_vername}）{_ver}' if _vername != '正式版' else f'{self.lang_text["title"]} {_short_ver}'
        self.wish_window.title_label.setText(newtitle)
        self.wish_window.information_button.setText(self.lang_text['information_button'])
        self.wish_window.button_once.setText(self.lang_text['button_once'])
        self.wish_window.button_ten.setText(self.lang_text['button_ten'])

        self.settings_title_label.setText(self.lang_text['settings_title'])
        self.theme_label.setText(self.lang_text['settings_theme'])
        self.guarantee_label.setText(self.lang_text['settings_guarantee'])
        self.tie_label.setText(self.lang_text['settings_tie'])
        self.separate_label.setText(self.lang_text['settings_separate'])
        self.apply_tie_separate_button.setText(self.lang_text['settings_apply'])
        self.onfront_label.setText(self.lang_text['settings_onfront'])
        self.about_button.setText(self.lang_text['settings_about'])
        self.log_button.setText(self.lang_text['settings_log'])
        
        self.activateWindow()  # 激活以刷新文字 避免 UpdateLayeredWindowIndirect
        self.wish_window.activateWindow()
        
        if self.LANGUAGE_INDEX == 1:
            self.wish_window.information.setText(self.wish_window.information_list_en[self.wish_window.guarantee_mode])
            self.theme_combo.clear()
            for _item in self.example_theme_list_en:
                self.theme_combo.addItem(_item)
            self.guarantee_combo.clear()
            self.guarantee_combo.addItem(self.guarantee_item_name_en)
            self.guarantee_combo.addItem("No Guarantee")
            self.guarantee_combo.setFixedWidth(350)
        else:
            self.wish_window.information.setText(self.wish_window.information_list_zh[self.wish_window.guarantee_mode])
            self.theme_combo.clear()
            for _item in self.example_theme_list_zh:
                self.theme_combo.addItem(_item)
            self.guarantee_combo.clear()
            self.guarantee_combo.addItem(self.guarantee_item_name_zh)
            self.guarantee_combo.addItem("无保底")
            self.guarantee_combo.setFixedWidth(200)
        self.adjustSize()
        self.adjustSize()

        self.activateWindow()  # 激活以刷新文字 避免 UpdateLayeredWindowIndirect
        self.wish_window.activateWindow()

    def toggle_theme(self, index):  # 2 主题配色切换
        colour, picture, stylesheet = None, None, None
        if index == 0:
            colour = Qt.white
            self.wish_window.setStyleSheet("")
        if index == 1:
            colour = QColor(0, 165, 0)
            stylesheet = "QWidget {background-color: #00a500; color: white}"
        elif index == 2:
            colour = QColor(255, 184, 198)
            stylesheet = "QWidget {background-color: #ffb8c6; color: white}"
        elif index == 3:   
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(None, self.lang_text['settings_filedialog_title'], r".wish\themes", self.lang_text['settings_filedialog_filetype'], options=options)  
            if fileName:  
                picture = fileName  
                stylesheet = "QLabel {color: white}"
                try:
                    file_name_split = fileName.split('/')[-1].split(', ')
                    file_infomation = f"{self.lang_text['settings_file_information_1']}{file_name_split[0]}\n{self.lang_text['settings_file_information_2']}{file_name_split[1]}\n{self.lang_text['settings_file_information_3']}{file_name_split[2].split('.')[0]}"
                except IndexError:
                    file_infomation = f"{self.lang_text['settings_file_information_4']}{fileName}"
                self.show_messagebox(f"{self.lang_text['settings_file_applied']}\n\n{file_infomation}\n\n{self.lang_text['settings_file_declare']}", QMessageBox.Information)
        self.wish_window.round_shadow.set_background(colour=colour, picture=picture)
        self.wish_window.setStyleSheet(stylesheet)

    def toggle_guarantee(self, index):  # 3 保底机制切换
        self.wish_window.reset_guarantee()
        self.wish_window.guarantee_mode = index
        if self.LANGUAGE_INDEX == 0:
            self.wish_window.information.setText(self.wish_window.information_list_zh[index])
        else:
            self.wish_window.information.setText(self.wish_window.information_list_en[index])
        self.wish_window.information.setFixedSize(950, [100, 60][index])
        self.wish_window.adjustSize()
   
    def apply_tie_separate(self):  # 4.1 / 4.2「心之捆绑」与「心之隔离」应用 
        detailed_message = ['存在错误输入，请检查。', '存在输入格式错误，请检查。', '存在不支持的学号，请检查。', '学号不得捆绑或隔离自身，请检查。', '「心之隔离」与「心之捆绑」已更新。'] if self.LANGUAGE_INDEX == 0 else ['There are errors in the input, please check.', 'There are input format errors, please check.', 'There are unsupported student numbers, please check.', 'Student number cannot be tied or separated with itself, please check.', '「the Tied」and「the Separated」have been updated.']
        def check_list(lineedit, message_prefix): 
            try: new_list = [int(item) for item in filter(None, re.split(r'[-| ]+', lineedit.text()))]  
            except ValueError: self.show_messagebox(f"「{message_prefix}」{detailed_message[0]}\n", QMessageBox.Critical); return None  
            if len(new_list) % 2 != 0:  
                self.show_messagebox(f"「{message_prefix}」{detailed_message[1]}\n", QMessageBox.Critical); return None  
            is_unsupported_number = False  
            for number in new_list:  
                if number not in self.wish_window.supportable_numbers.copy(): 
                    is_unsupported_number = True  
            if is_unsupported_number:
                self.show_messagebox(f"「{message_prefix}」{detailed_message[2]}\n", QMessageBox.Warning); return None 
            is_selfed = False
            for number in range(len(new_list)-1):
                if number % 2 == 0 and new_list[number] == new_list[number + 1]:
                    is_selfed = True
            if is_selfed:
                self.show_messagebox(f"{detailed_message[3]}\n", QMessageBox.Warning); return None  
            return new_list
            
        while True:  
            message_prefix = ["心之捆绑", "心之隔离"] if self.LANGUAGE_INDEX == 0 else ["the Tied", "the Separated"]
            new_tie_list = check_list(self.tie_lineedit, message_prefix[0])  
            new_separate_list = check_list(self.separate_lineedit, message_prefix[1]) 
            if new_tie_list is None or new_separate_list is None: break
            self.wish_window.tie_list, self.wish_window.separate_list = new_tie_list, new_separate_list
            self.show_messagebox(f"{detailed_message[4]}", QMessageBox.Information)
            break
    
    def toggle_onfront(self):  # 窗口置顶切换
        if self.onfront_checkbox.isChecked():
            self.wish_window.setWindowFlags(self.wish_window.windowFlags() | Qt.WindowStaysOnTopHint)
            self.wish_window.show()
        else:
            self.wish_window.setWindowFlags(self.wish_window.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.wish_window.show()
        pass
