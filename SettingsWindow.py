"""
祈愿 · 幸运观众：设置窗口

Copyright © 2024-2025 XuangeAha(轩哥啊哈OvO/卡猫kat)

"""

from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox, QMessageBox, QFileDialog, QCheckBox
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtCore import Qt
import re

from RoundShadow import RoundShadow
from MovableWindow import MovableWindow
from LogWindow import LogWindow
from AboutWindow import AboutWindow
import MessageBox

from config import _ver_short, _ver, _ver_type, _iconpath, _default_lang
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

        self.LANGUAGE_INDEX = _default_lang
        self.lang_text = STATIC_STRINGS[str(self.LANGUAGE_INDEX)]
        
        self.is_initializing = False

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

        self.settings_main_layout = QGridLayout()  # 设置栏面板

        self.languages_label = QLabel('语言/Languages：', self)  # 1 语言
        self.languages_label.setFont(QFont(_global_font, 12))
        self.languages_combo = QComboBox(self)
        self.languages_combo.setFont(QFont(_global_font, 12))
        for _item in ["中文", "English"]:
            self.languages_combo.addItem(_item)
        self.languages_combo.setCurrentIndex(self.LANGUAGE_INDEX)
        self.languages_combo.currentIndexChanged.connect(self.toggle_language)

        self.theme_label = QLabel('主题配色：', self)  # 2 主题配色
        self.theme_label.setFont(QFont(_global_font, 12))
        self.theme_combo = QComboBox(self)
        self.theme_combo.setFont(QFont(_global_font, 12))
        self.example_theme_list_zh = ["默认", "春日影", "海洋", "（自定义图片）"]
        self.example_theme_list_en = ["Default", "Spring's in the air", "Ocean Waves", "(Customed Image)"]
        for _item in self.example_theme_list_zh:
            self.theme_combo.addItem(_item)
        self.theme_combo.currentIndexChanged.connect(self.toggle_theme)

        self.avatar_label = QLabel('头像显示：', self)  # 3 头像显示
        self.avatar_label.setFont(QFont(_global_font, 12))
        self.avatar_checkbox = QCheckBox('', self)
        self.avatar_checkbox.setChecked(wish_window.is_avatar_shown)
        self.avatar_checkbox.stateChanged.connect(self.toggle_avatar)

        self.line_left = QLabel('', self)  # 分割线
        self.line_left.setFixedHeight(1)
        self.line_left.setStyleSheet("background-color: #696969")

        self.line_right = QLabel('', self)
        self.line_right.setFixedHeight(1)
        self.line_right.setStyleSheet("background-color: #696969")

        self.guarantee_label = QLabel('保底机制：', self)  # 4 保底机制
        self.guarantee_label.setFont(QFont(_global_font, 12))
        self.guarantee_combo = QComboBox(self)
        self.guarantee_combo.setFont(QFont(_global_font, 12))
        self.guarantee_item_name_zh = "8-60保底" if wish_window.GUARANTEE == [8,60] else f"自适应保底（当前{wish_window.GUARANTEE[0]}-{wish_window.GUARANTEE[1]}）"
        self.guarantee_item_name_en = "8-60 Guarantee" if wish_window.GUARANTEE == [8,60] else f"Adaptive Guarantee (Currently {wish_window.GUARANTEE[0]}-{wish_window.GUARANTEE[1]})"
        self.guarantee_combo.addItem(self.guarantee_item_name_zh)
        self.guarantee_combo.addItem("无保底")
        self.guarantee_combo.currentIndexChanged.connect(self.toggle_guarantee)

        self.tie_label = QLabel('「心之捆绑」：', self)  # 5.1 「心之捆绑」
        self.tie_label.setFont(QFont(_global_font, 12))
        self.tie_lineedit = QLineEdit(self)
        self.tie_lineedit.setFont(QFont(_global_font, 12))
        self.tie_lineedit.setText(''.join([str(item) + '-' if index % 2 == 0 else str(item) + ' ' for index, item in enumerate(self.wish_window.tie_list)]))

        self.separate_label = QLabel('「心之隔离」：', self)  # 5.2 「心之隔离」
        self.separate_label.setFont(QFont(_global_font, 12))
        self.separate_lineedit = QLineEdit(self)
        self.separate_lineedit.setFont(QFont(_global_font, 12))
        self.separate_lineedit.setText(''.join([str(item) + '|' if index % 2 == 0 else str(item) + ' ' for index, item in enumerate(self.wish_window.separate_list)]))

        self.apply_tie_separate_button = QPushButton('应用', self)  # 5.3 「心之捆绑」&「心之隔离」应用
        self.apply_tie_separate_button.setFont(QFont(_global_font, 11))
        self.apply_tie_separate_button.setFixedWidth(100)
        self.apply_tie_separate_button.clicked.connect(self.apply_tie_separate)

        for _widget in [[self.languages_label, 0, 0], [self.languages_combo, 0, 1],  # 设置栏面板布局
                        [self.theme_label, 1, 0], [self.theme_combo, 1, 1], 
                        [self.avatar_label, 2, 0], [self.avatar_checkbox, 2, 1],
                        [self.line_left, 4, 0], [self.line_right, 4, 1],
                        [self.guarantee_label, 6, 0], [self.guarantee_combo, 6, 1], 
                        [self.tie_label, 7, 0], [self.tie_lineedit, 7, 1],
                        [self.separate_label, 8, 0], [self.separate_lineedit, 8, 1], 
                        [self.apply_tie_separate_button, 9, 1]]:
            self.settings_main_layout.addWidget(_widget[0], _widget[1], _widget[2])

        self.settings_main_layout.setContentsMargins(30, 8, 30, 15)

        self.settings_bottom_layout = QHBoxLayout()  # 设置底栏
        
        self.onfront_label = QLabel('窗口始终置顶：', self)  # 窗口始终置顶
        self.onfront_label.setFont(QFont(_global_font, 11))
        self.onfront_checkbox = QCheckBox('', self)
        self.onfront_checkbox.stateChanged.connect(self.toggle_onfront)

        self.about_button = QPushButton('关于..', self)  # 关于
        self.about_button.setFont(QFont(_global_font, 9))
        self.about_button.clicked.connect(self.root_about.show)
        self.about_button.setFixedSize(160, 35)

        self.log_button = QPushButton('更新说明..', self)  # 更新说明
        self.log_button.setFont(QFont(_global_font, 9))
        self.log_button.clicked.connect(self.root_log.show)
        self.log_button.setFixedSize(160, 35)

        self.settings_bottom_layout.addWidget(self.onfront_label)  # 设置底栏布局
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

    def toggle_language(self, index:int):  # 1 语言切换
        self.LANGUAGE_INDEX = index
        self.lang_text = STATIC_STRINGS[str(self.LANGUAGE_INDEX)]
        self.wish_window.setWindowTitle(self.lang_text['title'])
        newtitle = f'{self.lang_text["title"]} {_ver_short}（{_ver_type}）{_ver}' if _ver_type != '正式版' else f'{self.lang_text["title"]} {_ver_short}'
        self.wish_window.title_label.setText(newtitle)
        self.wish_window.information_toggle_button.setText(self.lang_text['information_button'])
        self.wish_window.button_once.setText(self.lang_text['button_once'])
        self.wish_window.button_ten.setText(self.lang_text['button_ten'])

        self.settings_title_label.setText(self.lang_text['settings_title'])
        self.theme_label.setText(self.lang_text['settings_theme'])
        self.avatar_label.setText(self.lang_text['settings_avatar'])
        self.guarantee_label.setText(self.lang_text['settings_guarantee'])
        self.tie_label.setText(self.lang_text['settings_tie'])
        self.separate_label.setText(self.lang_text['settings_separate'])
        self.apply_tie_separate_button.setText(self.lang_text['settings_apply'])
        self.onfront_label.setText(self.lang_text['settings_onfront'])
        self.about_button.setText(self.lang_text['settings_about'])
        self.log_button.setText(self.lang_text['settings_log'])
        
        # self.activateWindow()  # 激活以刷新文字 避免 UpdateLayeredWindowIndirect
        # self.wish_window.activateWindow()
        
        self.theme_combo.blockSignals(True)  # 阻断信号以防止触发 toggle
        self.guarantee_combo.blockSignals(True)
        current_theme = self.theme_combo.currentIndex()  # 保存当前索引
        current_guarantee = self.guarantee_combo.currentIndex()
    
        if self.LANGUAGE_INDEX == 1:
            self.wish_window.information.setText(self.wish_window.information_list_en[self.wish_window.guarantee_mode])
            self.theme_combo.clear()
            for _item in self.example_theme_list_en:
                self.theme_combo.addItem(_item)
            self.guarantee_combo.clear()
            self.guarantee_combo.addItem(self.guarantee_item_name_en)
            self.guarantee_combo.addItem("No Guarantee")
            self.guarantee_combo.setFixedWidth(350)
            if self.is_initializing:
                MessageBox.show_messagebox(message='Language changed to English.', duration=1.5)
            self.is_initializing = True
        else:
            self.wish_window.information.setText(self.wish_window.information_list_zh[self.wish_window.guarantee_mode])
            self.theme_combo.clear()
            for _item in self.example_theme_list_zh:
                self.theme_combo.addItem(_item)
            self.guarantee_combo.clear()
            self.guarantee_combo.addItem(self.guarantee_item_name_zh)
            self.guarantee_combo.addItem("无保底")
            self.guarantee_combo.setFixedWidth(300)
            if self.is_initializing:
                MessageBox.show_messagebox(message='语言已切换为中文。', duration=1.5)
            self.is_initializing = True

        self.adjustSize()
        self.adjustSize()
        
        self.theme_combo.setCurrentIndex(current_theme)  # 恢复保底选择
        self.guarantee_combo.setCurrentIndex(current_guarantee)
        self.theme_combo.blockSignals(False)  # 解除信号阻断
        self.guarantee_combo.blockSignals(False)

        # self.activateWindow()  # 激活以刷新文字 避免 UpdateLayeredWindowIndirect
        # self.wish_window.activateWindow()

    def toggle_theme(self, index:int):  # 2 主题配色切换
        if not hasattr(self.wish_window, 'current_theme_index'):
            self.wish_window.current_theme_index = 0
            
        colour, picture, stylesheet = None, None, None
        if index == 0:
            colour = Qt.white
            self.wish_window.setStyleSheet("")
        if index == 1:
            picture = r'.wish\assets\themes\spring.jpg'
        elif index == 2:
            picture = r'.wish\assets\themes\ocean.png'
            stylesheet = "QLabel {color: white}"
        elif index == 3:   
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, self.lang_text['settings_filedialog_title'], r".wish\themes", self.lang_text['settings_filedialog_filetype'], options=options)  
            if fileName:  
                picture = fileName  
                stylesheet = "QLabel {color: white}"
                try:
                    file_name_split = fileName.split('/')[-1].split(', ')
                    file_infomation = f"{self.lang_text['settings_file_information_1']}{file_name_split[0]}\n{self.lang_text['settings_file_information_2']}{file_name_split[1]}\n{self.lang_text['settings_file_information_3']}{file_name_split[2].split('.')[0]}"
                except IndexError:
                    file_infomation = f"{self.lang_text['settings_file_information_4']}{fileName}"
                self.show_dialoguebox(f"{self.lang_text['settings_file_applied']}\n\n{file_infomation}\n\n{self.lang_text['settings_file_declare']}", type=QMessageBox.Information)
            else:
                self.theme_combo.blockSignals(True)
                self.theme_combo.setCurrentIndex(self.wish_window.current_theme_index)
                self.theme_combo.blockSignals(False)
                return
        self.wish_window.round_shadow.set_background(colour=colour, picture=picture)
        self.wish_window.setStyleSheet(stylesheet)
        self.wish_window.current_theme_index = index

        if self.is_initializing:
            MessageBox.show_messagebox(message=f"主题配色已切换为{self.theme_combo.itemText(index)}。" if self.LANGUAGE_INDEX == 0 else f"Theme colour switched to {self.theme_combo.itemText(index)}.", duration=1.5)

    def toggle_avatar(self):  # 3 头像显示切换
        if self.avatar_checkbox.isChecked():
            self.wish_window.is_avatar_shown = True
            MessageBox.show_messagebox(message='头像已切换显示。' if self.LANGUAGE_INDEX == 0 else 'Avatar shown.', duration=1.5)
        else:
            self.wish_window.is_avatar_shown = False
            MessageBox.show_messagebox(message='头像已切换隐藏。' if self.LANGUAGE_INDEX == 0 else 'Avatar hidden.', duration=1.5)

    def toggle_guarantee(self, index:int):  # 4 保底机制切换
        self.wish_window.reset_guarantee()
        self.wish_window.guarantee_mode = index
        if self.LANGUAGE_INDEX == 0:
            self.wish_window.information.setText(self.wish_window.information_list_zh[index])
            if self.is_initializing:
                MessageBox.show_messagebox(message=f"保底机制已切换为{self.guarantee_combo.itemText(index)}。", duration=1.5)
        else:
            self.wish_window.information.setText(self.wish_window.information_list_en[index])
            if self.is_initializing:
                MessageBox.show_messagebox(message=f"Guarantee mode has been switched to {self.guarantee_combo.itemText(index)}.", duration=1.5)
        self.wish_window.information.setFixedSize(950, [100, 60][index])
        self.wish_window.adjustSize()
   
    def apply_tie_separate(self):  # 5.1 / 5.2「心之捆绑」与「心之隔离」应用 
        detailed_message = ['存在错误输入，请检查。', '存在输入格式错误，请检查。', '存在不支持的学号，请检查。', '学号不得捆绑或隔离自身，请检查。', '「心之隔离」与「心之捆绑」已更新。'] if self.LANGUAGE_INDEX == 0 else ['There are errors in the input, please check.', 'There are input format errors, please check.', 'There are unsupported student numbers, please check.', 'Student number cannot be tied or separated with itself, please check.', '「The Tied」and「The Separated」have been updated.']
        def check_list(lineedit, message_prefix): 
            try: new_list = [int(item) for item in filter(None, re.split(r'[-| ]+', lineedit.text()))]  
            except ValueError: MessageBox.show_messagebox(message=f"⚠「{message_prefix}」{detailed_message[0]}", duration=2); return None  
            if len(new_list) % 2 != 0:  
                MessageBox.show_messagebox(f"⚠「{message_prefix}」{detailed_message[1]}", duration=2); return None 
            is_unsupported_number = False  
            for number in new_list:  
                if number not in self.wish_window.supportable_numbers.copy(): 
                    is_unsupported_number = True  
            if is_unsupported_number:
                MessageBox.show_messagebox(f"⚠「{message_prefix}」{detailed_message[2]}", duration=2); return None 
            is_selfed = False
            for number in range(len(new_list)-1):
                if number % 2 == 0 and new_list[number] == new_list[number + 1]:
                    is_selfed = True
            if is_selfed:
                MessageBox.show_messagebox(f"⚠{detailed_message[3]}", duration=2); return None 
            return new_list
            
        while True:  
            message_prefix = ["心之捆绑", "心之隔离"] if self.LANGUAGE_INDEX == 0 else ["The Tied", "The Separated"]
            new_tie_list = check_list(self.tie_lineedit, message_prefix[0])  
            new_separate_list = check_list(self.separate_lineedit, message_prefix[1]) 
            if new_tie_list is None or new_separate_list is None: break
            self.wish_window.tie_list, self.wish_window.separate_list = new_tie_list, new_separate_list
            MessageBox.show_messagebox(f"{detailed_message[4]}", duration=1.5)
            break
    
    def toggle_onfront(self):  # 窗口置顶切换
        if self.onfront_checkbox.isChecked():
            self.wish_window.setWindowFlags(self.wish_window.windowFlags() | Qt.WindowStaysOnTopHint)
            self.wish_window.show()
            MessageBox.show_messagebox(message='窗口已切换置顶。' if self.LANGUAGE_INDEX == 0 else 'Window pinned on top.', duration=1.5)
        else:
            self.wish_window.setWindowFlags(self.wish_window.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.wish_window.show()
            MessageBox.show_messagebox(message='窗口已取消置顶。' if self.LANGUAGE_INDEX == 0 else 'Window unpinned.', duration=1.5)

    def show_dialoguebox(self, message:str, lang:int=int, type=QMessageBox.Warning):  # 消息框弹出
        dialoguebox = QMessageBox()  
        dialoguebox.setIcon(type)
        dialoguebox.setWindowIcon(QIcon(_iconpath))
        dialogue_title = "祈愿 · 幸运观众" if lang == 0 else "Wish3: Who's the Luckiest Dog?"
        dialoguebox.setWindowTitle(dialogue_title)
        dialoguebox.setText(message)
        dialoguebox.exec_() 
