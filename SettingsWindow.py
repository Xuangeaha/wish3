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

from config import _iconpath

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

        self.theme_label = QLabel('主题配色：', self)  # 设置窗口：1 主题配色设置
        self.theme_label.setFont(QFont(_global_font, 12))
        self.theme_combo = QComboBox(self)
        self.theme_combo.setFont(QFont(_global_font, 12))
        for _item in ["默认", "轴月", "谢不开朗鸡罗", "（自定义图片）"]:
            self.theme_combo.addItem(_item)
        self.theme_combo.currentIndexChanged.connect(self.toggle_theme)

        self.guarantee_label = QLabel('保底机制：', self)  # 设置窗口：2 保底机制
        self.guarantee_label.setFont(QFont(_global_font, 12))
        self.guarantee_combo = QComboBox(self)
        self.guarantee_combo.setFont(QFont(_global_font, 12))
        guarantee_item_name = "8-60保底" if wish_window.GUARANTEE == [8,60] else f"自适应保底（当前{wish_window.GUARANTEE[0]}-{wish_window.GUARANTEE[1]}）"
        self.guarantee_combo.addItem(guarantee_item_name)
        self.guarantee_combo.addItem("无保底")
        self.guarantee_combo.currentIndexChanged.connect(self.toggle_guarantee)

        self.tie_label = QLabel('「心之捆绑」：', self)  # 设置窗口：3 「心之捆绑」
        self.tie_label.setFont(QFont(_global_font, 12))
        self.tie_lineedit = QLineEdit(self)
        self.tie_lineedit.setFixedWidth(160)
        self.tie_lineedit.setFont(QFont(_global_font, 12))
        self.tie_lineedit.setText(''.join([str(item) + '-' if index % 2 == 0 else str(item) + ' ' for index, item in enumerate(self.wish_window.tie_list)]))
        self.tie_lineedit.setToolTip("强制使两学号在两次连续祈愿中依次抽出。通过该方式祈愿获得的学号不计入保底。示例：“5-32 23-24”")

        self.separate_label = QLabel('「心之隔离」：', self)  # 设置窗口：4 「心之隔离」
        self.separate_label.setFont(QFont(_global_font, 12))
        self.separate_lineedit = QLineEdit(self)
        self.separate_lineedit.setFixedWidth(160)
        self.separate_lineedit.setFont(QFont(_global_font, 12))
        self.separate_lineedit.setText(''.join([str(item) + '|' if index % 2 == 0 else str(item) + ' ' for index, item in enumerate(self.wish_window.separate_list)]))
        self.separate_lineedit.setToolTip("限制两学号不得在两次连续祈愿中依次抽出。为满足该机制而进行强制插入的学号不计入保底。示例：“5|32 23|24”")

        self.apply_tie_separate_button = QPushButton('应用', self)
        self.apply_tie_separate_button.setFont(QFont(_global_font, 12))
        self.apply_tie_separate_button.setFixedWidth(100)
        self.apply_tie_separate_button.clicked.connect(self.apply_tie_separate)

        for _widget in [[self.theme_label, 0, 0], [self.theme_combo, 0, 1],  # 设置窗口中心布局
                        [self.guarantee_label, 1, 0], [self.guarantee_combo, 1, 1], 
                        [self.tie_label, 3, 0], [self.tie_lineedit, 3, 1],
                        [self.separate_label, 4, 0], [self.separate_lineedit, 4, 1], 
                        [self.apply_tie_separate_button, 5, 1]]:
            self.settings_main_layout.addWidget(_widget[0], _widget[1], _widget[2])

        self.settings_main_layout.setContentsMargins(30, 0, 30, 0)

        self.settings_bottom_layout = QHBoxLayout()
        
        self.onfront_label = QLabel('窗口始终置顶:', self)  # 窗口置顶设置
        self.onfront_label.setFont(QFont(_global_font, 12))
        self.onfront_checkbox = QCheckBox('', self)
        self.onfront_checkbox.stateChanged.connect(self.toggle_onfront)

        self.about_button = QPushButton('关于..', self)  # 设置窗口底栏
        self.about_button.setFont(QFont(_global_font, 10))
        self.about_button.clicked.connect(self.root_about.show)
        self.about_button.setFixedSize(120, 30)
        self.about_button.setToolTip('关于')

        self.log_button = QPushButton('更新说明..', self)
        self.log_button.setFont(QFont(_global_font, 10))
        self.log_button.clicked.connect(self.root_log.show)
        self.log_button.setFixedSize(120, 30)
        self.log_button.setToolTip('更新说明')

        self.settings_bottom_layout.addWidget(self.onfront_label)
        self.settings_bottom_layout.addWidget(self.onfront_checkbox)
        self.settings_bottom_layout.addWidget(self.about_button)
        self.settings_bottom_layout.addWidget(self.log_button)

        for _layout in [self.settings_header_layout, 10, self.settings_main_layout, 10, self.settings_bottom_layout]:  # 设置窗口布局
            try: self.settings_layout.addLayout(_layout)
            except TypeError: self.settings_layout.addStretch(_layout)
        self.settings_layout.setContentsMargins(30, 25, 30, 25)
        
        self.setWindowTitle("祈愿 · 幸运观众 - 设置")
        self.setWindowIcon(QIcon(_iconpath))
        self.setGeometry(200, 200, 360, 350)
    
    def show_messagebox(self, message, type=QMessageBox.Warning):
        msg = QMessageBox()  
        msg.setIcon(type)
        msg.setWindowIcon(QIcon(_iconpath))
        msg.setWindowTitle("祈愿 · 幸运观众")
        msg.setText(message)
        msg.exec_() 

    def toggle_theme(self, index):  # 1 主题配色切换
        colour, picture = None, None
        if index == 1:
            colour = QColor(0, 165, 0)
            stylesheet = "QWidget {background-color: #00a500; color: white}"
        elif index == 2:
            colour = QColor(255, 184, 198)
            stylesheet = "QWidget {background-color: #ffb8c6; color: white}"
        elif index == 3:
            options = QFileDialog.Options()  
            fileName, _ = QFileDialog.getOpenFileName(None, "选择背景图片（推荐大小：1050x210）", r".wish\themes", "图片文件 (*.jpg *.png)", options=options)  
            if fileName:  
                picture = fileName  
                stylesheet = "QLabel {color: white}"
                try:
                    file_name_split = fileName.split('/')[-1].split(', ')
                    file_infomation = f"照片标题：{file_name_split[0]}\n拍摄者：{file_name_split[1]}\n拍摄时间：{file_name_split[2].split('.')[0]}"
                except IndexError:
                    file_infomation = f"照片信息：{fileName}"
                declare_ch = ">>> 祈愿 · 幸运观众尊重并保护所有照片版权，不拥有、不转让任何照片知识产权，其解释权及所有权均严格归属于原始拍摄者所有。用户上传的照片需确保已获得合法授权或属于公共领域资源，不侵犯任何第三方权益。我们鼓励合法、健康的内容创作与分享，感谢您的使用。"
                declare_en = ">>> Wish3: Who's the Luckiest Dog? respects and protects all photo copyrights and does not own or transfer any intellectual property rights of the photos, with interpretation rights and ownership strictly belonging to the original photographers. Users must ensure that uploaded photos have been legally authorized or belong to public domain resources, without infringing upon any third-party rights. We encourage legal and healthy content creation and sharing. Thanks for your using."
                self.show_messagebox(f"自定义图片背景已应用。\n\n{file_infomation}\n\n{declare_ch}\n\n{declare_en}", QMessageBox.Information)
        else:
            colour = Qt.white
            stylesheet = "QWidget {background-color: white; color: black}"
        self.wish_window.round_shadow.set_background(colour=colour, picture=picture)
        self.wish_window.setStyleSheet(stylesheet)

    def toggle_guarantee(self, index):  # 2 保底机制切换
        self.wish_window.reset_guarantee()
        self.wish_window.guarantee_mode = index
        self.wish_window.information.setText(self.wish_window.information_list[index])
        self.wish_window.information.setFixedSize(950, [100, 60][index])
        self.wish_window.adjustSize()
   
    def apply_tie_separate(self):  # 3 / 4「心之捆绑」与「心之隔离」应用 
        def check_list(lineedit, message_prefix): 
            try: new_list = [int(item) for item in filter(None, re.split(r'[-| ]+', lineedit.text()))]  
            except ValueError: self.show_messagebox(f"「{message_prefix}」存在错误输入，请检查。\n", QMessageBox.Critical); return None  
            if len(new_list) % 2 != 0:  
                self.show_messagebox(f"「{message_prefix}」存在输入格式错误，请检查。\n", QMessageBox.Critical); return None  
            is_unsupported_number = False  
            for number in new_list:  
                if number not in self.wish_window.supportable_numbers.copy(): 
                    is_unsupported_number = True  
            if is_unsupported_number:
                self.show_messagebox(f"「{message_prefix}」存在不支持的学号，请检查。\n", QMessageBox.Warning); return None 
            is_selfed = False
            for number in range(len(new_list)-1):
                if number % 2 == 0 and new_list[number] == new_list[number + 1]:
                    is_selfed = True
            if is_selfed:
                self.show_messagebox(f"学号不得捆绑或隔离自身，请检查。\n", QMessageBox.Warning); return None  
            return new_list
            
        while True:  
            new_tie_list = check_list(self.tie_lineedit, "心之捆绑")  
            new_separate_list = check_list(self.separate_lineedit, "心之隔离") 
            if new_tie_list is None or new_separate_list is None: break
            self.wish_window.tie_list, self.wish_window.separate_list = new_tie_list, new_separate_list
            self.show_messagebox("「心之隔离」与「心之捆绑」已更新。\n", QMessageBox.Information)
            break
    
    def toggle_onfront(self):
        if self.onfront_checkbox.isChecked():
            self.wish_window.setWindowFlags(self.wish_window.windowFlags() | Qt.WindowStaysOnTopHint)
            self.wish_window.show()
        else:
            self.wish_window.setWindowFlags(self.wish_window.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.wish_window.show()
        pass
