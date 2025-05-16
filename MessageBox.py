"""
祈愿 · 幸运观众：消息气泡

Copyright © 2025 XuangeAha(轩哥啊哈OvO)

"""

from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect, QApplication
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer, QPoint, QEasingCurve

from RoundShadow import RoundShadow

class MessageBox(RoundShadow):
    def __init__(self, message:str, duration:int|float=3, parent=None):
        super(MessageBox, self).__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.Tool | Qt.WindowStaysOnTopHint)
        _global_font = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(r'.wish\fonts\HYWH-85w Heavy.ttf'))[0]

        self.message_label = QLabel(self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFont(QFont(_global_font, 12))
        self.message_label.setText(message)
        self.message_label.adjustSize()
        self.resize(self.message_label.width() + 120, self.message_label.height() + 50)
        self.message_label.move((self.width() - self.message_label.width()) // 2, (self.height() - self.message_label.height()) // 2)

        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = int(screen.height() * 0.18)
        self.move(x, y + 60)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.message_label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        self.show_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.show_anim.setDuration(500)
        self.show_anim.setStartValue(0)
        self.show_anim.setEndValue(1)
        self.show_anim.setEasingCurve(QEasingCurve.OutCubic)

        self.move_anim = QPropertyAnimation(self, b"pos")
        self.move_anim.setDuration(500)
        self.move_anim.setStartValue(QPoint(x, y + 60))
        self.move_anim.setEndValue(QPoint(x, y))
        self.move_anim.setEasingCurve(QEasingCurve.OutCubic)

        self.hide_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.hide_anim.setDuration(500)
        self.hide_anim.setStartValue(1)
        self.hide_anim.setEndValue(0)
        self.hide_anim.setEasingCurve(QEasingCurve.InCubic)

        self.hide_move_anim = QPropertyAnimation(self, b"pos")
        self.hide_move_anim.setDuration(500)
        self.hide_move_anim.setStartValue(QPoint(x, y))
        self.hide_move_anim.setEndValue(QPoint(x, y - 60))
        self.hide_move_anim.setEasingCurve(QEasingCurve.InCubic)

        self.show_anim.finished.connect(self._on_showed)
        self.hide_anim.finished.connect(self._on_hidden)

        self.show_duration = int(duration * 1000)

    def showEvent(self, event):
        self.show_anim.start()
        self.move_anim.start()
        super().showEvent(event)

    def _on_showed(self):
        QTimer.singleShot(self.show_duration, self._start_hide)

    def _start_hide(self):
        self.hide_anim.start()
        self.hide_move_anim.start()

    def _on_hidden(self):
        self.close()
        self.deleteLater()

def show_messagebox(message=str, duration:int|float=3):
    """
    显示消息气泡
    
    """
    app_messagebox = QApplication.instance()
    messagebox = MessageBox(message, duration)
    messagebox.show()
    if not QApplication.instance().thread().isRunning():
        app_messagebox.exec_()
