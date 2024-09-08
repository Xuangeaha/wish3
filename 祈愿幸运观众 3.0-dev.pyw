from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import random
import webbrowser

_ver = '3.0dev0.09.7100'


class RoundShadow(QWidget):
    def __init__(self, parent=None):
        super(RoundShadow, self).__init__(parent)
        self.border_width = 8
        self.background_color = QColor(Qt.white)  # 初始化背景颜色
        self.setAttribute(Qt.WA_TranslucentBackground)

    def set_background_color(self, color):
        self.background_color = color
        self.update()  # 调用 update 方法来重绘窗口

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.background_color)  # 使用存储的颜色
        painter.setPen(Qt.transparent)

        radius, rect = 16, self.rect()
        rect.adjust(radius, radius, -radius, -radius)
        painter.drawRoundedRect(rect, radius, radius)


class AboutWindow(QWidget):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.dragging = False
        self.dragPosition = None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.round_shadow = RoundShadow(self)
        self.round_shadow.setGeometry(0, 0, 300, 300)

        shadow = QGraphicsDropShadowEffect(self.round_shadow)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 127))
        self.round_shadow.setGraphicsEffect(shadow)

        self.about_layout = QVBoxLayout(self)

        self.about_header_layout = QHBoxLayout()
        self.about_title_label = QLabel('关于 祈愿·幸运观众', self)
        self.about_title_label.setFont(QFont('汉仪文黑-85w', 11))
        self.about_close_button = QPushButton('X', self)
        self.about_close_button.setFont(QFont('汉仪文黑-85w', 12))
        self.about_close_button.clicked.connect(self.close)
        self.about_close_button.setFixedSize(24, 24)
        self.about_close_button.setStyleSheet("""
            QPushButton:hover {
                border-radius: 5px;
                background-color: red;
                color: white;
            }
        """)
        self.about_header_layout.addWidget(self.about_title_label)
        self.about_header_layout.addStretch(1)
        self.about_header_layout.addWidget(self.about_close_button)

        self.wish_icon = QLabel(self)
        self.wish_icon.setPixmap(
            QIcon(r'.wish\assets\wish\wish.png').pixmap(100, 100))
        self.wish_icon.setAlignment(Qt.AlignCenter)

        self.wish_title = QLabel('祈愿·幸运观众 3.0', self)
        self.wish_title.setFont(QFont('汉仪文黑-85w', 18))
        self.wish_title.setAlignment(Qt.AlignCenter)

        self.wish_subtitle = QLabel(_ver, self)
        self.wish_subtitle.setFont(QFont('汉仪文黑-85w', 12))
        self.wish_subtitle.setAlignment(Qt.AlignCenter)

        self.wish_copyright = QLabel(
            'Copyright © 2023-2024 XuangeAha(轩哥啊哈OvO), \nAll rights reserved. | MIT License', self)
        self.wish_copyright.setFont(QFont('Arial', 10))
        self.wish_copyright.setAlignment(Qt.AlignCenter)

        def call_github_broser():
            webbrowser.open('https://www.github.com/xuangeaha')

        def call_csdn_broser():
            webbrowser.open('https://xuangeaha.blog.csdn.net/')

        self.call_github = QPushButton('Github(Xuangeaha) ↗', self)
        self.call_github.setFont(QFont('等线', 10))
        self.call_github.clicked.connect(call_github_broser)

        self.call_csdn = QPushButton('CSDN(轩哥啊哈OvO) ↗', self)
        self.call_csdn.setFont(QFont('等线', 10))
        self.call_csdn.clicked.connect(call_csdn_broser)

        self.about_layout.addLayout(self.about_header_layout)
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.dragPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = QPoint(event.globalPos() - self.dragPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.dragPosition = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def resizeEvent(self, event):
        self.round_shadow.resize(self.size())


class LogWindow(QWidget):
    def __init__(self, parent=None):
        super(LogWindow, self).__init__(parent)
        self.dragging = False
        self.dragPosition = None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.round_shadow = RoundShadow(self)
        self.round_shadow.setGeometry(0, 0, 300, 300)

        shadow = QGraphicsDropShadowEffect(self.round_shadow)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 127))
        self.round_shadow.setGraphicsEffect(shadow)

        self.log_layout = QVBoxLayout(self)

        self.log_header_layout = QHBoxLayout()
        self.log_title_label = QLabel('更新说明', self)
        self.log_title_label.setFont(QFont('汉仪文黑-85w', 11))
        self.log_close_button = QPushButton('X', self)
        self.log_close_button.setFont(QFont('汉仪文黑-85w', 12))
        self.log_close_button.clicked.connect(self.close)
        self.log_close_button.setFixedSize(24, 24)
        self.log_close_button.setStyleSheet("""
            QPushButton:hover {
                border-radius: 5px;
                background-color: red;
                color: white;
            }
        """)
        self.log_header_layout.addWidget(self.log_title_label)
        self.log_header_layout.addStretch(1)
        self.log_header_layout.addWidget(self.log_close_button)

        self.log = QGridLayout()

        with open('log.txt', 'r', encoding='utf-8') as file:
            content_list = [line.strip() for line in file]

        self.log_layout.addLayout(self.log_header_layout)

        for x in range(1, int(len(content_list)/3+1)):
            log1 = QLabel(content_list[x*3-3].split("    ")[0]+"    ", self)
            log1.setFont(QFont('汉仪文黑-85w', 12))
            self.log.addWidget(log1, x, 1)
            log2 = QLabel(content_list[x*3-3].split("    ")[1]+"    ", self)
            log2.setFont(QFont('汉仪文黑-85w', 12))
            self.log.addWidget(log2, x, 2)
            log3 = QLabel(content_list[x*3-2], self)
            log3.setFont(QFont('汉仪文黑-85w', 12))
            self.log.addWidget(log3, x, 3)

        self.log.setContentsMargins(35, 5, 35, 10)
        self.log_layout.addLayout(self.log)
        self.log_layout.setContentsMargins(30, 25, 30, 25)

        self.setGeometry(300, 300, 400, 400)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.dragPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = QPoint(event.globalPos() - self.dragPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.dragPosition = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def resizeEvent(self, event):
        self.round_shadow.resize(self.size())


class SettingsWindow(QWidget):
    def __init__(self, wish_window, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.wish_window = wish_window
        self.dragging = False
        self.dragPosition = None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.round_shadow = RoundShadow(self)
        self.round_shadow.setGeometry(0, 0, 300, 300)

        shadow = QGraphicsDropShadowEffect(self.round_shadow)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 127))
        self.round_shadow.setGraphicsEffect(shadow)

        self.settings_layout = QVBoxLayout(self)

        self.settings_header_layout = QHBoxLayout()
        self.settings_title_label = QLabel('设置', self)
        self.settings_title_label.setFont(QFont('汉仪文黑-85w', 11))
        self.settings_close_button = QPushButton('X', self)
        self.settings_close_button.setFont(QFont('汉仪文黑-85w', 12))
        self.settings_close_button.clicked.connect(self.close)
        self.settings_close_button.setFixedSize(24, 24)
        self.settings_close_button.setStyleSheet("""
            QPushButton:hover {
                border-radius: 5px;
                background-color: red;
                color: white;
            }
        """)
        self.settings_header_layout.addWidget(self.settings_title_label)
        self.settings_header_layout.addStretch(1)
        self.settings_header_layout.addWidget(self.settings_close_button)

        self.settings_main_layout = QGridLayout()

        self.theme_label = QLabel('主题配色：', self)
        self.theme_label.setFont(QFont('汉仪文黑-85w', 12))

        self.theme_combo = QComboBox(self)
        self.theme_combo.setFont(QFont('汉仪文黑-85w', 12))
        self.theme_combo.addItem("默认")
        self.theme_combo.addItem("轴月")
        # self.theme_combo.addItem("党")
        self.theme_combo.currentIndexChanged.connect(self.change_theme)

        self.guarantee_label = QLabel('保底机制：', self)
        self.guarantee_label.setFont(QFont('汉仪文黑-85w', 12))

        self.guarantee_combo = QComboBox(self)
        self.guarantee_combo.setFont(QFont('汉仪文黑-85w', 12))
        self.guarantee_combo.addItem("8-60保底")
        self.guarantee_combo.addItem("无保底")
        self.guarantee_combo.currentIndexChanged.connect(self.change_guarantee)

        self.settings_main_layout.addWidget(self.theme_label, 0, 0)
        self.settings_main_layout.addWidget(self.theme_combo, 0, 1)
        self.settings_main_layout.addWidget(self.guarantee_label, 1, 0)
        self.settings_main_layout.addWidget(self.guarantee_combo, 1, 1)

        self.settings_main_layout.setContentsMargins(30, 0, 30, 0)

        self.settings_bottom_layout = QHBoxLayout()

        self.about_button = QPushButton('关于..', self)
        self.about_button.setFont(QFont('汉仪文黑-85w', 12))
        self.about_button.clicked.connect(self.call_about_window)
        self.about_button.setFixedSize(120, 24)
        self.about_button.setToolTip('关于')

        self.log_button = QPushButton('更新说明..', self)
        self.log_button.setFont(QFont('汉仪文黑-85w', 12))
        self.log_button.clicked.connect(self.call_log_window)
        self.log_button.setFixedSize(120, 24)
        self.log_button.setToolTip('更新说明')

        self.settings_bottom_layout.addWidget(self.about_button)
        self.settings_bottom_layout.addWidget(self.log_button)

        self.settings_layout.addLayout(self.settings_header_layout)
        self.settings_layout.addStretch(10)
        self.settings_layout.addLayout(self.settings_main_layout)
        self.settings_layout.addStretch(10)
        self.settings_layout.addLayout(self.settings_bottom_layout)

        self.settings_layout.setContentsMargins(30, 25, 30, 25)
        self.setGeometry(100, 100, 320, 350)

    def change_theme(self, index):
        if index == 1:  # 假设 "轴月" 是第二个选项，设置为绿色
            color = QColor(0, 165, 0)  # 绿色
            stylesheet = "QWidget {background-color: #00a500; color: white}"
        elif index == 2:
            color = Qt.red  # 其他选项设为白色或其他颜色
            stylesheet = "QWidget {background-color: red; color: yellow}"
        else:
            color = Qt.white
            stylesheet = "QWidget {background-color: white; color: black}"
        self.wish_window.round_shadow.set_background_color(color)
        self.wish_window.setStyleSheet(stylesheet)

    def change_guarantee(self, index):
        self.wish_window.guarantee_mode = index

    def call_about_window(self):
        self.root_about = AboutWindow(self)
        self.root_about.show()

    def call_log_window(self):
        self.root_log = LogWindow(self)
        self.root_log.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.dragPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = QPoint(event.globalPos() - self.dragPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.dragPosition = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def resizeEvent(self, event):
        self.round_shadow.resize(self.size())


class WishWindow(QWidget):
    def __init__(self, parent=None):
        super(WishWindow, self).__init__(parent)
        self.numbers = []
        self.dragging = False
        self.dragPosition = None
        self.is_information_shown = False
        self.guarantee_mode = 0

        self.history_all = []
        self.history_last_60 = []
        self.pick_num = 0
        self.pick_num_rest = 60
        self.last_8_picks = []
        self.is_in_guarantee: bool = False
        self.lucky_rest = list(range(1, 41))

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.round_shadow = RoundShadow(self)
        self.round_shadow.setGeometry(0, 0, 300, 300)

        shadow = QGraphicsDropShadowEffect(self.round_shadow)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 127))
        self.round_shadow.setGraphicsEffect(shadow)

        self.main_layout = QVBoxLayout(self)

        self.header_layout = QHBoxLayout()

        self.title_label = QLabel('祈愿·幸运观众 3.0（早期开发）'+_ver, self)
        self.title_label.setFont(QFont('汉仪文黑-85w', 11))

        self.information_button = QPushButton('∨祈愿详情∨', self)
        self.information_button.setFont(QFont('汉仪文黑-85w', 10))
        self.information_button.clicked.connect(self.toggle_information)
        self.information_button.setFixedSize(150, 26)
        self.information_button.setToolTip('祈愿详情')
        self.information_button.setStyleSheet(""" 
            QPushButton:hover {
                border-radius: 5px;
                background-color: gray;
                color: white;
            }
        """)

        self.minimize_button = QPushButton('', self)
        self.minimize_button.setIcon(QIcon(r'.wish\assets\icon\minimize.png'))
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setFixedSize(24, 24)
        self.minimize_button.setToolTip('最小化')
        self.minimize_button.setStyleSheet(""" 
            QPushButton:hover {
                border-radius: 5px;
                background-color: blue;
                color: white;
            }
        """)

        self.settings_button = QPushButton('', self)
        self.settings_button.setIcon(QIcon(r'.wish\assets\icon\settings.png'))
        self.settings_button.clicked.connect(self.call_settings_window)
        self.settings_button.setFixedSize(24, 24)
        self.settings_button.setStyleSheet("""
            QPushButton:hover {
                border-radius: 5px;
                background-color: blue;
                color: white;
            }
        """)

        self.close_button = QPushButton('', self)
        self.close_button.setIcon(QIcon(r'.wish\assets\icon\close.png'))
        self.close_button.clicked.connect(self.close) 
        self.close_button.setFixedSize(24, 24)
        self.close_button.setStyleSheet("""
            QPushButton:hover {
                border-radius: 5px;
                background-color: red;
                color: white;
            }
        """)

        self.header_layout.addWidget(self.title_label)
        self.header_layout.addWidget(self.information_button)
        self.header_layout.addStretch(1)
        self.header_layout.addWidget(self.minimize_button)
        self.header_layout.addWidget(self.settings_button)
        self.header_layout.addWidget(self.close_button)

        self.information = QLabel(
            "当前保底机制：  · 每60次祈愿内，所有学号必出至少一次。\n                                · 任意连续8次祈愿内，相同学号至多出一次。", self)
        self.information.setFont(QFont('汉仪文黑-85w', 14))
        self.information.setAlignment(Qt.AlignCenter)
        self.information.setFixedSize(950, 60)
        self.information.setVisible(False)

        self.bottom_layout = QHBoxLayout()

        self.label = QLabel('', self)
        self.label.setFont(QFont('汉仪文黑-85w', 19))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedWidth(650)

        self.button_once = QPushButton('抽 1 次', self)
        self.button_once.setFont(QFont('汉仪文黑-85w', 14))
        self.button_once.clicked.connect(self.draw_once)
        self.button_once.setFixedSize(150, 60)

        self.button_ten = QPushButton('抽 10 次', self)
        self.button_ten.setFont(QFont('汉仪文黑-85w', 14))
        self.button_ten.clicked.connect(self.draw_ten)
        self.button_ten.setFixedSize(150, 60)

        self.bottom_layout.addWidget(self.label)
        self.bottom_layout.addWidget(self.button_once)
        self.bottom_layout.addWidget(self.button_ten)

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addWidget(self.information)
        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.setContentsMargins(30, 25, 30, 25)

        self.setGeometry(100, 100, 950, 60)

    def call_settings_window(self):
        self.root_settings = SettingsWindow(self)
        self.root_settings.show()

    def get_lucky(self):
        if self.guarantee_mode == 0:
            self.is_in_guarantee = len(self.lucky_rest) >= self.pick_num_rest
            if self.pick_num_rest == 0:
                self.reset_guarantee()
            if len(self.last_8_picks) > 7:
                self.last_8_picks.remove(self.last_8_picks[0])
            while True:
                if self.is_in_guarantee:
                    lucky_person = random.choice(self.lucky_rest)
                else:
                    lucky_person = random.randint(1, 40)
                if lucky_person not in self.last_8_picks:
                    break
            self.last_8_picks.append(lucky_person)
            if lucky_person not in self.history_last_60:
                self.history_last_60.append(lucky_person)
                self.lucky_rest.remove(lucky_person)
            self.pick_num += 1
            self.pick_num_rest -= 1
            self.history_all.append(lucky_person)
        else:
            self.reset_guarantee()
            lucky_person = random.randint(1, 40)
        return lucky_person

    def reset_guarantee(self):
        self.history_last_60 = []
        self.lucky_rest = list(range(1, 41))
        self.pick_num = 0
        self.pick_num_rest = 60
        self.is_in_guarantee = False

    def toggle_information(self):
        visible = not self.information.isVisible()
        self.information.setVisible(visible)
        self.information_button.setText('∧祈愿详情∧' if visible else '∨祈愿详情∨')
        self.adjustSize()

    def draw_once(self):
        self.clear_label()
        num = self.get_lucky()
        self.label.setText(f'{num}')

    def draw_ten(self):
        self.clear_label()
        self.numbers = [self.get_lucky() for _ in range(10)]
        self.update_label_timer = QTimer(self)
        self.update_label_timer.timeout.connect(self.update_label)
        self.update_label_index = 0
        self.update_label_timer.start(100)

    def update_label(self):
        if self.update_label_index < len(self.numbers):
            self.label.setText(
                ' '.join(f'{num}' for num in self.numbers[:self.update_label_index + 1]))
            self.update_label_index += 1
        else:
            self.update_label_timer.stop()

    def clear_label(self):
        self.label.setText('')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.dragPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = QPoint(event.globalPos() - self.dragPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.dragPosition = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def resizeEvent(self, event):
        self.round_shadow.resize(self.size())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    root = WishWindow()
    root.show()
    app.exec_()
